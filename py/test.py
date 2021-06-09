# Combine the strings to generate the text
file_text = "some content hereeeeeeeeeeeeee"
print (file_text)

# Write the text to the file
# If the file does not exist, create it
f_w = open("data/test.txt", "w")
f_w.write(file_text)
f_w.close()

# Open the file to read and print the text
print("\n--------------------------------------\nThe text of the file is:")
f_r = open("test.txt", "r")
print(f_r.read())
f_r.close()

print("\n--------------------------------------\n")