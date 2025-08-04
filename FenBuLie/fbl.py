import math
from rich import table
import rich
from rich import traceback
import re
from decimal import Decimal as D
from fractions import Fraction as F
import os

F2D = lambda f: (lambda a, b: D(a)/D(b))(*f.as_integer_ratio())

def binomial(X, n, p):
    Dn = D(n)
    Fn = F(n)
    Fp = F(p)
    Dp = F2D(Fp)
    tb = table.Table(X, *[str(i) for i in range(int(n)+1)], highlight=True)
    tb.add_row('P', *[str(D(math.comb(int(n), i))*Dp**D(i)*(D(1)-Dp)**(Dn-D(i))) for i in range(int(n)+1)])
    tb.add_row('', *[str(F(math.comb(int(n), i))*Fp**F(i)*(F(1)-Fp)**(Fn-F(i))) for i in range(int(n)+1)])
    rich.print(tb)
    rich.print(f'E{"(" if len(X) else ""}{X}{")" if len(X) else ""} = {Dn*Dp} = {Fn*Fp}')
    rich.print(f'D{"(" if len(X) else ""}{X}{")" if len(X) else ""} = {Dn*Dp*(D(1)-Dp)} = {Fn*Fp*(F(1)-Fp)}')
    rich.print(f'σ{"(" if len(X) else ""}{X}{")" if len(X) else ""} = {(Dn*Dp*(D(1)-Dp))**D(0.5)}')

def hypergeo(X, N, M, n):
    N = int(N)
    M = int(M)
    n = int(n)
    mi = max(0, n-N+M)
    ma = min(n, M)
    tb = table.Table(X, *[str(i) for i in range(mi, ma+1)], highlight=True)
    tb.add_row('P', *[str(D(math.comb(M, i)*math.comb(N-M, n-i))/D(math.comb(N, n))) for i in range(mi, ma+1)])
    tb.add_row('', *[str(F(math.comb(M, i)*math.comb(N-M, n-i))/F(math.comb(N, n))) for i in range(mi, ma+1)])
    rich.print(tb)
    rich.print(f'E{"(" if len(X) else ""}{X}{")" if len(X) else ""} = {D(n)*D(M)/D(N)} = {F(n)*F(M)/F(N)}')
    rich.print(f'D{"(" if len(X) else ""}{X}{")" if len(X) else ""} = {D(n)*(D(M)/D(N))*(D(1)-D(M)/D(N))*((D(N)-D(n))/(D(N)-D(1)))} = {F(n)*F(M)/F(N)*(F(1)-F(M)/F(N))*(F(N)-F(n))/(F(N)-F(1))}')
    rich.print(f'σ{"(" if len(X) else ""}{X}{")" if len(X) else ""} = {(D(n)*D(M)/D(N)*(D(1)-D(M)/D(N))*(D(N)-D(n))/(D(N)-D(1)))**D(0.5)}')

names = {
    'B': binomial,
    'H': hypergeo
}

while True:
    code = input('>')
    if code in ('', 'quit', 'q', 'exit', 'e'):
        exit()
    elif code.startswith('!'):
        os.system(code[1:])
        continue
    try:
        X, name, args = re.match(r'(.*?)~(.*?)\((.*?)\)', code).groups()
        arg = args.replace(' ', '').split(',')
        names[name](X, *arg)
    except:
        rich.print(traceback.Traceback())
