from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif

def split_data(stories,labels,test_size):

    # Create the training-test split of the data
    stories_train, stories_test, labels_train, labels_test = train_test_split(stories, labels, test_size=float(test_size), random_state=42)

    # stores_train = training data for classfier
    # stories_test = testing data for classifier
    # labels_train = training data for classifier
    # labels_test  = testing data for classifier

    vectorizer = TfidfVectorizer(min_df=1)
    stories_train_trans = vectorizer.fit_transform(stories_train)
    stories_test_trans = vectorizer.transform(stories_test)

    selector = SelectPercentile(f_classif, percentile=10)
    selector.fit(stories_train_trans, labels_train)
    stories_train_transformed = selector.transform(stories_train_trans).toarray()
    stories_test_transformed = selector.transform(stories_test_trans).toarray()

    return stories_train_transformed,stories_test_transformed,labels_train,labels_test