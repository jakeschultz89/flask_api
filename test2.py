# print your name on the console
print("Jake Schultz")


# print numbers from 30 to 70
for i in range(30, 71):
    print(i)


# working with files
# read notes.txt file and count the lines on it
file_read = open("notes.txt", "r")
all_lines = file_read.readlines()
print("There are " + str(len(all_lines)) + " lines in the file")
file_read.close()

# create a new file
test = open("demo.txt", "w")
test.write("Hello from Python\n")
test.write("This should be a second line\n")
test.close()

# write a line in the bottom of notes.txt
notes = open("notes.txt", "a")
notes.append("\nThis text was added with python code")
notes.clo