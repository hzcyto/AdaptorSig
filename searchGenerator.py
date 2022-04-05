import random

g = 2
q = 257
a = 6
p = 1543

while 1:
    flag = True
    for i in range(1, q):
        if pow(g, i, p) == 1:
            flag = False
            break
    if flag and pow(g, q, p) == 1:
        print("g : ", g)
        break
    g += 1
