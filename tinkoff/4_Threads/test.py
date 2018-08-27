#!/usr/bin/python3

a = list()
a.append(10)
a.append(11)

print(a.pop())
print(a.pop())
try:
    print(a.pop())
except IndexError:
    print("try else")