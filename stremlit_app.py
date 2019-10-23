import streamlit as st 
import pandas as pd
from PIL import Image
import sys
import os
import glob
import argparse
import numpy as np
import tensorflow as tf
from tensorflow.contrib.slim.python.slim.nets import inception
from tensorflow.python.framework import ops
from tensorflow.python.training import saver as tf_saver
from tensorflow.python.training import supervisor




slim = tf.contrib.slim
FLAGS = None

def PreprocessImage(image, central_fraction=0.875):
  """Load and preprocess an image.
  Args:
    image: a tf.string tensor with an JPEG-encoded image.
    central_fraction: do a central crop with the specified
      fraction of image covered.
  Returns:
    An ops.Tensor that produces the preprocessed image.
  """

  # Decode Jpeg data and convert to float.
  image = tf.cast(tf.image.decode_jpeg(image, channels=3), tf.float32)

  # image = tf.image.central_crop(image, central_fraction=central_fraction)
  # Make into a 4D tensor by setting a 'batch size' of 1.
  image = tf.expand_dims(image, [0])
  image = tf.image.resize_bilinear(image,
                                 [FLAGS.image_size, FLAGS.image_size],
                                 align_corners=False)

  # Center the image about 128.0 (which is done during training) and normalize.
  image = tf.multiply(image, 1.0/127.5)
  return tf.subtract(image, 1.0)
 

def LoadLabelMaps(num_classes, labelmap_path, dict_path):
  """Load index->mid and mid->display name maps.
  Args:
    labelmap_path: path to the file with the list of mids, describing predictions.
    dict_path: path to the dict.csv that translates from mids to display names.
  Returns:
    labelmap: an index to mid list
    label_dict: mid to display name dictionary
  """
  labelmap = [line.rstrip() for line in tf.gfile.GFile(labelmap_path).readlines()]
  if len(labelmap) != num_classes:
    tf.logging.fatal(
        "Label map loaded from {} contains {} lines while the number of classes is {}".format(
            labelmap_path, len(labelmap), num_classes))
    sys.exit(1)

  label_dict = {}
  for line in tf.gfile.GFile(dict_path).readlines():
    words = [word.strip(' "\n') for word in line.split(',', 1)]
    label_dict[words[0]] = words[1]

  return labelmap, label_dict


def main(img_dir):
 
  if not os.path.exists(FLAGS.checkpoint):
    tf.logging.fatal(
        'Checkpoint %s does not exist. Have you download it? See tools/download_data.sh',
        FLAGS.checkpoint)
  g = tf.Graph()
  with g.as_default():
    input_image = tf.placeholder(tf.string)
    processed_image = PreprocessImage(input_image)

    with slim.arg_scope(inception.inception_v3_arg_scope()):
      logits, end_points = inception.inception_v3(processed_image, num_classes=FLAGS.num_classes, is_training=False)

    predictions = end_points['multi_predictions'] = tf.nn.sigmoid(logits, name='multi_predictions')
    saver = tf_saver.Saver()
    sess = tf.Session()
    saver.restore(sess, FLAGS.checkpoint)
    
    # img_dir = sorted(glob.glob(os.path.join(FLAGS.image_folder_path, '*.jpg')))
    # sorted(img_dir, key = lambda d: d[-7: -4])   
   
  
  # Run the evaluation on the images
  image_path = os.path.join(FLAGS.image_folder_path, img_dir)

  # for i in range(len(img_dir)):
    # image_path = img_dir[i]
  if not os.path.exists(image_path):
    tf.logging.fatal('Input image does not exist %s', image_path)
  img_data = tf.gfile.FastGFile(image_path, "rb").read()
  print(image_path)
  predictions_eval = np.squeeze(sess.run(predictions, {input_image: img_data}))

  # Print top(n) results
  labelmap, label_dict = LoadLabelMaps(FLAGS.num_classes, FLAGS.labelmap, FLAGS.dict)

  top_k = predictions_eval.argsort()[-FLAGS.n:][::-1]
  label_confidence_dic = {}
  display_label_name = []
  display_score = []
  for idx in top_k:
    mid = labelmap[idx]
    display_name = label_dict.get(mid, 'unknown')
    score = predictions_eval[idx]
    label_confidence_dic[display_name] = score

    display_label_name.append(display_name)
    display_score.append(score)

    print('{}: {} - {} (score = {:.2f})'.format(idx, mid, display_name, score))

    display_dict = dict({'name': display_label_name, 'score': display_score})
    display_df = pd.DataFrame(display_dict)
  return display_df




if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--checkpoint', type=str, default='/inception/model/2016_08/model.ckpt',
                      help='Checkpoint to run inference on.')
  parser.add_argument('--labelmap', type=str, default='/inception/model/2016_08/labelmap.txt',
                      help='Label map that translates from index to mid.')
  parser.add_argument('--dict', type=str, default='/inception/data/dict.csv',
                      help='Path to a dict.csv that translates from mid to a display name.')
  parser.add_argument('--image_size', type=int, default=299,
                      help='Image size to run inference on.')
  parser.add_argument('--num_classes', type=int, default=6012,
                      help='Number of output classes.')
  parser.add_argument('--n', type=int, default=10,
                      help='Number of top predictions to print.')
  parser.add_argument('--image_folder_path', type=str, default='/inception/data/video_frames/mountain_lake/')

  FLAGS = parser.parse_args()
  # tf.app.run()


  st.title("auto annotation tool demo")

  # show dropdown table 
  example_img_dir = sorted(glob.glob(os.path.join(FLAGS.image_folder_path, '*.jpg')))
  sorted(example_img_dir, key = lambda d: d[-7: -4])  
  option_list = [example_img_dir[i].split('/')[-1] for i in range(len(example_img_dir))]
   
  option = st.selectbox(label = 'select the image you want to annotate', options = option_list)
  st.write('You selected: ', option)

  # show the selected image
  img = Image.open(os.path.join(FLAGS.image_folder_path, option))
  img_array = np.array(img)
  st.image(img_array, option, 250)

  # show button, when clicked, annotation result wil be shown below 
  if st.button('start annotation'):

	  display_df = main(img_dir = option)
	  st.write(display_df)

