import serial

from serialRead import BicepCurlData
from ClassifyData import ClassifyData
from filter import medianFilter, averageFilter2
import numpy as np
import tensorflow as tf
import serial

if __name__ == '__main__':
    best_model_path = "/home/wilhelm/Documents/GitHub/r2d2research/sua/"
    best_model = tf.keras.models.load_model(best_model_path)
    data_collecting = True
    bus = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)
    bcd = BicepCurlData()
    bcd.readFromSerial(bus, 1000, 20, 10)
    bcd.plotData()
    best_model_path = "/home/wilhelm/Documents/GitHub/r2d2research/sua/"
    while data_collecting :
        bcd = BicepCurlData()
        input_of_user = input("give classifier input [g:good, l:too much to the left , r:too much to the right , f:too fast , s:too slow ]: ")
        if input_of_user == "q":
            data_collecting = False
        bcd.readFromSerial(bus, 1000, 2, 2)
        bcd.plotData(input_of_user)
        mg = tf.keras.preprocessing.image.load_img("data.png", target_size=(420,420))
        image = tf.keras.preprocessing.image.img_to_array(mg)
        image = np.expand_dims(image,axis=0)
        val = best_model.predict(image)
        if val.argmax(axis=1) == [0] :
            print("good bicep curl")
        if val.argmax(axis=1) == [1] :
            print("too fast")
        if val.argmax(axis=1) == [2] :
            print("too slow")
        print( val.argmax(axis=1))



