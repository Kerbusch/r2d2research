import time
import serial
import json
import matplotlib.pyplot as plt
import numpy as np

# data verzamelen over 1 hele curl met 2 sensoren
# data opslaan
# data in array met daarin de sensorlocatie, de waarde en de tijd
# kijken wanneer de arm van onder naar boven en terug is

# data analyseren en feedback geven
# Kijken naar snelheid
# Kijken naar hoekhoogte


class BicepCurlData:
    # Constructor with read from file
    def __init__(self):
        # Initialize the data with forearm (yaw, roll, pitch), upperarm (yaw, roll, pitch) and time since last datapoint
        self.data = []  # [y, r, p, y, r, p, tijd]
        self.last_farm_data = None
        self.last_uarm_data = None
        self.start_time = None
        self.file_name = "data.txt"

        # read file
        # self.readJSONFile()

    # Get the data
    def input(self, yaw0, roll0, pitch0, yaw1, roll1, pitch1):
        if self.start_time is None:
            self.start_time = time.time()
        self.data.append([float(yaw0), float(roll0), float(pitch0), float(yaw1), float(roll1), float(pitch1), time.time() - self.start_time])

    # input data with farm prefix
    def input_farm(self, yaw, roll, pitch):
        self.last_farm_data = [yaw, roll, pitch]
        if self.last_uarm_data is not None:
            self.input(self.last_farm_data[0], self.last_farm_data[1], self.last_farm_data[2], self.last_uarm_data[0], self.last_uarm_data[1], self.last_uarm_data[2])
            self.last_uarm_data = None
            self.last_farm_data = None

    # input data with uarm prefix
    def input_uarm(self, yaw, roll, pitch):
        self.last_uarm_data = [yaw, roll, pitch]
        if self.last_farm_data is not None:
            self.input(self.last_farm_data[0], self.last_farm_data[1], self.last_farm_data[2], self.last_uarm_data[0], self.last_uarm_data[1], self.last_uarm_data[2])
            self.last_uarm_data = None
            self.last_farm_data = None

    # split the data on the :
    def splitData(self, data):
        data = str(data)
        data = data.replace("\\n", "")
        data = data.replace("\n", "")
        data = data.replace("\\r", "")
        data = data.replace("\r", "")
        data = data.replace("b'", "")
        data = data.replace("'", "")
        data_split = data.split(":")
        return data_split

    # input data with an array as input can use splitData function
    def inputData(self, sensor_data):
        if sensor_data is None:
            return None
        if sensor_data[0] == "farm":
            self.input_farm(sensor_data[1], sensor_data[2], sensor_data[3])
        elif sensor_data[0] == "uarm":
            self.input_uarm(sensor_data[1], sensor_data[2], sensor_data[3])
        return None

    # Write the data to a file
    def writeJSONFile(self):
        with open("data.json", "w") as file:
            json.dump(self.data, file, indent=1)

    # Read the data from a file
    def readJSONFile(self):
        with open("data.json", "r") as file:
            if file.read() == "":
                return None
        with open("data.json", "r") as file:
            self.data = json.load(file)
        return None

    def plotData(self):
        # Plot the data
        d = self.filterDataPeak()
        plt.plot(d)
        plt.legend(['f yaw', 'f roll', 'f pitch', 'u yaw', 'u roll', 'u pitch', 'time'])
        plt.show()
        return None

    def plotDataWithTime(self):
        # Plot the data
        d = self.filterDataPeak()

        x = []
        for point in d:
            x.append(point[6])

        y = []
        for point in d:
            y.append(point[0:6])

        plt.plot(x, y)
        plt.title("data from the 2 sensors on time base")
        plt.xlabel("Time")
        plt.ylabel("degrees")
        plt.legend(['f yaw', 'f roll', 'f pitch', 'u yaw', 'u roll', 'u pitch'])
        plt.show()
        return None

    def filterDataPeak(self):
        # for i in range(len(self.data[0])):  # 0 - 6
        #     for j in range(1, len(self.data)-1): # data
        #         self.data[j][i] = (self.data[j][i] + self.data[j][i-1] + self.data[j][i+1]) / 3
        for i in range(2, len(self.data)-2):
            for j in range(len(self.data[i])):
                # average of the 5 values
                # self.data[i][j] = (self.data[i][j] + self.data[i-1][j] + self.data[i-2][j] + self.data[i+1][j] + self.data[i+2][j]) / 5

                # median
                self.data[i][j] = np.median((self.data[i-2][j], self.data[i-1][j], self.data[i][j], self.data[i+1][j], self.data[i+2][j]))

        return self.data

    def readFromSerial(self, bus: serial.Serial):
        t_now = time.time()

        serial_timer_done = False

        for n in range(0, 1000):
            s_strin = ser.read_until(b'\n')
            if time.time() - t_now > 0:
                if not serial_timer_done:
                    serial_timer_done = True
                    print("now")
                self.inputData(bcd.splitData(s_strin))




# s = b'farm:90.00:90.00:90.00\n'
# s1 = b'farm:50.00:50.00:50.00\n'
# s2 = b'uarm:40.00:40.00:40.00\n'
# bcd = BicepCurlData()
# bcd.inputData(bcd.splitData(s))
# bcd.inputData(bcd.splitData(s1))
# bcd.inputData(bcd.splitData(s2))

# print("done")


if __name__ == "__main__":
    ser = serial.Serial("COM7", 9600, timeout=1)
    time_now = time.time()
    bcd = BicepCurlData()
    print("begin loading")
    bcd.readJSONFile()
    print("done loading")

    # bcd.readFromSerial(ser)
    # print("data collection done")
    #
    # bcd.writeJSONFile()
    # print("done writing")

    bcd.plotData()

    print("done")
