import math
import re, sys
import secrets
import hashlib
import uuid
import time


db = str()
try:
    cmd = sys.argv[1]
    db = sys.argv[2]
except:
    pass

dflag = False
if db == "debug":
    dflag = True

G = 7
H = 17
P = 1543
a = 2*3
Q =  (P - 1)//a

class KeyGenerator:
    def __init__(self):
        self.g = G
        self.h = H
        self.q = Q
        self.p = P

    def genKey(self):
        sec1 = self.getRandom()
        sec2 = self.getRandom()
        pub = self.mod(pow(self.g, sec1, self.p)*pow(self.h, sec2, self.p))
        return secKey(sec1, sec2), pubKey(pub)

    def getRandom(self):
        return secrets.randbelow(self.q)

    def calcP(self, sk, c=1):
        return self.mod(pow(self.g, sk.getsec1()*c, self.p)*pow(self.h, sk.getsec2()*c, self.p))

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

    def check(self, R, P, s1, s2, c, debug=False):
        c1 = self.mod(pow(self.g, s1, self.p)*pow(self.h, s2, self.p))
        c2 = self.mod(R*pow(P, c, self.p))
        if debug:
            print("=== Debug ===")
            print(f'  g^s1*h^s2 : {c1}')
            print(f'R*P^H(R|P|m): {c2}')
            print("=============")
        return c1 == c2

    def checkT(self, R, P, s1, s2, c, T, debug=False):
        c1 = self.mod(pow(self.g, s1, self.p)*pow(self.h, s2, self.p))
        c2 = self.mod(T*R*pow(P, c, self.p))
        if debug:
            print("=== Debug ===")
            print(f' g^as1*h^as2  : {c1}')
            print(f'T*R*P^H(R|P|m): {c2}')
            print("=============")
        return c1 == c2

    def checkTT(self, R, s1, s2, T, debug=False):
        c1 = self.mod(pow(self.g, s1, self.p)*pow(self.h, s2, self.p))
        c2 = self.mod(T*R)
        if debug:
            print("=== Debug ===")
            print(f'g^ts1*h^ts2 : {c1}')
            print(f'T*R: {c2}')
            print("=============")
        return c1 == c2
        
class pubKey:
    def __init__(self, num):
        self.key = num
        self.g = G
        self.h = H
        self.p = P

    def randy(self, r1, r2):
        return (pow(self.g, r1, self.p)*pow(self.h, r2, self.p)) % self.p
    
    def tandy(self, t1, t2):
        return (pow(self.g, t1, self.p)*pow(self.h, t2, self.p)) % self.p

    def get_num(self):
        return self.key

class secKey:
    def __init__(self, num1, num2):
        self.__key1 = num1
        self.__key2 = num2
        self.q = Q
    
    def modq(self, v):
        return v % self.q

    def sig(self, c, r1, r2):
        return (self.modq(r1 + c*self.__key1), self.modq(r2 + c*self.__key2))

    def aSig(self, t1, t2, c, r1, r2):
        return (self.modq(t1 + r1 + c*self.__key1), self.modq(t2 + r2 + c*self.__key2))

    #for debug
    def getsec1(self):
        return self.__key1
    def getsec2(self):
        return self.__key2

class User:
    def __init__(self, name:str, gen:KeyGenerator) -> None:
        self.name = name
        self.gen = gen
        self.seckey:secKey = None
        self.pubkey:pubKey = None
        self.seckey, self.pubkey = gen.genKey()
        self.__r1 = gen.getRandom()
        self.__r2 = gen.getRandom()

    def getPubK(self):
        return self.pubkey.get_num()

    def getR(self):
        return self.pubkey.randy(self.__r1, self.__r2)
    
    def getT(self, t1, t2):
        return self.pubkey.tandy(t1, t2)

    def sign(self, c):
        return self.seckey.sig(c, self.__r1, self.__r2)

    def adaptSign(self, t1, t2, c):
        return self.seckey.aSig(t1, t2, c, self.__r1, self.__r2)

    #for debug
    def getr1(self):
        return self.__r1
    def getr2(self):
        return self.__r2
    

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

    t1 = gen.getRandom()
    t2 = gen.getRandom()
    T = userA.getT(t1, t2)
    c = gen.H([RAB, PAB, m])

    # check start
    print(f"t1 = {t1}, t2 = {t2}, T = {T}")
    print(f"c = {c}, ra1 = {userA.getr1()}, ra2 = {userA.getr2()}, rb1 = {userB.getr1()}, rb2 = {userB.getr2()}")
    print(f"pa1 = {userA.seckey.getsec1()}, pa2 = {userA.seckey.getsec2()}, pb1 = {userB.seckey.getsec1()}, pb2 = {userB.seckey.getsec2()}")
    s11 = t1 + userA.getr1()
    s22 = t2 + userA.getr2()
    print(f"s11 = {s11}, s22 = {s22}")
    print(f"{gen.checkTT(RA, s11, s22, T, debug=True)} is the check result!")
    # check end

    aSA1, aSA2 = userA.adaptSign(t1, t2, c)
    print(f"signature : (aSA1, aSA2) = ({aSA1}, {aSA2})")
    if gen.checkT(RA, PA, aSA1, aSA2, c, T, debug=True):
        print("legal T!")
    else:
        print("Elegal T!!!!")

    aSAB1, aSAB2 = userB.adaptSign(aSA1, aSA2, c)
    print(f"signature : (aSAB1, aSAB2) = ({aSAB1}, {aSAB2})")

    SAB1 = gen.modq(aSAB1-t1)
    SAB2 = gen.modq(aSAB2-t2)

    if gen.check(RAB, PAB, SAB1, SAB2, c, debug=True):
        print("Verification success!")
    else:
        print("Verification fail ...")   

