#                        _____   ____     ___    ____    _____   _  _   
#                       |___ /  | ___|   / _ \  |___ \  |___ /  | || |  
#                         |_ \  |___ \  | | | |   __) |   |_ \  | || |_ 
#                        ___) |  ___) | | |_| |  / __/   ___) | |__   _|
#                       |____/  |____/   \___/  |_____| |____/     |_|  
#
# 　　　苦　　　苦　　　　　　　　　　命　　　　　　　　鸳鸳鸳鸳　鸳鸳鸳鸳鸳　　　　　　　鸯
# 苦苦苦苦苦苦苦苦苦苦苦　　　　　　命　命　　　　　　鸳　　　鸳　鸳　　　鸳　　　鸯鸯鸯鸯鸯鸯鸯鸯鸯
# 　　　苦　　　苦　　　　　　　命命　　　命命　　　　　鸳鸳　鸳　鸳　鸳鸳鸳　　　鸯　　　鸯　　　鸯
# 　　　　　苦　　　　　　　命命　命命命命命　命命　　　　　鸳　　鸳　　　　　　鸯鸯鸯鸯鸯鸯鸯鸯鸯鸯鸯
# 苦苦苦苦苦苦苦苦苦苦苦　　　　　　　　　　　　　　　鸳鸳鸳　　　鸳鸳鸳鸳鸳　　　鸯　　　鸯　　　鸯
# 　　　　　苦　　　　　　　　命命命命　命命命命　　　　　　　鸳　　　　　　　　鸯　鸯鸯鸯鸯鸯鸯鸯　鸯
# 　　　　　苦　　　　　　　　命　　命　命　　命　　　　鸳鸳鸳鸳鸳鸳鸳鸳鸳　　　　　鸯　鸯　　　鸯
# 　苦苦苦苦苦苦苦苦苦　　　　命　　命　命　　命　　　　鸳　　　鸳　　　鸳　　　　　鸯　　鸯　　鸯
# 　苦　　　　　　　苦　　　　命　　命　命　　命　　　　鸳鸳鸳鸳鸳鸳鸳鸳鸳鸳　　　　鸯鸯鸯鸯鸯鸯鸯鸯
# 　苦　　　　　　　苦　　　　命命命命　命　命命　　　　　　　　　　　　　鸳　　　　　　　　　　　鸯
# 　苦苦苦苦苦苦苦苦苦　　　　　　　　　命　　　　　　鸳鸳鸳鸳鸳鸳鸳　鸳鸳鸳　　　鸯鸯鸯鸯鸯　鸯鸯鸯
import math, random

elements = [3,5,0,2,3,4]
operations = ["+", "-", "*", "/"]
outputVal = {}

def quad(num: int) -> str:
    if num == 0:
        return "0"
    digits = []
    while num > 0:
        digits.append(str(num % 4))
        num //= 4
    
    return "".join(reversed(digits))

for i in range(4**5):
    command = ("00000"+quad(i))[-5:]
    expression = "3"
    for j in range(5):
        expression += operations[int(command[j])]
        expression += str(elements[j+1])
    try:
        expressionVal = eval(expression)
    except ZeroDivisionError:
        continue
    if isinstance(expressionVal, float) or expressionVal < 0:
        continue
    try:
        outputVal[expressionVal].append(expression)
    except KeyError:
        outputVal[expressionVal] = [expression]

choices = []
[choices.append(i) for i,j in outputVal.items()]
choices.sort()

def solution(choices, target):
    dp = [float('inf')] * (target + 1)
    dp[0] = 0
    num_used = [-1] * (target + 1)
    for num in choices:
        for i in range(num, target + 1):
            if dp[i - num] + 1 < dp[i]:
                dp[i] = dp[i - num] + 1
                num_used[i] = num
    if dp[target] == float('inf'):
        return []
    result = []
    while target > 0:
        result.append(num_used[target])
        target -= num_used[target]
    
    return result

print('                        _____   ____     ___    ____    _____   _  _   ')
print('                       |___ /  | ___|   / _ \\  |___ \\  |___ /  | || |  ')
print('                         |_ \\  |___ \\  | | | |   __) |   |_ \\  | || |_ ')
print('                        ___) |  ___) | | |_| |  / __/   ___) | |__   _|')
print('                       |____/  |____/   \\___/  |_____| |____/     |_|  ')
print()
output = ""
target = input("你可有话说？")
result = solution(choices, int(target))
for i in result:
    output += outputVal[i][random.randint(0,len(outputVal[i])-1)]
    output += "+"
print("你说的可是"+output[:-1]+"="+target)