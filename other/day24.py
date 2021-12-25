class Expr:
    def __init__(self, value=0, inputs=None, left=None):
        self.left = left
        self.inputs = inputs if inputs else []
        self.value = value
        self.base = 26

    def min(self):
        if self.left:
            return self.left.min()*self.base+len(self.inputs)+self.value
        else:
            return len(self.inputs)+self.value

    def max(self):
        if self.left:
            return self.left.max()*self.base+9*len(self.inputs)+self.value
        else:
            return 9*len(self.inputs)+self.value

    def equals(self, val):
        if self.left or self.inputs:
            return self.min() == val and self.max() == val
        else:
            return self.value == val

    def divX(self, val):
        if val == 1 or self.equals(0):
            return
        # check base?
        if self.left:
            self.inputs = self.left.inputs
            self.value = self.left.value
            self.left = self.left.left
        else:
            self.value = 0
            self.inputs = []

    def divR(self, other):
        # This is only supported if the right side is a fixed value
        self.divX(other.value)

    def modX(self, val):
        # check base?
        self.left = None

    def mulX(self, val):
        if val == 1 or self.equals(0):
            return
        if val == 0:
            self.left = None
        else:
            self.base = val
            self.left = Expr(self.value, self.inputs, self.left)
        self.value = 0
        self.inputs = []

    def mulR(self, other):
        # This is only supported if the right side is a fixed value
        self.mulX(other.value)

    def addR(self, other):
        if self.left and other.left:
            self.left.addR(other.left)
        elif other.left:
            self.left = other.left.copy()
        self.value += other.value
        self.inputs.extend(other.inputs)

    def addV(self, val):
        self.value += val

    def copy(self):
        if self.left:
            return Expr(self.value, self.inputs.copy(), self.left.copy())
        else:
            return Expr(self.value, self.inputs.copy())

    def str(self):
        ret = ""
        if self.left:
            ret = "({})*{}".format(self.left.str(), self.base)
        if len(self.inputs) > 0:
            if ret:
                ret += "+"
            ret += ("+".join(self.inputs))
        if not ret:
            return str(self.value)
        if self.value > 0:
            return "{}+{}".format(ret, self.value)
        elif self.value < 0:
            return "{}-{}".format(ret, -self.value)
        else:
            return ret if ret else "0"


class State:
    def __init__(self, entropy):
        self.regs = {'w': Expr(), 'x': Expr(), 'y': Expr(), 'z': Expr()}
        self.entropy = entropy
        self.pos = 0
        self.conds = []
        pass

    def inp(self, dst):
        self.regs[dst] = Expr(inputs=["inp[{}]".format(self.pos)])
        self.pos += 1

    def add(self, dst, var):
        if var not in self.regs:
            self.regs[dst].addV(int(var))
        else:
            self.regs[dst].addR(self.regs[var])

    def mul(self, dst, var):
        if var not in self.regs:
            self.regs[dst].mulX(int(var))
        else:
            self.regs[dst].mulR(self.regs[var])

    def div(self, dst, var):
        self.regs[dst].divX(int(var))

    def mod(self, dst, var):
        self.regs[dst].modX(int(var))

    def eql(self, dst, var):
        if var not in self.regs:
            if self.regs[dst].equals(int(var)):
                self.regs[dst] = Expr(1)
            else:
                self.regs[dst] = Expr(0)
        else:
            bit = self.entropy % 2
            self.entropy //= 2
            if bit:
                self.conds.append("{} == {}".format(self.regs[var].str(), self.regs[dst].str()))
                if self.regs[var].max() < self.regs[dst].min() or self.regs[dst].max() < self.regs[var].min():
                    return False
                self.regs[dst] = Expr(1)
            else:
                if self.regs[var].max() < self.regs[dst].min() or self.regs[dst].max() < self.regs[var].min():
                    self.regs[dst] = Expr(0)
                    return True
                self.conds.append("{} != {}".format(self.regs[var], self.regs[dst]))
                self.regs[dst] = Expr(0)
        return True

lines = open("input/day24.txt").read().splitlines()
for e in range(2, 2**14, 2):
    st = State(e)
    valid = True
    for l in lines:
        # print(l)
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
        # print(a[1], "=", st.regs[a[1]].str())
    if not valid or st.regs["z"].min() > 0:
        continue
    print("Good entropy value: {}".format(e))
    print("\n".join(st.conds))
    for r in st.regs:
        print("{} = {}..{}".format(r, st.regs[r].min(), st.regs[r].max()))
        print()
    break