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
    for ch in postfix:
        plus = None
        if ch.strip() == '':
            continue
        elif ch == "&":
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
            if ch != postfix[-1]:
                print(plus, end=',')
    return stack.pop()


def truthTable(postfix):
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
        for i in range(numOfVar):
            dictVal[listVar[i]] = line[i]
            print(line[i], end=",")
        print(eval_postfix(postfix, dictVal), end=";")


infix = input('Enter infix expression: ')
print('infix expression: ', infix)
postfix = infix_to_postfix(infix)
print('postfix expression: ', postfix)
truthTable(postfix)
