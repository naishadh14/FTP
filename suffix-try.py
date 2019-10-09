a = str(input("Enter string: "))
if a[0] == '*':
    flag = 1;
elif a[-1] == '*':
    flag = 0;
a = a.replace('*', '')
print(a)
for i in range(5):
    x = str(input("File name: "))
    if flag == 1:
        if x.endswith(a):
            print("Yes")
        else:
            print("No")
    elif flag == 0:
        if x.startswith(a):
            print("Yes")
        else:
            print("No")
