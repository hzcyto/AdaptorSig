import math
import re
import secrets
import hashlib
import uuid

G = 7
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
        pub = self.mod(pow(self.g, sec, self.p))
        return secKey(sec), pubKey(pub)

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
        return self.mod(int.from_bytes(hashlib.sha256(data.encode()).digest(), "big"))

    def mod(self, v):
        return v % self.p

    def modq(self, v):
        return v % self.q

    def check(self, R, P, s, c, debug=False):
        c1 = pow(self.g, s, self.p)
        c2 = self.mod(R*pow(P, c, self.p))
        if debug:
            print("=== Debug ===")
            print(f' g^s : {c1}')
            print(f'R*P^c: {c2}')
            print("=============")
        return c1 == c2

    def checkT(self, R, P, s, c, T, debug=False):
        c1 = pow(self.g, s, self.p)
        c2 = self.mod(T*R*pow(P, c, self.p))
        if debug:
            print("=== Debug ===")
            print(f' g^as  : {c1}')
            print(f'T*R*P^c: {c2}')
            print("=============")
        return c1 == c2

    def checkTT(self, R, s, T, debug=False):
        c1 = pow(self.g, s, self.p)
        c2 = self.mod(T*R)
        if debug:
            print("=== Debug ===")
            print(f'g^ts: {c1}')
            print(f'T*R : {c2}')
            print("=============")
        return c1 == c2
        
class pubKey:
    def __init__(self, num):
        self.key = num
        self.g = G
        self.p = P

    def randy(self, r):
        return pow(self.g, r, self.p)
    
    def tandy(self, t):
        return pow(self.g, t, self.p)

    def get_num(self):
        return self.key

class secKey:
    def __init__(self, num):
        self.__key = num
        self.q = Q
    
    def modq(self, v):
        return v % self.q

    def sig(self, c, r):
        return self.modq(r + c*self.__key)

    def aSig(self, t, c, r):
        return self.modq(t + r + c*self.__key)
    
    #for debug
    def getsec(self):
        return self.__key

class User:
    def __init__(self, name:str, gen:KeyGenerator) -> None:
        self.name = name
        self.gen = gen
        self.seckey:secKey = None
        self.pubkey:pubKey = None
        self.seckey, self.pubkey = gen.genKey()
        self.__r = gen.getRandom()

    def getPubK(self):
        return self.pubkey.get_num()

    def getR(self):
        return self.pubkey.randy(self.__r)
    
    def getT(self, t):
        return self.pubkey.tandy(t)

    def sign(self, c):
        return self.seckey.sig(c, self.__r)

    def adaptSign(self, t, c):
        return self.seckey.aSig(t, c, self.__r)

    #for debug
    def getr(self):
        return self.__r
    

def mySign(userA:User, userB:User, gen:KeyGenerator):
    P = userA.getPubK()
    R = userA.getR()
    m = uuid.uuid4().hex
    print(f'{userA.name}: 署名開始 -> R = {R}')
    c = gen.H([R, P, m])
    print(f'{userB.name}: チャレンジナンバー c = {c}')
    sign1, sign2 = userA.sign(c)
    print(f'{userA.name}: 署名 (s1, s2, R) = ({sign1}, {sign2}, {R})')
    print(f"P = {P} で検証中...")
    if gen.check(R, P, sign1, sign2, c, debug=False):
        print('検証成功！')
    else:
        print('(x_x) < 検証失敗 > この署名は無効です...')

def mySignAS(userA:User, userB:User, gen:KeyGenerator):
    PA = userA.getPubK()
    RA = userA.getR()

    PB = userB.getPubK()
    RB = userB.getR()
    m = uuid.uuid4().hex

    PAB = gen.mod(PA * PB)
    RAB = gen.mod(RA * RB)
    print(f"PAB = {PA} * {PB} mod q = {PAB}")
    print(f"RAB = {RA} * {RB} mod q = {RAB}")

    t = gen.getRandom()
    T = userA.getT(t)
    c = gen.H([RAB, PAB, m])

    # check start
    s11 = t + userA.getr()
    print(f"{gen.checkTT(RA, s11, T, debug=True)} is the check result!")
    # check end

    aSA = userA.adaptSign(t, c)
    print(f"signature : aSA = {aSA}")

    if gen.checkT(RA, PA, aSA, c, T, debug=True):
        print("legal T!")
    else:
        print("Elegal T!!!!")

    aSAB = userB.adaptSign(aSA, c)
    print(f"signature : aSAB = {aSAB}")

    SAB = gen.modq(aSAB-t)

    SA = userA.sign(c)
    SB = userB.sign(c)
    cSAB = gen.modq(SA + SB)

    print(f"SAB  : {SAB}")
    print(f"cSAB : {cSAB}")
    # for debug
    print(f"c = {c}, ra = {userA.getr()}, rb = {userB.getr()}, pa = {userA.seckey.getsec()}, pb = {userB.seckey.getsec()}")

    if gen.check(RAB, PAB, SAB, c, debug=True):
        print("Verification success!")
    else:
        print("Verification fail ...")   



generator = KeyGenerator()
alice = User("Alice", generator)
bob = User("Bob", generator)
#mySign(alice, bob, generator)
mySignAS(alice, bob, generator)