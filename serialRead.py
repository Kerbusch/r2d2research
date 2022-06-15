import time
import serial
import json
import matplotlib.pyplot as plt
import numpy as np

from filter import medianFilter, averageFilter


class BicepCurlData:
    # Constructor with read from file
    def __init__(self):
        # Initialize the data with forearm (yaw, roll, pitch), upperarm (yaw, roll, pitch) and time since last datapoint
        self.data = []  # [y, r, p, y, r, p, tijd]
        self.last_farm_data = None
        self.last_uarm_data = None
        self.start_time = None

    # Get the data
    def input(self, yaw0, roll0, pitch0, yaw1, roll1, pitch1):
        if self.start_time is None:
            self.start_time = time.time()
        try:
            self.data.append([float(yaw0), float(roll0), float(pitch0), float(yaw1), float(roll1), float(pitch1), time.time() - self.start_time])
        except ValueError:
            print("ValueError, data not added")
            # this happens when the arduino sends wrong data to the serial bus.

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
    def splitData(self, data, expected_output_length=6):
        data = str(data)
        data = data.replace("\\n", "")
        data = data.replace("\n", "")
        data = data.replace("\\r", "")
        data = data.replace("\r", "")
        data = data.replace("b'", "")
        data = data.replace("'", "")
        data_split = data.split(":")
        if len(data_split) != expected_output_length:
            return None
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
    def writeJSONFile(self, file_name):
        with open(file_name, "w") as file:
            print(type(self.data))
            if type(self.data) is np.ndarray:
                json.dump(self.data.tolist(), file, indent=1)
            else:
                json.dump(self.data, file, indent=1)

    # Read the data from a file
    def readJSONFile(self, file_name):
        with open(file_name, "r") as file:
            if file.read() == "":
                return None
        with open(file_name, "r") as file:
            self.data = json.load(file)
        return None

    # Plot the data with time on the x-axis and the data on the y-axis
    def plotDataWithTime(self):
        # Plot the data
        d = self.data
        # d = medianFilter(self.data)
        # d = averageFilter2(d, 11)
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

    # Read the data from the serial port and input it to the data array
    def readFromSerial(self, bus: serial.Serial, n: int = 1000, wait: int = 10, length: int = 10):
        t_now = time.time()
        t_begin = None
        print("waiting {} seconds".format(wait))

        serial_timer_done = False
        done = False

        while not done:
            s_strin = bus.read_until(b'\n')
            if time.time() - t_now > wait:
                if not serial_timer_done:
                    serial_timer_done = True
                    print("now")
                    t_begin = time.time()
                    self.start_time = time.time()
                self.inputData(self.splitData(s_strin, 4))
            if t_begin is not None and time.time() - t_begin > length:
                done = True
                print("done")
