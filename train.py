import data_io
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

def main():
    print("Reading training data")
    train = data_io.read_train()

    train.fillna(-1, inplace=True)

    #train_sample = train.fillna(value=-2)
    #train_sample = train[:2500000].fillna(value=0)
    train_sample = train[:100000]
    #train_sample = train.fillna(value=0)

    feature_names = list(train_sample.columns)
    feature_names.remove("click_bool")
    feature_names.remove("booking_bool")
    feature_names.remove("gross_bookings_usd")
    feature_names.remove("date_time")
    feature_names.remove("position")

    features = train_sample[feature_names].values
    #trin_sample["position"] *= -1.0
    #target = train_sample["position"].values
    target = train_sample["booking_bool"].values

    print("Training the Classifier")
    classifier = GradientBoostingClassifier(n_estimators=50,
                                        verbose=2,
                                        min_samples_split=10,
                                        random_state=1)
    classifier.fit(features, target)

    print("Saving the classifier")
    data_io.save_model(classifier)

if __name__=="__main__":
    main()
