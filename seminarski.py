import SouthwellSearchLibVH as lib

#jednostavni primjer
'''
x1, x2, x3 = lib.symbols('x1 x2 x3')
funkcija = x1**2 + x2**2 + x3**2
x0 = (1,2,3)
x_min, f_min, dots, k = lib.Southwell_search(funkcija, x0, tacnost=1e-3, crtanje=1)
'''

#primjer sa redoslijedom varijabli
'''
x, y, m = lib.symbols('x y m')
f = m**2 + y**2 + x**2
t0 = (1,2,3)
#red_varijabli = ['x','y','m']
#df,f0 = lib.parcijalni_izvod(f, m, t0,red_varijabli=red_varijabli)
df,f0 = lib.parcijalni_izvod(f, m, t0)
print("Izvod funkcije: ", df)
print("Vrijednost izvoda u tacki:", f0)
'''

#funkcija dvije promjenljive
'''
x1, x2 = lib.symbols('x1 x2')
f = (x1-1)**2 + (x2-9)**2
x0 = (5,4)
lib.Southwell_search(f, x0,tacnost=1e-3,crtanje=1)
'''

#funkcija cetiri promjenljive
'''
x1, x2, x3, x4 = lib.symbols('x1 x2 x3 x4')
f = (x1-1)**2+(x2+5)**2+x3**2+(x4+4)**2+2
x0 = (-1,9,9,7)
lib.Southwell_search(f,x0,ispis=1)
'''
'''
#neparabolicna funkcija unimodalna
x, y = lib.symbols('x y')
f = 0.26 * (x**2 + y**2) - 0.48 * x * y;
x0 = (-11,-8);
lib.Southwell_search(f, x0, crtanje = 1)
'''
'''
from sympy import exp
from numpy import round

#multimodalni kriterij
x, y = lib.symbols('x y')
f = (x**2 + y - 11)**2 + (x + y**2 -7)**2
x0 = (1,1)

lib.Southwell_search(f,x0)

### []
'''
