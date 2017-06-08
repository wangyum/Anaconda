from FuncDesigner import *
a, b = oovars('a', 'b')
point = {a:10, b:[2, -5, -4]}
f1 = ifThenElse(a+sum(b)<1, 3*a, 15*(a+5/b[0]))
f2 = 4*sin(a) + 5 * ifThenElse(a+sum(abs(b))>1, 3, 4*a)
f3 = 15 + 25 * ifThenElse(2>1, -100, 3*sum(log2(abs(b))))
f4 = 15 + 25 * ifThenElse(1>2, -100, 3*sum(log2(abs(b))))
for f in [f1, f2, f3, f4]: 
    print(f(point))
    print(f.D(point))

#[ 187.5]
#{a: array([ 15.]), b: array([-18.75,  -0.  ,  -0.  ])}
#[ 12.82391556]
#{a: array([-3.35628612])}
#[-2485]
#{}
#[ 414.14460712]
#{b: array([ 54.10106403, -21.64042561, -27.05053202])}

