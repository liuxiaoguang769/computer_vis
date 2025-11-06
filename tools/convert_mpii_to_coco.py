#!/usr/bin/env python3
"""
将 MPII 原始标注（通常是 .mat）转换为 COCO 风格的 detection JSON。
我们将从 keypoints 生成 person bbox（xmin,ymin,w,h），并生成一个 head bbox 近似作为 face bbox（可选）。
用法：
python tools/convert_mpii_to_coco.py --mpii-root path/to/mpii --out-json path/to/mpiidet.json --make-face
"""
import os
import json
import argparse
import scipy.io as sio
import numpy as np
from tqdm import tqdm

def load_mpii(mat_path):
    data = sio.loadmat(mat_path, squeeze_me=True, struct_as_record=False)
    # MPII 原始 mat 中包含 annolist
    annolist = data.get('annolist', None)
    return annolist

def keypoints_to_bbox(kps):
    # kps: N x 3 (x, y, vis) or list of keypoints
    xs = [p[0] for p in kps if p[2] > 0]
    ys = [p[1] for p in kps if p[2] > 0]
    if len(xs) == 0 or len(ys) == 0:
        return None
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    # expand a bit
    w = xmax - xmin
    h = ymax - ymin
    pad = 0.15
    xmin = max(0, xmin - pad*w)
    ymin = max(0, ymin - pad*h)
    w = w * (1 + pad*2)
    h = h * (1 + pad*2)
    return [xmin, ymin, w, h]

def estimate_head_bbox(kps):
    # 简单用 nose/eyes/head-top 等关键点估计 head bbox
    # kps indexed by MPII order -- we assume common order: 0..15
    # For safety, select a few likely indices: nose(2), head_top may not exist -> fallback to eyes
    points = []
    for idx in [2,1,0,3,4]:  # nose, (left/right eye) order may vary
        if idx < len(kps) and kps[idx][2] > 0:
            points.append((kps[idx][0], kps[idx][1]))
    if not points:
        return None
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    w = xmax - xmin; h = ymax - ymin
    # head bbox enlarge
    scale = 1.6
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    new_w = max(20, w * scale)
    new_h = max(20, h * scale)
    nx = cx - new_w/2
    ny = cy - new_h/2
    return [nx, ny, new_w, new_h]

def convert(args):
    annolist = load_mpii(os.path.join(args.mpii_root, 'mpii_human_pose_v1_u12_1.mat'))
    images = []
    annotations = []
    img_id = 1
    ann_id = 1
    for item in tqdm(annolist):
        imgname = item.image.name if hasattr(item.image, 'name') else item.image
        imgpath = os.path.join(args.mpii_root, 'images', imgname)
        # create image entry
        # if file missing skip
        if not os.path.exists(imgpath):
            continue
        # image size unknown in MPII; set dummy or use PIL to read size
        from PIL import Image
        try:
            w,h = Image.open(imgpath).size
        except Exception:
            w,h = 0,0
        images.append({'file_name': imgname, 'height':h, 'width':w, 'id':img_id})
        # annolist may have multiple people
        if hasattr(item, 'annorect'):
            rects = item.annorect
            if not isinstance(rects, (list, tuple, np.ndarray)):
                rects = [rects]
            for r in rects:
                # if keypoints provided
                kps = []
                if hasattr(r, 'annopoints') and r.annopoints is not None:
                    pts = r.annopoints.point
                    if not isinstance(pts, (list, tuple, np.ndarray)):
                        pts = [pts]
                    for p in pts:
                        x = float(p.x); y = float(p.y)
                        v = int(getattr(p, 'is_visible', 2))
                        kps.append([x,y,v])
                # else skip
                if not kps:
                    # try rect fields
                    if hasattr(r, 'x1'):
                        x1 = float(r.x1); y1 = float(r.y1); x2 = float(r.x2); y2 = float(r.y2)
                        bbox = [x1, y1, x2-x1, y2-y1]
                    else:
                        continue
                else:
                    bbox = keypoints_to_bbox(kps)
                    head_bbox = estimate_head_bbox(kps) if args.make_face else None
                if bbox is None:
                    continue
                ann = {
                    'id': ann_id,
                    'image_id': img_id,
                    'category_id': 1,  # person
                    'bbox': [float(b) for b in bbox],
                    'area': float(bbox[2]*bbox[3]),
                    'iscrowd': 0,
                }
                if kps:
                    # convert keypoints to COCO format (x,y,v) flattened
                    kps_flat = []
                    for p in kps:
                        # ensure 17 keypoints? We'll append as available
                        kps_flat.extend([float(p[0]), float(p[1]), int(p[2])])
                    ann['keypoints'] = kps_flat
                    ann['num_keypoints'] = sum(1 for p in kps if p[2]>0)
                annotations.append(ann)
                ann_id += 1
                # optionally create face ann using head_bbox
                if args.make_face and head_bbox is not None:
                    face_ann = {
                        'id': ann_id,
                        'image_id': img_id,
                        'category_id': 2,  # face class if you decide
                        'bbox': [float(b) for b in head_bbox],
                        'area': float(head_bbox[2]*head_bbox[3]),
                        'iscrowd': 0,
                    }
                    annotations.append(face_ann)
                    ann_id += 1
        img_id += 1
    coco_out = {
        'images': images,
        'annotations': annotations,
        'categories': [
            {'id':1, 'name':'person', 'supercategory':'person'},
        ]
    }
    if args.make_face:
        coco_out['categories'].append({'id':2,'name':'face','supercategory':'face'})
    with open(args.out_json, 'w') as f:
        json.dump(coco_out, f)
    print("Saved COCO json to", args.out_json)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mpii-root', required=True)
    parser.add_argument('--out-json', required=True)
    parser.add_argument('--make-face', action='store_true', help="同时生成 face bbox（id=2）")
    args = parser.parse_args()
    convert(args)
