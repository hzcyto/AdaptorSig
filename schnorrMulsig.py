import math
import re
import secrets
import hashlib

G = 7
#P = 68893228236460459212259390067756135621390999268498766607510866631630411351587
P = 1543
a = 2*3
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

    def H(self, inputs):
        data = str()
        for d in inputs:
            try:
                sd = str(d)
            except:
                pass
            data += sd
        return int.from_bytes(hashlib.sha256(data.encode()).digest(), "big")

    def mod(self, v):
        return v % self.p

    def modq(self, v):
        return v % self.q
    
    def publicize(self, secret):
        return pow(self.g, secret, self.p)

    def check(self, R, P, S, m, debug=False):
        c1 = pow(self.g, S, self.p)
        c2 = (R*pow(P, self.H([R, P, m]), self.p)) % self.p
        if debug:
            print("=== Debug ===")
            print(f'    g^S       : {c1}')
            print(f'R + P^H(R|P|m): {c2}')
            print("=============")
        return c1 == c2
        

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
        self.__r = gen.getRandom()

    def getPubK(self):
        return self.pubkey.get_num()

    def consP(self, L):
        pub = self.pubkey.get_num()
        return (pub * self.gen.H([L, pub])) % self.gen.p

    def consR(self):
        return self.gen.publicize(self.__r)

    def sign(self, R, P, m):
        return self.gen.modq(self.__r + self.gen.H([R, P, m]))

def mulsig(userA, userB, gen):
    print("Let's make mult-sig Pubkey!")
    print(f'{userA.name}: P1 = {userA.getPubK()}')
    print(f'{userB.name}: P2 = {userB.getPubK()}')
    L = gen.mod(gen.H([userA.getPubK(), userB.getPubK()]))
    print(f"Use L = {L} to make it ...")
    PA = userA.consP(L)
    PB = userB.consP(L)
    Pub =gen.modq(PA * PB)
    print(f'{userA.name}: PA = {PA}')
    print(f'{userB.name}: PB = {PB}')
    print(f"We consent to use P = {Pub} as mult-sig Pubkey.")
    print("Now, Let's decide mult-sig R!")
    R1 = userA.consR()
    R2 = userB.consR()
    print(f'{userA.name}: R1 = {R1}')
    print(f'{userB.name}: R2 = {R2}')
    Rand = gen.modq(R1 * R2)
    print(f"We consent to use R = {Rand} as mult-sig Random Number.")
    print("singing ...")
    m = "supercalifragilisticexpialidocious"
    S1 = userA.sign(Rand, Pub, m)
    S2 = userB.sign(Rand, Pub, m)
    print(f'{userA.name}: S1 = {S1}')
    print(f'{userB.name}: S2 = {S2}')
    S = gen.modq(S1 + S2)
    print(f"The sign for message m is S = {S}")
    if gen.check(Rand, Pub, S, m, debug=True):
        print('Verification Success!')
    else:
        print('(x_x) < Verification Fail > Did someone cheated?')

generator = KeyGenerator()
alice = User("Alice", generator)
bob = User("Bob", generator)
mulsig(alice, bob, generator)