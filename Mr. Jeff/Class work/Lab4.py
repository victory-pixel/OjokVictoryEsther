#Functions
#Syntax
#def function_name(parameters):
#    #function body 
#return value
#Built-in functions
#len() - returns length of an object
#print() - prints the value of an object
#type() - returns the type of an object
#input() - reads input from the user
#range() - returns a sequence of numbers often used in for loops

#components of a function
#1. Function Name: A descriptive name that indicates what the function does.
#2. Parameters: Variables that the function can accept as input to perform its task.
#3. Function Body: The block of code that defines what the function does with the parameters.
#4. Return Statement: (Optional) A statement that specifies the value to be returned by the function after execution.
#5. Indentation: The function body must be indented to indicate that it belongs to the function definition.
 #eg
#def greet():
    #print("Hello, welcome to Python programming!")
#greet()  # Calling the function to execute its code

#Exercise 1: Area of a rectangle



#def calculate_area_of_rectangle(length, width):
 #   area = length * width
 #   return area

#length = float(input("Enter the length of the rectangle: "))
#width = float(input("Enter the width of the rectangle: "))
#area = calculate_area_of_rectangle(length, width)
#print(f"The area of the rectangle is: {area}")


#Parameters vs Arguments
#Parameters are the variables defined in the function definition that act as placeholders for the values that will
#eg
#def greet_user(name):  # 'name' is a parameter
  #  print(f"Hello, {name}! Welcome to Python programming!")

#Arguments
#are the actual values passed to the function when it is called. 
#Eg
#greet_user("Alice")  # "Alice" is an argument

#Exercise 2
# Name = input("Enter your name: ")
#Age = int(input("Enter your age: "))
#Course = input("Enter your course: ")
#student_no = input("Enter your student number: ")
#def display_student_info(name, age, course, student_no):
 #   print(f"\nStudent Information:\nName: {name}\nAge: {age}\nCourse: {course}\nStudent Number: {student_no}")
#display_student_info(Name, Age, Course, student_no)


#Exercise 3
#Create a function that calcs the area of a circle

#Exercise 4
#Write a program demonstrating the difference between local and global varables

#assignment
#Create a menu driven calc GUI using functions for addition, subtractionn, multiplication and divition.
