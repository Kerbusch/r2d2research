class ClassifyData:
    def __init__(self, data):
        # Initialize the data with forearm (yaw, roll, pitch), upper arm (yaw, roll, pitch) and time since last datapoint
        self.data = data  # [y, r, p, y, r, p, tijd]
        self.classification_data = data  # PLACEHOLDER voor 'goede data' voor classification

        # TODO mogelijk classification waarden eruit en zelf waardes bepalen.
        # TODO is sneller en misschien meer makkelijker

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

    # def ClassifyCheck(self, data):
    #     if (data[0] < self.farm_minimum_yaw_classify_waarde or data[0] > self.farm_maximum_yaw_classify_waarde) or (data[3] < self.uarm_minimum_yaw_classify_waarde or data[3] > self.uarm_maximum_yaw_classify_waarde):  # if yaw is outside the minimum and maximum yaw classify value
    #         # zet in yaw feedback classification
    #         return
    #     if (data[1] < self.farm_minimum_roll_classify_waarde or data[1] > self.farm_maximum_roll_classify_waarde) or (data[4] < self.uarm_minimum_roll_classify_waarde or data[4] > self.uarm_maximum_roll_classify_waarde):  # if roll is outside the minimum and maximum roll classify value
    #         # zet in roll feedback classification
    #         return
    #     if (data[2] < self.farm_minimum_pitch_classify_waarde or data[2] > self.farm_maximum_pitch_classify_waarde) or (data[5] < self.uarm_minimum_pitch_classify_waarde or data[5] > self.uarm_maximum_pitch_classify_waarde):  # if pitch is outside the minimum and maximum pitch classify value
    #         # zet in pitch feedback classification
    #         return
    #     if data[6] < self.tijd_minimum_classify_waarde or data[6] > self.tijd_maximum_classify_waarde:
    #         # zet in tijd feedback classification
    #         return
    #     else:
    #         # zet bicep curl in correcte classificatie
    #         return

    def getAverageTimeBetweenCurls(self):
        # all data from forearm
        # Find the lowest points with their indexes
        # get the time between the lowest points
        # calculate the average time between the lowest points

        lowest_points = []

        # using the data from the forearm pitch
        for i in range(1, len(self.data) - 1):
            if self.data[i-1][2] > self.data[i][2] and self.data[i+1][2] > self.data[i][2]:
                lowest_points.append(self.data[i-1])

        print(lowest_points)
        for i in range(1, len(lowest_points)):
            print(lowest_points[i][6]-lowest_points[i-1][6])


        return 0
