#!/usr/bin/python
# -*- coding: <encoding name> -*-

# Standard imports
import csv
import multiprocessing
# Library imports
import numpy as np
from sklearn import neighbors
from sklearn.model_selection import train_test_split
# Project imports
import tools

def dummyWrite(languageId):
    with open('test_set_x.csv', 'rb') as csvFileX, open('test_set_y_%s.csv' % languageId, 'wb') as csvFileY:

        csvReader = csv.reader(csvFileX, delimiter=',')
        csvReader.next() # Skip header
        fieldnames = ['Id', 'Category']
        writer = csv.DictWriter(csvFileY, fieldnames=fieldnames)
        writer.writeheader()

        for row in csvReader:
            writer.writerow({
                'Id': row[0],
                'Category': languageId,
            })

def computeKNN(k):

    validation = False
    write = True

    trainingDataX = 'train_set_x.csv'
    trainingDataY = 'train_set_y.csv'
    testDataX = 'test_set_x.csv'

    analyzer = tools.languageAnalyzer()

    print('Reading training and test data...')
    trainingSet = analyzer.loadTrainingData(trainingDataX, trainingDataY, preprocessed=True)
    testSet = analyzer.loadTestData(testDataX)

    # For each language, find the distribution of each character
    for language in analyzer.languages:
        analyzer.calcFrequency(trainingSet, language)

    #alphaTotal = 0
    # languageDistribution = {}
    #for language in analyzer.languages:
    #    alphaTotal += analyzer.languages[language]['alphaCount']
    #for language in analyzer.languages:
    #    languageDistribution.update({
    #        language: float(analyzer.languages[language]['alphaCount'])/alphaTotal,
    #    })
    #print(languageDistribution)

    analyzer.normalizeFreq()

    #for alpha in analyzer.alphaSet:
    #    print('%s:' % alpha)
    #    for language in analyzer.languages:
    #        print('\t%f %s' % (analyzer.languages[language]['alphaTable'].get(alpha, 0), analyzer.languages[language]['name']))

    print('Plotting training data...')
    npX = []
    npY = []
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

    print('Pre-processing done. Start prediction...')
    if validation:
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)

        distribution = {
            0: 0.05601467767616493,
            1: 0.5279295196011857,
            2: 0.23368595562907218,
            3: 0.13965946637040746,
            4: 0.042710380723169704,
        }
        clf = neighbors.KNeighborsClassifier(k, weights='distance', metric='euclidean', n_jobs=-1)
        #clf = RandomForestClassifier(k, class_weight=distribution, n_jobs=-1)
        clf.fit(X_train, y_train)

        predictions = clf.predict(X_test)
        score = clf.score(X_test, y_test)

        print('k=%d -> score=%f' % (k, score))

    else:
        print('Plotting test data...')
        npZ = []
        for testData in testSet:
            analyzer.plotData(testData)

            zPoints = []
            for i in range(len(analyzer.languages)):
                zPoints.append(testData.features[str(i)])

            npZ.append(zPoints)
        Z = np.array(npZ)

        clf = neighbors.KNeighborsClassifier(k, weights='distance', p=5, n_jobs=-1)
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

    distribution = {
        '0': 0.05601467767616493,
        '1': 0.5279295196011857,
        '2': 0.23368595562907218,
        '3': 0.13965946637040746,
        '4': 0.042710380723169704,
    }

    error = 0.0
    for i in range(len(analyzer.languages)):
        actual = float(predictions.tolist().count(i)) / len(predictions.tolist())
        target = distribution[str(i)]
        diff = target - actual
        error += abs(diff)
        print('%s = %.2f%% -> %.2f%% = %.2f%%' % (analyzer.languages[str(i)]['name'], actual*100, target*100, diff*100))
    print('Total error: %.2f%%' % (error*100))
    return predictions


def main():
    #processes = multiprocessing.cpu_count() / 2
    #print('Running on %d processes...' % processes)
    #pool = multiprocessing.Pool(processes=processes)

    kList = [128]
    #predictions = pool.map(computeKNN, kList)
    for k in kList:
        print('')
        computeKNN(k)


    #analyzer = tools.languageAnalyzer()
    #languageIds = analyzer.languages.keys()
    #result = pool.map(dummyWrite, languageIds)





if __name__ == '__main__':
    main()