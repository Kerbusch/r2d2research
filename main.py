import serial

from serialRead import BicepCurlData
from ClassifyData import ClassifyData

import serial

if __name__ == '__main__':
    bcd = BicepCurlData()
    # bcd.readJSONFile()
    bcd.readFromSerial(serial.Serial("COM7", 9600, timeout=1), 1000, 18)
    bcd.plotDataWithTime()
    bcd.writeJSONFile()

    # cd = ClassifyData(bcd.data)
    # cd.getAverageTimeBetweenCurls()



