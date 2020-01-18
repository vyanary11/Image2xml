import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

from imageio import imread
import numpy as np
import tensorflow as tf
from io import BytesIO
#from utils import label_map_util

from PIL import Image
import re, time, base64

from random import randint

import mappingjson

app = Flask(__name__)

# Adding Cross Origin Resource Sharing to allow requests made from the front-end
# to be successful.
CORS(app)

# Defining the model configuration files.
# Change these files to add your own model!
dir_path = os.path.dirname(os.path.realpath(__file__))
MODEL_DETECT_PATH = dir_path + '/model/frozen_inference_graph.pb'

##################################################
# Utilities
##################################################



# Membaca classes
def getLabel(index):
    label=[
        'toolbar',
        'switch',
        'textView',
        'slider',
        'radioButton',
        'navigationButton',
        'button',
        'checkBox',
        'editText',
        'ratingBar',
        'floatingButton',
    ]
    return label[index-1]

# Merubah codec base64 menjadi gambar
def getImageDataFromBase64(codec):
    base64_data = re.sub(b'^data:image/.+;base64,', b'', codec)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img.convert('RGB')

def sortDataJsonASC(e):
    return e['ymax']

def sortDataJsonxmax(e):
    return e['xmax']  

def medianKoordinat(array): 
    median=(array[0]+array[1])/2
    return median

# menghitung max score dan menjadikan data JSON
def getJSONdata(scores, num, predictions_det, prediction_boxes_det):
    maxes=[]
    classes=[]
    databelumurut=[]
    databbox=[]
    data={}
    jsonMentah=[]
    jsonWithHorizontal={}
    jsonWithHorizontalArray=[]
    jsonChildrenHorizontalArrayFix=[]
    jsonWithVertical={}
    jumlahHorizontal=0
    horizontalFind = False

    #Menghitung Score tertinggi dari jumlah deteksi untuk mendapatkan object yang valid dengan nilai thershold 0.85
    for i in range(num):
        if scores[i] > 0.85:
            classes.append(getLabel(predictions_det[i]))
            maxes.append(scores[i])
            databbox.append(prediction_boxes_det[i])

    #Menjadikan data yang telah terpilih menjadi JSON dan diurutkan berdasarkan nilai YMAX atau titik Y yang paling besar
    for i in range(len(classes)):        
        data={
            'label'     : classes[i],
            'score'     : maxes[i],
            'ymin'      : databbox[i][0],
            'xmin'      : databbox[i][1],
            'ymax'      : databbox[i][2],
            'xmax'      : databbox[i][3],  
        }
        jsonMentah.append(data)
    jsonMentah.sort(key=sortDataJsonASC)

    #Proses Memunculkan Label Linier Horizontal
    for i in range(len(jsonMentah)):
        #Menjadikan Nilai ymin dan ymax dari object acuan menjadi deret angka
        deretKoordinat=[]
        deretKoordinat.append(jsonMentah[i-1]['ymin'])
        deretKoordinat.append(jsonMentah[i-1]['ymax'])

        #Mencari Nilai Tengah dari deret angka sebelumnya
        median=medianKoordinat(deretKoordinat)
 
        if(jsonMentah[i]['ymin']<median and jsonMentah[i]['ymax']>median): #Kondisi jika Nilai tengah dari acuan ada diantara object ini
            if(horizontalFind==False): #Kondisi jika linier horizontal ditemukan untuk pertama kalinya maka object acuan akan dimasukkan sebagai children dari linear horizontal
                jsonChildrenHorizontal={}
                jsonChildrenHorizontalArray=[]
                jsonChildrenHorizontal={
                    'label'     : jsonMentah[i-1]['label'],
                    'score'     : jsonMentah[i-1]['score'],
                    'ymin'      : jsonMentah[i-1]['ymin'],
                    'xmin'      : jsonMentah[i-1]['xmin'],
                    'ymax'      : jsonMentah[i-1]['ymax'],
                    'xmax'      : jsonMentah[i-1]['xmax'],
                }
                jsonChildrenHorizontalArray.append(jsonChildrenHorizontal)
                if(i==len(jsonMentah)-1): #Kondisi menambahkan liniear horizontal pada data mentah jika kondisi sebelumnya terpenuhi. kondisi ini berlaku pada saat ditemukan liniear horizontal pada data terakhir
                    jumlahHorizontal=jumlahHorizontal+1
                    jsonChildrenHorizontalArrayFix.append(jsonChildrenHorizontalArray)
                    jsonWithHorizontalArray.pop(len(jsonWithHorizontalArray)-1)
                    jsonWithHorizontal={
                        'label'     : 'linearHorizontal',
                        'children'  : jsonChildrenHorizontalArrayFix[jumlahHorizontal-1]
                    }
                    jsonWithHorizontalArray.append(jsonWithHorizontal)

            #menambahkan object(bukan object acuan) menjadi sebuah children dari liniear horizontal
            jsonChildrenHorizontal={
                'label'     : jsonMentah[i]['label'],
                'score'     : jsonMentah[i]['score'],
                'ymin'      : jsonMentah[i]['ymin'],
                'xmin'      : jsonMentah[i]['xmin'],
                'ymax'      : jsonMentah[i]['ymax'],
                'xmax'      : jsonMentah[i]['xmax'],
            }
            jsonChildrenHorizontalArray.append(jsonChildrenHorizontal)
            horizontalFind=True    
        else:
            if(horizontalFind==True):  #Kondisi menambahkan liniear horizontal pada data mentah kondisi ini berlaku saat ada linier horizontal yang berada di tengah - tengah object yang lain
                jumlahHorizontal=jumlahHorizontal+1
                jsonChildrenHorizontalArrayFix.append(jsonChildrenHorizontalArray)
                jsonWithHorizontalArray.pop(len(jsonWithHorizontalArray)-1)
                jsonChildrenHorizontalArrayFix[jumlahHorizontal-1].sort(key=sortDataJsonxmax)
                jsonWithHorizontal={
                    'label'     : 'linearHorizontal',
                    'children'  : jsonChildrenHorizontalArrayFix[jumlahHorizontal-1]
                }
                jsonWithHorizontalArray.append(jsonWithHorizontal)

            #menambahkan object yang bersifat tunggal tidak memiliki parent liniear horizontal
            jsonWithHorizontal={
                'label'     : jsonMentah[i]['label'],
                'score'     : jsonMentah[i]['score'],
                'ymin'      : jsonMentah[i]['ymin'],
                'xmin'      : jsonMentah[i]['xmin'],
                'ymax'      : jsonMentah[i]['ymax'],
                'xmax'      : jsonMentah[i]['xmax'], 
            }
            jsonWithHorizontalArray.append(jsonWithHorizontal)
            horizontalFind=False
    print(jsonWithHorizontalArray)
    #Menyederhanakan JSON dan mapping json android
    jsonForXMLArray=[]
    jsonVerticalArray={}
    verticalFind=False
    verticalAdd=False
    for i in range(len(jsonWithHorizontalArray)):
        jsonForXML={}
        if(jsonWithHorizontalArray[i]['label']=='toolbar' or jsonWithHorizontalArray[i]['label']=='navigationButton' or jsonWithHorizontalArray[i]['label']=='floatingButton'):            
            jsonForXML = mappingjson.get(jsonWithHorizontalArray[i]['label'])
            jsonForXMLArray.append(jsonForXML)
        else:
            if(verticalFind==False):
                jsonVerticalArray = {
                    'name'      : 'LinearLayout',
                    'attrs'     : {
                        'android:layout_margin' : '8dp',
                        'android:layout_below'  : '@+id/toolbar',
                        'android:layout_width'  : 'match_parent',
                        'android:layout_height' : 'wrap_content',
                        'android:orientation'   : 'vertical',
                    },
                    'children'  : []
                }
                verticalFind=True

            if(jsonWithHorizontalArray[i]['label']=='linearHorizontal'):
                jsonVerticalArray['children'].append(mappingjson.get(jsonWithHorizontalArray[i]['label']))
                for j in range(len(jsonWithHorizontalArray[i]['children'])):
                    jsonVerticalArray['children'][len(jsonVerticalArray['children'])-1]['children'].append(mappingjson.get(jsonWithHorizontalArray[i]['children'][j]['label']))                                       
            else:        
                jsonVerticalArray['children'].append(mappingjson.get(jsonWithHorizontalArray[i]['label']))

            if(verticalAdd==False):
                jsonForXMLArray.append(jsonVerticalArray)   
                verticalAdd=True

    return jsonForXMLArray

