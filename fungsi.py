import os
import glob
import string
import random
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt

from flask import session
from tensorflow.keras import backend
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Conv2D, Lambda, Dense, Flatten

siamese_model = tf.keras.models.load_model('Model-epoch-4')

path_store = 'static/pict_test/stored_image'
path_input = 'static/pict_test/input_image'
dir_path = r'static/pict_test/stored_image/**/*.jpg*'
img_path = []
for file in glob.glob(dir_path, recursive=True):
    img_path.append(file)

def get_random_string(length):
    # random string dengan kombinasi upper dan lower case
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def pair_list(input_file_name):
    dir_inp = os.path.join(path_input,input_file_name)
    stored_img_path = []
    input_img_path = []
    for file in glob.glob(dir_path, recursive=True):
        stored_img_path.append(file)
        input_img_path.append(dir_inp)
    return stored_img_path, input_img_path

def prep(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (128,128))
    image = tf.expand_dims(image, axis=0)
    return image

def preds(input):
    y_pred = siamese_model.predict(input)
    return y_pred[0][0]

def pred_image(data):
    input_dir = session.get('uploaded_img_file_path', None)
    file_dir  = data['file_path']
    y_pred = []
    
    #membaca gambar input/yang ingin ditest karena semua input sama maka tidak perlu dilooping
    im_test = prep(input_dir)
    for i in range(len(file_dir)):
        #membaca gambar stored
        im_strd = prep(file_dir[i])
        #membuat list untuk dimasukan ke dua input
        im = [im_test,im_strd]
        pred = preds(im)
        y_pred.append(pred)

    return y_pred

def visualize(data):
    data = df.loc[df['pred'] >= 0.5]
    inp = df['input_path'].iloc[0]
    plt.figure(figsize = (5,5))
    inp_im = cv2.imread(inp)
    inp_im = cv2.cvtColor(inp_im, cv2.COLOR_BGR2RGB)
    plt.imshow(inp_im)
    plt.title(label="Input Image",fontsize=14)
    plt.show()
    for i in range(len(data)):
        #membuat variabel path stored image
        strd = data['file_path'].iloc[i]
        #membuat variabel nama image
        fl_name = data['file_path'].iloc[i].split("\\")[3]
        #membuat variabel nilai preediksi
        pred = round(float(data['pred'].iloc[0]),3)
        
        #membuat plot gambar
        plt.figure(figsize = (5,5))
        strd_im = cv2.imread(strd)
        strd_im = cv2.cvtColor(strd_im, cv2.COLOR_BGR2RGB)
        plt.imshow(strd_im)
        plt.title(label=f"{fl_name} have {pred} similarity with Input Image",fontsize=14)
        plt.show()