import csv
import collections
<<<<<<< HEAD
import pandas as pd
import numpy as np
trainfile1 = "train_set_x.csv"
trainfile2 = "train_set_y.csv"
testfile = "test_set_x.csv"
outputfile = "test_set_y_temp.csv"

=======

trainfile1 = "dat_train_x.csv"
trainfile2 = "dat_train_y.csv"
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> parent of 4bef187... add new train set
=======
>>>>>>> parent of 4bef187... add new train set
>>>>>>> 0ccd3d1a284ea40e6a3e6a85667f75b0fe75ef0c


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
    for index,x in enumerate(xreader[1:]):
        #first value of csv column is "Category" so it should be skipped.
        x = x[1]
        counter = collections.Counter(x)
        y = yreader[index+1][1]
        y = int(y)
        CounterList[y] = CounterList[y] + counter
    DictList = []
    for counter in CounterList:
        totalchar = float(sum(counter.values()))
        #CounterList2.append([(i, float(counter[i]) / float(totalchar)) for i in counter])
        dict = {}
        for i in counter:
            dict[ord(i)] = float(counter[i])/totalchar
        DictList.append(dict)
    #print DictList
    # for counter in CounterList2:
    #     print type(counter)
    #     print counter.get(' ')
    Matrix = pd.DataFrame(DictList).fillna(0.0)
    #print Matrix
    utflist = list(Matrix.columns)
    Matrix = np.array(Matrix.values)
    #print Matrix # 5*158
    for index,input in enumerate(testreader[1:]):
        input = "".join(input[1].split())
        Py = np.array([1.0] * 5)
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




