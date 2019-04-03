s = '1+2*3-(1+2)'#(1+2)*3

def calculate(s):
    stack = []
    pre_op = '+'
    num = 0
    for i, each in enumerate(s):
        if each.isdigit():
            num = 10 * num + int(each)
        print(num)
        if i == len(s) - 1 or each in '+-*/':
            if pre_op == '+':
                stack.append(num)
            elif pre_op == '-':
                stack.append(-num)
            elif pre_op == '*':
                stack.append(stack.pop() * num)
            elif pre_op == '/':
                top = stack.pop()
                if top < 0:
                    stack.append(int(top / num))
                else:
                    stack.append(top // num)
            pre_op = each
            num = 0
    print(stack)
    return sum(stack)

print(calculate(s))
stack_op = []
stack_num = []
#  + - * ( )
# op_order = ['#','+','-','*','(']  1代表进栈
level = [[0,1,1,1,1,0],[0,0,0,1,1,0],[0,0,0,1,1,0],[0,0,0,0,1,0],[0,1,1,1,1,0]]
stack_op.append('#')                                     #*

def get_op_order(top):
    if top == '#':
        op_order = 0
    elif top == '+':
        op_order = 1
    elif top == '-':
        op_order = 2
    elif top == '*':
        op_order = 3
    elif top == '(':
        op_order = 4
    elif top == ')':
        op_order = 5
    return op_order

for i in range(len(s)):
    if s[i] >= '0' and s[i] <= '9':
        stack_num.append(int(s[i]))
        continue
    top = stack_op[-1]
    top_order = get_op_order(top)
    now_order = get_op_order(s[i])
    if level[top_order][now_order] == 1:
        stack_op.append(s[i])
    else:#应该出战
        if s[i] == ')':
            while(stack_op[-1] != '('):
                num_2 = stack_num.pop()
                num_1 = stack_num.pop()
                top = stack_op.pop()

                if top == '+':
                    stack_num.append(num_1+num_2)
                elif top == '-':
                    stack_num.append(num_1 - num_2)
                elif top == '*':
                    stack_num.append(num_1 * num_2)
                elif top == '(':
                    pass
                # print(')))))', stack_op, stack_num)
        else:
            num_2 = stack_num.pop()
            num_1 = stack_num.pop()
            stack_op.pop()
            if top == '#':
                pass
                # print(stack_num.pop())
            elif top == '+':
                stack_num.append(num_1 + num_2)

            elif top == '-':
                stack_num.append(num_1 - num_2)
            elif top == '*':
                stack_num.append(num_1 * num_2)
            elif top == '(':
                pass
        stack_op.append(s[i])
        if len(stack_op) > 2 and stack_op[-1] == ')' and stack_op[-2] == '(':
            stack_op.pop()
            stack_op.pop()
# print(stack_op,stack_num)
# print(stack_op,stack_num)
# print('!!!!!!!!!!!')
while len(stack_num) > 2:
    # print(stack_op,stack_num)
    top = stack_op[-1]
    stack_op.pop()
    num_2 = stack_num.pop()
    num_1 = stack_num.pop()
    if top == '+':
        stack_num.append(num_1 + num_2)
    elif top == '-':
        stack_num.append(num_1 - num_2)
    elif top == '*':
        stack_num.append(num_1 * num_2)

top = stack_op[-1]
num_2 = stack_num.pop()
num_1 = stack_num.pop()
# print('########')
if top == '+':
   print(num_1+num_2)
elif top == '-':
    print(num_1 - num_2)
elif top == '*':
    print(num_1 * num_2)




