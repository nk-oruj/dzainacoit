import random
import csv

letters = 'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփք'
handsets = []

letters_total_amount = len(letters)
letters_half_amount = letters_total_amount // 2

handset_total_amount = 100
handset_half_amount = handset_total_amount // 2
iteration_amount = 1000
digraph_check_amount = 100
mutation_percent = 75
mutation_amount = (letters_half_amount * mutation_percent) // 100 

monograph_list_reader = csv.reader(open('./statistics/monographs/total_list_no_o_f.csv', mode='r', encoding='utf-8'))
next(monograph_list_reader, None) 

monograph_list = dict((rows[0],int(rows[1])) for rows in monograph_list_reader)

print(monograph_list)

digraph_list_reader = csv.reader(open('./statistics/digraphs/total_list_no_o_f.csv', mode='r', encoding='utf-8'))
next(digraph_list_reader, None) 

digraph_list = [[rows[0], int(rows[1])] for rows in digraph_list_reader]
digraph_list_length = len(digraph_list)
digraph_list_max_fitness = 0

for i in range(0, digraph_list_length):
    digraph_list_max_fitness += digraph_list[i][1]

for i in range(handset_total_amount):
    letters_shuffled = ''.join(random.sample(letters, len(letters)))

    first_hand = letters_shuffled[:letters_half_amount]
    second_hand = letters_shuffled[letters_half_amount:]

    handsets.append({"first_hand": first_hand, "second_hand": second_hand, "fitness": 0.0})


for i in range(iteration_amount):
    for j in range(handset_total_amount):
        handsets[j]['fitness'] = 0.0

        handset = handsets[j]
        first_hand = handset['first_hand']
        second_hand = handset['second_hand']

        first_hand = ''.join(sorted(first_hand, key=lambda letter: monograph_list[letter], reverse=True))
        second_hand = ''.join(sorted(second_hand, key=lambda letter: monograph_list[letter], reverse=True))
        
        handsets[j]['first_hand'] = first_hand
        handsets[j]['second_hand'] = second_hand

        for k in range(digraph_list_length):

            digraph = digraph_list[k]

            first_letter = digraph[0][0]
            second_letter = digraph[0][1]

            digraph_weight = digraph[1]

            first_letter_hand = 0 if first_letter in first_hand else 1
            second_letter_hand = 0 if second_letter in first_hand else 1

            if first_letter_hand != second_letter_hand:
                handsets[j]['fitness'] += digraph_weight

        handsets[j]['fitness'] /= digraph_list_max_fitness

    handsets.sort(key=lambda handset: handset['fitness'], reverse=True)
    handsets = handsets[:handset_half_amount]

    print(str(i) + " " + str(len(handsets)))
    print(handsets[0])

    for j in range(handset_half_amount):
        parent_handset = handsets[j]
        first_hand = parent_handset['first_hand']
        second_hand = parent_handset['second_hand']

        first_hand_random_indexes = random.sample(range(len(first_hand)), mutation_amount)
        second_hand_random_indexes = random.sample(range(len(second_hand)), mutation_amount)

        mut = (letters_half_amount * random.randint(1, letters_half_amount)) // 100 

        for k in range(mut):
            first_index = first_hand_random_indexes[k]
            second_index = second_hand_random_indexes[k]

            first_letter = first_hand[first_index]
            second_letter = second_hand[second_index]

            first_hand = first_hand[:first_index] + second_letter + first_hand[first_index + 1:]
            second_hand = second_hand[:second_index] + first_letter + second_hand[second_index + 1:]

        handsets.append({"first_hand": first_hand, "second_hand": second_hand, "fitness": 0.0})

    # print(handsets)