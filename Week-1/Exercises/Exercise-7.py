"""
Have a look at the script called 'human-guess-a-number.py' (in the same folder as this one).

Your task is to invert it: You should think of a number between 1 and 100, and the computer 
should be programmed to keep guessing at it until it finds the number you are thinking of.

At every step, add comments reflecting the logic of what the particular line of code is (supposed 
to be) doing. 
"""

#Suppose you have already chosen a number beforehand

#The computer will suggest 50 at first : it will perform a binary search to find the correct number
guess = 50
win = False

#at first all numbers between 0 and 100 are possible: the binary search is between 0 and 100
current_max = 100
current_min = 0

print("Current guess: ", guess)
while win != True: 
    response = input("""Please answer : "Win" / "Too high" / "Too low" \n""")
    
    print()

    if "high" in response.casefold():
        #We know that the guess is too high: we update current_max to guess and 
        #we continue the binary search between current_min and current_max
        current_max = guess 
        guess = (guess + current_min) // 2

    elif "low" in response.casefold():
        #We know that the guess is too low: we update current_min to guess and 
        #we continue the binary search between current_min and current_max
        current_min = guess 
        guess = (guess + current_max) // 2

    elif "win" in response.casefold():
        #The computer has found the number, we can stop the search
        win = True 
        print("The computer found the number!")
        exit()

    else:
        print("Invalid answer")

    print("Current guess: ", guess)