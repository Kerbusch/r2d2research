# import sklearn
import numpy as np
import json


class ClassifyDataVariable:
    def __init__(self):
        self.dataFloats = []

        self.max_time = None
        self.min_time = None
        self.avg_time = None

        self.farm_yaw_diff = None
        self.farm_roll_diff = None
        self.farm_pitch_diff = None

        self.uarm_yaw_diff = None
        self.uarm_roll_diff = None
        self.uarm_pitch_diff = None

    def convertToList(self):
        self.dataFloats = [self.max_time,
                           self.min_time,
                           self.avg_time,
                           self.farm_yaw_diff,
                           self.farm_roll_diff,
                           self.farm_pitch_diff,
                           self.uarm_yaw_diff,
                           self.uarm_roll_diff,
                           self.uarm_pitch_diff
                           ]
        return self.dataFloats

    def getFromList(self, data: list):
        self.max_time = data[0]
        self.min_time = data[1]
        self.avg_time = data[2]
        self.farm_yaw_diff = data[3]
        self.farm_roll_diff = data[4]
        self.farm_pitch_diff = data[5]
        self.uarm_yaw_diff = data[6]
        self.uarm_roll_diff = data[7]
        self.uarm_pitch_diff = data[8]
        return self

    def checkDataValid(self) -> bool:
        if self.max_time is None or self.min_time is None or self.avg_time is None:
            return False
        if self.farm_yaw_diff is None or self.farm_roll_diff is None or self.farm_pitch_diff is None:
            return False
        if self.uarm_yaw_diff is None or self.uarm_roll_diff is None or self.uarm_pitch_diff is None:
            return False
        return True


