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
        print_sign = "+"
        total += n
    # make the number negative
    else:
        print_sign = "-"
        total -= n

    return total, print_sign, n


def play_game(number_quantity, maximum, seconds):
    """Play the game. Parameters are:
        - number_quantity (int): how many numbers will be displayed
        - maximum (int): set the maximum number to be selected at every turn
        - seconds (float or int): interval between each number display

       Return: None
    """
    total = 0
    selected_numbers = []
    partial_totals = []

    for i in range(number_quantity):
        # first number choice for the current round i
        last_result = 0
        last_result, print_sign, n = new_number(maximum)
        total += last_result

        # if the chosen number makes the total either lesser than 0 or
        # greater than the maximum, it throws out this number and chooses
        # another one
        while total < 0 or total > maximum:
            total -= last_result
            last_result, print_sign, n = new_number(maximum)
            total += last_result

        # append the final number, with its sign, to the list
        selected_numbers.append(f"{print_sign} {n}")
        if i != 0:
            partial_totals.append(str(total))

    # Show the selected numbers to the user
    for item in selected_numbers:
        print(item)
        time.sleep(seconds)

    # user gives the answer
    my_total = input("\n\nResult?  ")

    # compare user's answer with total
    if int(my_total) == total:
        print("\n\nYou are correct.")
        print("Congratulations! \n\n")
    else:
        print("\n\nYou are wrong.")

    # print the formatted number sequence and total:
    final_display = ""
    final_display_one_line = ""
    final_display += f"{selected_numbers[0]} {selected_numbers[1]} = {partial_totals[0]}\n"
    final_display_one_line += f"{selected_numbers[0]} {selected_numbers[1]}"
    for i in range(len(selected_numbers[2:])):
        final_display += f"{partial_totals[i]} {selected_numbers[i+2]} = {partial_totals[i+1]}\n"
        final_display_one_line += f" {selected_numbers[i+2]}"

    print(
        f"{final_display_one_line} = \n\n\nPartial results:\n\n{final_display[2:]}\n")


if __name__ == '__main__':
    # game set up for:
    # 5 numbers
    # 9 is the maximum random number
    # 3 seconds intervals
    play_game(5, 9, 0.1)
