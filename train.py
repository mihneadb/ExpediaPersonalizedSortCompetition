import data_io
from sklearn.ensemble import RandomForestClassifier

def main():
    print("Reading training data")
    train = data_io.read_train()
    train.fillna(0, inplace=True)

    train_sample = train.fillna(value=0)

    feature_names = list(train_sample.columns)
    feature_names.remove("click_bool")
    feature_names.remove("booking_bool")
    feature_names.remove("gross_bookings_usd")
    feature_names.remove("date_time")
    feature_names.remove("position")

    feature_names.remove("orig_destination_distance")
    feature_names.remove("srch_room_count")
    feature_names.remove("srch_saturday_night_bool")

    target_names = ["booking_bool", "click_bool"]
    features = train_sample[feature_names].values
    target = train_sample[target_names].values

    print("Training the Classifier")
    classifier = RandomForestClassifier(n_estimators=3200,
                                        verbose=2,
                                        n_jobs=1,
                                        min_samples_split=10,
                                        random_state=1)
    classifier.fit(features, target)

    print("Saving the classifier")
    data_io.save_model(classifier)

if __name__=="__main__":
    main()
