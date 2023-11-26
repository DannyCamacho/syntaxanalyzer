#! /usr/bin/env python3

import csv  # import csv to convert predictive parsing table to list


def read_csv(filename):  # read_csv(): read a .csv file and convert contents into a list
    item_list = []  # list used to store contents of .csv file
    with open(filename) as file:  # open file for reading
        for row in csv.reader(file):  # for loop to access each row of file
            item_list.append(row)  # append row to end of list
    return item_list  # return list to caller


def build_parsing_table(parse_list):  # build_parsing_table(): build a dictionary from parsing table list
    parsing_table = {}  # dictionary to store parsing table
    inputs = parse_list[0][1:]  # take first row of parst_list (inputs)
    for rule in parse_list[1:]:  # for loop to access each rule in parse_list
        for index, current_input in enumerate(rule[1:]):  # for loop to access each rule for each input
            parsing_table[rule[0] + inputs[index]] = current_input  # add rule to dictionary
    return parsing_table  # return dictionary to caller


def stack_implementation(input_string):  # stack_implementation(): determine if input is valid using parsing table
    stack_table = []  # list to store stack table
    parsing_table = build_parsing_table(read_csv("predictive_parsing_table.csv"))  # build parsing table from .csv file
    stack = "$" + list(parsing_table.keys())[0][0]  # create stack using "$" and starting symbol from parsing table
    stack_table.append([stack, input_string, ""])  # append start of stack to stack table
    while stack != "$":  # while loop to reach end of stack ($) if input is valid
        if stack[-1] + input_string[0] in parsing_table:  # check if parsing table has rule for current combination
            if parsing_table[stack[-1] + input_string[0]] == "É›":  # if epsilon is the rule for combination
                stack_table.append([stack[:-1], input_string, stack[-1] + "→" + "ɛ"])  # perform epsilon operation
                stack = stack[:-1]  # remove last element of stack
            else:  # otherwise use standard rule operation
                stack_table.append([stack, input_string, stack[-1] + "→" + parsing_table[stack[-1] + input_string[0]]])
                stack = stack[:-1] + parsing_table[stack[-1] + input_string[0]][::-1]  # shift input to stack
        elif stack[-1] == input_string[0]:  # else if the current stack and input symbols match
            stack = stack[:-1]  # remove current stack symbol
            input_string = input_string[1:]  # remove current input symbol
            stack_table.append([stack, input_string, ""])  # append updated stack table and input string to table
        else:  # else input string is invalid
            break  # break out of loop
    print(f"{'Stack':15}{'Input':15}Output")
    for row in stack_table:
        print(f"{row[0]:15}{row[1]:15}{row[2]}")
    result = "accepted/valid" if stack == "$" and input_string == "$" else "not accepted/invalid"
    print(f"\nString is {result}.")


def main():
    input_string = "a+(a+a)$"
    stack_implementation(input_string)


if __name__ == "__main__":
    main()
