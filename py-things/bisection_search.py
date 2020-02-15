
N = int(input("Enter an integer number: "))
unknown = int(input("Enter the number to guess: "))

low = 0
high = N
guess = (low + high)/2
k = 0
while guess != unknown:
    k += 1
    if guess < unknown:
        low = guess
    else:
        high = guess
    guess = (low + high)/2

print("The guess number is close to", guess)
print("%d number of guesses" % k)

