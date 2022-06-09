# import sklearn
import numpy as np

class ClassifyData:
    def __init__(self, data):
        # Initialize the data with forearm (yaw, roll, pitch), upper arm (yaw, roll, pitch) and time since last datapoint
        self.data = data  # [y, r, p, y, r, p, tijd]
        self.classification_data = data  # PLACEHOLDER voor 'goede data' voor classification

        # self.standaardafwijking_yaw = 2 # PLACEHOLDER afwijking
        # self.standaardafwijking_roll = 2 # PLACEHOLDER afwijking
        # self.standaardafwijking_pitch = 2 # PLACEHOLDER afwijking
        # self.standaardafwijking_tijd = 0.5 # goeie afwijking qua tijd
        #
        # self.farm_minimum_yaw_classify_waarde = self.classification_data[0]-self.standaardafwijking_yaw  # min van data[0] met standaardafwijking van 2
        # self.farm_maximum_yaw_classify_waarde = self.classification_data[0]+self.standaardafwijking_yaw  # max van data[0] met standaardafwijking van 2
        # self.uarm_minimum_yaw_classify_waarde = self.classification_data[3]-self.standaardafwijking_yaw  # min van data[3] met standaardafwijking van 2
        # self.uarm_maximum_yaw_classify_waarde = self.classification_data[3]+self.standaardafwijking_yaw  # max van data[3] met standaardafwijking van 2
        #
        # self.farm_minimum_roll_classify_waarde = self.classification_data[1]-self.standaardafwijking_roll  # min van data[1] met standaardafwijking van 2
        # self.farm_maximum_roll_classify_waarde = self.classification_data[1]+self.standaardafwijking_roll  # max van data[1] met standaardafwijking van 2
        # self.uarm_minimum_roll_classify_waarde = self.classification_data[4]-self.standaardafwijking_roll  # min van data[4] met standaardafwijking van 2
        # self.uarm_maximum_roll_classify_waarde = self.classification_data[4]+self.standaardafwijking_roll  # max van data[4] met standaardafwijking van 2
        #
        # self.farm_minimum_pitch_classify_waarde = self.classification_data[2]-self.standaardafwijking_pitch  # min van data[2] met standaardafwijking van 2
        # self.farm_maximum_pitch_classify_waarde = self.classification_data[2]+self.standaardafwijking_pitch  # max van data[2] met standaardafwijking van 2
        # self.uarm_minimum_pitch_classify_waarde = self.classification_data[5]-self.standaardafwijking_pitch  # min van data[5] met standaardafwijking van 2
        # self.uarm_maximum_pitch_classify_waarde = self.classification_data[5]+self.standaardafwijking_pitch  # max van data[5] met standaardafwijking van 2
        #
        # self.tijd_minimum_classify_waarde = 2-self.standaardafwijking_tijd
        # self.tijd_maximum_classify_waarde = 2+self.standaardafwijking_tijd

    def ClassifyCheck(self, data):
        if (data[0] < self.farm_minimum_yaw_classify_waarde or data[0] > self.farm_maximum_yaw_classify_waarde) or (data[3] < self.uarm_minimum_yaw_classify_waarde or data[3] > self.uarm_maximum_yaw_classify_waarde):  # if yaw is outside the minimum and maximum yaw classify value
            # zet in yaw feedback classification
            return
        if (data[1] < self.farm_minimum_roll_classify_waarde or data[1] > self.farm_maximum_roll_classify_waarde) or (data[4] < self.uarm_minimum_roll_classify_waarde or data[4] > self.uarm_maximum_roll_classify_waarde):  # if roll is outside the minimum and maximum roll classify value
            # zet in roll feedback classification
            return
        if (data[2] < self.farm_minimum_pitch_classify_waarde or data[2] > self.farm_maximum_pitch_classify_waarde) or (data[5] < self.uarm_minimum_pitch_classify_waarde or data[5] > self.uarm_maximum_pitch_classify_waarde):  # if pitch is outside the minimum and maximum pitch classify value
            # zet in pitch feedback classification
            return
        if data[6] < self.tijd_minimum_classify_waarde or data[6] > self.tijd_maximum_classify_waarde:
            # zet in tijd feedback classification
            return
        else:
            # zet bicep curl in correcte classificatie
            return

    def giveFeedback(self, classifiers: list):
        for classifier in classifiers:
            if classifier == 0:
                print("Bicep curl is done correctly")
            elif classifier == 1:
                print("Bicep curl is done too fast")
            elif classifier == 2:
                print("Bicep curl is done too slow")
            elif classifier == 3:
                print("Arm is not brought up high enough")
            elif classifier == 4:
                print("")

    def getLowPoints(self, sensor: int):
        lowest_points = []
        rounded_data = []
        for i in range(len(self.data)):
            rounded_data.append(round(self.data[i][sensor], 1))

        # print(rounded_data)

        # using the data from the forearm pitch
        for i in range(2, len(self.data)-2):
            if (rounded_data[i - 2] > rounded_data[i - 1] >= rounded_data[i]) and (rounded_data[i + 2] > rounded_data[i + 1] >= rounded_data[i]):
            # if (self.data[i - 2][sensor] > self.data[i - 1][sensor] > self.data[i][sensor]) and (self.data[i+2][sensor] > self.data[i+1][sensor] > self.data[i][sensor]):
                lowest_points.append(self.data[i])
        return lowest_points

    def getHighPoints(self, sensor: int):
        highest_points = []
        rounded_data = []
        for i in range(len(self.data)):
            rounded_data.append(round(self.data[i][sensor], 1))

        # using the data from the forearm pitch
        for i in range(2, len(self.data) - 2):
            if (rounded_data[i - 2] < rounded_data[i - 1] <= rounded_data[i]) and (
                    rounded_data[i + 2] < rounded_data[i + 1] <= rounded_data[i]):
                highest_points.append(self.data[i])
        return highest_points

    def getAverageTimeBetweenLowPoints(self, sensor: int):
        # get the time between the lowest points
        # calculate the average time between the lowest points
        lowest_points = self.getLowPoints(sensor)
        average_time_between_low_points = 0
        for i in range(len(lowest_points)-1):
            average_time_between_low_points += lowest_points[i+1][6] - lowest_points[i][6]
        average_time_between_low_points /= len(lowest_points)
        return average_time_between_low_points

    # def maxTimeBetweenPoints(self, points: list):
    #     time_between = []
    #     for i in range(len(points)-1):
    #         time_between.append(points[])
    #     return max(np.array(points)[:, 6])

    def minTimeBetweenPoints(self, points: list):
        return min(np.array(points)[:, 6])
