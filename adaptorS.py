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