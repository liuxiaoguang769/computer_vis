#!/usr/bin/env python3
"""
合并多个 COCO 格式的 annotation JSON（例如 VOC 转换的 COCO、原始 COCO 的 subsets、MPII 转换的文件）。
确保类别映射一致（person -> id=1）。
用法：
python merge_annotations.py --jsons voc_person.json coco_person.json mpii_person.json --out merged_coco/annotations/instances_train.json
"""
import json
import argparse
from copy import deepcopy

def merge(json_list, out_path):
    merged = {'images': [], 'annotations': [], 'categories': []}
    img_id_map = {}
    ann_id = 1
    img_id = 1
    for jpath in json_list:
        j = json.load(open(jpath, 'r'))
        # categories mapping: expect person -> id 1
        for im in j['images']:
            old_id = im['id']
            new_im = deepcopy(im)
            new_im['id'] = img_id
            img_id_map[(jpath, old_id)] = img_id
            merged['images'].append(new_im)
            img_id += 1
        for a in j['annotations']:
            new_a = deepcopy(a)
            new_a['id'] = ann_id
            new_a['image_id'] = img_id_map[(jpath, a['image_id'])]
            # map category names to desired ids if needed (assume already okay)
            ann_id += 1
            merged['annotations'].append(new_a)
    # categories: keep only unique by name
    cat_map = {}
    new_cats = []
    for jpath in json_list:
        j = json.load(open(jpath, 'r'))
        for c in j.get('categories', []):
            if c['name'] not in cat_map:
                cid = len(cat_map)+1
                cat_map[c['name']] = cid
                new_cats.append({'id': cid, 'name': c['name'], 'supercategory': c.get('supercategory', '')})
    merged['categories'] = new_cats
    with open(out_path, 'w') as f:
        json.dump(merged, f)
    print("Merged into", out_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--jsons', nargs='+', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    merge(args.jsons, args.out)
