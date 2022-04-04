import math
import secrets

G = 7
#P = 68893228236460459212259390067756135621390999268498766607510866631630411351587
P = 1543
a = 2*3*2081*2129*427369*1608697*16814011
Q =  (P - 1)//a

class KeyGenerator:

    def __init__(self):
        self.g = G
        self.q = Q
        self.p = P

    def genKey(self):
        sec = self.getRandom()
        pub = pow(self.g, sec, self.p)
        return Key(True, sec), Key(False, pub)

    def getRandom(self):
        return secrets.randbelow(self.q)

    def calcX(self, r):
        return pow(self.g, r, self.p)

    def check(self, x, y, h, c):
        print(f'g^y : {pow(self.g, y, self.p)}')
        print(f'xh^c: {(x * pow(h, c, self.p)) % self.p}')
        return pow(self.g, y, self.p) == (x * pow(h, c, self.p)) % self.p
        

class Key:
    def __init__(self, sec, num):
        self.is_sec = sec
        self.__key = num

    def get_num(self):
        if not self.is_sec:
            return self.__key
        return None

    def product(self, c):
        if self.is_sec:
            return self.__key * c
        return None

class User:
    def __init__(self, name, gen) -> None:
        self.name = name
        self.gen = gen
        self.seckey, self.pubkey = gen.genKey()

    def calcY(self, r, c):
        return r + (self.seckey.product(c) % self.gen.q)

def schnorring(userA, userB, gen):
    r = gen.getRandom()
    x = gen.calcX(r)
    print(f'{userA.name}: to {userB.name} x = {x}')
    c = gen.getRandom()
    print(f'{userB.name}: to {userA.name} c = {c}')
    y = userA.calcY(r, c)
    print(f'{userA.name}: to {userB.name} y = {y}')
    h = userA.pubkey.get_num()
    if gen.check(x, y, h, c):
        print(f'{userB.name}: Thank you {userA.name}, you know the secrect key of {h}')
    else:
        print(f'{userB.name}: Naah, you aren\'t {userA.name} or are you?')

generator = KeyGenerator()
alice = User("Alice", generator)
bob = User("Bob", generator)
schnorring(alice, bob, generator)