import os, errno
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from absl import logging
import numpy as np
import tensorflow as tf

from networks.models import ArcFaceModel

import cv2
from PIL import Image

from silence_tensorflow import silence_tensorflow
silence_tensorflow()

import csv
from pathlib import Path
import yaml


USER_IMG = 'temp.png'
CMP_PATH = 'cropped_images'
LOG_PATH = 'log.csv'

THRESHOLD = 1.0

def l2_norm(x, axis=1):
    norm = np.linalg.norm(x, axis=axis, keepdims=True)
    return x / norm

def load_yaml(load_path):
    """load yaml file"""
    with open(load_path, 'r') as f:
        loaded = yaml.load(f, Loader=yaml.Loader)

    return loaded


def remove(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def get_embedding(model, x):
    if len(x.shape) == 3:
        x = np.expand_dims(x, 0)
    embeds = model(x, training=False) # to tensor array
    embeds = l2_norm(embeds)
    return embeds

def calculate_distance(embd1, embd2):
    diff = np.subtract(embd1, embd2)
    dist = np.sum(np.square(diff), axis=1)
    return dist

def is_same(dist):
    return np.less(dist, THRESHOLD)


# def search_leaked_image(files):
#     log = open(LOG_PATH, 'r')
#     detect_log = open(LEAKED_LOG_PATH, 'a')
    
#     wr = csv.writer(detect_log)
#     rdr = csv.reader(log)
        
#     user_img_name = Path(USER_IMG).stem
    
#     for f in files:
#         for line in rdr:
#             words = line.split(',')
            
#             f_name = words[1]
#             f_name = Path(f_name).stem
#             link = words[0]
            
#             if(user_img_name == f_name):
#                 wr.writerow([link])


def main():
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    logger = tf.get_logger()
    logger.disabled = True
    logger.setLevel(logging.FATAL)

    cfg = load_yaml('./configs/config.yaml')

    global model
    model = ArcFaceModel(size=cfg['input_size'],
                         backbone_type=cfg['backbone_type'],
                         training=False,
                         w_decay=cfg['w_decay'])
    
    ckpt_path = tf.train.latest_checkpoint('weights/checkpoints/' + cfg['sub_name'])
    if ckpt_path is not None:
        print("[*] load ckpt from {}".format(ckpt_path))
        model.load_weights(ckpt_path)
    else:
        print("[*] Cannot find ckpt from {}.".format(ckpt_path))
        exit()


    user_embd = np.array(Image.open(USER_IMG), dtype=np.uint8).astype(np.float32) / 255.
    user_embd = get_embedding(model, user_embd)

    leaked_imgs = []
    for img_ in os.listdir(CMP_PATH):
        cur_img_path = os.path.join(CMP_PATH, img_)
        
        if cv2.imread(cur_img_path) is None:
            continue

        cur_embd = np.array(Image.open(cur_img_path), dtype=np.uint8).astype(np.float32) / 255.
        cur_embd = get_embedding(model, cur_embd)
        
        dist = calculate_distance(user_embd, cur_embd)
        chk = is_same(dist[0])
        if chk == True:
            leaked_imgs.append(Path(img_).stem)
            
            try:
                pil_image = Image.fromarray(cv2.cvtColor(cv2.imread('crawled_images/' + img_), cv2.COLOR_BGR2RGB))
            except:
                continue
            pil_image.save(os.path.join('output/', Path(img_).stem) + '.PNG', format='PNG', quality=100)
    
    # search_leaked_image(leaked_imgs)
    # remove(USER_IMG)
    
    print("[*] Done !")
    

if __name__ == "__main__":
    main()