from gtts import gTTS
import os
import random
import time


def new_number(maximum):
    """Generate a random number and choose one of the two 
    operations (sum or subtraction).
    Return a tuple with the following types: int, str, int
    """
    n = random.randint(1, maximum)
    sign = random.randint(1, 2)
    total = 0

    # make the number positive
    if sign == 1:
        print_sign = "mais"
        total += n
    # make the number negative
    else:
        print_sign = "menos"
        total -= n

    return total, print_sign, n


def play_audios(selected_numbers, seconds):
    files = []
    for i in range(len(selected_numbers)):
        myobj = gTTS(text=selected_numbers[i], lang='pt', slow=False)
        i_string = str(i)
        file = f"{str(0)*(4-len(i_string))}{int(i+1)}.mp3"
        myobj.save(file)
        files.append(file)

    for file in files:
        os.system("mpg321 " + file)
        time.sleep(seconds)
        os.remove(file)


def play_game(number_quantity, maximum, seconds):
    """Play the game. Parameters are all int:
        - number_quantity: how many numbers will be displayed
        - maximum: set the maximum number to be selected at every turn
        - seconds: interval between each number display

       Return: None
    """
    total = 0
    selected_numbers = []

    for i in range(number_quantity):
        # first number choice for the current round i
        last_result = 0
        last_result, print_sign, n = new_number(maximum)
        total += last_result

        # if the chosen number makes the total either lesser than 0 or
        # greater than 9, it throws out this number and chooses
        # another one
        while total < 0 or total > maximum:
            total -= last_result
            last_result, print_sign, n = new_number(maximum)
            total += last_result

        # append the final number, with its sign, to the list
        selected_numbers.append(f"{print_sign} {n}")

    selected_numbers.append("Result?")

    # Say the numbers out loud to the user:
    play_audios(selected_numbers, seconds)

    # user gives the answer
    my_total = input("\n\nWhat is the total?  ")

    # compare user's answer with total
    if int(my_total) == total:
        print("\n\nYou are correct.")
        print("Congratulations! \n\n")
    else:
        print("\n\nYou are wrong.")
        print("Correct total: ", total, "\n\n")


if __name__ == '__main__':
    # game set up for:
    # 5 numbers
    # 9 is the maximum random number
    # 3 seconds intervals
    play_game(5, 9, 3)