##################################################
# REST API Endpoints For Web App
##################################################

@app.route('/')
def homepage():
    return ''


@app.route('/detect_image_objects', methods=['POST'])
def detect_image_objects():
    request.get_data()
    
    # Load in an image to object detect and preprocess it
    img_data = getImageDataFromBase64(request.data)
    x_input = np.expand_dims(img_data, axis=0)

    # Setting initial detection time, so execution time can be calculated.    
    t_det = time.time()

    # Get the predictions (output of the softmax) for this image
    tf_results_det = sess_det.run([output_tensor_det,detection_boxes,detection_scores,detection_num], {input_tensor_det : x_input})

    dt_det = time.time() - t_det
    app.logger.info("Execution time: %0.2f" % (dt_det * 1000.))

    # Different results arrays
    predictions_det = tf_results_det[0]
    prediction_scores_det=tf_results_det[2]
    prediction_boxes_det=tf_results_det[1]
    prediction_num_det=tf_results_det[3]
    
    jsonData = {
        'type'  : "test",
        'data'  : getJSONdata(prediction_scores_det[0], int(prediction_num_det), predictions_det[0].astype(int).tolist(), prediction_boxes_det[0].astype(float).tolist())
    }
    return jsonify(jsonData)


##################################################
# Mulai server
##################################################


if __name__ == '__main__':
    print('Starting TensorFlow Server')

    print('Mengkonfigurasi TensorFlow Graph..')
    sess_config = tf.ConfigProto(
        log_device_placement=False,
        allow_soft_placement = True
    )

    print('Loading Model...')
    with open(MODEL_DETECT_PATH, 'rb') as k:
        graph_def=tf.GraphDef()
        graph_def.ParseFromString(k.read())

    graph = tf.Graph()
    with graph.as_default():
        tf.import_graph_def(graph_def, name='')

    graph.finalize()

    sess_det = tf.Session(graph=graph, config=sess_config)

    print('Server Start.')

    input_op_det = graph.get_operation_by_name('image_tensor')
    input_tensor_det = input_op_det.outputs[0]

    output_op_det = graph.get_operation_by_name('detection_classes')
    output_tensor_det = output_op_det.outputs[0]

    detection_boxes_op=graph.get_operation_by_name('detection_boxes')
    detection_boxes=detection_boxes_op.outputs[0]

    detection_scores_op=graph.get_operation_by_name('detection_scores')
    detection_scores=detection_scores_op.outputs[0]

    detection_num_op=graph.get_operation_by_name('num_detections')
    detection_num=detection_num_op.outputs[0]

    app.run(debug=False, host='0.0.0.0', port='5000')