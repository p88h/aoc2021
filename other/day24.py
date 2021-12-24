import itertools
lines = open("input/day24.txt").read().splitlines()

class Expr:
    def __init__(self, right = "0", left = None):
        self.left = left
        self.right = right
        self.base = 26
    
    def divX(self):
        if self.left:
            self.right = self.left.right
            self.left = self.left.left
        else:
            self.right = "0"
    
    def modX(self):
        self.left = None
    
    def mulX(self):
        self.left = Expr(self.right, self.left)
        self.right = "0"
    
    def addR(self, other):
        if self.left and other.left:
            self.left.addR(other.left)
        elif other.left:
            self.left=other.left.copy()
        self.right = "{}+{}".format(self.right, other.right)

    def addV(self, val):
        self.right = "{}+{}".format(self.right, val)
    
    def copy(self):
        if self.left:
            return Expr(self.right, self.left.copy())
        else:
            return Expr(self.right)

    def str(self):
        if self.left:
            return "({})*{}+{}".format(self.left.str(), self.base, self.right)
        else:
            return self.right

class State:
    def __init__(self, entropy):
        self.regs = {'w':Expr(), 'x': Expr(), 'y': Expr(), 'z': Expr()}
        self.rmin = {'w':0, 'x': 0, 'y': 0, 'z': 0}
        self.rmax = {'w':0, 'x': 0, 'y': 0, 'z': 0}
        self.entropy = entropy
        self.pos = 0
        self.conds = []
        pass

    def inp(self, dst):
        self.regs[dst]=Expr("in[{}]".format(self.pos))
        self.rmin[dst]=1
        self.rmax[dst]=9
        self.pos += 1

    def add(self, dst, var):
        if var not in self.regs or self.rmin[var]==self.rmax[var]:
            if var in self.regs:
                val = self.rmin[var]
            else:
                val = int(var)
            self.rmin[dst] += val
            self.rmax[dst] += val
            if self.rmin[dst] == self.rmax[dst]:
                self.regs[dst] = Expr(str(self.rmin[dst]))
            elif val != 0:
                self.regs[dst].addV(val)
        elif self.rmin[dst] == 0 and self.rmax[dst] == 0:
            self.regs[dst]=self.regs[var].copy()
            self.rmin[dst]=self.rmin[var]
            self.rmax[dst]=self.rmax[var]
        else:
            self.regs[dst].addR(self.regs[var])
            self.rmin[dst]+=self.rmin[var]
            self.rmax[dst]+=self.rmax[var]

    def mul(self, dst, var):
        if var not in self.regs or self.rmin[var]==self.rmax[var]:
            if var in self.regs:
                val = self.rmin[var]
            else:
                val = int(var)
            if val < 0:
                self.rmin[dst] = self.rmax[dst] * val
                self.rmax[dst] = self.rmin[dst] * val
            else:
                self.rmin[dst] *= val
                self.rmax[dst] *= val
            if self.rmin[dst] == self.rmax[dst]:
                self.regs[dst] = Expr(str(self.rmin[dst]))
            elif val != 1:
                self.regs[dst].mulX()
        elif self.rmin[dst] == 0 and self.rmax[dst] == 0:
            pass
        elif self.rmin[dst] == 1 and self.rmax[dst] == 1:
            self.regs[dst]=self.regs[var].copy()
            self.rmin[dst]=self.rmin[var]
            self.rmax[dst]=self.rmax[var]
        else:
            print("Invalid mul", self.regs[dst].str(), self.regs[var].str())
            exit(1)
            self.regs[dst] = "({})*({})".format(self.regs[dst], self.regs[var]) 
            r1 = [self.rmin[dst],self.rmax[dst]]
            r2 = [self.rmin[var],self.rmax[var]]
            prods = [ a*b for (a,b) in itertools.product(r1,r2)]
            self.rmin[dst]=min(prods)
            self.rmax[dst]=max(prods)

    def div(self, dst, var):
        val = int(var)
        self.rmin[dst] //= val
        self.rmax[dst] //= val
        if self.rmin[dst] == self.rmax[dst]:
            self.regs[dst] = Expr(str(self.rmin[dst]))
        elif val != 1:
            self.regs[dst].divX()
    
    def mod(self, dst, var):
        val = int(var)
        if val > self.rmax[dst] and self.rmin[dst] >= 0:
            return
        self.rmin[dst] %= val
        self.rmax[dst] %= val
        if self.rmin[dst] == self.rmax[dst]:
            self.regs[dst] = Expr(str(self.rmin[dst]))
        else:
            self.regs[dst].modX()

    def eql(self, dst, var):
        if var.isnumeric():
            val = int(var)
            if self.rmin[dst] == val and self.rmax[dst] == val:
                self.regs[dst] = Expr("1")
                self.rmin[dst] = self.rmax[dst] = 1
            else:
                self.regs[dst] = Expr("0")
                self.rmin[dst] = self.rmax[dst] = 0
        else:
            bit = self.entropy % 2
            self.entropy //= 2
            if bit:
                self.conds.append("{} [{}..{}]== {} [{}..{}]".format(self.regs[var].str(), self.rmin[var], self.rmax[var], self.regs[dst].str(), self.rmin[dst], self.rmax[dst]))
                if self.rmax[var] < self.rmin[dst] or self.rmax[dst] < self.rmin[var]:
                    return False
                self.regs[dst] = Expr("1")
                self.rmin[dst] = self.rmax[dst] = 1
            else:
                if self.rmax[var] < self.rmin[dst] or self.rmax[dst] < self.rmin[var]:
                    self.regs[dst] = Expr("0")
                    self.rmin[dst] = self.rmax[dst] = 0
                    return True
                self.conds.append("{} != {}".format(self.regs[var], self.regs[dst]))
                self.regs[dst] = Expr("0")
                self.rmin[dst] = self.rmax[dst] = 0
        return True

for e in range(2,2**14,2):
    st = State(e)
    valid = True
    for l in lines:
        a = l.split()
        dst = a[1]
        var = ""
        if len(a) > 2:
            var = a[2]
        if a[0] == "inp":
            st.inp(a[1])
        elif a[0] == "add":
            st.add(a[1], a[2])
        elif a[0] == "mul":
            st.mul(a[1], a[2])
        elif a[0] == "div":
            st.div(a[1], a[2])
        elif a[0] == "mod":
            st.mod(a[1], a[2])
        elif a[0] == "eql":
            if not st.eql(a[1], a[2]):
                valid = False
                break
    # print(a[1], st.regs[a[1]].str(), st.rmin[a[1]], st.rmax[a[1]])
    if not valid or st.rmin["z"] > 0:
        continue
    print("Good entropy value: {}".format(e))
    print("\n".join(st.conds))
    for r in st.regs:
        print("{} = {}..{}".format(r, st.rmin[r], st.rmax[r]))
        print()