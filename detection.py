from __future__ import annotations
import os, errno
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np

import tensorflow as tf
from utils import label_map_util
import os
import cv2

from PIL import Image

from silence_tensorflow import silence_tensorflow
silence_tensorflow()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = './model/frozen_inference_graph_face.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = './protos/face_label_map.pbtxt'
NUM_CLASSES = 2

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

class TensoflowFaceDector(object):
    def __init__(self, PATH_TO_CKPT):
        """Tensorflow detector
        """

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        with self.detection_graph.as_default():
            config = tf.compat.v1.ConfigProto()
            config.gpu_options.allow_growth = True
            self.sess = tf.compat.v1.Session(
                graph=self.detection_graph, config=config)
            self.windowNotSet = True

    def run(self, image):
        """image: bgr image
        return (boxes, scores, classes, num_detections)
        """

        image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        image_tensor = self.detection_graph.get_tensor_by_name(
            'image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        classes = self.detection_graph.get_tensor_by_name(
            'detection_classes:0')
        num_detections = self.detection_graph.get_tensor_by_name(
            'num_detections:0')
        # Actual detection.
        # start_time = time.time()
        (boxes, scores, classes, num_detections) = self.sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        # elapsed_time = time.time() - start_time
        # print('inference time cost: {}'.format(elapsed_time))

        return (boxes, scores, classes, num_detections)


def silentRemove(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def main():
    db_path = 'crawled images'
    tDetector = TensoflowFaceDector(PATH_TO_CKPT)
    
    print(f"[*] Detection and RoI cropping !")
    
    while(True):
        num_imgs = len(os.listdir(db_path))
        if num_imgs < 20:
            continue
        if num_imgs == 20:
            print(f"[*] 20 images RoI cropping")
        
        for i in os.listdir(db_path):
            path = os.path.join(db_path, i)
            img = cv2.imread(path, cv2.IMREAD_COLOR)

            if img is None: 
                silentRemove(path)
                continue
            
            [h, w] = img.shape[:2]

            (boxes, scores, classes, num_detections) = tDetector.run(img)

            box = np.squeeze(boxes)
            score = np.squeeze(scores)

            if (score[0] > 0.90):   # if detect face
                ymin, xmin, ymax, xmax = box[0]

                # pil_image = Image.fromarray(np.uint8(image)).convert('RGB')
                temp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(temp)


                (left, right, top, bottom) = (xmin * w, xmax * w,
                                              ymin * h, ymax * h)

                cropped = pil_image.crop((left, top, right, bottom))
                cropped = cropped.resize((112, 112), Image.ANTIALIAS)
                # cropped.show()
                cropped.save(os.path.join('cropped images', i), format='PNG', quality=100)

            silentRemove(path)



if __name__ == '__main__':
    main()