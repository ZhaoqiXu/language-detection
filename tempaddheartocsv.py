#-*- coding: utf-8 -*-
import csv
from googletrans import Translator
import re
import time
import json
from langdetect import detect
start_time = time.time()
trainfile1 = "train_set_x.csv"
trainfile2 = "train_set_y.csv"
modifiedx = "train_set_x_cleaned.csv"
modifiedy = "train_set_y_cleaned.csv"


# try:
#     emoji_pattern = re.compile(r'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
# except re.error: # pragma: no cover
#     emoji_pattern = re.compile(r'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')

emoji_pattern = re.compile(r'([\U00002600-\U000027BF\U0001F300-\U0001F64F\U0001F680-\U0001F6FF])')
def remove_emoji(text):
    return emoji_pattern.sub('', text)

with open(trainfile1,'rt') as f1,open(trainfile2,'rt') as f2,open(modifiedx,'wt') as f3,open(modifiedy,'wt') as f4:
    xreader = list(csv.reader(f1))
    yreader = list(csv.reader(f2))
    yfieldnames = ["Id", "Category"]
    xfieldnames = ["Id", "Text"]
    ywriter = csv.DictWriter(f4,fieldnames=yfieldnames)
    xwriter = csv.DictWriter(f3,fieldnames=xfieldnames)
    dict = {0:"sk",1:"fr",2:"es",3:"de",4:"pl"}#{0: Slovak, 1: French, 2: Spanish, 3: German, 4: Polish}
    reversedict = {"sk":0,"fr":1,"es":2,"de":3,"pl":4}
    xwriter.writeheader()
    ywriter.writeheader()
    translator = Translator()

    try:
    # UCS-4
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
    # UCS-2
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    # for index,char in enumerate(xreader[77][1]):
    #     print str(index) + char

    truenum = 0
    for index,x in enumerate(xreader[2000:5000]):
        #first value of csv column is "Category" so it should be skipped.
        x = x[1]
        if len(x) == 0:
            continue

        x = remove_emoji(x)
        y = yreader[index+1][1]
        y = int(y)

        #print dict.get(y)
        # try:
        #     result = translator.detect(x).lang
        # except json.decoder.JSONDecodeError as e:
        #     print(index)
        #     print(x)
        #     continue

        result = translator.detect(x).lang
        if dict.get(y) == result or result == "":
            truenum = truenum + 1
        #time.sleep(0.15)
        # if int(index/300) > int((index - 1)/300):
        #     time.sleep(40)
        #print (result)
    print(truenum)
    print("--- %s seconds ---" % (time.time() - start_time))
