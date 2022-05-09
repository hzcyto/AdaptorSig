import secrets
import sys

cmd = sys.argv[1]
try:
    value = int(sys.argv[2])
    svalue = int(sys.argv[3])
    tvalue = int(sys.argv[4])
except:
    pass

g = 2
#p = 68893228236460459212259390067756135621390999268498766607510866631630411351587
p = 1543
a = 2*3
q =  (p - 1)//a

cnt = 0

if cmd == "gen":
    while 1:
        flag = True
        for i in range(1, q):
            if pow(g, i, p) == 1:
                flag = False
                break
        if flag and pow(g, q, p) == 1:
            print("g : ", g)
            cnt+=1
        if cnt > 100:
            break
        g += 1
elif cmd == "check":
    g = svalue
    results = list()
    for i in range(1, tvalue):
        print(f'g^{i} = {pow(g, i, value)}')
        results.append(pow(g, i, value))
    results.sort()
    print(results)
elif cmd == "supergen":
    n = (value-1)//svalue
    print(f"p={value}, q={svalue}, n={n}")
    while 1:
        g = secrets.randbelow(svalue)
        flag = True
        for i in range(10):
            if not pow(g, (i+1)*svalue-1,value) == pow(g,(i+2)*svalue-1,value):
                flag = False
                break
        if flag:
            break
    print(f"g={g}")
