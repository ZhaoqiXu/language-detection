#!/usr/bin/python
# -*- coding: <encoding name> -*-

import tools


def main():
    trainingDataX = 'train_set_x.csv'
    trainingDataY = 'train_set_y.csv'
    testDataX = 'test_set_x.csv'

    analyzer = tools.languageAnalyzer()

    trainingDataFull = analyzer.loadTrainingData(trainingDataX, trainingDataY)
    #testDataFull = analyzer.loadTestData(testDataX)

    (freq, count) = analyzer.calcFrequency(trainingDataFull, 1)

    print('Total count: %d' % count)
    for key in freq:
        print('%s occured %d times (%.2f percent)' % (key, freq[key], (freq[key]*100.0)/count))



if __name__ == '__main__':
    main()