import os

a = input("Command: ")
l = a.split()
if os.path.isfile(l[1]):
    print("File 1 exists.")
    if os.path.isfile(l[2]):
        print("File with same name exists.")
    else:
        os.renames(l[1], l[2])
        print("Successful")
else:
    print("File 1 does not exist")

