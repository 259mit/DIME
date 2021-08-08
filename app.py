import streamlit as st
from pyngrok import ngrok
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import re
from matplotlib.backends.backend_agg import RendererAgg
from numpy.lib.stride_tricks import as_strided
import skimage.measure
import os
import cv2
import numpy as np
import keras
from keras.preprocessing import image
from keras.preprocessing.image import load_img, img_to_array
import pydicom
import pydicom.uid
from pydicom.data import get_testdata_files
import warnings
warnings.filterwarnings('ignore')

col1, col2, col3 = st.columns([1,6,1])

with col1:
  st.write("")

with col2:
  st.image('/content/Dime.png', clamp = True, use_column_width=True)
  st.title("DIME - Disease Identification Made Easy")
  st.header("Breast Cancer CT Scan Classification using CNNs")
  st.subheader('By Mithesh Ramachandran and Sagarika Raje')

with col3:
  st.write("")


st.text("Upload a CT Scan Image (Dicom format) for image classification as PCR or NON PCR")


model = keras.models.load_model('/content/final_model.h5')

uploaded_file = st.file_uploader("Choose a DICOM IMAGE ...", type="dcm")
if uploaded_file is not None:
        ds = pydicom.read_file(uploaded_file, force=True)
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        #img = np.array(pydicom.dcmread(uploaded_file).pixel_array)
        img = np.array(ds.pixel_array)
        st.image(img, caption='Uploaded CT Scan.', clamp=True, use_column_width=True)
        img=img/4096
        img=np.reshape(img,(700,700))
        img = np.expand_dims(img, axis=0)
        st.write("")
        st.write("Classifying...")
        ans=(model.predict(img) > 0.5).astype("int32")
        if ans.astype('int32') == 0:
            st.write('Its a PCR Image')
        elif ans.astype('int32') == 1:
            st.write('Its a Non PCR Image')
