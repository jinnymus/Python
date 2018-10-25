#!/usr/bin/python3


def print_max(li=None):
    print('[print_max] list: ' + str(li) + ' max: ' + str(max(li)))

def rem_max(li=None):
    print('[rem_max] l: ' + str(li))
    print_max(li)
    li.remove(max(li))
    print('[rem_max] l: ' + str(li))
    print_max(li)
    #return



l = [10, 5, 6, 7, 10, 21,11,23,45]
#s = {'b':5, '4':7, '11':21,'1':23}

#print(s)
#print(sorted(s.items(),key=lambda item: item[0]))
#print_max(l)
s = set(l)
print(s)
ll = list(s)
ll.sort()
print(ll)
#sorted(ll)
print(ll)
sl = sorted(ll)
print(sl)
print(sl.reverse())
print(sl)
print(sl[0])
print(sl[1])
rem_max(l)
rem_max(l)
#rem_max(ll)


