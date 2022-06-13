import serial

from serialRead import BicepCurlData
from ClassifyData import ClassifyData, ClassifyDataVariable
from filter import medianFilter, averageFilter2
import numpy as np


import serial

#TODO: verander var naar diff ipv min en max
#TODO: samenvoegen van de classifier data voor de perfecte curl
#TODO: toepassen classifier op de data


def readWithLoop():
    bcd = BicepCurlData()

    wait_t = 20

    bus = serial.Serial("COM7", 9600, timeout=1)

    while (True):

        i_in = input("pres enter to start or \"exit\"")
        if i_in == "exit":
            break
        bcd.data = []
        bcd.readFromSerial(bus, 1000, wait_t, 10)
        bcd.plotDataWithTime()
        f_name = "data_" + input("filename:") + ".json"
        print(f_name)
        bcd.writeJSONFile(f_name)
        print("")
        wait_t = 1


if __name__ == '__main__':
    # readWithLoop()

    bcd = BicepCurlData()
    # bcd.readJSONFile("data_emma_goed4.json")
    bcd.readFromSerial(serial.Serial("COM7", 9600, timeout=1), 1000, 20, 10)
    bcd.data = medianFilter(bcd.data)
    bcd.data = averageFilter2(bcd.data, 11)
    bcd.plotDataWithTime()

    cd = ClassifyData()
    cd.importInputData(bcd.data)
    # print(cd)
    cd.classifyCheck()
    # cd.importClassificationData(bcd.data)
    # cd.writeJSONFile()




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



