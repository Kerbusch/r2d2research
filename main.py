from serialRead import BicepCurlData
from ClassifyData import ClassifyData

if __name__ == '__main__':
    bcd = BicepCurlData()
    bcd.readJSONFile()
    bcd.plotDataWithTime()

    # cd = ClassifyData(bcd.data)
    # cd.getAverageTimeBetweenCurls()



