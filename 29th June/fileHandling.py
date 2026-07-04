#Reading a file
'''
file= open("student.txt", "r")
content = file.read()

print(content)
file.close()
'''
'''
with open('student.txt', 'r') as file:
    data = file.read()
print(data)

'''

#reading line by line
'''
with open('student.txt', 'r') as file:
   # Read one line at a go
   for line in file:
     print(line.strip())
     '''
#Exercise 1: Write a file with the content 'I love python programming'in the first line,
#'I am becoming a data scientist, second line, save your file as report.txt

'''
with open('report.txt','w') as file:
    file.write("I love python programming \n")
    file.write("I am becoming a data scientist \n")
'''

#Appending text
'''
with open("report.txt", "a") as file:
    file.write("Every data scientist  must learn python\n")

with open('report.txt','r') as file:
    data = file.read()
print(data)
'''

#Reading a CSV file
#import csv
#open the csv file
'''
with open('students.csv', 'r') as file:
    reader = csv.reader(file)
    #loop through each row
    for row in reader:
        print(row)
        '''


#Exercise 2: Add your reg no, name, gender, age, course, score to the student csv file using a dictionary csv writer


#JSON  processing - javascript object notation


#Exception Handling
'''
File not found
Invalid input
index out of range

'''