# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:21:47 2019

@author: palewis
"""

import numpy as np
import pandas as pd
import requests
import time
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

class Cheque(object):
    def __init__(self, API_Code, date_chequed = '', text_value= 0, numeric_value= 0, recipient = '', sender = '',memo='',MICR=''):
        self.API_Code = API_Code
        self.date_chequed = date_chequed
        self.text_value = text_value
        self.numeric_value = numeric_value
        self.recipient = recipient
        self.sender = sender
        self.memo = memo

def check_cheque(subscription_key, image_input):
    assert subscription_key

    vision_base_url = "https://northcentralus.api.cognitive.microsoft.com/vision/v2.0/"
    
    text_recognition_url = vision_base_url + "read/core/asyncBatchAnalyze"
    
    
    

    
    params  = {'language': 'unk', 'detectOrientation': 'true'}


    #Here we split out whether we are accessing local data or URL data
    #simply split by whether there is https on the front of the input
    if image_input[0:5] != 'https':
        headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
        image_data = open(image_input, "rb").read()
        response = requests.post(
            text_recognition_url, headers=headers, params=params, data=image_data)
        image = Image.open(BytesIO(image_data))


    else:
        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        data    = {'url': image_input}
        response = requests.post(
            text_recognition_url, params=params, headers=headers, json=data)
        image = Image.open(BytesIO(requests.get(image_input).content))

        
    response.raise_for_status()
    
    # Extracting handwritten text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.
    
    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]
    
    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        #print(analysis)
        time.sleep(1)
        if ("recognitionResults" in analysis):
            poll= False 
        if ("status" in analysis and analysis['status'] == 'Failed'):
            poll= False
    
    polygons=[]
    if ("recognitionResults" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
            for line in analysis["recognitionResults"][0]["lines"]]
    
    
    
    #print(polygons)
    #at this point we have all of the text that we have recognized
    
    
    #Display the image and overlay it with the extracted text.
    
    plt.figure(figsize=(15, 15))
    
    ax = plt.imshow(image)
    for polygon in polygons:
        vertices = [(polygon[0][i], polygon[0][i+1])
            for i in range(0, len(polygon[0]), 2)]
        text     = polygon[1]
        patch    = Polygon(vertices, closed=True, fill=False, linewidth=2, color='b')
        ax.axes.add_patch(patch)
        plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
        
    
    text_analysis =  [text[1] for text in polygons]
    return text_analysis
        
