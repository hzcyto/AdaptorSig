import math, sys
import random
import secrets

cmd = sys.argv[1]
try:
    value = int(eval(sys.argv[2]))
except:
    pass

def is_prime(n, debug=False):
    if n == 1: return False
    if n == 2: return True

    for k in range(100):
        a = random.randint(2, n-1)

        if gcd(n, a) != 1:
            if debug:
                print("\n", a, "\n", gcd(n, a), "\n")
            return False

        if pow(a, n - 1, n) != 1:
            return False

    return True

def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def genPrime(n):
    while 1:
        p = secrets.randbelow(n)+1
        if is_prime(p):
            break
    return p

if cmd == "gen":
    while 1:
        q = random.randint(2, 2 ** value - 1)
        if is_prime(q):
            break
    print(q)
elif cmd == "check":
    print(f"is {value} prime? {is_prime(value, True)}")
elif cmd == "div":
    x =972249167 #269220053 #96485131 to 224196561666767548608204057308312976422247279836753
    while 1:
        while 1:
            x += 2
            if is_prime(x):
                break
        print(x)
        if gcd(value, x) != 1:
            with open("prime", "a") as f:
                f.write(str(x)+"\n")
elif cmd  == "genpq":
    w=3
    boarder = pow(2, 1024)
    while w < boarder:
        w*=genPrime(1024)
    k=1
    while not is_prime(k*w-1):
        k+=1
    q=k*w-1
    print(f"k={k}, q={q}")
    l=1
    while not is_prime(4*l*q-1):
        l+=1
    p=4*l*q-1
    print(f"l={l}, p={p}")

