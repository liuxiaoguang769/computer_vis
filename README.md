# 人脸检测与行人检测 — 实验骨架

说明（中文）：
本仓库新增了一个实验框架，用于完成“人脸检测与行人检测任务”对比实验，满足：至少 3 个数据集、至少 4 种检测模型（基于 CNN 或 Transformer）。

快速步骤：
1. 克隆或切换到本仓库的 experiment/ 目录。
2. 创建 Python 虚拟环境并安装依赖：
   - pip install -r requirements.txt
3. 下载并准备数据集（默认下载到 ./data/）：
   - bash scripts/download_datasets.sh
   - 注意：部分数据集需要用户手动注册并下载后放在 data/ 下（脚本会提示）
4. 运行实验（示例）：
   - python3 scripts/run_experiments.py --config configs/experiments.yml
5. 结果和评估：
   - 结果输出在 outputs/{dataset}/{model}/ 下，包含 COCO 格式的 JSON 预测文件和评估报告。
6. 分析报告模版：
   - analysis/report_template.md

推荐数据集（本骨架默认启用）：
- WIDER FACE（人脸检测）
- FDDB（人脸检测） — 需转换为 COCO 风格
- COCO (person 类)（行人检测）
可选：Caltech Pedestrian、CityPersons（如需要请手动下载并写转换器）

推荐模型（至少使用 4 种）：
- fasterrcnn_resnet50_fpn (torchvision) — CNN
- retinanet_resnet50_fpn (torchvision) — CNN
- detr_resnet50 (torchvision) — Transformer
- yolov5s (ultralytics/yolov5) — CNN （通过调用 yolov5 仓库的 inference 脚本）

指标（默认输出）：
- mAP (COCO) 全尺度与 AP50
- Precision / Recall 曲线
- FPS（推理速度，选测）
- 可视化若干检测结果图片（存于 outputs/.../vis/）

注意事项：
- 部分数据集（WIDER/FDDB/Caltech）需要转换为 COCO 格式以统一评估，本仓库提供转换函数模板（scripts/run_experiments.py 中）。
- YOLOv5 依赖其仓库代码，需要额外 git clone yolov5。