class ClassifyData:
    def __init__(self):
        # Initialize the data with forearm (yaw, roll, pitch), upper arm (yaw, roll, pitch) and time since last point
        self.data = []  # [y, r, p, y, r, p, tijd]
        self.classification_data = []
        self.classification_super_data = ClassifyDataVariable()
        self.classification_stand_data = ClassifyDataVariable()
        self.classification_input_data = ClassifyDataVariable()
        self.classification_file_name = "classification_data.json"

        # self.importInputData(self.data)  # nog even naar kijken
        self.readJSONFile()
        self.makeSuperData()
        self.createStandardDeviationVariable()

    def classifyCheck(self):
        self.makeSuperData()
        self.createStandardDeviationVariable()

        classifier_list = []

        if self.classification_input_data.farm_yaw_diff < \
                (self.classification_super_data.farm_yaw_diff - self.classification_stand_data.farm_yaw_diff):
            classifier_list.append(3)
            print("farm_yaw_diff - ")

        if self.classification_input_data.farm_yaw_diff > \
                (self.classification_super_data.farm_yaw_diff + self.classification_stand_data.farm_yaw_diff):
            classifier_list.append(4)
            print("farm_yaw_diff +")

        if self.classification_input_data.farm_pitch_diff < \
                (self.classification_super_data.farm_pitch_diff - self.classification_stand_data.farm_pitch_diff):
            classifier_list.append(3)
            print("farm_pitch_diff -")

        if self.classification_input_data.farm_pitch_diff > \
                (self.classification_super_data.farm_pitch_diff + self.classification_stand_data.farm_pitch_diff):
            classifier_list.append(4)
            print("farm_pitch_diff +")

        if self.classification_input_data.farm_roll_diff < \
                (self.classification_super_data.farm_roll_diff - self.classification_stand_data.farm_roll_diff):
            classifier_list.append(3)
            print("farm_roll_diff -")

        if self.classification_input_data.farm_roll_diff > \
                (self.classification_super_data.farm_roll_diff + self.classification_stand_data.farm_roll_diff):
            classifier_list.append(4)
            print("farm_roll_diff +")

        if self.classification_input_data.uarm_yaw_diff < \
                (self.classification_super_data.uarm_yaw_diff - self.classification_stand_data.uarm_yaw_diff):
            classifier_list.append(3)
            print("uarm_yaw_diff -")

        if self.classification_input_data.uarm_yaw_diff > \
                (self.classification_super_data.uarm_yaw_diff + self.classification_stand_data.uarm_yaw_diff):
            classifier_list.append(4)
            print("uarm_yaw_diff +")

        if self.classification_input_data.uarm_pitch_diff < \
                (self.classification_super_data.uarm_pitch_diff - self.classification_stand_data.uarm_pitch_diff):
            classifier_list.append(3)
            print("uarm_pitch_diff -")

        if self.classification_input_data.uarm_pitch_diff > \
                (self.classification_super_data.uarm_pitch_diff + self.classification_stand_data.uarm_pitch_diff):
            classifier_list.append(4)
            print("uarm_pitch_diff +")

        if self.classification_input_data.uarm_roll_diff < \
                (self.classification_super_data.uarm_roll_diff - self.classification_stand_data.uarm_roll_diff):
            classifier_list.append(3)
            print("uarm_roll_diff - ")

        if self.classification_input_data.uarm_roll_diff > \
                (self.classification_super_data.uarm_roll_diff + self.classification_stand_data.uarm_roll_diff):
            classifier_list.append(4)
            print("uarm_roll_diff + ")

        if self.classification_input_data.avg_time < \
                (self.classification_super_data.avg_time - self.classification_stand_data.avg_time):
            classifier_list.append(1)
            print("max_time - ")

        if self.classification_input_data.avg_time > \
                (self.classification_super_data.avg_time + self.classification_stand_data.avg_time):
            classifier_list.append(2)
            print("max_time + ")

        # create a list with indicators of the classifiers
        classifier_list = list(set(classifier_list))

        # if the list is empty, classify as correct
        if len(classifier_list) == 0:
            classifier_list.append(0)

        self.giveFeedback(classifier_list)

    def giveFeedback(self, classifiers: list):
        # give feedback according to the classification
        for classifier in classifiers:
            if classifier == 0:
                print("You performed a correct bicep curl, Good job")
            elif classifier == 1:
                print("The bicep curl was performed too fast, try to do it slower")
            elif classifier == 2:
                print("The bicep curl was performed too slow, try to do it faster")
            elif classifier == 3:
                print("The bicep curl was too far from the upper arm, try to do it closer towards the upper arm")
            elif classifier == 4:
                print("he bicep curl was too close to the upper arm, try to do it further away from the upper arm")

    def getLowPoints(self, data, sensor: int):
        lowest_points = []
        rounded_data = []
        for i in range(len(data)):
            rounded_data.append(round(data[i][sensor], 2))

        # using the data from the forearm pitch
        for i in range(2, len(data)-2):
            if (rounded_data[i - 2] > rounded_data[i - 1] >= rounded_data[i]) and (rounded_data[i + 2] > rounded_data[i + 1] >= rounded_data[i]):
            # if (self.data[i - 2][sensor] > self.data[i - 1][sensor] > self.data[i][sensor]) and (self.data[i+2][sensor] > self.data[i+1][sensor] > self.data[i][sensor]):
                lowest_points.append(data[i])
        return lowest_points

    def getHighPoints(self, data, sensor: int):
        highest_points = []
        rounded_data = []
        for i in range(len(data)):
            rounded_data.append(round(data[i][sensor], 1))

        # using the data from the forearm pitch
        for i in range(2, len(data) - 2):
            if (rounded_data[i - 2] < rounded_data[i - 1] <= rounded_data[i]) and (
                    rounded_data[i + 2] < rounded_data[i + 1] <= rounded_data[i]):
                highest_points.append(data[i])
        return highest_points

    def getTimeBetweenPoints(self, points: list):
        time_between = []
        for i in range(len(points) - 1):
            time_between.append(points[i + 1][6] - points[i][6])
        return time_between

    def getAverageTimeBetweenPoints(self, points: list):
        time_between = self.getTimeBetweenPoints(points)
        return sum(time_between) / len(time_between)

    def maxTimeBetweenPoints(self, points: list):
        return max(self.getTimeBetweenPoints(points))

    def minTimeBetweenPoints(self, points: list):
        return min(self.getTimeBetweenPoints(points))

    def maxValueOnPoint(self, high_points: list, sensor: int):
        if not high_points:
            return max(np.array(self.data)[:, sensor])
        return max(np.array(high_points)[:, sensor])

    def minValueOnPoint(self, low_points: list, sensor: int):
        if not low_points:
            return min(np.array(self.data)[:, sensor])
        return min(np.array(low_points)[:, sensor])

    def createClassificationDataVariable(self, data: list):
        c = ClassifyDataVariable()

        lp_0 = self.getLowPoints(data, 0)
        hp_0 = self.getHighPoints(data, 0)
        lp_1 = self.getLowPoints(data, 1)
        hp_1 = self.getHighPoints(data, 1)
        lp_2 = self.getLowPoints(data, 2)
        hp_2 = self.getHighPoints(data, 2)
        lp_3 = self.getLowPoints(data, 3)
        hp_3 = self.getHighPoints(data, 3)
        lp_4 = self.getLowPoints(data, 4)
        hp_4 = self.getHighPoints(data, 4)
        lp_5 = self.getLowPoints(data, 5)
        hp_5 = self.getHighPoints(data, 5)

        c.avg_time = self.getAverageTimeBetweenPoints(lp_1)
        c.max_time = self.maxTimeBetweenPoints(lp_1)
        c.min_time = self.minTimeBetweenPoints(lp_1)

        farm_yaw_max = self.maxValueOnPoint(hp_0, 0)
        farm_roll_max = self.maxValueOnPoint(hp_1, 1)
        farm_pitch_max = self.maxValueOnPoint(hp_2, 2)
        uarm_yaw_max = self.maxValueOnPoint(hp_3, 3)
        uarm_roll_max = self.maxValueOnPoint(hp_4, 4)
        uarm_pitch_max = self.maxValueOnPoint(hp_5, 5)

        farm_yaw_min = self.minValueOnPoint(lp_0, 0)
        farm_roll_min = self.minValueOnPoint(lp_1, 1)
        farm_pitch_min = self.minValueOnPoint(lp_2, 2)
        uarm_yaw_min = self.minValueOnPoint(lp_3, 3)
        uarm_roll_min = self.minValueOnPoint(lp_4, 4)
        uarm_pitch_min = self.minValueOnPoint(lp_5, 5)

        c.farm_yaw_diff = farm_yaw_max - farm_yaw_min
        c.farm_roll_diff = farm_roll_max - farm_roll_min
        c.farm_pitch_diff = farm_pitch_max - farm_pitch_min

        c.uarm_yaw_diff = uarm_yaw_max - uarm_yaw_min
        c.uarm_roll_diff = uarm_roll_max - uarm_roll_min
        c.uarm_pitch_diff = uarm_pitch_max - uarm_pitch_min

        if c.checkDataValid():
            return c
        raise "Data is not valid"

    def importInputData(self, data: list):
        self.data = data
        self.classification_input_data = self.createClassificationDataVariable(data)

    def importClassificationData(self, data: list):
        x = self.createClassificationDataVariable(data)
        if x is not None:
            self.classification_data.append(x)

    def writeJSONFile(self):
        with open(self.classification_file_name, "w") as file:
            x = []
            if self.classification_data is None:
                return False
            for c_data in self.classification_data:
                x.append(c_data.convertToList())
            json.dump(x, file, indent=1)
        return True

    # Read the data from a file
    def readJSONFile(self):
        with open(self.classification_file_name, "r") as file:
            if file.read() == "":
                return None
        with open(self.classification_file_name, "r") as file:
            x = json.load(file)
            for part in x:
                cdv = ClassifyDataVariable()
                cdv.getFromList(part)
                self.classification_data.append(cdv)
        return None

    def createStandardDeviationVariable(self):
        l_time_max = []
        l_time_min = []
        l_time_avg = []
        l_farm_yaw = []
        l_farm_roll = []
        l_farm_pitch = []
        l_uarm_yaw = []
        l_uarm_roll = []
        l_uarm_pitch = []

        for data in self.classification_data:
            l_time_max.append(data.max_time)
            l_time_min.append(data.min_time)
            l_time_avg.append(data.avg_time)
            l_farm_yaw.append(data.farm_yaw_diff)
            l_farm_roll.append(data.farm_roll_diff)
            l_farm_pitch.append(data.farm_pitch_diff)
            l_uarm_yaw.append(data.uarm_yaw_diff)
            l_uarm_roll.append(data.uarm_roll_diff)
            l_uarm_pitch.append(data.uarm_pitch_diff)

        n = 2

        self.classification_stand_data.avg_time = n*np.std(l_time_avg)
        self.classification_stand_data.max_time = n*np.std(l_time_max)
        self.classification_stand_data.min_time = n*np.std(l_time_min)
        self.classification_stand_data.farm_yaw_diff = n*np.std(l_farm_yaw)
        self.classification_stand_data.farm_roll_diff = n*np.std(l_farm_roll)
        self.classification_stand_data.farm_pitch_diff = n*np.std(l_farm_pitch)
        self.classification_stand_data.uarm_yaw_diff = n*np.std(l_uarm_yaw)
        self.classification_stand_data.uarm_roll_diff = n*np.std(l_uarm_roll)
        self.classification_stand_data.uarm_pitch_diff = n*np.std(l_uarm_pitch)
    
    def makeSuperData(self):
        if not self.classification_data:
            return None
        sum_time_max = 0
        sum_time_min = 0
        sum_time_avg = 0
        sum_farm_yaw = 0
        sum_farm_roll = 0
        sum_farm_pitch = 0
        sum_uarm_yaw = 0
        sum_uarm_roll = 0
        sum_uarm_pitch = 0

        for i in range(len(self.classification_data)):
            sum_time_max += self.classification_data[i].max_time
            sum_time_min += self.classification_data[i].min_time
            sum_time_avg += self.classification_data[i].avg_time
            sum_farm_yaw += self.classification_data[i].farm_yaw_diff
            sum_farm_roll += self.classification_data[i].farm_roll_diff
            sum_farm_pitch += self.classification_data[i].farm_pitch_diff
            sum_uarm_yaw += self.classification_data[i].uarm_yaw_diff
            sum_uarm_roll += self.classification_data[i].uarm_roll_diff
            sum_uarm_pitch += self.classification_data[i].uarm_pitch_diff

        self.classification_super_data.avg_time = sum_time_avg / len(self.classification_data)
        self.classification_super_data.max_time = sum_time_max / len(self.classification_data)
        self.classification_super_data.min_time = sum_time_min / len(self.classification_data)
        self.classification_super_data.farm_yaw_diff = sum_farm_yaw / len(self.classification_data)
        self.classification_super_data.farm_roll_diff = sum_farm_roll / len(self.classification_data)
        self.classification_super_data.farm_pitch_diff = sum_farm_pitch / len(self.classification_data)
        self.classification_super_data.uarm_yaw_diff = sum_uarm_yaw / len(self.classification_data)
        self.classification_super_data.uarm_roll_diff = sum_uarm_roll / len(self.classification_data)
        self.classification_super_data.uarm_pitch_diff = sum_uarm_pitch / len(self.classification_data)

        if self.classification_super_data.avg_time < 0:
            self.classification_super_data.avg_time *= -1
        if self.classification_super_data.max_time < 0:
            self.classification_super_data.max_time *= -1
        if self.classification_super_data.min_time < 0:
            self.classification_super_data.min_time *= -1
        if self.classification_super_data.farm_yaw_diff < 0:
            self.classification_super_data.farm_yaw_diff *= -1
        if self.classification_super_data.farm_roll_diff < 0:
            self.classification_super_data.farm_roll_diff *= -1
        if self.classification_super_data.farm_pitch_diff < 0:
            self.classification_super_data.farm_pitch_diff *= -1
        if self.classification_super_data.uarm_yaw_diff < 0:
            self.classification_super_data.uarm_yaw_diff *= -1
        if self.classification_super_data.uarm_roll_diff < 0:
            self.classification_super_data.uarm_roll_diff *= -1
        if self.classification_super_data.uarm_pitch_diff < 0:
            self.classification_super_data.uarm_pitch_diff *= -1
