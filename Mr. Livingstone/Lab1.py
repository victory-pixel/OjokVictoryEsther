total = 0
count = 0

while count < 5:
    number = float(input("Enter a number: "))
    total += number
    count += 1
    average = total / count
    print("Average is: ", average)