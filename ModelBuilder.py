__author__ = 'BlackPros Team'

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.decomposition import PCA
from sklearn.externals import joblib

class Model(object):
    def __init__(self, file_plays='newPlays.csv', cv=6, debug=False, file_model='botmodel.pkl',
                 num_estimators=300, max_depth=15, min_samples_split=5, min_samples_leaf=12, verbose=0):
        self.file_plays = file_plays
        self.cv = cv
        self.debug = debug
        self.file_model = file_model
        self.clf = None
        self.num_estimators = num_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.verbose = verbose
        self.train()

    def train(self):
        if self.debug:
            print("Reading the data...\n")
        data = pd.read_csv(self.file_plays, sep=',')
        self.clf = RandomForestClassifier(n_estimators=self.num_estimators, max_depth=self.max_depth,
                                          min_samples_split = self.min_samples_split,
                                          min_samples_leaf= self.min_samples_leaf,
                                          n_jobs=-1, max_features=None, verbose=self.verbose)
        if self.debug:
            print("Evaluating the model...\n")
        self.clf.fit(data.iloc[:,:-1], data['result'])
        if self.debug:
            print("Saving the model...\n")
        joblib.dump(self.clf, self.file_model)
        if self.debug:
            print("Done!\n")

    def load(self):
        self.clf = joblib.load(self.file_model)

    def get_classifier(self):
        return self.clf

    def evaluate(self):
        if self.debug:
            print("Reading the data...\n")
        data = pd.read_csv(self.file_plays, sep=',')

        trainx = data.iloc[:, :-1]
        trainy = data['result']

        self.clf = RandomForestClassifier(n_estimators=self.num_estimators, max_depth=self.max_depth,
                                          min_samples_split = self.min_samples_split,
                                          min_samples_leaf= self.min_samples_leaf,
                                          n_jobs=-1, max_features=None, verbose=self.verbose)
        if self.debug:
            print("Evaluating the model...\n")
        scores = cross_val_score(self.clf, trainx, trainy, cv=self.cv, verbose=3, n_jobs=-1)
        return scores


if __name__ == '__main__':
    model = Model(debug=True, num_estimators=300, file_plays='newPlays.csv')
    print("Model Evaluated: ", model.evaluate())
