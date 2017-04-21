from classification.processing import prediction
from classification.processing import training
from classification.processing import vector

from classification.processing import split_train_test
from sklearn.metrics import classification_report

def perform(stopword,size):

    # get input data vector
    stories_train , labels_train = vector.make_vector(stopword)
    # get split into traninig and testing
    feature_train, feature_test, labels_train, labels_test = split_train_test.split_data(stories_train, labels_train, size)
    #Now train machine
    classifier = training.train_machine(feature_train, labels_train)
    #now make prediction
    pred =  prediction.prediction_fun(classifier, feature_test)
    #now get accuracy
    accuracy = prediction.accuracy_score(pred, labels_test)
    #return accuracy
    print(classification_report(labels_test, pred))
    return accuracy


