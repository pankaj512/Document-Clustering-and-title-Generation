# Document Clustering and Title generation
A news Document classifier with supervised learning algorithm and title generation with machine learning.

Needed python libraries:

1. Pandas
2. Scipy
3. Numpy
4. sciket-learn
4. Pygubu
5. tkinter

To Run:
run mainApp.py file.

how to Use:
1. A simple GUI will pop-up after running mainApp.py file.
2. Select the classifier from drop-down.
3. Select the parition size for training and testing.
4. Select stop word removal condition.
5. Click on classify button.
6. Wait for operation to complete. Once it complete it will show result.

List of features used:
1. Language model features
2. title Length feature
3. Part of Speech Language Model Feature
4. N-Gram Match feature
5. Content selection feature

Used file features:
1. is word in first sentence
2. in what range a word occurred in this file
Features from news title:
1. Pos tri-gram and probability
2. Content score and its probability of occurrence
3. bleu score and its probability of occurrence

Features used from news contents:
1. Current Story Word
2. Word Bi-gram Context - both sides -1 and +1
3. POS of Current Story Word
4. POS Bi-gram of Current Word - both sides -1 and +1
5. POS Tri-gram of Current Word - both sides -1, -2 and +1, +2
6. Word Position in Lead sentence
7. Word Position
8. First Word Occurrence Position
9. Word TF-IDF Range
