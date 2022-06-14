import serial

from serialRead import BicepCurlData
from ClassifyData import ClassifyData, ClassifyDataVariable
from filter import medianFilter, averageFilter
import numpy as np


def readWithLoop():
    bcd_ = BicepCurlData()

    # make first wait 20 sec
    wait_t = 20

    # open serial port
    bus = serial.Serial("COM7", 115200, timeout=1)

    while True:
        # start when enter is pressed or exit with "exit"
        i_in = input("pres enter to start or \"exit\"")
        if i_in == "exit":
            break
        bcd_.data = []  # clear data

        # read data from serial port
        bcd_.readFromSerial(bus, 1000, wait_t, 10)
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


def compairInput():
    bcd_ = BicepCurlData()
    cd_ = ClassifyData()

    # make first wait 20 sec
    wait_t = 20

    # open serial port
    bus = serial.Serial("COM7", 9600, timeout=1)

    while True:
        # start when enter is pressed or exit with "exit"
        i_in = input("press enter to start or \"exit\"")
        if i_in == "exit":
            break
        bcd_.data = []  # clear data

        # read data from serial port
        bcd_.readFromSerial(bus, 1000, wait_t, 10)
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


def importAllClassificationData():
    emma = 15
    jarno = 11
    joris = 12
    sua = 20

    filter_n = 15

    for i in range(1,emma+1):
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
    # compairInput()
    # readWithLoop()
    # importAllClassificationData()

    bcd = BicepCurlData()
    bcd.readJSONFile("valid/data_emma_valid_snel_en_hoog.json")
    bcd.data = medianFilter(bcd.data)
    bcd.data = averageFilter(bcd.data, 15)
    bcd.plotDataWithTime()
    #
    cd = ClassifyData()
    cd.importInputData(bcd.data)
    cd.classifyCheck()
    # print(cd)
    # cd.importClassificationData(bcd.data)
    # cd.writeJSONFile()


    # bcd = BicepCurlData()
    # bcd.readJSONFile("sua/goede_data.json")
    # # # bcd.writeJSONFile("fail.json")
    # bcd.data = medianFilter(bcd.data)
    # bcd.data = averageFilter(bcd.data, 11)
    # # # bcd.writeJSONFile("fail.json")
    # #
    # # # # bcd.readFromSerial(serial.Serial("COM7", 9600, timeout=1), 1000, 20, 10)
    # # # bcd.data = medianFilter(bcd.data)
    # # # bcd.data = averageFilter(bcd.data, 11)
    # # # bcd.plotDataWithTime()
    # # #
    # cd = ClassifyData()
    # cd.importInputData(bcd.data)
    # # # # print(cd)
    # cd.classifyCheck()
    # # cd.importClassificationData(bcd.data)
    # # cd.writeJSONFile()




    # bcd.readJSONFile("sua/goede_data.json")
    # bcd.data = averageFilter2(bcd.data, 11)
    # bcd.plotDataWithTime()

    # cd = ClassifyData(bcd.data)
    # cd.readJSONFile()
    # # cd.importClassificationData()

    # cd.writeJSONFile()


    # c = ClassifyDataVariable()
    # cd = ClassifyData(bcd.data)
    # print(c.checkDataValid())
    # lp_0 = cd.getLowPoints(0)
    # hp_0 = cd.getHighPoints(0)
    # lp_1 = cd.getLowPoints(1)
    # hp_1 = cd.getHighPoints(1)
    # lp_2 = cd.getLowPoints(2)
    # hp_2 = cd.getHighPoints(2)
    # lp_3 = cd.getLowPoints(3)
    # hp_3 = cd.getHighPoints(3)
    # lp_4 = cd.getLowPoints(4)
    # hp_4 = cd.getHighPoints(4)
    # lp_5 = cd.getLowPoints(5)
    # hp_5 = cd.getHighPoints(5)
    #
    # c.avg_time = cd.getAverageTimeBetweenPoints(lp_1)
    # c.max_time = cd.maxTimeBetweenPoints(lp_1)
    # c.min_time = cd.minTimeBetweenPoints(lp_1)
    #
    # c.farm_yaw_max = cd.maxValueOnPoint(hp_0, 0)
    # c.farm_roll_max = cd.maxValueOnPoint(hp_1, 1)
    # c.farm_pitch_max = cd.maxValueOnPoint(hp_2, 2)
    # c.uarm_yaw_max = cd.maxValueOnPoint(hp_3, 3)
    # c.uarm_roll_max = cd.maxValueOnPoint(hp_4, 4)
    # c.uarm_pitch_max = cd.maxValueOnPoint(hp_5, 5)
    #
    # c.farm_yaw_min = cd.minValueOnPoint(lp_0, 0)
    # c.farm_roll_min = cd.minValueOnPoint(lp_1, 1)
    # c.farm_pitch_min = cd.minValueOnPoint(lp_2, 2)
    # c.uarm_yaw_min = cd.minValueOnPoint(lp_3, 3)
    # c.uarm_roll_min = cd.minValueOnPoint(lp_4, 4)
    # c.uarm_pitch_min = cd.minValueOnPoint(lp_5, 5)
    #
    # print(c.checkDataValid())



    # bcd = BicepCurlData()
    # bcd.readJSONFile("sua/goede_data.json")
    #
    # # bcd.plotDataWithTime()
    # bcd.data = averageFilter2(bcd.data, 11)
    # bcd.plotDataWithTime()
    #
    # cd = ClassifyData(bcd.data)
    # lp = cd.getLowPoints(1)
    # hp = cd.getHighPoints(1)
    # print("aantal points = {}".format(len(lp)))
    # print("max time = {}".format(cd.maxTimeBetweenPoints(lp)))
    # print("min time = {}".format(cd.minTimeBetweenPoints(lp)))
    # print("avg time lp = {}".format(cd.getAverageTimeBetweenPoints(lp)))
    # print(hp)
    # print(cd.maxValueOnPoint(hp, 1))


    # # bcd.readFromSerial(serial.Serial("COM5", 9600, timeout=1), 1000, 20, 10)
    # bcd.plotDataWithTime()
    # bcd.writeJSONFile()
    #
    # m = medianFilter(bcd.data)
    # for i in range(6):
    #
    # a = np.convolve(bcd.data[], [0.5, 1, 0.5], 'full')
    #
    # cd = ClassifyData(a)
    # x = cd.getAverageTimeBetweenCurls(1)
    # print(x)