def mySignASM(userA:User, userB:User, gen:KeyGenerator):
    num = max([len(userA.name), len(userB.name)])
    PA = userA.getPubK()
    RA = userA.getR()

    PB = userB.getPubK()
    RB = userB.getR()
    m = uuid.uuid4().hex
    print("共通の公開鍵を作成します…")
    print(f"{userA.name:>{num}}: P = {PA}")
    print(f"{userB.name:>{num}}: P = {PB}")
    L = gen.H([PA, PB])
    print(f"L = {L} で共通公開鍵に使用する P' = g^H(L,P)p*h^H(L,P)q を公開してください…")
    CA = gen.H([L, PA])
    CB = gen.H([L, PB])
    PAL = gen.calcP(userA.seckey, CA)
    PBL = gen.calcP(userB.seckey, CB)
    print(f"{userA.name:>{num}}: P' = {PAL}")
    print(f"{userB.name:>{num}}: P' = {PBL}")
    PABL = gen.mod(PAL*PBL)
    print(f"共通公開鍵として P'AB = {PABL} を使用します")
    print(f"{userA.name:>{num}}: R = {RA}")
    print(f"{userB.name:>{num}}: R = {RB}")
    RAB = gen.mod(RA * RB)
    print(f"共通ランダムナンバーとして RAB = {RAB} を使用します")
    t1 = gen.getRandom()
    t2 = gen.getRandom()
    T = userA.getT(t1, t2)
    c = gen.H([RAB, PABL, m])
    
    if dflag:
        # check start
        print(f"t1 = {t1}, t2 = {t2}, T = {T}")
        print(f"c = {c}, ra1 = {userA.getr1()}, ra2 = {userA.getr2()}, rb1 = {userB.getr1()}, rb2 = {userB.getr2()}")
        print(f"pa1 = {userA.seckey.getsec1()}, pa2 = {userA.seckey.getsec2()}, pb1 = {userB.seckey.getsec1()}, pb2 = {userB.seckey.getsec2()}")
        s11 = t1 + userA.getr1()
        s22 = t2 + userA.getr2()
        print(f"s11 = {s11}, s22 = {s22}")
        print(f"{gen.checkTT(RA, s11, s22, T, debug=True)} is the check result!")
        # check end

    aSA1, aSA2 = userA.adaptSign(t1, t2, c*CA)
    print(f"{userA.name}: Adaptor Signature : (aSA1, aSA2) = ({aSA1}, {aSA2})")

    if gen.checkT(RA, PAL, aSA1, aSA2, c, T, debug=dflag):
        print("T の検証に成功!")
    else:
        print("T の値が不正値です!!!!")

    aSAB1, aSAB2 = userB.adaptSign(aSA1, aSA2, c*CB)
    print(f"{userB.name}: Adaptor Signature : (aSAB1, aSAB2) = ({aSAB1}, {aSAB2})")

    SAB1 = gen.modq(aSAB1-t1)
    SAB2 = gen.modq(aSAB2-t2)

    if gen.check(RAB, PABL, SAB1, SAB2, c, debug=dflag):
        print("Verification success!")
    else:
        print("Verification fail ...")



generator = KeyGenerator()
#tstart = time.time()
alice = User("Alice", generator)
#tend = time.time() - tstart
#print(tend)
bob = User("Bob", generator)
if cmd == "sign":
    mySign(alice, bob, generator)
elif cmd == "AS":
    mySignAS(alice, bob, generator)
elif cmd == "mult-AS":
    mySignASM(alice, bob, generator)