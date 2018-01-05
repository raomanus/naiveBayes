from probCalculator import trainingSet

trainingFile = open('train','r')
trainedData = trainingSet(trainingFile)
trainedData.classifyTestMail('test')
print "Accuracy:", float(trainedData.correct*100)/(trainedData.correct+trainedData.error)
