#!/bin/bash
# 示例：在已经安装好 MMDetection 的环境下运行下面命令来训练不同模型
# 修改 CONFIG 和 WORK_DIR、DATA_ROOT 为实际路径

# 示例：Faster R-CNN
python tools/train.py configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py \
    --work-dir work_dirs/fasterrcnn_person \
    --cfg-options \
    data.train.dataset.data_root=/path/to/merged_coco/ \
    data.train.ann_file=/path/to/merged_coco/annotations/instances_train.json \
    data.train.img_prefix=/path/to/merged_coco/images/ \
    total_epochs=12 \
    optimizer.lr=0.02

# 示例：RetinaNet
python tools/train.py configs/retinanet/retinanet_r50_fpn_1x_coco.py \
    --work-dir work_dirs/retinanet_person \
    --cfg-options \
    data.train.ann_file=/path/to/merged_coco/annotations/instances_train.json \
    data.train.img_prefix=/path/to/merged_coco/images/ \
    total_epochs=12

# 示例：FCOS
python tools/train.py configs/fcos/fcos_r50_caffe_fpn_gn-head_1x_coco.py \
    --work-dir work_dirs/fcos_person \
    --cfg-options \
    data.train.ann_file=/path/to/merged_coco/annotations/instances_train.json \
    data.train.img_prefix=/path/to/merged_coco/images/ \
    total_epochs=12

# 示例：Deformable DETR (Transformer-based)
python tools/train.py configs/detr/deformable_detr_refine_r50_16x2_50e_coco.py \
    --work-dir work_dirs/detr_person \
    --cfg-options \
    data.train.ann_file=/path/to/merged_coco/annotations/instances_train.json \
    data.train.img_prefix=/path/to/merged_coco/images/ \
    total_epochs=50
