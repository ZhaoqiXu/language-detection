#-*- coding: utf-8 -*-

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