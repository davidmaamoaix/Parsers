#ExpressionParser

class Node:

    def __init__(self,value,l=None,r=None):
        self.value=value
        self.l=l;self.r=r
        pass

def leaf(node:Node)->bool:
    return node==None or (node.l==None and node.r==None)

def fact(n:int)->int:
    return 1 if n<=1 else n*fact(n-1)

def inBrac(index:int,exp:str)->bool:
    depth=0
    for i in exp[:index]:
        if i=='(': depth+=1
        elif i==')': depth-=1
    return not depth==0

def validBrac(exp:str)->bool:
    depth=0
    for i in exp:
        if i=='(': depth+=1
        elif i==')': depth-=1
        if depth<0: return False
    return depth==0

def parse(exp:str)->Node:
    if exp[0]=='(' and exp[-1]==')' and validBrac(exp[1:-1]):
        return parse(exp[1:-1])
    for op in ['+','-','*','/','C','P','!','^']:
        for i in range(len(exp)-1,-1,-1):
            char=exp[i]
            if char==op and not inBrac(i,exp):
                l=parse(exp[:i] if exp[:i]!='' else '0'+exp[:i] if op in ['+','-'] else exp[:i])
                r=parse(exp[i+1:]) if op!='!' else None
                return Node(op,l,r)
    return Node(exp)

def calc(tree:Node)->float:
    if leaf(tree):
        return float(tree.value) if tree!=None else None
    func={'+':lambda a,b:a+b,
          '-':lambda a,b:a-b,
          '*':lambda a,b:a*b,
          '/':lambda a,b:a/b,
          'C':lambda a,b:fact(a)/(fact(a-b)*fact(b)),
          'P':lambda a,b:fact(a)/fact(a-b),
          '^':lambda a,b:a**b,
          '!':lambda a,b:fact(a)}
    return func[tree.value](calc(tree.l),calc(tree.r))

def evaluate(exp:str)->float:
    return float(calc(parse(exp)))

while 1:
    print(evaluate(input()))
