#!/bin/bash
# 使用 YOLOv5 (ultralytics) 训练的示例
# 1) 克隆 https://github.com/ultralytics/yolov5 并安装 requirements
# 2) 准备 data/person.yaml (数据集描述)
# 3) 运行训练

# data/person.yaml 的示例:
# train: /path/to/merged_coco/images/train
# val: /path/to/merged_coco/images/val
# nc: 1
# names: ['person']

# 训练
python yolov5/train.py --img 640 --batch 16 --epochs 50 --data data/person.yaml --weights yolov5s.pt --name yolov5_person
