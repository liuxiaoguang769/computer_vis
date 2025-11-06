@echo off
REM Merge images from three datasets into a single folder and merge COCO annotations, then run MMDetection training (Windows, PyCharm-friendly)

REM --- dataset 1: coco-person ---
set SRC1=E:\xunleiDownload\dataset\persondata_200\outputscoco_train2014_person_200_coco\images
set ANN1=E:\xunleiDownload\dataset\persondata_200\outputscoco_train2014_person_200_coco\annotations_coco_train2014.json

REM --- dataset 2: voc-person ---
set SRC2=E:\xunleiDownload\dataset\persondata_200\outputsVOCtest_06-Nov-2007_person_200_coco\images
set ANN2=E:\xunleiDownload\dataset\persondata_200\outputsVOCtest_06-Nov-2007_person_200_coco\annotations_VOCtest_06-Nov-2007.json

REM --- dataset 3: mpii-person ---
set SRC3=E:\xunleiDownload\dataset\persondata_200\outputsmpii_human_pose_v1_person_200_coco\images
set ANN3=E:\xunleiDownload\dataset\persondata_200\outputsmpii_human_pose_v1_person_200_coco\annotations_mpii_human_pose_v1.json

REM --- merged output locations ---
set MERGED_IMG_DIR=E:\xunleiDownload\dataset\persondata_200\outputs\merged_person_200\images
set MERGED_ANN_DIR=E:\xunleiDownload\dataset\persondata_200\outputs\merged_person_200\annotations
set MERGED_ANN_JSON=%MERGED_ANN_DIR%\instances_train.json

REM Create directories if not exist
if not exist "%MERGED_IMG_DIR%" mkdir "%MERGED_IMG_DIR%"
if not exist "%MERGED_ANN_DIR%" mkdir "%MERGED_ANN_DIR%"

REM Copy images (robocopy will skip existing files)
echo Copying images from dataset 1...
robocopy "%SRC1%" "%MERGED_IMG_DIR%" /E
echo Copying images from dataset 2...
robocopy "%SRC2%" "%MERGED_IMG_DIR%" /E
echo Copying images from dataset 3...
robocopy "%SRC3%" "%MERGED_IMG_DIR%" /E

REM Merge annotations JSONs using the repository script (merge_annotations.py)
echo Merging annotation JSONs...
python tools/merge_annotations.py --jsons "%ANN1%" "%ANN2%" "%ANN3%" --out "%MERGED_ANN_JSON%"

REM Check merged JSON quick info (print counts)
python - <<PY
import json,sys
p=r"%MERGED_ANN_JSON%"
try:
    j=json.load(open(p,'r',encoding='utf-8'))
    print("Merged JSON loaded. images:", len(j.get('images',[])), "annotations:", len(j.get('annotations',[])), "categories:", j.get('categories',[]))
except Exception as e:
    print("Failed to read merged json:", e)
    sys.exit(1)
PY

REM Configuration for training (modify as needed)
set CONFIG=configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py
set WORK_DIR=work_dirs\fasterrcnn_person_from_persondata200
set EPOCHS=12
set LR=0.02

REM Run MMDetection training (ensure Python environment activated in PyCharm or terminal)
echo Starting MMDetection training...
python tools/train.py %CONFIG% --work-dir %WORK_DIR% --cfg-options data.train.ann_file="%MERGED_ANN_JSON%" data.train.img_prefix="%MERGED_IMG_DIR%/" data.val.ann_file="%MERGED_ANN_JSON%" data.val.img_prefix="%MERGED_IMG_DIR%/" model.roi_head.bbox_head.num_classes=1 total_epochs=%EPOCHS% optimizer.lr=%LR%

pause