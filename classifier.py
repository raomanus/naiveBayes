import csv
from probCalculator import trainingSet

trainingFile = open('train','r')
trainedData = trainingSet(trainingFile)

testFile = open('test','r')
testContent = testFile.readlines()

correct = 0
error = 0
outputFile = open("output.csv","w")
csvWriter = csv.writer(outputFile)
csvWriter.writerow(["Predicted Value", "Actual Value", "Data"])

for line in testContent:
	line = line.split(' ')
	emailId = line[0]
	actualClass = line[1]
	predictedClass = trainedData.classifyMail(line[2:])
	if actualClass == predictedClass:
		correct += 1
	else:
		error += 1
	outputLine = [predictedClass, actualClass, ' '.join(line)]
	csvWriter.writerow(outputLine)

print correct,error