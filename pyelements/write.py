#method1 fully functioning
print("fullhtmlfile", file=open("output.txt", "a"))

#method2 notworks on big codes
with open('file.txt', 'w') as f:
    f.write('mytext')
