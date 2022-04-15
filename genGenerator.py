import sys

cmd = sys.argv[1]
try:
    value = sys.argv[2]
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
        if cnt > 5:
            break
        g += 1
elif cmd == "check":
    results = list()
    for i in range(1, q + 1):
        print(f'g^{i} = {pow(g, i, p)}')
    results.sort()
    print(results)
