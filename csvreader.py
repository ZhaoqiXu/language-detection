import csv
import collections
import pandas as pd
import numpy as np
import re
trainfile1 = "train_set_x.csv"
trainfile2 = "train_set_y.csv"
testfile = "test_set_x.csv"
outputfile = "test_set_y_temp.csv"
modifiedx = "train_set_x_cleaned.csv"
modifiedy = "train_set_y_cleaned.csv"

# trainfile1 = "dat_train_x.csv"
# trainfile2 = "dat_train_y.csv"

emoji_pattern = re.compile(r'([\U00002600-\U000027BF\U0001F300-\U0001F64F\U0001F680-\U0001F6FF])')
def remove_emoji(text):
    return emoji_pattern.sub('', text)

with open(trainfile1,'rt') as f1,open(trainfile2,'rt') as f2,open(testfile,'rt') as f3,open(outputfile,'wt') as f4:
    xreader = list(csv.reader(f1))
    yreader = list(csv.reader(f2))
    testreader = list(csv.reader(f3))
    fieldnames = ["Id", "Category"]
    writer = csv.DictWriter(f4,fieldnames=fieldnames)
    writer.writeheader()
    CounterList = []
    Nt_Counter = []
    for i in range(0,5):
        CounterList.append(collections.Counter())
        Nt_Counter.append(collections.Counter())
    Occur = [0.0]*5
    for index,x in enumerate(xreader[1:]):
        #first value of csv column is "Category" so it should be skipped.
        x = x[1]
        x = remove_emoji(x)
        counter = collections.Counter(x)
        counter2 = collections.Counter({i for i in counter})
        y = yreader[index+1][1]
        y = int(y)
        Occur[y] = Occur[y] + 1
        CounterList[y] = CounterList[y] + counter
        Nt_Counter[y] = Nt_Counter[y] + counter2

    word_count_in_classList = [dict() for i in range(0,5)]
    totaloccur = sum(Occur)
    Freq = [i/totaloccur for i in Occur]
    total_words_in_class = []
    for index,counter in enumerate(CounterList):
        totalchar = (sum(counter.values()))
        total_words_in_class.append(totalchar)
        word_count_in_class = {}
        for i in counter:
            word_count_in_class[ord(i)] = float((counter[i]))
        word_count_in_classList[index] = word_count_in_class
    Nt_Dict = [None for x in range(5)]
    total_unique_words_in_class = []
    for index,counter in enumerate(Nt_Counter):
        dict = {}
        for i in counter:
            dict[ord(i)] = (counter[i])+1.0
        total_unique_words_in_class.append(len(counter))
        Nt_Dict[index] = dict


    Nt_Matrix = pd.DataFrame(Nt_Dict).fillna(1.0)
    word_count_in_classMatrix = pd.DataFrame(word_count_in_classList).fillna(0.0)
    utflist = list(word_count_in_classMatrix.columns)
    word_count_in_classMatrix = np.array(word_count_in_classMatrix.values)
    Nt_Matrix = np.array(Nt_Matrix.values)
    Occur = np.array(Occur)
    total_unique_words_in_class = np.array(total_unique_words_in_class)
    total_words_in_class = np.array(total_words_in_class)
    Denominator = np.add(total_words_in_class,total_unique_words_in_class)
    for index,input in enumerate(testreader[1:]):
        input = "".join(remove_emoji(input[1]).split())
        Py = np.array(Freq)
        for char in input:
            charutfval = ord(char)
            try:
                columnindex = utflist.index(charutfval)
            except ValueError:
                continue
            word_count_in_class = word_count_in_classMatrix[:,columnindex]
            Ntxi = Nt_Matrix[:,columnindex]
            ITF = np.log(np.divide(Occur,Ntxi))
            if not word_count_in_class.any():
                #if all the P(xi) are zero this char will be skipped.
                print(word_count_in_class)
                continue
            Py = np.multiply(Py,np.divide(np.multiply(word_count_in_class,ITF)+1,Denominator))
            #Py = np.multiply(Py,Pxi)
        if len(Py) != 5:
            print(Py)
        result = np.argmax(Py)

        writer.writerow({'Id': str(index), 'Category': str(result)})




