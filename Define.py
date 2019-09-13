# Copyright (C) 2019 * Ltd. All rights reserved.
# author : SangHyeon Jo <josanghyeokn@gmail.com>

# dataset parameters
ROOT_DIR = 'D:/_ImageDataset/'

CLASS_NAMES = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
CLASS_DIC = {class_name : index for index, class_name in enumerate(CLASS_NAMES)}
CLASSES = len(CLASS_NAMES)

# network parameters
IMAGE_HEIGHT = 416
IMAGE_WIDTH = 416
IMAGE_CHANNEL = 3

NMS_THRESHOLD = 0.5
AP_THRESHOLD = 0.5
POSITIVE_IOU_THRESHOLD = 0.5

DIVIDE = 2 ** 5

S = IMAGE_WIDTH // DIVIDE
B = 5
ANCHORS = [[0.57273, 0.677385],
           [1.87446, 2.06253],
           [3.33843, 5.47434],
           [7.88282, 3.52778],
           [9.77052, 9.16828]]

# loss parameters
COORD = 5.0
NOOBJ = 0.5

WEIGHT_DECAY = 0.0001

# train
NUM_GPU = 2
BATCH_SIZE = NUM_GPU * 16
INIT_LEARNING_RATE = 1e-4

MAX_EPOCH = 200
LOG_ITERATION = 50
VALID_ITERATION = 5000
