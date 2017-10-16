import csv
import collections
import pandas as pd
import numpy as np
trainfile1 = "train_set_x.csv"
trainfile2 = "train_set_y.csv"
testfile = "test_set_x.csv"
outputfile = "test_set_y_temp.csv"

# trainfile1 = "dat_train_x.csv"
# trainfile2 = "dat_train_y.csv"



with open(trainfile1,'rt') as f1,open(trainfile2,'rt') as f2,open(testfile,'rt') as f3,open(outputfile,'wt') as f4:
    xreader = list(csv.reader(f1))
    yreader = list(csv.reader(f2))
    testreader = list(csv.reader(f3))
    fieldnames = ["Id", "Category"]
    writer = csv.DictWriter(f4,fieldnames=fieldnames)
    writer.writeheader()
    CounterList = []
    for i in range(0,5):
         CounterList.append(collections.Counter())
    Occur = [0.0]*5
    for index,x in enumerate(xreader[1:]):
        #first value of csv column is "Category" so it should be skipped.
        x = x[1]
        counter = collections.Counter(x)
        y = yreader[index+1][1]
        y = int(y)
        Occur[y] = Occur[y] + 1
        CounterList[y] = CounterList[y] + counter
    DictList = []
    totaloccur = sum(Occur)
    Freq = [i/totaloccur for i in Occur]
    for counter in CounterList:
        totalchar = float(sum(counter.values()))
        counter[' '] = 0
        #CounterList2.append([(i, float(counter[i]) / float(totalchar)) for i in counter])
        dict = {}
        for i in counter:
            dict[ord(i)] = (float(counter[i])+1)/(totalchar+2)
        DictList.append(dict)
    #print(DictList)
    # for counter in DictList:
    #     print(counter.get(ord('a')))
    #     print(counter)
    Matrix = pd.DataFrame(DictList).fillna(0.0)
    #print Matrix
    utflist = list(Matrix.columns)
    Matrix = np.array(Matrix.values)
    #print Matrix # 5*158
    for index,input in enumerate(testreader[1:]):
        input = "".join(input[1].split())
        Py = np.array(Freq)
        for char in input:
            charutfval = ord(char)
            try:
                columnindex = utflist.index(charutfval)
            except ValueError:
                print(input)
                print(char)
                continue
            Pxi = Matrix[:,columnindex]
            if not Pxi.any():
                #if all the P(xi) are zero this char will be skipped.
                print(Pxi)
                continue
            Py = np.multiply(Py,Pxi)
        if len(Py) != 5:
            print(Py)
        result = np.argmax(Py)

        writer.writerow({'Id': str(index), 'Category': str(result)})




