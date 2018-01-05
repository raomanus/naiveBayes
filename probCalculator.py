import math
import csv
from stop_words import get_stop_words

class trainingSet:
	def updateSpamWords(self, words):
		for i in range(0,len(words),2):
			if words[i] not in self.stopWords and len(words[i]) >= 3 and len(words[i]) < 10:
				self.spamWordCount += int(words[i+1])
				try:
					self.spamWords[words[i]] += int(words[i+1])
				except:
					self.spamWords[words[i]] = int(words[i+1])

	def updateHamWords(self, words):
		for i in range(0,len(words),2):
			if words[i] not in self.stopWords and len(words[i]) >= 3 and len(words[i]) < 10:
				self.hamWordCount += int(words[i+1])
				try:
					self.hamWords[words[i]] += int(words[i+1])
				except:
					self.hamWords[words[i]] = int(words[i+1])


	def removeRecurring(self):
		for key in list(self.spamWords.keys()):
			if self.spamWords[key] < 200:
				self.spamWords[key] *= 10

		for key in list(self.hamWords.keys()):
			if self.hamWords[key] < 200:
				self.hamWords[key] *= 10


	def calculateProbabilities(self):
		
		self.probSpam = float(self.spamMail)/(self.spamMail+self.hamMail)
		self.probHam = float(self.hamMail)/(self.spamMail+self.hamMail)

		self.removeRecurring()

		for key in list(self.spamWords.keys()):
			total = self.spamWords[key]
			if key in self.hamWords.keys():
				total += self.hamWords[key]
			self.spamWords[key] = (self.spamWords[key]*self.probSpam)/total

		for key in list(self.hamWords.keys()):
			total = self.hamWords[key]
			if key in self.spamWords.keys():
				total += self.spamWords[key]
			self.hamWords[key] = (self.hamWords[key]*self.probHam)/total


	def classifyMail(self,mailContent):
		spamProbability = 1
		hamProbability = 1
		for i in range(0,len(mailContent),2):
			word = mailContent[i]
			wordCount = int(mailContent[i+1])
			wordSpamProb = 1
			wordHamProb = 1
			wordTotalProb = 0
			if word in self.spamWords:
				wordTotalProb = self.spamWords[word]*self.probSpam
				if word in self.hamWords:
					wordTotalProb += self.hamWords[word]*self.probHam
				spamProbability *= math.pow((self.spamWords[word]*self.probSpam/wordTotalProb), wordCount)
			if word in self.hamWords:
				wordTotalProb = self.hamWords[word]*self.probHam
				if word in self.spamWords:
					wordTotalProb += self.spamWords[word]*self.probSpam	
				hamProbability *= math.pow((self.hamWords[word]*self.probHam/wordTotalProb), wordCount)

		if spamProbability > hamProbability:
			return "spam"
		else:
			return "ham"

	def classifyTestMail(self,fileName):
		testFile = open(fileName,'r')
		testContent = testFile.readlines()

		outputFile = open("output.csv","w")
		csvWriter = csv.writer(outputFile)
		csvWriter.writerow(["Predicted Value", "Actual Value", "Data"])

		for line in testContent:
			line = line.split(' ')
			emailId = line[0]
			actualClass = line[1]
			predictedClass = self.classifyMail(line[2:])
			if actualClass == predictedClass:
				self.correct += 1
			else:
				self.error += 1
			outputLine = [predictedClass, actualClass, ' '.join(line)]
			csvWriter.writerow(outputLine)

		

	def __init__(self, file):
		self.spamMail = 0
		self.hamMail = 0
		self.spamWordCount = 0
		self.hamWordCount = 0
		self.spamWords = dict()
		self.hamWords = dict()
		self.stopWords = get_stop_words('en')
		self.correct = 0
		self.error = 0

		lines = file.readlines()
		for line in lines:
			splitLine = line.split(' ')
			mailClass = splitLine[1]
			if mailClass == 'spam':
				self.spamMail += 1
				self.updateSpamWords(splitLine[2:])
			else:
				self.hamMail += 1
				self.updateHamWords(splitLine[2:])

		self.calculateProbabilities()