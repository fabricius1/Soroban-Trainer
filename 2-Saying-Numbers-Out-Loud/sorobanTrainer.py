from gtts import gTTS
import os
import random
import time

dict = {
    "plus": ["plus", "mais"],
    "minus": ["minus", "menos"],
    "Result?": ["Result?", "Resultado?"],
    "What is the total?": ["What is the total?", "Qual é o total?"],
    "You are correct.": ["You are correct.", "Você acertou."],
    "Congratulations!": ["Congratulations!", "Parabéns!"],
    "You are wrong.": ["You are wrong.", "Você errou."],
    "Partial results:": ["Partial results:", "Resultados parciais:"]
}


def translate_str(string, language):
    if language == 'pt':
        return dict[string][1]
    return dict[string][0]


def new_number(minimum, maximum, language):
    """Generate a random number and choose one of the two 
    operations (sum or subtraction).
    Return a tuple with the following types: int, str, int
    """
    n = random.randint(minimum, maximum)
    sign = random.randint(1, 2)
    total = 0

    # make the number positive
    if sign == 1:
        print_sign = translate_str("plus", language)
        total += n
    # make the number negative
    else:
        print_sign = translate_str("minus", language)
        total -= n

    return total, print_sign, n


def play_audios(selected_numbers, seconds, language):
    files = []
    for i in range(len(selected_numbers)):
        myobj = gTTS(text=selected_numbers[i], lang=language, slow=False)
        i_string = str(i)
        file = f"{str(0)*(4-len(i_string))}{int(i+1)}.mp3"
        myobj.save(file)
        files.append(file)

    for file in files:
        os.system("mpg321 " + file)
        time.sleep(seconds)
        os.remove(file)


def play_game(number_quantity, minimum, maximum, seconds, language):
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
        last_result, print_sign, n = new_number(minimum, maximum, language)
        total += last_result

        # if the chosen number makes the total either lesser than 0 or
        # greater than 9, it throws out this number and chooses
        # another one
        while total < 0 or total > maximum:
            total -= last_result
            last_result, print_sign, n = new_number(minimum, maximum, language)
            total += last_result

        # append the final number, with its sign, to the list
        selected_numbers.append(f"{print_sign} {n}")
        if i != 0:
            partial_totals.append(str(total))

    selected_numbers.append(translate_str("Result?", language))

    # Say the numbers out loud to the user:
    play_audios(selected_numbers, seconds, language)

    # user gives the answer
    my_total = input(
        "\n\n" + translate_str("What is the total?", language) + " ")

    # compare user's answer with total
    if int(my_total) == total:
        print("\n\n" + translate_str("You are correct.", language))
        print(translate_str("Congratulations!", language) + "\n\n")
    else:
        print("\n\n" + translate_str("You are wrong.", language))

    # print the formatted number sequence and total:
    final_display = ""
    final_display_one_line = ""
    final_display += f"{selected_numbers[0][3:]} {selected_numbers[1]} = {partial_totals[0]}\n"
    final_display_one_line += f"{selected_numbers[0]} {selected_numbers[1]}"
    for i in range(len(selected_numbers[2:-1])):
        final_display += f"{partial_totals[i]} {selected_numbers[i+2]} = {partial_totals[i+1]}\n"
        final_display_one_line += f" {selected_numbers[i+2]}"

    final_display = final_display.replace(translate_str(
        "minus", language), "-").replace(translate_str("plus", language), "+")
    final_display_one_line = final_display_one_line.replace(
        translate_str("minus", language), "-").replace(translate_str("plus", language), "+")
    print(
        f"{final_display_one_line} = \n\n\n"
        f"{translate_str('Partial results:', language)} "
        f"\n\n{final_display[2:]}\n")


if __name__ == '__main__':
    # game set up for:
    # 5 numbers
    # 9 is the maximum random number
    # 3 seconds intervals
    play_game(10, 1, 9, 3, "en")
