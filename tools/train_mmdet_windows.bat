@echo off
REM Merge images from three datasets into a single folder and merge COCO annotations, then run MMDetection training (Windows, PyCharm-friendly)

set SRC1=E:\xunleiDownload\dataset\persondata_200\outputs\coco_person_200_coco\images
set SRC2=E:\xunleiDownload\dataset\persondata_200\outputs\voc_person_200_coco\images
set SRC3=E:\xunleiDownload\dataset\persondata_200\outputs\mpii_person_200_coco\images
set MERGED_IMG_DIR=E:\xunleiDownload\dataset\persondata_200\outputs\merged_person_200\images
set MERGED_ANN_DIR=E:\xunleiDownload\dataset\persondata_200\outputs\merged_person_200\annotations
set MERGED_ANN_JSON=%MERGED_ANN_DIR%\instances_train.json

REM Create directories if not exist
if not exist "%MERGED_IMG_DIR%" mkdir "%MERGED_IMG_DIR%"
if not exist "%MERGED_ANN_DIR%" mkdir "%MERGED_ANN_DIR%"

REM Copy images (robocopy will skip existing files)
robocopy "%SRC1%" "%MERGED_IMG_DIR%" /E
robocopy "%SRC2%" "%MERGED_IMG_DIR%" /E
robocopy "%SRC3%" "%MERGED_IMG_DIR%" /E

REM Merge annotations JSONs using the repository script (merge_annotations.py)
python tools/merge_annotations.py --jsons "E:\xunleiDownload\dataset\persondata_200\outputs\coco_person_200_coco\annotations.json" "E:\xunleiDownload\dataset\persondata_200\outputs\voc_person_200_coco\annotations.json" "E:\xunleiDownload\dataset\persondata_200\outputs\mpii_person_200_coco\annotations.json" --out "%MERGED_ANN_JSON%"

REM Configuration for training (modify as needed)
set CONFIG=configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py
set WORK_DIR=work_dirs\fasterrcnn_person_from_persondata200
set EPOCHS=12
set LR=0.02

REM Run MMDetection training (ensure Python environment activated in PyCharm or terminal)
python tools/train.py %CONFIG% --work-dir %WORK_DIR% --cfg-options data.train.ann_file="%MERGED_ANN_JSON%" data.train.img_prefix="%MERGED_IMG_DIR%/" data.val.ann_file="%MERGED_ANN_JSON%" data.val.img_prefix="%MERGED_IMG_DIR%/" total_epochs=%EPOCHS% optimizer.lr=%LR%

pause