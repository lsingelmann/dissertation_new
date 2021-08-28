import MOOCIBLToolbox
import classificationToolbox
import sklearn
import sklearn.neighbors
import sklearn.ensemble
import sklearn.svm
import sklearn.linear_model
import numpy as np

def DissertationPreprocess(sql2019,sql2020):
    Log2019=MOOCIBLToolbox.RawToLog2019(sql2019)
    Log2020=MOOCIBLToolbox.RawToLog2020(sql2020)
    ListOfTokens=MOOCIBLToolbox.LogsToTokens('2019processedLog.csv','2020processedLog.csv','listOfTokens.csv')
    return Log2019, Log2020, ListOfTokens;

def DissertationStep1(tokenClassesFile,studentClassesFile):
    tokenClasses=MOOCIBLToolbox.ImportTokenClasses(tokenClassesFile)
    studentClasses=MOOCIBLToolbox.ImportStudentClasses(studentClassesFile)
    return tokenClasses, studentClasses;


def DissertationStep2(inputs,outputs):
    #inputs=classificationToolbox.remove_string_special_characters(inputs)
    inputs=classificationToolbox.stop_words_removal(inputs,[])
    tfidf,featureNames=classificationToolbox.tokenize(inputs,1)
    n_splits = 10
    svmmodel = sklearn.svm.SVC(kernel='linear', decision_function_shape="ovr", gamma='scale', class_weight='balanced')
    knnmodel=sklearn.neighbors.KNeighborsClassifier(n_neighbors=3)
    rfcmodel = sklearn.ensemble.RandomForestClassifier(class_weight='balanced')
    lrmodel= sklearn.linear_model.LogisticRegression()
    print(classificationToolbox.train_test_model(tfidf,np.array(outputs),svmmodel,n_splits))
    print(classificationToolbox.getFeatureNamesAll(tfidf,np.array(outputs),svmmodel,featureNames))

def DissertationStep3():
    [performanceMetricsStudents, tokenEstimatedClassesStudents, topModelStudents, topFeaturesStudents] = MOOCIBLToolbox.FindBestSets(ListOfTokens[3],ListOfTokens[8],studentClasses)
