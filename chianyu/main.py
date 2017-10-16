#!/usr/bin/python
# -*- coding: <encoding name> -*-

import time
import tools
import operator
import multiprocessing


def validate():
    trainingDataX = 'validation_train_x.csv'
    trainingDataY = 'validation_train_y.csv'
    testDataX = 'validation_test_x.csv'
    testDataY = 'validation_test_y.csv'

    analyzer = tools.languageAnalyzer()

    trainingSet = analyzer.loadTrainingData(trainingDataX, trainingDataY, preprocessed=True)
    testSet = analyzer.loadTestData(testDataX)

    for language in analyzer.languages:
        print('Analyzing frequency for %s' % (analyzer.languages[language]['name']))
        analyzer.calcFrequency(trainingSet, language)

    #print('Plotting training set...')
    #for tid in trainingSet:
    #    analyzer.plotFeature(trainingSet[tid])

    k = 5
    count = 0
    print('Received data: %d examples and %d tests, computing KNN...' % (len(trainingSet), len(testSet)))
    for tid in testSet:
        count += 1
        if len(testSet[tid].Text) == 0:
            prediction = '1'
            neighbors = {}
        else:
            neighbors = getNeighbors(trainingSet, testSet[tid], k, analyzer)
            prediction = surveyPrediction(neighbors)
        testSet[tid].Category = prediction
        testSet[tid].Neighbors = neighbors
        print(count)
    print('K-Nearest Neighbors Done.')

    correct = 0
    validationSet = analyzer.loadTrainingData(testDataX, testDataY, preprocessed=False)
    for tid in testSet:
        t = testSet[tid]
        v = validationSet[tid]
        if t.Category == v.Category:
            correct += 1
        else:
            print('(%s) %s: predicted %s, labeled %s' % (t.Id, t.Text, t.Category, v.Category))
    print('Summary: %.2f correct' % (correct*1.0/len(testSet)))


class KNN():

    def __init__(self, trainingSet, k, analyzer):
        self.trainingSet = trainingSet
        self.k = k
        self.analyzer = analyzer


    def predict(self, testData):
        if len(testData.Text) > 0:
            neighbors = self.getNeighbors(testData)
            prediction = self.surveyNeighbors(neighbors)
        else:
            neighbors = {}
            prediction = '1'
        testData.Neighbors = neighbors
        testData.Category = prediction
        return testData


    def getNeighbors(self, testData):
        distList = []
        for trainingData in self.trainingSet:
            dist = self.analyzer.calcEuclideanDistance(trainingData, testData)
            distList.append(
                (trainingData, dist)
            )
        distList.sort(key=operator.itemgetter(1))

        neighbors = []
        for i in range(self.k):
            neighbors.append(distList[i][0])
        return neighbors


    def surveyNeighbors(self, neighborSet):
        election = {}
        for neighbor in neighborSet:
            vote = neighbor.Category
            election[vote] = election.get(vote, 0) + 1
        ranking = sorted(election, key=election.__getitem__, reverse=True)
        return ranking[0]


def printPrediction(testSet):
    with open('test_set_y.csv'):
        pass

    for testData in testSet:
        print('Test %s <%s> is predicted %s' % (testData.Id, testData.Text, testData.Category))


def startKNN(testData):
    t0 = time.time()

    analyzer = tools.languageAnalyzer()

    trainingDataX = 'train_set_x.csv'
    trainingDataY = 'train_set_y.csv'

    print('Reading training set...')
    trainingSet = analyzer.loadTrainingData(trainingDataX, trainingDataY, preprocessed=True)
    print('Training set read complete.')

    print('Analyzing training set...')
    for language in analyzer.languages:
        analyzer.calcFrequency(trainingSet, language)

    print('Plotting data points...')
    for trainingData in trainingSet:
        analyzer.plotData(trainingData)

    k = 4
    myKNN = KNN(trainingSet, k, analyzer)
    print('Preprocessing takes %.3f seconds' % (time.time()-t0))

    print('Starting KNN with k=%d...' % k)
    t0 = time.time()
    resultData = myKNN.predict(testData)
    print('K-Nearest Neighbors Done. Time: %.3f' % (time.time() - t0))

    return resultData

def main():
    #validate()

    testDataX = 'test_set_x.csv'
    analyzer = tools.languageAnalyzer()
    testSet = analyzer.loadTestData(testDataX)

    pool = multiprocessing.Pool(processes=12)
    result = pool.map(startKNN, testSet[:1])

    printPrediction(result)


if __name__ == '__main__':
    main()