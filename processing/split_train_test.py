from sklearn.model_selection import train_test_split

def split_data(stories,labels,test_size):

    # Create the training-test split of the data
    stores_train, stories_test, labels_train, labels_test = train_test_split( stories, labels, test_size=test_size, random_state=42)

    # stores_train = training data for classfier
    # stories_test = testing data for classifier
    # labels_train = training data for classifier
    # labels_test  = testing data for classifier
    return stores_train,stories_test,labels_train,labels_test