import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('punkt')
import re
import sklearn
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
import sklearn.metrics
import csv
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def remove_string_special_characters(s):
    # removes special characters with ' '
    stripped = re.sub('[^a-zA-z\s]', '', s)
    stripped = re.sub('_', '', stripped)

    # Change any white space to one space
    stripped = re.sub('\s+', ' ', stripped)

    # Remove start and end white spaces
    stripped = stripped.strip()
    if stripped != '':
        return stripped.lower()

def stop_words_removal(words,list2Remove):
    stop_words = set(stopwords.words('english'))
    for i, line in enumerate(words):
        words[i] = ' '.join([words for
                         words in nltk.word_tokenize(line) if
                         (words not in stop_words) and (words not in list2Remove)])
    return words

def tokenize(inputs,grams):
    vectorizer=sklearn.feature_extraction.text.TfidfVectorizer(ngram_range=(1,grams))
    inputs=vectorizer.fit_transform(inputs)
    featureNames=vectorizer.get_feature_names()
    return inputs,featureNames

def train_test_fold(train_in, test_in, train_out,test_out, fold_no,model):
  model.fit(train_in,train_out)
  predictions = model.predict(test_in)
  accuracy=sklearn.metrics.accuracy_score(test_out,predictions)
  kappa=sklearn.metrics.cohen_kappa_score(test_out,predictions)
  f1=sklearn.metrics.f1_score(test_out,predictions,average='macro')
  recall=sklearn.metrics.recall_score(test_out,predictions,average='macro')
  precision=sklearn.metrics.precision_score(test_out,predictions,average='macro')
  return accuracy,kappa,f1,recall,precision



def train_test_model(inputs,outputs,model,n_splits):
    fold_no = 1
    accuracy=np.zeros(n_splits)
    kappa=np.zeros(n_splits)
    f1=np.zeros(n_splits)
    precision=np.zeros(n_splits)
    recall=np.zeros(n_splits)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=25)
    for train_index, test_index in skf.split(inputs, outputs):
        #sm = SMOTE( )
        #train_in,train_out = sm.fit_resample(X2[train_index,:],Y[train_index])
        train_in=inputs[train_index,:]
        print(train_index)
        train_out=outputs[train_index]
        test_in = inputs[test_index,:]
        test_out=outputs[test_index]
        accuracy[fold_no-1],kappa[fold_no-1],f1[fold_no-1],recall[fold_no-1],precision[fold_no-1]=train_test_fold(train_in,test_in,train_out,test_out,fold_no,model)
        fold_no += 1

    accuracy=accuracy.mean()
    kappa=kappa.mean()
    f1=f1.mean()
    recall=recall.mean()
    precision=precision.mean()
    return(accuracy,kappa,f1,recall,precision)


def getFeatureNamesClass(inputs,outputs,model,uniqueClass):
        outputs0=[0]*len(outputs)
        for i in range(len(outputs)):
            if (outputs[i] == uniqueClass):
                outputs0[i] = "1"
            else:
                outputs0[i] = "0"
        model0=model
        model0.fit(inputs,outputs0)
        coef1 = pd.DataFrame.sparse.from_spmatrix(model0.coef_)
        print(coef1)
        print(type(coef1))
        return(coef1)

def getFeatureNamesAll(inputs,outputs,model,featureNames):
        unique_classes=list(set(outputs))
        listOfCoefs=[]
        featureDataFrame=pd.DataFrame(featureNames)
        featureDataFrame=featureDataFrame.T
        with open('coefficients.csv', 'w', newline='', encoding="utf8") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            filewriter.writerow([featureNames])
            for i in range(len(unique_classes)):
                coef=getFeatureNamesClass(inputs, outputs, model, unique_classes[i])
                out_arr = np.argsort(coef)
                print('look here',unique_classes[i])
                print(out_arr.iloc[:,-20])
                for a in range(len(featureNames)-20,len(featureNames)):
                    x=out_arr.iloc[0][a]
                    print(x)
                    print(featureDataFrame.iloc[0][x])
                listOfCoefs.append(coef)
                filewriter.writerow([coef])
                line_count += 1
        return(listOfCoefs)