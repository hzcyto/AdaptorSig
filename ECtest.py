from ec import Ec, Fr
from ec import initSecp256k1

P = initSecp256k1()
a = Fr()
b = Fr()
a.setRand()
b.setRand()
print(f"a={a}")
print(f"b={b}")
aP = P * a
bP = P * b
baP = aP * b
abP = bP * a
print(f"baP={baP}")
print(f"abP={abP}")
print(f"baP == abP? {baP == abP}")