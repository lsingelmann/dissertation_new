import preprocessAndCleanToolbox

def RawToLog2019(sql):
  preprocessAndCleanToolbox.importCSV(sql, ',')
  csvToWrite = createCSV2019(sql, '2019processedLog.csv', ',')
  return csvToWrite

def RawToLog2020(sql):
  preprocessAndCleanToolbox.importCSV(sql, ',')
  csvToWrite=createCSV2020(sql, '2020processedLog.csv', ',')
  return csvToWrite

def LogsToTokens(fileNameIn1,fileNameIn2,fileNameOut):
  import csv
  delimiter=','
  with open(fileNameOut, 'w',newline='',  encoding="utf8") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=delimiter, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    line_count = 0
    with open(fileNameIn1,  encoding="utf8") as csv_file:
      csvToRead = csv.reader(csv_file, delimiter=',')
      dictionary=[]
      learningobjectiveDictionary={}
      for row in csvToRead:
        stringToCheck=row[7]+' '+row[11]+' '+row[12]
        if line_count == 0:
          filewriter.writerow(['User Number','Date Time','Year','Token Number','Text 1','Text 2', 'Text 3', 'Text 4','Text Concat'])
          line_count += 1
        elif row[1] in ['6','98','10','3','7','87','9','95','User Number']:
          line_count+=1
        elif row[2]=='Insert Learning Objective' or row[2]=='Update Learning Objective':
          learningobjectiveDictionary[row[5]]={'loname': row[7],'lodescription':row[11]}
          line_count+=1
        elif not row[12]:
          line_count+=1
        elif stringToCheck in dictionary:
          line_count+=1
        else:
          filewriter.writerow([row[1],row[3],row[4],row[6],learningobjectiveDictionary[row[5]]['loname'],learningobjectiveDictionary[row[5]]['lodescription'],row[12],row[16],learningobjectiveDictionary[row[5]]['loname']+' '+learningobjectiveDictionary[row[5]]['lodescription']+' '+row[12]])
          new_item=row[7]+' '+row[11]+' '+row[12]
          dictionary.append(new_item)
          line_count += 1
    with open(fileNameIn2,  encoding="utf8") as csv_file:
      csvToRead = csv.reader(csv_file, delimiter=',')
      dictionary=[]
      for row in csvToRead:
        if line_count == 0:
          line_count += 1
        elif row[1] in ['6','98','10','3','7','87','9','95','User Number']:
          line_count+=1
        elif not row[7]:
          line_count+=1
        elif row[7] + ' ' + row[11] + ' ' + row[12] in dictionary:
          line_count += 1
        else:
          filewriter.writerow(
            [row[1], row[3], row[4], row[6],row[7], row[11], row[12], row[16], row[7] + ' ' + row[11] + ' ' + row[12]])
          new_item = row[7] + ' ' + row[11] + ' ' + row[12]
          dictionary.append(new_item)
          line_count += 1
  return filewriter

def checkType2020(command):
  words = (command.split(' '))
  if words[0] == 'Login':
    return ('Login')
  if words[0] == 'Logout':
    return ('Logout')
  if words[0] == 'INSERT':
    if words[2] == 'users':
      return ('Insert User')
    if words[2] == 'reviewDef':
      return ('Insert Definition Review')
    if words[2] == 'reviewEvi':
      return ('Insert Evidence Review')
    if words[2] == 'tokens':
      return ('Insert Token')
    else:
      return ('Insert')
  if words[0] == 'UPDATE':
    if words[1] == 'users':
      return ('Update User')
    if words[1] == 'reviewDef':
      return ('Update Definition Review')
    if words[1] == 'reviewEvi':
      return ('Update Evidence Review')
    if words[1] == 'tokens':
      return ('Update Token')
    else:
      return ('Update')
  if words[0] == 'DELETE':
    if words[2] == 'users':
      return ('Delete User')
    if words[2] == 'tokens':
      return ('Delete Token')
    else:
      return ('Delete')
  else:
    return (words[0])

