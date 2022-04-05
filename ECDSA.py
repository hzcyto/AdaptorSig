import math, secrets

class Fp:
    @classmethod
    def init(cls, p):
        cls.p = p

    def __init__(self, v=0):
        self.v = v % Fp.p

    def __add__(self, rhs):
        return Fp(self.v + rhs.v)

    def __sub__(self, rhs):
        return Fp(self.v - rhs.v)

    def __mul__(self, rhs):
        return Fp(self.v * rhs.v)

    def inv(self):
        v = self.v
        if v == 0:
            raise Exception("zero inv")
        p = Fp.p
        return Fp(pow(v, p-2, p))

    def __truediv__(self, rhs):
        return self * rhs.inv()

    def __str__(self):
        return str(self.v)

class Ec:
    @classmethod
    def init(cls, a, b, p, r):
        Fp.init(p)
        #cls.a = Fp(a)
        #cls.b = Fp(b)
        cls.a = a
        cls.b = b
        cls.p = p
        cls.r = r

    def base(self):
        pass

    def __init__(self):
        #self.x = Fp(secrets.randbelow(self.p))
        self.x = secrets.randbelow(self.p)
        self.y = int(math.sqrt((self.x*self.x+self.a)*self.x+self.b)) % self.p

    def isValid(self):
        if self.isZero:
            return True
        a = self.a
        b = self.b
        x = self.x
        y = self.y
        return y*y == (x*x+a)*x+b

    def __add__(self, rhs):
        if self.isZero:
            return rhs
        if rhs.isZero:
            return self
        x1 = self.x
        y1 = self.y
        x2 = rhs.x
        y2 = rhs.y
        if x1 == x2:
            # P + (-P) = 0
            if y1 == -y2:
                return Ec()
            # dbl
            L = x1 * x1
            L = (L + L + L + self.a) / (y1 + y1)
        else:
            L = (y1 - y2) / (x1 - x2)
        x3 = L * L - (x1 + x2)
        y3 = L * (x1 - x3) - y1
        return Ec(x3, y3, False)

    def __mul__(self, rhs):
        if rhs == 0:
            return Ec()
        bs = bin(rhs)[2:]
        ret = Ec()
        for b in bs:
            ret += ret
            if b == '1':
                ret += self
        return ret

    def __str__(self):
        return f"({self.x}, {self.y})"


P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
RR = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
Ec.init(0, 7, P, RR)

P = Ec()
s = Ec()
print(s)

