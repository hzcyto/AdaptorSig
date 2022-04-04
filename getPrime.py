import math, sys
import random

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

if cmd == "gen":
    while 1:
        q = random.randint(2, 2 ** value - 1)
        if is_prime(q):
            break
    print(q)
elif cmd == "check":
    print(f"is {value} prime? {is_prime(value, True)}")
elif cmd == "div":
    x = 268797847 #96485131 to 224196561666767548608204057308312976422247279836753
    while 1:
        while 1:
            x += 1
            if is_prime(x):
                break
        print(x)
        if gcd(value, x) != 1:     
            print("\n", x, "\n", gcd(value, x), "\n")