def checkType2019(command):
  words = (command.split(' '))
  if words[0] == 'Login':
    return ('Login')
  if words[0] == 'Logout':
    return ('Logout')
  if words[0] == 'INSERT':
    if words[2] == 'users':
      return ('Insert User')
    if words[2] == 'Deliverables':
      return ('Insert Deliverable')
    if words[2] == 'LearningObjectives':
      return ('Insert Learning Objective')
    else:
      return ('Insert')
  if words[0] == 'UPDATE':
    if words[1] == 'users':
      return ('Update User')
    if words[1] == 'Deliverables':
      return ('Update Deliverable')
    if words[1] == 'LearningObjectives':
      return ('Update Learning Objective')
    else:
      return ('Update')
  if words[0] == 'DELETE':
    if words[2] == 'users':
      return ('Delete User')
    if words[2] == 'Deliverables':
      return ('Delete Deliverable')
    if words[2] == 'LearningObjectives':
      return ('Delete Learning Objective')
    else:
      return ('Delete')
  else:
    return (words[0])

def createCSV2020(filenameIn, filenameOut, delimiter):
  import csv
  from datetime import datetime
  with open(filenameOut, 'w',newline='',  encoding="utf8") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=delimiter, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    line_count = 0
    with open(filenameIn,  encoding="utf8") as csv_file:
      csvToRead = csv.reader(csv_file, delimiter=',')
      for row in csvToRead:
        if line_count == 0:
          filewriter.writerow(['Log Number', 'User Number', 'Action Type', 'Time','Year','ReviewNumber','TokenNumber','TokenName','','Token Webbs','Token Impact','Token Description','Evidence Description','Reviewed Acceptance','Reviewed Notes','Token Stage','Link'])
          line_count += 1
        else:
          if checkType2020(row[4]) == 'Login':
            filewriter.writerow([row[0], row[1], 'Login', row[3], '2020', '', '', '', '', '', '', '', '', '', '', '',''])

          if checkType2020(row[4]) == 'Logout':
            filewriter.writerow([row[0], row[1], 'Logout', row[3], '2020', '', '', '', '', '', '', '', '', '', '', '',''])

          if checkType2020(row[4]) == 'Insert User':
            filewriter.writerow([row[0], row[1], 'Insert User', row[3], '2020', '', '', '', '', '', '', '', '', '', '', '',''])

          if checkType2020(row[4]) == 'Insert Token':
            words = (row[4].split('='))
            tokenName = words[1].split(';')
            tokenName = tokenName[0]
            tokenName = tokenName.replace(',', '').replace('\n', '').replace('\r', '')
            tokenDescription = words[2].split(';')
            tokenDescription = tokenDescription[0]
            tokenDescription = tokenDescription.replace(',', '').replace('\n', '').replace('\r', '')
            kLevel = words[3].split(';')
            kLevel = kLevel[0]
            iLevel = words[4].split(';')
            iLevel = iLevel[0]
            evidence = words[5].split(';')
            evidence = evidence[0]
            evidence = evidence.replace(',', '').replace('\n', '').replace('\r', '')
            evidence2 = words[6].split(';')
            evidence2 = evidence2[0].replace(',', '').replace('\n', '').replace('\r', '')
            tokenStage = words[7].split(';')
            tokenStage = tokenStage[0]
            filewriter.writerow(
              [row[0], row[1], 'Insert Token', row[3], '2020','',row[2], tokenName,'', kLevel, iLevel,tokenDescription,evidence,'','', tokenStage, evidence2])

          if checkType2020(row[4]) == 'Insert Definition Review':
            words = (row[4].split('='))
            kLevel = words[1].split(';')
            kLevel = kLevel[0]
            iLevel = words[2].split(';')
            iLevel = iLevel[0]
            reviewAcceptance = words[3].split(';')
            reviewAcceptance = reviewAcceptance[0]
            reviewNotes = words[4].split(';')
            reviewNotes = reviewNotes[0]
            reviewNotes = reviewNotes.replace(',', '').replace('\n', '').replace('\r', '')
            filewriter.writerow(
              [row[0], row[1], 'Insert Definition Review', row[3], '2020','',row[2], '', '',  kLevel, iLevel, '', '',
               reviewAcceptance, reviewNotes,'',''])

          if checkType2020(row[4]) == 'Insert Evidence Review':
            words = (row[4].split('='))
            kLevel = words[1].split(';')
            kLevel = kLevel[0]
            iLevel = words[2].split(';')
            iLevel = iLevel[0]
            reviewAcceptance = words[3].split(';')
            reviewAcceptance = reviewAcceptance[0]
            reviewNotes = words[4].split(';')
            reviewNotes = reviewNotes[0]
            reviewNotes = reviewNotes.replace(',', '').replace('\n', '').replace('\r', '')
            filewriter.writerow(
              [row[0], row[1], 'Insert Evidence Review', row[3], '2020','',row[2], '', '',  kLevel, iLevel, '', '',
               reviewAcceptance, reviewNotes,'',''])

          if checkType2020(row[4]) == 'Update Definition Review':
            words = (row[4].split('='))
            kLevel = words[1].split(';')
            kLevel = kLevel[0]
            iLevel = words[2].split(';')
            iLevel = iLevel[0]
            reviewAcceptance = words[3].split(';')
            reviewAcceptance = reviewAcceptance[0]
            reviewNotes = words[4].split(';')
            reviewNotes = reviewNotes[0]
            reviewNotes = reviewNotes.replace(',', '').replace('\n', '').replace('\r', '')
            filewriter.writerow(
              [row[0], row[1], 'Update Definition Review', row[3], '2020','',row[2], '', '',  kLevel, iLevel, '', '',
               reviewAcceptance, reviewNotes,'',''])

          if checkType2020(row[4]) == 'Update Evidence Review':
            words = (row[4].split('='))
            kLevel = words[1].split(';')
            kLevel = kLevel[0]
            iLevel = words[2].split(';')
            iLevel = iLevel[0]
            reviewAcceptance = words[3].split(';')
            reviewAcceptance = reviewAcceptance[0]
            reviewNotes = words[4].split(';')
            reviewNotes = reviewNotes[0]
            reviewNotes = reviewNotes.replace(',', '').replace('\n', '').replace('\r', '')
            filewriter.writerow(
              [row[0], row[1], 'Update Evidence Review', row[3], '2020','',row[2], '', '',  kLevel, iLevel, '', '',
               reviewAcceptance, reviewNotes,'',''])

          if checkType2020(row[4]) == 'Update User':
            n = 1
            # NA for now

          if checkType2020(row[4]) == 'Update Token':
            words = (row[4].split('=',5))
            tokenName = words[1].split(';')
            tokenName = tokenName[0]
            tokenName = tokenName.replace(',', '').replace('\n', '').replace('\r', '')
            tokenDescription = words[2].split(';')
            tokenDescription = tokenDescription[0]
            tokenDescription = tokenDescription.replace(',', '').replace('\n', '').replace('\r', '')
            kLevel = words[3].split(';')
            kLevel = kLevel[0]
            iLevel = words[4].split(';')
            iLevel = iLevel[0]
            placeholder1 = words[5].split(';',1)
            evidence = placeholder1[0]
            evidence = evidence.replace(',', '').replace('\n', '').replace('\r', '')
            placeholder2 = placeholder1[1].split(';')
            evidence2=placeholder2[0]
            evidence2 = evidence2.replace(',', '').replace('\n', '').replace('\r', '')
            tokenStage = placeholder2[1].split('=')
            tokenStage = tokenStage[1]
            filewriter.writerow(
              [row[0], row[1], 'Update Token', row[3],'2020','',row[2], tokenName,'', kLevel, iLevel,tokenDescription,evidence,'','', tokenStage, evidence2])


          if checkType2020(row[4]) == 'Delete User':
            n = 1
            # NA for now

          if checkType2020(row[4]) == 'Delete Token':
            filewriter.writerow(
              [row[0], row[1], 'Delete Token', row[3], '2020','',row[2], tokenName,'', kLevel, iLevel,tokenDescription,evidence,'','', tokenStage, evidence2])

          line_count += 1

    return (filewriter)


