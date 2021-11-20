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
l = ["miles", "has", "a", "fat", "ass"]
ml = [1, 4, "miles", 6, 3.2]
print(type(l)) #list

t = ("what", "the", "fuck", "is", "this")
print(type(t)) #tuple 

r = range(6) # need to do some research on this
print(type(r)) #range


#MAPPING TYPE - DICT (basically the same thing as an object literal or hash in javascript)
d = {"Name": "Miles Herrman", "Inseam Length": "very short"}
cd = {"thing in string": 2, "another string": 1.44, 1: "maybe", "list": [2, 4, 5]} #more complicated, shows you can have different data types and stuff
print(type(d)) #dict

#SET TYPES: SET, FROZENSET
setaroo = {"a", "set", "of", "things"}
print(type(m)) 

#BOOLEAN TYPE - BOOL
b = True
print(type(b)) #bool

#BINARY TYPES - BYTES, BYTEARRAY, MEMORYVIEW