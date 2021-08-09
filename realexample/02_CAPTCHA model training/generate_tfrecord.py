"""
Usage:
  # In local folder
  # Create train data:
  python generate_tfrecord.py --csv_input=CSGO_images\train_labels.csv --image_dir=CSGO_images\train --output_path=CSGO_images\train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=CSGO_images\test_labels.csv --image_dir=CSGO_images\test --output_path=CSGO_images\test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf
from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('image_dir', '', 'Path to the image directory')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'A':
        return 1
    if row_label == 'B':
        return 2
    if row_label == 'C':
        return 3
    if row_label == 'D':
        return 4
    if row_label == 'E':
        return 5
    if row_label == 'F':
        return 6
    if row_label == 'G':
        return 7
    if row_label == 'H':
        return 8
    if row_label == 'I':
        return 9
    if row_label == 'J':
        return 10
    if row_label == 'K':
        return 11
    if row_label == 'L':
        return 12
    if row_label == 'M':
        return 13
    if row_label == 'N':
        return 14
    if row_label == 'O':
        return 15
    if row_label == 'P':
        return 16
    if row_label == 'Q':
        return 17
    if row_label == 'R':
        return 18
    if row_label == 'S':
        return 19
    if row_label == 'T':
        return 20
    if row_label == 'U':
        return 21
    if row_label == 'V':
        return 22
    if row_label == 'W':
        return 23
    if row_label == 'X':
        return 24
    if row_label == 'Y':
        return 25
    if row_label == 'Z':
        return 26
    if row_label == '0':
        return 27
    if row_label == '1':
        return 28
    if row_label == '2':
        return 29
    if row_label == '3':
        return 30
    if row_label == '4':
        return 31
    if row_label == '5':
        return 32
    if row_label == '6':
        return 33
    if row_label == '7':
        return 34
    if row_label == '8':
        return 35
    if row_label == '9':
        return 36
    if row_label == 'a':
        return 37
    if row_label == 'b':
        return 38
    if row_label == 'c':
        return 39
    if row_label == 'd':
        return 40
    if row_label == 'e':
        return 41
    if row_label == 'f':
        return 42
    if row_label == 'g':
        return 43
    if row_label == 'h':
        return 44
    if row_label == 'i':
        return 45
    if row_label == 'j':
        return 46
    if row_label == 'k':
        return 47
    if row_label == 'l':
        return 48
    if row_label == 'm':
        return 49
    if row_label == 'n':
        return 50
    if row_label == 'o':
        return 51
    if row_label == 'p':
        return 52
    if row_label == 'q':
        return 53
    if row_label == 'r':
        return 54
    if row_label == 's':
        return 55
    if row_label == 't':
        return 56
    if row_label == 'u':
        return 57
    if row_label == 'v':
        return 58
    if row_label == 'w':
        return 59
    if row_label == 'x':
        return 60
    if row_label == 'y':
        return 61
    if row_label == 'z':
        return 62
    if row_label == '!':
        return 63
    if row_label == '?':
        return 64
    if row_label == '%':
        return 65
    else:
        return None
        
def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_png = fid.read()
    encoded_png_io = io.BytesIO(encoded_png)
    image = Image.open(encoded_png_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'png'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_png),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(os.getcwd(), FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
