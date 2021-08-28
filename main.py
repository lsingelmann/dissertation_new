# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import dissertationWorkflow
import pandas

Log2019, Log2020, ListOfTokens = dissertationWorkflow.DissertationPreprocess('2019sql.csv', '2020sql.csv')
#print(Log2019)
#print(Log2020)
#print(ListOfTokens)

spreadsheet=pandas.read_csv("sampleTokens.csv")
Inputs=spreadsheet['tokens']
Inputs=Inputs.astype(str).values.tolist()

spreadsheet=pandas.read_csv("sampleClasses.csv")
Y=spreadsheet['labels']
Y=Y.astype(str).values.tolist()

dissertationWorkflow.DissertationStep2(Inputs,Y)