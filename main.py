import serial

from serialRead import BicepCurlData
from ClassifyData import ClassifyData
from filter import medianFilter, averageFilter2
import numpy as np

import serial

if __name__ == '__main__':
    bcd = BicepCurlData()
    bcd.readJSONFile("sua/goede_data.json")

    # bcd.plotDataWithTime()
    bcd.data = averageFilter2(bcd.data, 11)
    bcd.plotDataWithTime()

    cd = ClassifyData(bcd.data)
    lp = cd.getLowPoints(1)
    hp = cd.getHighPoints(1)
    print("aantal points = {}".format(len(lp)))
    print("max time = {}".format(cd.maxTimeBetweenPoints(lp)))
    print("min time = {}".format(cd.minTimeBetweenPoints(lp)))
    print("avg time lp = {}".format(cd.getAverageTimeBetweenPoints(lp)))
    print(hp)


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



