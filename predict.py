import data_io
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np

# http://stackoverflow.com/questions/21506128/best-way-to-combine-probabilistic-classifiers-in-scikit-learn
class EnsembleClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, classifiers=None):
        self.classifiers = classifiers

    def fit(self, X, y):
        for classifier in self.classifiers:
            classifier.fit(X, y)

    def predict_proba(self, X):
        self.predictions_ = list()
        for classifier in self.classifiers:
            self.predictions_.append(classifier.predict_proba(X))
        # booking is first, click is second
        return np.average(self.predictions_, axis=0, weights=[0.15, 0.85])
        #return np.sum(self.predictions_, axis=0)

def main():
    print("Reading test data")
    test = data_io.read_test()
    test.fillna(-1, inplace=True)

    feature_names = list(test.columns)
    feature_names.remove("date_time")

    #feature_names = [
        #'srch_id',
        #'price_usd',
        #'price_person',
        #'price_usd',
        #'prop_location_score2',
        #'prop_log_historical_price',
        #'srch_children_count',
        #'srch_query_affinity_score',
        #'prop_starrating',
        #'visitor_hist_starrating',
        #'promotion_flag',
        #'prop_review_score',
        #'srch_destination_id',
        #'prop_id',
        #'visitor_hist_adr_usd',
        #'prop_brand_bool',
    #]

    features = test[feature_names].values

    print("Loading the classifier")
    classifier_booking = data_io.load_model('booking')
    classifier_click = data_io.load_model('click')

    ensemble = EnsembleClassifier([classifier_booking, classifier_click])

    print("Making predictions")
    #predictions = classifier.predict_proba(features)[:,1]
    predictions = ensemble.predict_proba(features)[:,1]
    predictions = list(-1.0*predictions)
    recommendations = zip(test["srch_id"], test["prop_id"], predictions)

    print("Writing predictions to file")
    data_io.write_submission(recommendations)

if __name__=="__main__":
    main()
