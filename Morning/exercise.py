secret = int(input("Guess a number between 1 and 10: "))
attempts = 0
while attempts < 3:
    guess = int(input("Enter your guess: "))
    attempts += 1
if guess == secret:
    print("Congratulations! You guessed the CORRECT number.")
else:
    print("Sorry, that's not correct. Try again.")

if guess !=secret:
    print("Game Over! The correct number was:", secret)