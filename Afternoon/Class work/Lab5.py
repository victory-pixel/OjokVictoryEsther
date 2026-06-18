#1Advanced Functions
#2Lambda functions
'''
Small annonymous functions that have any number of arguments but only one expression. 
They're defined by the keyword Lambda.
Syntax:
Lambda arguments: expression

Key X-tics
1. no name
2. single expression
3.Can be used where function objects are required
'''
#Example:
#Simple Lambda function
#square = lambda x:x*x
# print(square(5))

'''
#Lambda Vs Traditional function
def add(x,y):
    return x+y
print(add(3,4))

add_lambda = lambda x,y:x+y
print(add_lambda(3,4))
'''
#Exercise 1 : Lamda function to check if value is even.
even = lambda x: x%2 == 0
print(even(4))
print(even(5))


#Example 2: Lambda function with filter()
numbers = [1,2,3,4,5,6,7,8,9]
even_numbers = list(filter(lambda x: x%2==0, numbers))
print(even_numbers)

#filter number greater than 20
less= list(filter(lambda x: x<5, numbers))
print(less)

#Example 3m: Using Lambda with sorted()
Fruit=['Cherry', 'banana', 'date', 'apple', 'Mango','Dragonfruit']
#Arrange using length of words
arrange = Fruit.sort(key = lambda x:len(x))
print(Fruit)


'''
#3. Recursive functions
Recurssion is a function that calls itself to solve
 a problem by breaking it down into smaller subproblems
 Components
 base case - condition that stops the recursion
 Recursive case - function that calls itself with a smaller function
'''
#Eg: Factorial calculation
#in plain text: 5! = 5x4x3x2x1 Output:120
#in python
#Mtd 1
def factorial(n):
    #Base case
    if n<=1:
        return 1
    #recursive case
    else:
        return n*factorial(n-1)
print(factorial(6))

#Mtd 2
def factorial(n):
    if n==1:
        return 1
    return n*factorial(n-1)
print(factorial(6))

#countdown
def count_down(n):
    if n==0:
        print("Done")
    else:
        print(n)
        count_down(n-1)
count_down(10)

#Exercise 2 : Using fibonacci sequence, get the first 10 fibonacci number in the range of 10
def fibonacci(n):
    if n==0:
        return 0
    if n==1:
        return 1
    return (n-1) + (n-2)
print(fibonacci(10))

#4Built-in functions
#5Function - based project
