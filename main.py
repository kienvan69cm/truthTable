from itertools import product
OPERATORS = set(['~', '&', '|', '=', '>', '(', ')'])  # set of operators
PRIORITY = {'=': 0, '>': 1, '|': 2, '&': 3,
            '~': 4}  # dictionary having priorities


def infix_to_postfix(expression):  # input expression
    stack = []  # initially stack empty
    output = ''  # initially output empty
    for ch in expression:
        if ch not in OPERATORS:  # if an operand then put it directly in postfix expression
            output += ch
        elif ch == '(':  # else operators should be put in stack
            stack.append('(')
        elif ch == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop()
        else:
            # lesser priority can't be on top on higher or equal priority
            # so pop and put in output
            while stack and stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[stack[-1]]:
                output += stack.pop()
            stack.append(ch)
    while stack:
        output += stack.pop()
    return output


def eval_postfix(postfix, dictVal):
    stack = []
    ansLine = []
    for ch in postfix:
        plus = None
        if ch == "&":
            plus = stack.pop() & stack.pop()
        elif ch == "|":
            plus = stack.pop() | stack.pop()
        elif ch == '~':
            plus = (not(stack.pop()))
        elif ch == '>':
            plus = stack.pop() | (not(stack.pop()))
        elif (ch not in OPERATORS):
            stack.append(dictVal[ch])
        if plus is not None:
            stack.append(plus)
            ansLine.append(plus)
    ansLine.append(stack.pop())
    return ansLine


def truthTable(postfix):
    table = []
    listVar = []
    dictVal = {}
    for ch in postfix:
        if ch not in OPERATORS and ch not in listVar:
            listVar.append(ch)
    listVar.sort()
    numOfVar = len(listVar)
    lines = list(product((True, False), repeat=numOfVar))
    lines.reverse()
    for line in lines:
        tableLine = []
        for i in range(numOfVar):
            dictVal[listVar[i]] = line[i]
            tableLine.append(line[i])
        tableLine += eval_postfix(postfix, dictVal)
        table.append(tableLine)
    return table


def writeTruthtable(table):
    import sys
    outfile = sys.argv[0]
    outfile = outfile[0:-2]
    outfile += "txt"
    with open(outfile, 'w') as f:
        for lines in table:
            for item in lines:
                f.write("%s\t" % item)
            f.write("\n")
    f.close()


def main():
    infix = input('Enter infix expression: ')
    print('infix expression: ', infix)
    postfix = infix_to_postfix(infix)
    print('postfix expression: ', postfix)
    table = truthTable(postfix)
    writeTruthtable(table)


main()
