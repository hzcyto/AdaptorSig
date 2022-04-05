import secrets, hashlib

p = 1543
q = 257
g = 7

s = secrets.randbelow(p)
h = pow(g, s, p)

r = secrets.randbelow(p)
x = pow(g, r, p)

m = "the secret message"

c = int.from_bytes(hashlib.sha256((str(x)+m).encode()).digest(), "big")
y = (r + s*c) % q

checkX = (pow(g, y, p) * pow(pow(h, c, p), p-2, p)) % p
checkSign = int.from_bytes(hashlib.sha256((str(checkX)+m).encode()).digest(), "big")

print(f'key info s : {s}, h : {h}')
print(f'secret sign info : {r}, x : {x}')
print(f'sign info c : {c}, y : {y}, m : {m}')
print(f'check sign  : {checkSign}, (cX = {checkX})')

"""
s = secrets.randbelow(p)
h = pow(g, s, p)

r = secrets.randbelow(p)
x = pow(g, r, p)

m = "the secret message"

#c = secrets.randbelow(p)
#c = hash(tuple(map(int, str(x).split())))
c = int.from_bytes(hashlib.sha256((str(x)+m).encode()).digest(), "big")
y = (r + s*c) % q

check1 = pow(g, y, p)
check2 = (x * pow(h, c, p)) % p

print(f'key info s : {s}, h : {h}')
print(f'first info r : {r}, x : {x}')
print(f'second info c : {c}')
print(f'third info y : {y}')
print(f'check info g^y  : {check1}')
print(f'check info xh^c : {check2}')
"""