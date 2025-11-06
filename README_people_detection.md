# 人脸检测与行人检测实验教程（适合小白） — 使用 VOC / COCO / MPII，训练多种检测器

说明
- 目标：使用 VOC、COCO、MPII 三个数据源完成“行人检测与人脸检测”实验；训练并比较至少 4 个检测器（示例：Faster R-CNN、RetinaNet、FCOS、Deformable DETR、YOLOv5）。
- 框架：MMDetection（主要）、Ultralytics YOLO（可选）。
- 分支：task1-peopleModel
- 假设你对 Linux 或 WSL 下的命令行有基本了解。

目录结构（示例）
- data/
  - VOCdevkit/ (VOC 数据目录)
  - coco/ (COCO 数据集)
  - mpii/ (MPII 原始数据)
  - merged_coco/ (合并后的 COCO 格式数据集：用于训练)
- tools/
  - convert_mpii_to_coco.py
  - merge_annotations.py
  - train_mmdet.sh
  - yolov5_train.sh
- configs/ (mmdetection config，可以从 mmdet 拷贝后修改)
- outputs/ (训练结果、日志、模型权重)

步骤总览（高层）
1. 环境准备（Python、PyTorch、MMCV、MMDetection、Ultralytics）
2. 下载数据（VOC / COCO / MPII）
3. 将 MPII 转换为 COCO-format（检测用），并从 VOC/COCO 提取 person 类（或 face 的近似 bbox）
4. 合并注释（生成 merged_coco）
5. 配置 MMDetection：classes= ['person']（以及 face 的训练集如果需要）
6. 使用多种模型训练：Faster R-CNN、RetinaNet、FCOS、Deformable DETR、YOLOv5
7. 评估与可视化（mAP、PR 曲线、可视化检测结果）
8. 比较结果并写报告

注意事项（关键）
- MPII 是姿态（keypoints）数据集：我们通过 keypoints 计算 bbox（person bbox）并另从头部关键点生成 face bbox（近似），可用于人脸检测的训练样本（注意：这是近似方法，若需要精确 face 数据，建议额外使用 WiderFace 等数据集）。
- 合并不同数据集前要统一类别（这里只做 person 类的行人检测）；若同时做 face 检测，则需要建立一个新的类别集合并训练/分开训练两个检测器。
- 训练前按 GPU/内存调整 batch size / lr / epoch。

下面是可以直接使用/参考的脚本内容（已放在 tools/）：

- tools/convert_mpii_to_coco.py：把 MPII 的 keypoint 标注转换为 COCO 检测格式（生成 person bbox，和 head bbox 用作 face）
- tools/merge_annotations.py：把 VOC（person 类）、COCO(person) 与转换好的 MPII COCO-format 合并为一个 COCO-format 数据集（可用于行人检测）
- tools/train_mmdet.sh：使用 MMDetection 训练 Faster R-CNN / RetinaNet / FCOS / Deformable DETR 的示例命令（需修改 config 路径/数据路径）
- tools/yolov5_train.sh：使用 YOLOv5 训练的示例命令（pip 安装 ultralytics / yolov5）

更多操作详见仓库中的 tools/ 脚本和注释。