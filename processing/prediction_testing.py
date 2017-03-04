#predict the result with testing data
from sklearn.metrics import confusion_matrix,accuracy_score

def prediction_fun(clf,stories_test):
    # test classiefir with argument
    pred = clf.predict(stories_test)
    return pred

def get_accuracy(pred,labels_test):
    accuracy = accuracy_score(pred,labels_test)
    return accuracy
