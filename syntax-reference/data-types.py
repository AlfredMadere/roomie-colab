#README
#How to use this file: 
#select the lines you want to run, then right click and select "run in interactive window" It will ask you if you want to install jupyter notebook, say yes
#you'll then be able to highlight random lines of code and run them independently and see how their outputs look
#Jupyter notebook is super powerful and I have lowkey no idea how to use it (I know you can create whole files of shit with independent code blocks kinda like google colab)
######################################################################################################################################################################################

#STRINGS

s = "hello world" 
print(type(s)) # str

#NUMERIC - INT, FLOAT, COMPLEX
i = 20
print(type(i)) # int

f = 20.5
print(type(f)) # float

c = 1j
print(type(c)) # complex

#SEQUENCE TYPES - LIST, TUPLE, RANGE

#read these docs on tuples, they are kinda weird DOCS: https://www.geeksforgeeks.org/tuples-in-python/
#the most common use case for tuples that I have seen is to pass parameters to functions 

#an array in javascript is a list in python
l = ["miles", "has", "a", "fat", "ass"]
ml = [1, 4, "miles", 6, 3.2]
print(type(l)) #list

#tuple shit
t = ("what", "the", "fuck", "is", "this")
print(type(t)) #tuple 

# An empty tuple
empty_tuple = ()
print (empty_tuple)

# An empty tuple
empty_tuple = ()
print (empty_tuple)

#concatenating 2 tuples

tuple1 = (0, 1, 2, 3)
tuple2 = ('foo', 'bar')
print(tuple1 + tuple2) #(0, 1, 2, 3, 'python', 'geek')

# Code for creating nested tuples

tuple1 = (0, 1, 2, 3)
tuple2 = ('python', 'geek')
tuple3 = (tuple1, tuple2)
print(tuple3) #((0, 1, 2, 3), ('python', 'geek'))

#Check out the documentation I linked for more examples




r = range(6) # need to do some research on this
print(type(r)) #range


#MAPPING TYPE - DICT (basically the same thing as an object literal or hash in javascript)
d = {"Name": "Miles Herrman", "Inseam Length": "very short"}
cd = {"thing in string": 2, "another string": 1.44, 1: "maybe", "list": [2, 4, 5]} #more complicated, shows you can have different data types and stuff
print(type(d)) #dict

#SET TYPES: SET, FROZENSET
setaroo = {"a", "set", "of", "things"}
print(type(setaroo)) 

#BOOLEAN TYPE - BOOL
b = True
print(type(b)) #bool

#BINARY TYPES - BYTES, BYTEARRAY, MEMORYVIEW