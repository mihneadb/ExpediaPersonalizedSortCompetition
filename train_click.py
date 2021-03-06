import data_io
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

def main():
    print("Reading training data")
    train = data_io.read_train()

    train.fillna(-2, inplace=True)

    #train_sample = train.fillna(value=-2)
    train_sample = train
    #train_sample = train[:100000]
    #train_sample = train.fillna(value=0)

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

    feature_names = list(train_sample.columns)
    feature_names.remove("click_bool")
    feature_names.remove("booking_bool")
    feature_names.remove("gross_bookings_usd")
    feature_names.remove("date_time")
    feature_names.remove("position")

    #feature_names.remove('price_diff')
    #feature_names.remove('price_person')
    feature_names.remove('star_diff')
    #feature_names.remove('pay_diff')
    feature_names.remove('price_night')
    feature_names.remove('loc_desire')
    feature_names.remove('no_kids')
    feature_names.remove('couple')
    feature_names.remove('price_down')
    feature_names.remove('same_country')

    #feature_names.remove('prop_location_score1')

    features = train_sample[feature_names].values
    #train_sample["position"] *= -1.0
    #target = train_sample["position"].values
    #target = train_sample["booking_bool"].values
    target = train_sample["click_bool"].values

    print("Training the Classifier")
    classifier = GradientBoostingClassifier(n_estimators=80,
                                        verbose=2,
                                        min_samples_split=10,
                                        random_state=1)
    classifier.fit(features, target)

    print("Saving the classifier")
    data_io.save_model(classifier, 'click')

if __name__=="__main__":
    main()
