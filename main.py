#! /usr/bin/env python3

import csv


def read_csv(filename):
    item_list = []
    with open(filename) as file:
        for row in csv.reader(file):
            item_list.append(row)
    return item_list


def build_parsing_table(parse_list):
    parsing_table = {}
    inputs = parse_list[0][1:]
    for rule in parse_list[1:]:
        for index, current_input in enumerate(rule[1:]):
            parsing_table[rule[0] + inputs[index]] = current_input
    return parsing_table


def stack_implementation(input_string):
    stack_table = []
    parsing_table = build_parsing_table(read_csv("predictive_parsing_table.csv"))
    stack = "$" + list(parsing_table.keys())[0][0]
    stack_table.append([stack, input_string, ""])
    while stack != "$":
        if stack[-1] == input_string[0]:
            stack = stack[:-1]
            input_string = input_string[1:]
            stack_table.append([stack, input_string, ""])
        elif parsing_table[stack[-1] + input_string[0]] == "É›":
            stack_table.append([stack[:-1], input_string, stack[-1] + "→" + "ɛ"])
            stack = stack[:-1]
        elif stack[-1] + input_string[0] in parsing_table:
            curr = stack[-1]
            stack = stack[:-1] + parsing_table[stack[-1] + input_string[0]][::-1]
            stack_table.append([stack, input_string, curr + "→" + parsing_table[curr + input_string[0]]])
        else:
            break
    return stack_table


def main():
    input_string = "(a+a)$"
    stack_table = stack_implementation(input_string)
    print(f"{'Stack':15}{'Input':15}Output")
    for row in stack_table:
        print(f"{row[0]:15}{row[1]:15}{row[2]}")
    if stack_table[-1][0] == "$" and stack_table[-1][1] == "$":
        print("\nString is accepted/valid.")
    else:
        print("\nString is not accepted/invalid.")


if __name__ == "__main__":
    main()
