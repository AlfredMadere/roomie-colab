#looping

# A programming structure that repeats a sequence of instructions until a specific condition is met. 

# Uses - cycle through values, sum numbers, repeat function, etc...

# Supported in all modern languages, most common are for and while loops

# While loop (simplest), while condition is valid it will keep looping

x = 1
while x <= 8:
	print(x)
	x += 1

print()
print()

#Break command can exit a while loop even if statement is still true

while True:
	reply = input('Enter Text, [type "stop" to quit]: ')
	if(reply == 'stop'):
		break
	print(reply)


print()
print()

# For loop, defines start and end points, as well as incrementation per iteration
#range command goes up to, but does not include the second number
total = 0
for y in range(0,6):
	total = total + y 
print(total)

print()
print()

#Can loop through strings letter by letter
word = "computer"
for letter in word:
	print(letter)

print()
print()

#Can loop through arrays 
Months = ["Jan","Feb","Mar","April","May","June"]
for m in Months:
		print(m)

print()
print()

#Continue statment will terminate the current iteration but continue executing remaining iterations
for x in range (10,20):
			#if (x == 15): break
			if (x % 2 == 0) : continue
			print(x)

print()
print()

#Enumerate function used to number/index the members of the list
Months = ["Jan","Feb","Mar","April","May","June"]
for i, m in enumerate (Months):
		print(i,m)