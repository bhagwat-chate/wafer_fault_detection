from wafer.logger import logging
from wafer.exception import WaferException
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score
from xgboost import XGBClassifier


class Model_Finder:
    def __init__(self):
        self.random_forest_score = None
        self.prediction_random_forest = None
        self.random_forest = None
        self.xgboost_score = None
        self.prediction_xgboost = None
        self.xgboost = None
        self.learning_rate = None
        self.param_grid_xgboost = None
        self.n_estimators = None
        self.max_features = None
        self.max_depth = None
        self.criterion = None
        self.grid = None
        self.param_grid = None
        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')

    def get_best_param_for_random_forest(self, train_x, train_y):
        try:
            self.param_grid = {'n_estimators': [10, 50, 100, 130], 'criterion': ['gini', 'entropy'],
                               'max_depth': range(2, 4, 1), 'max_features': ['auto', 'log2']}
            self.grid = GridSearchCV(estimator=self.clf, param_grid=self.param_grid, cv=5, verbose=3)
            self.grid.fit(train_x, train_y)

            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            self.clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)
            self.clf.fit(train_x, train_y)

            logging.info("Random Forest model training complete")

            return self.clf
        except WaferException as e:
            raise WaferException(e, sys)

    def get_best_params_for_xgboost(self, train_x, train_y):
        try:
            self.param_grid_xgboost = {'learning_rate': [0.5, 0.1, 0.01, 0.00, ], 'max_depth': [3, 5, 10, 20],
                                       'n_estimators': [10, 50, 100, 200]}
            self.grid = GridSearchCV(XGBClassifier(objective='binary:logistic'), self.param_grid_xgboost, verbose=3,
                                     cv=5)
            self.grid.fit(train_x, train_y)

            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth,
                                     n_estimators=self.n_estimators)
            self.xgb.fit(train_x, train_y)
            logging.info("XGBoost model training complete")

            return self.xgb
        except WaferException as e:
            raise WaferException(e, sys)

    def get_best_model(self, train_x, train_y, test_x, test_y):
        try:
            self.xgboost = self.get_best_params_for_xgboost(train_x, train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x)

            if len(test_y.unique()) == 1:
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                logging.info("Accuracy of XGBoost: {}".format(str(self.xgboost_score*100)))
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost)
                logging.info("Accuracy of XGBoost: {}".format(str(self.xgboost_score*100)))

            self.random_forest = self.get_best_param_for_random_forest(train_x, train_y)
            self.prediction_random_forest = self.random_forest.predict(test_x)

            if len(test_y.unique()) == 1:
                self.random_forest_score = accuracy_score(test_y, self.prediction_random_forest)
                logging.info("Accuracy of random forest: {}".format(self.random_forest_score*100))
            else:
                self.random_forest_score = roc_auc_score((test_y, self.prediction_random_forest))
                logging.info("Accuracy of random forest: {}".format(self.random_forest_score*100))

            if self.xgboost_score > self.random_forest_score:
                return 'XGBoost', self.xgboost
            else:
                return 'Random Forest', self.random_forest
        except WaferException as e:
            raise WaferException(e, sys)
