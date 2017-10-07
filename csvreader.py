import csv
import collections

trainfile1 = "train_set_x.csv"
trainfile2 = "train_set_y.csv"


with open(trainfile1,'rb') as f1,open(trainfile2,'rb') as f2:
    xreader = list(csv.reader(f1))
    yreader = list(csv.reader(f2))
    CounterList = []
    for i in range(0,5):
         CounterList.append(collections.Counter())
    for index,x in enumerate(xreader[1:]):
        #first value of csv column is "Category" so it should be skipped.
        x = x[1]
        counter = collections.Counter(x)
        y = yreader[index+1][1]
        y = int(y)
        CounterList[y] = CounterList[y] + counter
    CounterList2 = []
    for counter in CounterList:
        totalchar = sum(counter.values())
        CounterList2.append([(i, float(counter[i]) / float(totalchar)) for i in counter])
    for counter in CounterList2:
        print counter
