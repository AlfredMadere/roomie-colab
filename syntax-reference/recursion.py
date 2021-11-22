#Recursion - a defined function that calls itslef 
#beneficial for looping through data to find a result
#also used to traverse tree-like data
#recursion often uses more memory/is slower than other functions
#be careful not to create a function that never terminates

def rec(r):
    if(r>0):
        result = r + rec(r-1)
        print(result)
    else:
        result = 0
    return result

print("\n Example of recursion \n")
rec(5)
print()

#Python has a set recursion limit of 1000,
#which can be changed with function setrecursionlimit(___)
#returning nothing will terminate recursion

#Common example is finding the factorial of an integer

print("\n Example of Using Recursion for Factorials \n")
def factorial(x):
    if x <= 1:
        return 1
    else:
        return (x * factorial(x-1))
num = 3
print("The factorial of", num, "is", factorial(num))
print()