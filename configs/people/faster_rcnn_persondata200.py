# ----- file: configs/people/faster_rcnn_persondata200.py -----
# Based on configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py
# Adjusted for the merged person dataset paths (Windows), single class 'person'

_base_ = '../faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'

# dataset settings
dataset_type = 'CocoDataset'
classes = ('person',)
# Use forward slashes in paths or raw strings; MMDetection accepts either on Windows
data_root = r'E:/xunleiDownload/dataset/persondata_200/outputs/merged_person_200/'

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_train.json',
        img_prefix=data_root + 'images/',
        classes=classes),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_train.json',
        img_prefix=data_root + 'images/',
        classes=classes),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_train.json',
        img_prefix=data_root + 'images/',
        classes=classes)
)

# model: set number of classes for the bbox head
model = dict(
    roi_head=dict(
        bbox_head=dict(
            num_classes=1
        )
    )
)

# optimizer & learning rate (keep default structure but you can tune)
optimizer = dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(step=[8, 11])
runner = dict(type='EpochBasedRunner', max_epochs=12)

# evaluation and checkpoint
evaluation = dict(interval=1, metric='bbox')
checkpoint_config = dict(interval=1)

# logging
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
    ])

# NOTE: You can override any item from the base config when running with --cfg-options as well.
# Save this file to configs/people/faster_rcnn_persondata200.py
# To run training in PyCharm Terminal (from repository root), use:
# python tools/train.py configs/people/faster_rcnn_persondata200.py --work-dir work_dirs/fasterrcnn_person_from_persondata200
