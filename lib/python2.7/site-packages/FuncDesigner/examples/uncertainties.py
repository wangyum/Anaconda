'''
Example of getting uncertainties
Usage:
    result = oofun.uncertainty(point, deviations, actionOnAbsentDeviations='warning')
point and deviations should be Python dicts of pairs (oovar, value_for_oovar)
actionOnAbsentDeviations = 
    'error' (raise FuncDesigner exception) | 
    'skip' (treat as fixed number with zero deviation) |
    'warning' (print warning, treat as fixed number) 
Sparse large-scale examples haven't been tested,
we could implement and test it properly on demand
'''
from FuncDesigner import *
from numpy import mat
a, b = oovars('a', 'b')
f1 = a + 2 * b
f2 = sin(a**2)
point1 = {a:1, b:1}
point2 = {a:0.5, b:0.15}
deviations1 = {a:0.1, b:0.1}
deviations2 = {a:0.01, b:0.015}
for f in [f1, f2]:
    for point in (point1, point2):
        for deviations in [deviations1, deviations2]:
            print('%f+/-%f   ' % (f(point), f.uncertainty(point, deviations))), # comma will work in other way in Python3
    print('\n')
# Vectorized example
point = {a:[1, 2, 3], b:0.1}
deviations1 = {a:0.01, b:0.015}
deviations2 = {a:[0.01, 0.2, 0.3], b:0.015}
M = mat('2 3 4; 3 4 5')
f = dot(M, a) + b
for deviations in [deviations1, deviations2]:
    print('%s +/- %s     ' % (f(point), f.uncertainty(point, deviations))), # comma will work in other way in Python3
# Output: 
# 3.000000+/-0.223607    3.000000+/-0.031623    0.800000+/-0.223607    0.800000+/-0.031623    
# 0.841471+/-0.108060    0.841471+/-0.010806    0.247404+/-0.096891    0.247404+/-0.009689    
# [ 20.1  26.1] +/- [ 0.0559017   0.07228416] [ 20.1  26.1] +/- [ 1.82006181  2.33004828]
