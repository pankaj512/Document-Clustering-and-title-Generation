# this is Support vector machine classifier
from sklearn import svm

def train_machine(stories_train,labels_train):
    # three parameter is used of SVM
    # 1. C
    # 2. gamma
    # 3. kernal
    clf = svm.SVC(C=1000000.0, kernel='rbf')
    # fit data to train classifier
    clf.fit(stories_train,labels_train)
    # return trained classifier
    return clf
