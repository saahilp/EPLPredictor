import numpy as np
from sklearn.linear_model import LinearRegression


class Team:

    def __init__(self, name):
        self.name = name
        self.results = []
        self.homeXG = 0
        self.awayXG = 0
        self.homeXGA = 0
        self.awayXGA = 0
        self.averageXG = 0
        self.averageXGA = 0
        self.averagePoss = 0
        self.averagePossHome = 0
        self.averagePossAway = 0
        self.xGCurve = []
        self.xGACurve = []
        self.weight = []

    def add_result(self, result):
        self.results.append(result)

    def calculate_metrics(self):
        nResults = np.array(self.results)
        self.averageXG = np.mean([result.xG for result in nResults])
        self.averageXGA = np.mean([result.xGA for result in nResults])
        self.averagePoss = np.mean([result.poss for result in nResults])
        qualiResults = [result for result in nResults if result.home]
        self.homeXG = np.mean([result.xG for result in qualiResults])
        self.homeXGA = np.mean([result.xGA for result in qualiResults])
        self.averagePossHome = np.mean([result.poss for result in qualiResults])
        qualiResults = [result for result in nResults if not result.home]
        self.awayXG = np.mean([result.xG for result in qualiResults])
        self.awayXGA = np.mean([result.xGA for result in qualiResults])
        self.averagePossAway = np.mean([result.poss for result in qualiResults])
    def get_avg_stats(self):
        return [self.averagePoss, self.averageXG, self.averageXGA]

    def get_home_stats(self):
        return [self.averagePossHome, self.homeXG, self.homeXGA]

    def get_away_stats(self):
        return [self.averagePossAway, self.awayXG, self.awayXGA]

    def create_curves(self):
        self.init_weight_array()
        xgData = [result.xG for result in self.results]
        xgaData = [result.xGA for result in self.results]
        possData = [result.poss for result in self.results]
        self.xGCurve = LinearRegression().fit(np.array(possData).reshape(-1, 1), xgData, sample_weight = self.weight)
        self.xGACurve = LinearRegression().fit(np.array(possData).reshape(-1, 1), xgaData, sample_weight=self.weight)


    def init_weight_array(self):
        self.weight = [float(0)] * len(self.results)
        for i in range(0, len(self.results)-9):
            self.weight[i] = float(1)
        for i in (range(1, 10)):
            self.weight[len(self.results)-10+i] = float(i+1)

    def diffInRation(self):

        homeXGRatio = self.homeXG/self.averageXG
        homeXGARatio = self.homeXGA/self.averageXGA
        homePossRatio = self.averagePossHome/self.averagePoss

        awayXGRatio = self.awayXG / self.averageXG
        awayXGARatio = self.awayXGA / self.averageXGA
        awayPossRatio = self.averagePossAway / self.averagePoss

        return [homeXGRatio, homeXGARatio, homePossRatio, awayXGRatio, awayXGARatio, awayPossRatio]

    def predict(self, poss):
        return [self.xGCurve.predict(np.array([poss]).reshape(1, -1)), self.xGACurve.predict(np.array([poss]).reshape(1, -1))]



