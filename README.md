# naiveBayes
This is an implementation of a Naive Bayesian classfier for spam and ham emails. The code has ~91% accuracy on the test dataset. 
*******************************************************************************************************************************
* Implementation Desc
1. test file contains a list of spam and ham mails with the constituent words and their word counts.
2. We train the classifier by calculating the probabilities for an e-mail being spam/ham and also the conditional probabilities
   for each word appearing in a spam/ham email.
3. We store these probabilites in an object of the class trainingSet
4. We then calculate the score for the test e-mails by calculating the product of the conditional probabilities for each constituent
   word and then classify based on the larger score. 
