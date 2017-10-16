#!/usr/bin/python
# -*- coding: <encoding name> -*-

import time
import csv
import multiprocessing

import numpy as np
from sklearn import neighbors
from sklearn.model_selection import train_test_split

import tools


def knn(k):

    validation = False
    write = True

    t0 = time.time()

    trainingDataX = 'train_set_x.csv'
    trainingDataY = 'train_set_y.csv'
    testDataX = 'test_set_x.csv'

    analyzer = tools.languageAnalyzer()

    #print('Reading training set...')
    trainingSet = analyzer.loadTrainingData(trainingDataX, trainingDataY, preprocessed=True)
    #print('Training set read complete.')

    #print('Analyzing training set...')
    for language in analyzer.languages:
        analyzer.calcFrequency(trainingSet, language)
    analyzer.analyzeFreq()

    npX = []
    npY = []
    #print('Plotting training data...')
    for trainingData in trainingSet:
        analyzer.plotData(trainingData)

        xPoints = []
        for i in range(5):
            xPoints.append(trainingData.features[str(i)])
        yPoints = int(trainingData.Category)

        npX.append(xPoints)
        npY.append(yPoints)
    X = np.array(npX)
    Y = np.array(npY)
    #print('Preprocessing time: %.2f' % (time.time() - t0))

    if validation:
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4)
        clf = neighbors.KNeighborsClassifier(k, 'distance')
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        print('k=%d -> score=%f' % (k, score))

    else:
        print('Reading test set...')
        testSet = analyzer.loadTestData(testDataX)
        print('Test set read complete.')

        npZ = []
        print('Plotting test data...')
        for testData in testSet:
            analyzer.plotData(testData)

            zPoints = []
            for i in range(5):
                zPoints.append(testData.features[str(i)])

            npZ.append(zPoints)
        Z = np.array(npZ)
        clf = neighbors.KNeighborsClassifier(k, 'distance')
        clf.fit(X, Y)
        predictions = clf.predict(Z)

        if write:
            with open('test_set_y.csv', 'wb') as csvFile:
                fieldnames = ['Id', 'Category']
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                writer.writeheader()

                count = 0
                for p in predictions:
                    writer.writerow({
                        'Id': count,
                        'Category': p,
                    })
                    count += 1

def main():

    kList = range(61)
    kList.remove(0)
    kList = [15]

    pool = multiprocessing.Pool(processes=15)
    result = pool.map(knn, kList)





if __name__ == '__main__':
    main()