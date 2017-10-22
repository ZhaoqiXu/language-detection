#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard imports
import csv
# Scipy imports
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

    def __init__(self):
        self.alphabet26 = {u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0',
                           u'a',u'b',u'c',u'd',u'e',u'f',u'g',
                           u'h',u'i',u'j',u'k',u'l',u'm',u'n',
                           u'o',u'p',u'q',u'r',u's',u't',
                           u'u',u'v',u'w',u'x',u'y',u'z',
                           u'+',u'­',u'*',u'/',u'’',u'…',u'º',u',',u'±',}
        self.alphabetSK = {u'á',u'ä',u'č',u'ď',u'é',u'í',u'ĺ',u'ľ',u'ň',u'ó',u'ô',u'ŕ',u'š',u'ť',u'ú',u'ý',u'ž'}
        self.alphabetFR = {u'à',u'â',u'æ',u'ç',u'é',u'è',u'ê',u'ë',u'î',u'ï',u'ô',u'œ',u'ù',u'û',u'ü',u'ÿ'}
        self.alphabetES = {u'á',u'ã',u'é',u'í',u'ó',u'ú',u'ñ',u'ü',u'¿',u'¡'}
        self.alphabetDE = {u'ä',u'ö',u'ü',u'ß'}
        self.alphabetPL = {u'ą',u'ć',u'ę',u'ł',u'ń',u'ó',u'ś',u'ź',u'ż'}

        self.languages = {
            '0': {
                'name': 'Slovak',
                'alphabet': self.alphabet26 | self.alphabetSK,
                'alphaTable': {},
                'alphaCount': 1,
            },
            '1': {
                'name': 'French',
                'alphabet': self.alphabet26 | self.alphabetFR,
                'alphaTable': {},
                'alphaCount': 1,
            },
            '2': {
                'name': 'Spanish',
                'alphabet': self.alphabet26 | self.alphabetES,
                'alphaTable': {},
                'alphaCount': 1,
            },
            '3': {
                'name': 'German',
                'alphabet': self.alphabet26 | self.alphabetDE,
                'alphaTable': {},
                'alphaCount': 1,
            },
            '4': {
                'name': 'Polish',
                'alphabet': self.alphabet26 | self.alphabetPL,
                'alphaTable': {},
                'alphaCount': 1,
            },
        }

        self.alphaSet = set()
        for language in self.languages:
            self.alphaSet.update(self.languages[language]['alphabet'])

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
                    if len(Text) < 1:
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

    def defineFeatures(self, dataset):
        featureSpace = {}
        featureCount = 0
        
        for data in dataset:
            unicodeText = data.Text.replace(" ", "").lower()
            for alpha in unicodeText:
                if alpha in featureSpace:
                    featureSpace[alpha] += 1
                else:
                    featureSpace[alpha] = 1
                featureCount += 1

        return featureSpace, featureCount

    # Calculate occurrences of each item in featureSpace (char)
    def calcFrequency(self, trainingSet, languageId):
        alphabet = self.languages[languageId]['alphabet']
        alphaCount = 0
        alphaTable = { char: 1 for char in alphabet }

        for trainingData in trainingSet:
            if trainingData.Category == languageId:
                unicodeText = trainingData.Text.replace(" ", "").decode('utf-8').lower()
                for alpha in unicodeText:
                    if alpha in alphaTable:
                        alphaTable[alpha] += 1
                        if alpha not in self.alphabet26:
                            alphaTable[alpha] += 1
                        alphaCount += 1

        self.languages[languageId].update({
            'alphaTable': alphaTable,
            'alphaCount': alphaCount,
        })

    # Normalize weights based on language distribution
    def normalizeFreq(self):
        featureTable = {
            char: 1 for char in self.alphaSet
        }

        for language in self.languages:
            alphaTable = self.languages[language]['alphaTable']
            for alpha in alphaTable:
                featureTable[alpha] += alphaTable[alpha]

        for language in self.languages:
            alphaTable = self.languages[language]['alphaTable']
            for alpha in alphaTable:
                weight = float(alphaTable.get(alpha, 1))/featureTable[alpha]
                self.languages[language]['alphaTable'].update({
                    alpha: weight,
                })

    # Calculate confidence for text is in languageId
    def calcConfidence(self, languageId, unicodeText):
        if len(unicodeText) > 0:
            confidence = 0.0
            alphaCount = self.languages[languageId].get('alphaCount', 1)
            alphaTable = self.languages[languageId].get('alphaTable', {})

            # Idea: more probable = higher penalty if witnessing a foreign char
            featureCount = 0.0
            for language in self.languages:
                featureCount += self.languages[language]['alphaCount']
            penalty = float(alphaCount)/featureCount

            for alpha in unicodeText:
                if alpha in alphaTable:
                    confidence += float(alphaTable[alpha])/alphaCount
                else:
                    confidence -= penalty

            return confidence/len(unicodeText)
        else:
            return 0.5

    # Plot based on features (Slovak-ness, French-ness, etc.)
    def plotData(self, dataPoint):
        unicodeText = dataPoint.Text.replace(" ", "").decode('utf-8').lower()
        for language in self.languages:
            confidence = self.calcConfidence(language, unicodeText)
            dataPoint.features.update({
                language: confidence
            })

    # Calculate Euclidean distance of two data points
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
    print('Printing alphabet26...%s' % ', '.join(analyzer.alphabet26))
    print('Printing alphabetSK...%s' % ', '.join(analyzer.alphabetSK))
    print('Printing alphabetFR...%s' % ', '.join(analyzer.alphabetFR))
    print('Printing alphabetES...%s' % ', '.join(analyzer.alphabetES))
    print('Printing alphabetGE...%s' % ', '.join(analyzer.alphabetDE))
    print('Printing alphabetPL...%s' % ', '.join(analyzer.alphabetPL))


if __name__ == '__main__':
    main()