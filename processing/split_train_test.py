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
    """
    TF_IDF = "  term frequency-inverse document frequency"
    TF: Term Frequency, which measures how frequently a term occurs in a document. Since every document is different in length,
       it is possible that a term would appear much more times in long documents than shorter ones. Thus, the term frequency is
       often divided by the document length (aka. the total number of terms in the document) as a way of normalization:

    TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).

    IDF: Inverse Document Frequency, which measures how important a term is. While computing TF, all terms are considered equally
    important. However it is known that certain terms, such as "is", "of", and "that", may appear a lot of times but have little
    importance. Thus we need to weigh down the frequent terms while scale up the rare ones, by computing the following: 

    IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
    """
    vectorizer = TfidfVectorizer(min_df=1)
    # count the word occurrences of text documents
    stories_train_trans = vectorizer.fit_transform(stories_train)
    stories_test_trans = vectorizer.transform(stories_test)
    
    # Select features according to a percentile of the highest scores
    selector = SelectPercentile(f_classif, percentile=10)
    selector.fit(stories_train_trans, labels_train)
    stories_train_transformed = selector.transform(stories_train_trans).toarray()
    stories_test_transformed = selector.transform(stories_test_trans).toarray()

    return stories_train_transformed,stories_test_transformed,labels_train,labels_test
