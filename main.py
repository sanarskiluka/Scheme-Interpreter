class My_Dict(dict):
    def __init__(self, symbs = None, par = None):
        if symbs:
            super().__init__(symbs)
        else:
            super().__init__({})
        self.par = par
        self.update({
            '+': lambda *args: sum(args), '-': lambda x, y: x - y, '*': lambda *args: multiply(*args), '/': lambda x, y: x / y,
            '<': lambda x, y: (x < y), '>': lambda x, y: (x > y), '=': lambda x, y: (x == y), '<=': lambda x, y: (x <= y), '>=': lambda x, y: (x >= y),
            "not": lambda x: (not x), "and": lambda x, y: (x and y), "or: ": lambda x, y: (x or y),
            'car': lambda x: x[0], 'cdr': lambda x: x[1:], 'cons': lambda x, y: [x] + y,
            'null?': lambda x: x == [], 'length': lambda x: len(x), 
            'append': lambda *lists: append(*lists),
            'map': lambda fn, l: list(map(fn, l)),
            'apply': lambda fn, args: fn(*args) if isinstance(args, list) else fn(args),  # gavtesto (flatten-list '(2 ((((4) 5))) ((3)) 9 7 ((8 1) 6)))
            'quotient': lambda x, y: x // y,
            'list': lambda *args: list(args),
            'list?': lambda x: isinstance(x, list),
            'exit': lambda: exit()
        })

    def find_symb(self, symb):
        if symb in self:
            return self
        elif self.par:
            return self.par.find_symb(symb)
        else:
            print(f'{symb} is not defined')
            return None

def append(*lists):
    l = []
    for lst in lists:
        l += lst
    return l

def divide(tokens):
    token = tokens.pop(0)
    if token == '(':
        l = []
        while tokens[0] != ')':
            l.append(divide(tokens))
        tokens.pop(0)
        return l
    elif token == "'":
        return ['quote', divide(tokens)]
    else:
        return toElem(token)
    
def toElem(token):
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            return token

def multiply(*args):
    result = 1
    for arg in args:
        result *= arg
    return result

def load_file(filename, my_dict):
    with open(filename, 'r') as f:
        exprs = f.read()
    exprs = exprs.replace('(', ' ( ').replace(')', ' ) ').replace("'", " ' ")
    exprs = exprs.split()
    while exprs:
        expr = divide(exprs)
        evaluate(expr, my_dict)

def merge(l1, l2):
    n = min(len(l1), len(l2))
    ans = []
    for i in range(n):
        ans.append([l1[i], l2[i]])
    return ans

def evaluate(expr, my_dict):
    if isinstance(expr, str):
        return my_dict.find_symb(expr)[expr]
    elif isinstance(expr, list) == False:
        return expr
    elif expr[0] == 'quote':
        return expr[1]
    elif expr[0] == 'if':
        proc, cond, res1, res2 = expr
        expr = res1 if evaluate(cond, my_dict) else res2
        return evaluate(expr, my_dict)
    elif expr[0] == 'cond':
        for test, result in expr[1:]:
            if test == 'else' or evaluate(test, my_dict):
                return evaluate(result, my_dict)
    elif expr[0] == 'define':
        proc, symb, expr1 = expr
        if isinstance(symb, list):
            symbName, args = symb[0], symb[1:]
            my_dict[symbName] = lambda *args1: evaluate(expr1, My_Dict(dict(merge(args, args1)), par=my_dict))
        else:
            my_dict[symb] = evaluate(expr1, my_dict)
    elif expr[0] == 'lambda':
        proc, args, block = expr
        return lambda *args1: evaluate(block, My_Dict(dict(merge(args, args1)), par=my_dict))
    elif expr[0] == 'load':
        proc, filename = expr
        load_file(filename[1:-1], my_dict)
    else:
        proc = evaluate(expr[0], my_dict)
        args = [evaluate(arg, my_dict) for arg in expr[1:]]
        return proc(*args)
    
def toKawaList(l):
    if isinstance(l, list) == False:
        return str(l)
    else:
        s = '('
        for elem in l:
            s += toKawaList(elem)
            s += ' '
        s = s[:-1]
        s += ')'
        return s

def main():
    my_dict = My_Dict()
    cnt = 1
    while True:
        expr = input(f'#|kawa:{cnt}|# ')
        cnt += 1
        if expr.lower() == "exit":
            break
        tokens = expr.replace('(', ' ( ').replace(')', ' ) ').replace("'", " ' ")
        tokens = tokens.split()
        expr1 = divide(tokens)
        ans = evaluate(expr1, my_dict)
        if ans != None:
            print(toKawaList(ans))

if __name__ == '__main__':
    main()