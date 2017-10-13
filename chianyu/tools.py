#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv

class DataPoint:

    def __init__(self, Id, Text, Category=None):
        self.Id = Id
        self.Text = Text
        self.Category = Category
        self.Neighbors = {}

    def __repr__(self):
        return 'ID: %s\nText: %s\nCategory: %s\nNeighbors: %s' % (
            self.Id,
            self.Text,
            self.Category,
            self.Neighbors,
        )

class languageAnalyzer():

    def __init__(self, dataset=None):
        self.numerals =   ['1','2','3','4','5','6','7','8','9','0']
        self.alphabet26 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.alphabetES = [u'á',u'é',u'í',u'ó',u'ú',u'ñ',u'Ñ',u'ü',u'Ü',u'¿',u'¡']
        self.alphabetFR = [u'à',u'â',u'æ',u'ç',u'é',u'è',u'ê',u'ë',u'î',u'ï',u'ô',u'œ',u'ù',u'û',u'ü',u'ÿ']
        self.alphabetSK = [u'á',u'ä',u'č',u'ď',u'é',u'í',u'ĺ',u'ľ',u'ň',u'ó',u'ô',u'ŕ',u'š',u'ť',u'ú',u'ý',u'ž']
        self.alphabetDE = [u'ä',u'ö',u'ü',u'ß']
        self.alphabetPL = [u'ą',u'ć',u'ę',u'ł',u'ń',u'ó',u'ś',u'ź',u'ż']

        print('Printing numerals...%s' % ', '.join(self.numerals))
        print('Printing alphabet26...%s' % ', '.join(self.alphabet26))
        print('Printing alphabetES...%s' % ', '.join(self.alphabetES))
        print('Printing alphabetFR...%s' % ', '.join(self.alphabetFR))
        print('Printing alphabetSK...%s' % ', '.join(self.alphabetSK))
        print('Printing alphabetGE...%s' % ', '.join(self.alphabetDE))
        print('Printing alphabetPL...%s' % ', '.join(self.alphabetPL))

        self.labels = {
            '0': {'name':'Slovak', 'special':self.alphabetSK},
            '1': {'name':'French', 'special':self.alphabetFR},
            '2': {'name':'Spanish', 'special':self.alphabetES},
            '3': {'name':'German', 'special':self.alphabetDE},
            '4': {'name':'Polish', 'special':self.alphabetPL},
        }

        self.dataset = dataset


    def loadTrainingData(self, filenameX, filenameY, preprocessed=False):
        trainingSet = {}

        print('Reading training set X...')
        with open(filenameX, 'rb') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            fieldNames = csvReader.next()
            dictReader = csv.DictReader(csvFile, fieldnames=fieldNames)
            for row in dictReader:
                Id = row['Id']
                Text = row['Text']
                if preprocessed:
                    if not len(Text) > 1:
                        break
                entry = DataPoint(Id, Text)
                trainingSet.update({Id: entry})

        print('Reading training set Y...')
        with open(filenameY, 'rb') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            fieldNames = csvReader.next()
            dictReader = csv.DictReader(csvFile, fieldnames=fieldNames)
            for row in dictReader:
                Id = row['Id']
                if trainingSet.has_key(Id):
                    trainingSet[Id].Category = row['Category']

        print('Training set read complete.')
        return trainingSet


    def loadTestData(self, filename):
        testSet = {}

        print('Reading test set X...')
        with open(filename, 'rb') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            fieldNames = csvReader.next()
            dictReader = csv.DictReader(csvFile, fieldnames=fieldNames)
            for row in dictReader:
                entry = sentence.sentence(row['Id'], row['Text'])
                testSet.update({row['Id']: entry})

        print('Test set read complete.')
        return testSet


    def calcFrequency(self, dataset, languageId):

        language = str(languageId)
        specialA = []
        specialB = []
        if language in self.labels:
            for l in self.labels:
                if l == language:
                    specialA = self.labels[l]['special']
                else:
                    specialB.extend(self.labels[l]['special'])
        else:
            print('Language ID %s is not supported.' % language)
            return

        alphabets = list(self.alphabet26)
        alphabets.extend(specialA)
        frequency = {a: 0 for a in alphabets}

        count = 0
        for sid in dataset:
            sentence = dataset[sid]
            if sentence.Category == language:
                try:
                    charList = sentence.Text.replace(" ", "").decode('utf-8').lower()
                except:
                    print('Unicode encoding failed.')
                    break
                for c in charList:
                    if frequency.has_key(c):
                        frequency[c] += 1
                        count += 1
                    #elif c in specialB:
                    #    print('Entry %s contain %s from other alphabets' % (sentence.Id, c))

        return (frequency, count)


def main():
    print('hello world!')


if __name__ == '__main__':
    main()