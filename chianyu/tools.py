#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

from scipy.spatial.distance import euclidean


class DataPoint:

    def __init__(self, Id, Text, Category=None):
        self.Id = Id
        self.Text = Text
        self.Category = Category
        self.Neighbors = {}
        self.features = {
            '0': 0.0,
            '1': 0.0,
            '2': 0.0,
            '3': 0.0,
            '4': 0.0,
        }

    def __repr__(self):
        return 'ID: %s\nText: %s\nCategory: %s\nNeighbors: %s\nFeatures: %s' % (
            self.Id,
            self.Text,
            self.Category,
            self.Neighbors,
            self.features,
        )


class languageAnalyzer():

    def __init__(self, dataset=None):
        self.numerals =   ['1','2','3','4','5','6','7','8','9','0']
        self.alphabet26 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '’']
        self.alphabetES = [u'á',u'é',u'í',u'ó',u'ú',u'ñ',u'ü',u'¿',u'¡']
        self.alphabetFR = [u'à',u'â',u'æ',u'ç',u'é',u'è',u'ê',u'ë',u'î',u'ï',u'ô',u'œ',u'ù',u'û',u'ü',u'ÿ']
        self.alphabetSK = [u'á',u'ä',u'č',u'ď',u'é',u'í',u'ĺ',u'ľ',u'ň',u'ó',u'ô',u'ŕ',u'š',u'ť',u'ú',u'ý',u'ž']
        self.alphabetDE = [u'ä',u'ö',u'ü',u'ß']
        self.alphabetPL = [u'ą',u'ć',u'ę',u'ł',u'ń',u'ó',u'ś',u'ź',u'ż']

        self.languages = {
            '0': {'name':'Slovak', 'special':self.alphabetSK},
            '1': {'name':'French', 'special':self.alphabetFR},
            '2': {'name':'Spanish', 'special':self.alphabetES},
            '3': {'name':'German', 'special':self.alphabetDE},
            '4': {'name':'Polish', 'special':self.alphabetPL},
        }

        self.dataset = dataset
        self.frequency = {
            '0': {'total':0, 'table':{}},
            '1': {'total':0, 'table':{}},
            '2': {'total':0, 'table':{}},
            '3': {'total':0, 'table':{}},
            '4': {'total':0, 'table':{}},
        }


    def loadTrainingData(self, filenameX, filenameY, preprocessed=False):
        trainingSet = []
        with open(filenameX, 'rb') as csvFileX, open(filenameY, 'rb') as csvFileY:
            csvReaderX = csv.reader(csvFileX, delimiter=',')
            fieldnameX = csvReaderX.next()
            csvReaderY = csv.reader(csvFileY, delimiter=',')
            fieldnameY = csvReaderY.next()

            dictReaderX = csv.DictReader(csvFileX, fieldnames=fieldnameX)
            dictReaderY = csv.DictReader(csvFileY, fieldnames=fieldnameY)
            for (x, y) in zip(dictReaderX, dictReaderY):
                Id = x['Id']
                Text = x['Text']
                Category = y['Category']
                if preprocessed:
                    if len(Text) < 5:
                        continue
                entry = DataPoint(Id, Text, Category)
                trainingSet.append(entry)
        return trainingSet


    def loadTestData(self, filename):
        testSet = []
        with open(filename, 'rb') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            fieldNames = csvReader.next()
            dictReader = csv.DictReader(csvFile, fieldnames=fieldNames)
            for row in dictReader:
                entry = DataPoint(row['Id'], row['Text'])
                testSet.append(entry)
        return testSet


    def calcFrequency(self, dataset, languageId):

        specials = self.languages[languageId]['special']

        # E.g. French alphabets = 26 regulars + specials
        alphabets = list(self.alphabet26)
        alphabets.extend(specials)
        alphaTable = {
            char: 1 for char in alphabets
        }

        alphaCount = 0
        for sentence in dataset:
            if sentence.Category == languageId:
                try:
                    unicodeText = sentence.Text.replace(" ", "").decode('utf-8').lower()
                except:
                    print('Unicode encoding failed.')
                    break
                for alpha in unicodeText:
                    if alpha in alphaTable:
                        alphaTable[alpha] += 1
                        alphaCount += 1
                        if alpha in specials:
                            alphaTable[alpha] += 1

        self.frequency[languageId].update({
            'total': alphaCount,
            'table': alphaTable,
        })


    def analyzeFreq(self):
        alphabets = []
        alphabets.extend(self.alphabet26)
        alphabets.extend(self.alphabetES)
        alphabets.extend(self.alphabetFR)
        alphabets.extend(self.alphabetSK)
        alphabets.extend(self.alphabetDE)
        alphabets.extend(self.alphabetPL)
        alphaTable = {
            char: 1 for char in alphabets
        }

        for fid in self.frequency:
            freqTable = self.frequency[fid]['table']
            for alpha in freqTable:
                alphaTable[alpha] += freqTable[alpha]

        for fid in self.frequency:
            freqTable = self.frequency[fid]['table']
            for alpha in freqTable:
                try:
                    charCount = freqTable[alpha]
                    f = float(charCount)/alphaTable[alpha]
                except ZeroDivisionError:
                    f = 0.0
                self.frequency[fid]['table'].update({
                    alpha: f,
                })


    # Calculate confidence for text is in languageId
    def calcConfidence(self, languageId, unicodeText):
        confidence = 0.0
        freqRecord = self.frequency[languageId]

        penalty = 0.0
        for language in self.languages:
            penalty += self.frequency[language]['total']
        penalty = freqRecord['total']/penalty

        for char in unicodeText:
            if char in freqRecord['table']:
                confidence += float(freqRecord['table'][char])/ freqRecord['total']
            else:
                confidence -= penalty

        if len(unicodeText) > 0:
            return confidence / len(unicodeText)
        else:
            return 0


    def plotData(self, dataPoint):
        unicodeText = dataPoint.Text.replace(" ", "").decode('utf-8').lower()
        for language in self.languages:
            confidence = self.calcConfidence(language, unicodeText)
            dataPoint.features.update({
                language: confidence
            })


    def calcEuclideanDistance(self, trainingData, testData):

        trainingFeatures = []
        testFeatures = []

        testUnicodeText = testData.Text.replace(" ", "").decode('utf-8').lower()
        for language in self.languages:
            trainingFeatures.append(trainingData.features[language])
            testFeatures.append(self.calcConfidence(language, testUnicodeText))
        distance = euclidean(trainingFeatures, testFeatures)
        return distance




def main():
    analyzer = languageAnalyzer()
    print('Printing numerals...%s' % ', '.join(analyzer.numerals))
    print('Printing alphabet26...%s' % ', '.join(analyzer.alphabet26))
    print('Printing alphabetSK...%s' % ', '.join(analyzer.alphabetSK))
    print('Printing alphabetFR...%s' % ', '.join(analyzer.alphabetFR))
    print('Printing alphabetES...%s' % ', '.join(analyzer.alphabetES))
    print('Printing alphabetGE...%s' % ', '.join(analyzer.alphabetDE))
    print('Printing alphabetPL...%s' % ', '.join(analyzer.alphabetPL))


if __name__ == '__main__':
    main()