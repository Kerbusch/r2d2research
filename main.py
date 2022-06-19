import serial

from serialRead import BicepCurlData
from ClassifyData import ClassifyData, ClassifyDataVariable
from filter import medianFilter, averageFilter
import numpy as np


# get the data from the serial port and write it to a json file
def readWithLoop():
    bcd_ = BicepCurlData()

    # make first wait 20 sec
    wait_t = 20

    # open serial port
    bus = serial.Serial("COM5", 115200, timeout=1)

    while True:
        # start when enter is pressed or exit with "exit"
        i_in = input("pres enter to start or \"exit\"")
        if i_in == "exit":
            break
        bcd_.data = []  # clear data

        # read data from serial port
        bcd_.readFromSerial(bus, wait_t, 10)
        if bcd_.data == []:
            print("no data, try again")
            continue

        # print(bcd_.data)
        bcd_.data = medianFilter(bcd_.data)
        # print(bcd_.data)
        bcd_.data = averageFilter(bcd_.data, 11)
        # print(bcd_.data)
        bcd_.plotDataWithTime()

        # get filename for saving data
        f_name = "data_" + input("filename:") + ".json"
        print(f_name)
        bcd_.writeJSONFile(f_name)
        print("")
        wait_t = 1


# read the input classification files and get the classification of the input data
def compareInput():
    bcd_ = BicepCurlData()
    cd_ = ClassifyData()

    # make first wait 20 sec
    wait_t = 20

    # open serial port
    bus = serial.Serial("COM5", 9600, timeout=1)

    while True:
        # start when enter is pressed or exit with "exit"
        i_in = input("press enter to start or \"exit\"")
        if i_in == "exit":
            break
        bcd_.data = []  # clear data

        # read data from serial port
        bcd_.readFromSerial(bus, wait_t, 10)
        if bcd_.data == []:
            print("no data, try again")
            continue

        bcd_.data = medianFilter(bcd_.data)
        bcd_.data = averageFilter(bcd_.data, 11)
        bcd_.plotDataWithTime()

        # import the data into the classifier and get the result
        cd_.importInputData(bcd_.data)
        cd_.classifyCheck()

        print("")
        wait_t = 1


# read the input classification files and import it into the classifier
# made for easy testing
def importAllClassificationData():
    emma = 15
    jarno = 11
    joris = 12
    sua = 20

    filter_n = 15

    for i in range(2,emma+1):  # skip first
        f_name = "data/data_emma_goed" + str(i) + ".json"
        print(f_name)
        bcd_ = BicepCurlData()
        bcd_.readJSONFile(f_name)
        bcd_.data = medianFilter(bcd_.data)
        bcd_.data = averageFilter(bcd_.data, filter_n)
        # bcd_.plotDataWithTime()
        cd_ = ClassifyData()
        cd_.importInputData(bcd_.data)
        cd_.importClassificationData(bcd_.data)
        cd_.writeJSONFile()

    for i in range(1,jarno+1):
        f_name = "data/data_jarno_goed" + str(i) + ".json"
        print(f_name)
        bcd_ = BicepCurlData()
        bcd_.readJSONFile(f_name)
        bcd_.data = medianFilter(bcd_.data)
        bcd_.data = averageFilter(bcd_.data, filter_n)
        cd_ = ClassifyData()
        cd_.importInputData(bcd_.data)
        cd_.importClassificationData(bcd_.data)
        cd_.writeJSONFile()

    for i in range(1,joris+1):
        f_name = "data/data_joris_goed" + str(i) + ".json"
        print(f_name)
        bcd_ = BicepCurlData()
        bcd_.readJSONFile(f_name)
        bcd_.data = medianFilter(bcd_.data)
        bcd_.data = averageFilter(bcd_.data, filter_n)
        cd_ = ClassifyData()
        cd_.importInputData(bcd_.data)
        cd_.importClassificationData(bcd_.data)
        cd_.writeJSONFile()

    for i in range(1,sua+1):
        f_name = "data/data_sua_goed" + str(i) + ".json"
        print(f_name)
        bcd_ = BicepCurlData()
        bcd_.readJSONFile(f_name)
        bcd_.data = medianFilter(bcd_.data)
        bcd_.data = averageFilter(bcd_.data, filter_n)
        cd_ = ClassifyData()
        cd_.importInputData(bcd_.data)
        cd_.importClassificationData(bcd_.data)
        cd_.writeJSONFile()


if __name__ == '__main__':
    # compareInput()
    # readWithLoop()
    # importAllClassificationData()

    bcd = BicepCurlData()  # create a bicep curl data object
    bcd.readJSONFile("valid/data_joris_te_laag.json")  # read the data from the json file
    bcd.data = medianFilter(bcd.data)  # apply median filter
    bcd.data = averageFilter(bcd.data, 15)  # apply average filter with 15 samples
    bcd.plotDataWithTime()  # plot the data with time

    cd = ClassifyData()  # create the classifier object
    cd.importInputData(bcd.data)  # import the data into the classifier
    cd.classifyCheck()  # classify the data
    # cd.importClassificationData(bcd.data)  # import the input data into the classification data
    # cd.writeJSONFile()  # write the classification data to a json file




