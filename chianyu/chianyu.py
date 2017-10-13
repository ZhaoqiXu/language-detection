#-*- coding: utf-8 -*-

import csv

import sentence

numerals = ['1','2','3','4','5','6','7','8','9','0',' ']
alphabet26 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','','v','w','x','y','z']
alphabetE = ['á','é','í','ó','ú','ñ','Ñ','ü','Ü','¿','¡']
alphabetF = ['à','â','æ','ç','é','è','ê','ë','î','ï','ô','œ','ù','û','ü','ÿ']
alphabetS = ['á','ä','č','ď','é','í','ĺ','ľ','ň','ó','ô','ŕ','š','ť','ú','ý','ž']
alphabetG = ['ä','ö','ü','ß']
alphabetP = ['ą','ć','ę','ł','ń','ó','ś','ź','ż']

print('printing alphabetE...%s' % ', '.join(alphabetE))
print('printing alphabetF...%s' % ', '.join(alphabetF))
print('printing alphabetS...%s' % ', '.join(alphabetS))
print('printing alphabetG...%s' % ', '.join(alphabetG))
print('printing alphabetP...%s' % ', '.join(alphabetP))


def loadTrainingData(filenameX, filenameY, preprocessed=False):
    trainingData = {}

    print('Loading training set X...')
    with open(filenameX, 'rb') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        fieldNames = csvReader.next()
        dictReader = csv.DictReader(csvFile, fieldnames=fieldNames)
        for row in dictReader:
            Id = row['Id']
            Text = row['Text']
            if preprocessed:
                if Text == '':
                    break
            entry = sentence.sentence(Id, row['Text'])
            trainingData.update({Id:entry})

    print('Loading training set Y...')
    with open(filenameY, 'rb') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        fieldNames = csvReader.next()
        dictReader = csv.DictReader(csvFile, fieldnames=fieldNames)
        for row in dictReader:
            Id = row['Id']
            if trainingData.has_key(Id):
                trainingData[Id].Category = row['Category']

    print('Training set read complete.')
    return trainingData


def loadTestData(filenameX):
    testData = {}

    print('Loading training set X...')
    with open(filenameX, 'rb') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        fieldNames = csvReader.next()
        dictReader = csv.DictReader(csvFile, fieldnames=fieldNames)
        for row in dictReader:
            entry = sentence.sentence(row['Id'], row['Text'])
            testData.update({row['Id']: entry})

    print('Test set read complete.')
    return testData


def euclideanDistance(sampleText, testText):
    # Examples
    distance = 0
    testList = str(testText).lower().split('')
    sampleList = str(sampleText).lower().split('')
    for t in testList:
        if t in sampleList:
            distance += 1
            sampleList.remove(t)
    return distance


def getNeighbors(trainingSet, testSentence, k):
    distances = []
    for nid in trainingSet:
        dist = euclideanDistance(trainingSet[nid].Text, testSentence.Text)
        distances.append((nid, dist))
    distances.sort(key=lambda t:t[1])
    # Return top k closest neighbors
    neighbors = {}
    for i in range(k):
        nid = distances[i][0]
        neighbors.update({
            nid:trainingSet[nid],
        })
    return neighbors


def getResponse(neighborSet):
    election = {}
    for nid in neighborSet:
        vote = neighborSet[nid].Category
        if vote in election:
            election[vote] += 1
        else:
            election[vote] = 1
    # Return the most voted category
    ranking = sorted(election.iteritems(), key=lambda t:t[1], reverse=True)
    return ranking[0][0]


def knn(trainingSet, testSet, k):
    print('Received data: %d examples and %d tests' % (len(trainingSet), len(testSet)))
    for tid in testSet:
        neighbors = getNeighbors(trainingSet, testSet[tid], k)
        prediction = getResponse(neighbors)
        testSet[tid].Category = prediction
        testSet[tid].Neighbors = neighbors
    print('K-Nearest Neighbors Done.')


def main():
    trainingDataX = 'train_set_x.csv'
    trainingDataY = 'train_set_y.csv'
    testDataX = 'test_set_x.csv'

    trainingDataFull = loadTrainingData(trainingDataX, trainingDataY)
    #testDataFull = loadTestData(testDataX)

    strange = {'',}
    for sid in trainingDataFull:
        alpha = set(trainingDataFull[sid].Text.lower())
        for a in alpha:
            if len(a) > 0:
                if a not in alphabet26:
                    if a not in numerals:
                        strange = strange | (set(a))

    for a in strange:
        include = []
        if a in alphabetE:
            include.append('Spanish')
        if a in alphabetF:
            include.append('French')
        if a in alphabetS:
            include.append('Slovak')
        if a in alphabetG:
            include.append('German')
        if a in alphabetP:
            include.append('Polish')
        print('%s is found in %s' % (str(a), ', '.join(include)))
    return

    k = 5
    tid = '12'
    sampleTest = {
        tid: testDataFull.get(tid),
    }
    neighbors = knn(trainingDataFull, sampleTest, k)

    for tid in sampleTest:
        print(sampleTest[tid])
        print(neighbors)




if __name__ == '__main__':
    main()