def createCSV2019(filenameIn, filenameOut, delimiter):
  import csv
  with open(filenameOut, 'w',newline='',encoding="utf8") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=delimiter, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    line_count = 0
    with open(filenameIn,  encoding="utf8") as csv_file:
      csvToRead = csv.reader(csv_file, delimiter=',')
      for row in csvToRead:
        if line_count == 0:
          filewriter.writerow(['Log Number', 'User Number', 'Action Type', 'Time','Year','LO Number','D Number','LO Name','LOType','Blooms1','Blooms2','Description','Deliverable Name','Deliverable Type','Progress','Quarter','Deliverable Description'])
          line_count += 1
        else:
          if checkType2019(row[4]) == 'Login':
            filewriter.writerow(
              [row[0], row[1], 'Login', row[3], '2019', '', '', '', '', '', '', '', '', '', '', '', ''])

          if checkType2019(row[4]) == 'Logout':
            filewriter.writerow(
              [row[0], row[1], 'Logout', row[3], '2019','', '', '', '', '', '', '', '', '', '', '', ''])

          if checkType2019(row[4]) == 'Insert User':
            filewriter.writerow(
              [row[0], row[1], 'Insert User', row[3], '2019','', '', '', '', '', '', '', '', '', '', '', ''])

          if checkType2019(row[4]) == 'Insert Learning Objective':
            words = (row[4].split(','))
            Title = row[1]
            Title = Title.replace(',', '').replace('\n', '').replace('\r', '')
            Description = words[11].replace(',', '').replace('\n', '').replace('\r', '')
            filewriter.writerow(
              [row[0], Title, 'Insert Learning Objective', row[3], '2019', row[2], '', words[7], words[8], words[9],
               words[10], Description, '', '', '', '', ''])

          if checkType2019(row[4]) == 'Insert Deliverable':
            words = (row[4].split(','))
            words2 = words[len(words) - 1].split(' ')

            if len(words2) > 2:
              words3 = words2[2].split('=')

            else:
              words3 = ['stuff', 'dID']
            filewriter.writerow(
              [row[0], row[1], 'Insert Deliverable', row[3],'2019', row[2], words3[1], '', '', '', '', '', words[5],
               words[6], words[len(words) - 2], words2[0], ''])

          if checkType2019(row[4]) == 'Update User':
            n = 1
            # NA for now

          if checkType2019(row[4]) == 'Update Learning Objective':
            words = (row[4].split('='))
            Title = words[2]
            Title = Title[:-5]
            Title = Title.replace(',', '').replace('\n', '').replace('\r', '')
            # Title=Title.replace('-','')
            Code = words[3]
            Code = Code[:-8]
            Blooms1 = words[4]
            Blooms1 = Blooms1[:-8]
            Blooms2 = words[5]
            Blooms2 = Blooms2[:-6]
            Description = words[7]
            print(Description)
            Description = Description[:-10]
            Description = Description.replace(',', '').replace('\n', '').replace('\r', '')
            filewriter.writerow(
              [row[0], row[1], 'Update Learning Objective', row[3], '2019',row[2], '', Title, Code, Blooms1,
               Blooms2, Description, '', '', '', '',''])

          if checkType2019(row[4]) == 'Update Deliverable':
            words = (row[4].split('='))
            Title = words[1]
            Title = Title[:-5]
            Title = Title.replace(',', '')
            Type = words[2]
            Type = Type[:-10]
            Completion = words[3]
            Completion = Completion[:-18]
            ExpectedCompletion = words[4]
            ExpectedCompletion = ExpectedCompletion[:-10]

            filewriter.writerow(
              [row[0], row[1], 'Update Deliverable', row[3], '2019', row[2], words[5], '', '', '', '', '', Title,
               Type, Completion, ExpectedCompletion, ''])

          if checkType2019(row[4]) == 'Delete User':
            n = 1
            # NA for now

          if checkType2019(row[4]) == 'Delete Learning Objective':
            words = (row[4].split(','))
            filewriter.writerow(
              [row[0], row[1], 'Delete Learning Objective', row[3], '2019', row[2], '', '', '', '', '', '', '', '',
               '', '', ''])

          if checkType2019(row[4]) == 'Delete Deliverable':
            words = (row[4].split(','))
            dID = (row[4].split('='))
            dID = dID[1]
            filewriter.writerow(
              [row[0], row[1], 'Delete Deliverable', row[3], '2019',row[2], dID, '', '', '', '', '', '', '', '', '',
               ''])
          line_count += 1

    return (filewriter)


def dateToNum(date):
  from datetime import datetime
  a = datetime(2019, 8, 29).timestamp()
  b = datetime.fromisoformat(date).timestamp()
  delta = b - a
  return (delta)


def makeWordChart(processedLog,listOfStudents):
  import csv
  import numpy as np
  line_count=0
  wordChart=['Number','Time','Text']
  with open(processedLog,  encoding="utf8") as csv_file:
    csvToRead = csv.reader(csv_file, delimiter=',')
    for row in csvToRead:
      try:
        if (row[0] in (None, "")):
          pass
        elif (row[1] in listOfStudents):
          newrow=[row[1],row[3],row[6]+' '+row[7]+' '+row[10]]
          wordChart=np.vstack([wordChart,newrow])
        else:
          pass
        line_count += 1
      except:
        pass

    print(wordChart)
  return(wordChart)
  #Figure out what students are in the list. Don't add the piece of text if they aren't in it.