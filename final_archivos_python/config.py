import os

cwd = os.getcwd()

if not os.path.exists('model'):
    os.mkdir('model')

if not os.path.exists(f'{cwd}/result'):
    os.mkdir(f'{cwd}/result')

TRAIN_DATASET_PATH = f'{cwd}/dataset/train'
VALID_DATASET_PATH = f'{cwd}/dataset/valid'
TEST_DATASET_PATH = f'{cwd}/dataset/test'
MODEL_PATH = f'{cwd}'

MODEL = 'efficientdet_lite0'
MODEL_NAME = 'model.tflite'
CLASSES = ['pelusa']
EPOCHS = 10
BATCH_SIZE = 2