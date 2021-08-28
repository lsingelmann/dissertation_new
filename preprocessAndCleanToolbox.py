def importCSV(filenameIn,delimiter):
  import csv
  with open(filenameIn) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=delimiter)
    return(csv_reader)

def getStudentNumbers(filenameIn,delimiter):
 import csv
 with open(filenameIn) as csv_file:
         csvToRead = csv.reader(csv_file, delimiter=',')
         listOfStudents=[]
         for row in csvToRead:
             listOfStudents.append(row[0])
 return(listOfStudents)