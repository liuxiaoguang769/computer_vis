````markdown name=Windows_instructions.md
# 在 Windows (PyCharm) 上使用仓库中的脚本训练（面向小白）

下面的说明基于你提供的数据路径：
- coco-person annotations: E:\xunleiDownload\dataset\persondata_200\outputs\coco_person_200_coco\annotations.json
- coco-person images: E:\xunleiDownload\dataset\persondata_200\outputs\coco_person_200_coco\images
- voc-person annotations: E:\xunleiDownload\dataset\persondata_200\outputs\voc_person_200_coco\annotations.json
- voc-person images: E:\xunleiDownload\dataset\persondata_200\outputs\voc_person_200_coco\images
- mpii-person annotations: E:\xunleiDownload\dataset\persondata_200\outputs\mpii_person_200_coco\annotations.json
- mpii-person images: E:\xunleiDownload\dataset\persondata_200\outputs\mpii_person_200_coco\images

## 目标
把三份 images 合并到一个文件夹，把三份 annotations 合并成一个 COCO 格式的 instances_train.json，然后使用 MMDetection 的 train.py 训练模型（示例使用 Faster R-CNN）。

## 步骤（推荐，按顺序）
1. 在 Windows 上安装并配置好 Python、PyTorch（带 CUDA）、MMCV、MMDetection。推荐使用 Anaconda/venv。
   - 在 PyCharm 中为项目配置好对应的 Python 解释器（虚拟环境）。
   - 在终端里确认 `python --version` 和 `python -c "import torch; print(torch.cuda.is_available())"`。

2. 打开 PyCharm Terminal（或 Windows CMD / PowerShell），切换到仓库根目录（包含 tools/ 和 configs/）。

3. 运行仓库里新增的批处理脚本（会合并图片、合并annotations并启动训练）：

   双击运行（或在 PyCharm Terminal 中）:
   ```bat
   tools\train_mmdet_windows.bat
   ```

   脚本会执行以下操作：
   - 使用 robocopy 将三个 images 文件夹复制合并到 `E:\xunleiDownload\dataset\persondata_200\outputs\merged_person_200\images`（如果目标已存在则跳过已存在文件）
   - 调用 `python tools/merge_annotations.py --jsons ... --out merged_person_200/annotations/instances_train.json` 合并三个 COCO 注释文件
   - 使用 MMDetection 的 `tools/train.py` 以配置文件 `configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py` 启动训练，`cfg-options` 已设置为使用合并后的 annotations 和合并后的 images 文件夹

4. 如果你希望使用其他模型（例如 RetinaNet、FCOS、Deformable DETR 或 YOLOv5），请在 `tools/train_mmdet_windows.bat` 中修改 `CONFIG` 变量，或参考 `tools/train_mmdet.sh` 中的示例命令。

## 注意事项
- 合并 images 会占用额外磁盘空间（大约为三个文件夹大小之和）。如果磁盘空间不足，可以改为创建符号链接（需要管理员权限）或只选择部分数据复制。
- 合并 annotations 前请打开并检查每个 JSON 的 `images` 字段中的 `file_name` 是否与原 images 文件夹里的文件名相匹配；如果 `file_name` 中包含路径片段，请确保这些路径能被合并后的 images 访问到（通常保持仅文件名是最简单的做法）。
- Windows 路径里有空格时请确保路径用双引号包裹。

## 运行环境提示（PyCharm）
- 在 PyCharm 中，打开 `Settings > Tools > Terminal`，确认启动 Shell 是 cmd.exe 或 PowerShell，然后在 Terminal 里运行 `tools\train_mmdet_windows.bat`。
- 或者在 PyCharm 的 Run/Debug Configurations 中创建一个 Python 运行/调试配置，Script path 指向 `tools\train.py`（MMDetection 的 train.py），并在 Parameters 中添加对应的 `--cfg-options ...`。这种方式更便于调试。

````