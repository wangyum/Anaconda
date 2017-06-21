'''
An example of solving global multiobjective optimization problem
with categorical variables and general logical constraints
with guaranteed precision |f-f*| < fTol
'''
import sys
sys.path.append('/home/dmitrey/OOSuite/OpenOpt')
#sys.path.append('/home/dmitrey/OOSuite/DerApproximator')
sys.path.append('/home/dmitrey/OOSuite/FuncDesigner')

from FuncDesigner import *
from openopt import *

aircraft, engine = oovars('aircraft',  'engine')

aircraft.fields = ('name', 'price', 'capacity')
#name; price (millions Euro); lifting capacity (tons)
aircraft.domain = [
                ('AN-15', 15, 15), 
                ('AN-30', 30, 30), 
                ('AN-70', 50, 45),
                ('AN-124', 200, 170),
                ('AN-138', 130, 140),
                ('AN-140', 145, 147),
                ('AN-148', 150, 160), 
                ('AN-225', 240, 230)
                ]

engine.fields = ('name', 'price', 'efficiency')
engine.domain = [
               #name, price (millions Euro), efficiency (%)
               ('Ivchenko AI-14', 1.4, 30.1), 
               ('Ivchenko AI-26', 2.6, 32.2),
               ('MotorSich MD-18T', 1.8, 31.5),
               ('MotorSich MS400', 2.1, 33.4),
               ('MotorSich D-436TP', 2.4, 34.2),
               ('MotorSich D-27', 2.7, 35.7)
               ]

# suppose that we can chose Fuel Octane Number as a continuous variable 
FuelOctaneNumber = oovar('Fuel Octane Number') 

# suppose fuel consumption is 
fuelConsumption = 4000 / (engine.efficiency * FuelOctaneNumber) 
# suppose annual profit is
annualProfit = (20 - aircraft.price - fuelConsumption)('annual profit')
# define initial payment
initialPayment = (aircraft.price + engine.price)('initial payment')

a_name, e_name = aircraft.name, engine.name

constraints = [
               FuelOctaneNumber > 30, FuelOctaneNumber < 105, 

              # suppose for AN-15 FuelOctaneNumber has to be less than 100
               ifThen(a_name == 'AN-15', FuelOctaneNumber < 100), 
               # suppose for AN-140 only MotorSich MD-18T, Ivchenko AI-14 or MotorSich D-436TP are suitable
               ifThen(a_name == 'AN-140', 
                      (e_name == 'MotorSich MD-18T') | (e_name == 'Ivchenko AI-14') | (e_name == 'MotorSich D-436TP')), 
               # suppose for AN-138 engine MotorSich D-27 is not suitable; we could use  
               #ifThen(aircraft == 'AN-138', engine != 'MotorSich D-27'), 
               # but let's assign it via NAND ("not and"), see FuncDesigner or interalg doc for  other funcs like AND, XOR, NOR etc
               NAND(a_name == 'AN-138', e_name == 'MotorSich D-27'), 
               # suppose for MotorSich MS400 fuelConsumption has to be at least 15.8:
               # we can use synonim "IMPLICATION" for ifThen:
               IMPLICATION(e_name == 'MotorSich MS400', fuelConsumption >= 15.8), 
               # suppose only Ivchenko AI-14 and MotorSich MD-18T can use fuel with octane number < 50:
               ifThen(FuelOctaneNumber < 50, (e_name == 'MotorSich MS400') | (e_name == 'MotorSich MD-18T')), 
               # suppose for AN-225 FuelOctaneNumber has to be at least 80 and fuelConsumption should be between 1.5 and 15
               ifThen(a_name == 'AN-225', FuelOctaneNumber > 80 ,  fuelConsumption > 1.5, fuelConsumption < 15)
               ]

# start point can have any coords, even infiasibl, 
# but for soma difficault problems a good start point matters for time elapsed

startPoint = {
              FuelOctaneNumber:80, 
              aircraft:0, # for categorical - position in domain, integer, from zero
              engine:-1 # may be negative, to start from last
              }

solver='interalg'
# or this solver with some non-default parameters:
#solver=oosolver('interalg', maxIter = 1000, maxNodes = 1000, maxActiveNodes = 15, sigma = 0.2, maxActiveNodes = 15)

# for variables without assigned lb <= x <= ub 
# +/-implicitBounds have to be used (or LB,UB, if implicitBounds is tuple (LB,UB))
# e.g. implicitBounds = (1, 2000) 
# we have provided lb and ub for FuelOctaneNumber, for discrete and bool variables they are not required

# we could define ordinary nonlinear problem:
p = NLP(annualProfit, startPoint, constraints = constraints, goal = 'max', fTol = 0.05)
#p = NLP(FuelOctaneNumber, startPoint,  goal = 'min', fTol = 0.05)
# but let's consider multiextremum problem: search for minimal initial payment and maximal annual profit
objectives = [
              # function, required accuracy, goal
              annualProfit, 0.05,'max', 
              initialPayment, 0.05, 'min'
              ]  
p = MOP(objectives, startPoint, constraints = constraints)
r = p.solve(solver, plot = False, iprint = 1, maxIter  = 400)

''' results for notebook Intel Atom 2 GHz:
------------------------- OpenOpt 0.5307 -------------------------
solver: interalg   problem: unnamed    type: MOP   goal: weak Pareto front
 ...
istop: 1001 (all solutions have been obtained)
Solver:   Time Elapsed = 1.47 	CPU Time Elapsed = 0.77
5 solutions have been obtained

to view list of solutions you could use print(r.solutions), it has 3 entries like
{aircraft: {'price': 15, 'capacity': 15, 'name': 'AN-15'}, engine: {'efficiency': 35.7, 'price': 2.7, 'name': 'MotorSich D-27'}, 
  Fuel Octane Number: 105.0, annual profit: 3.9329064959317073, initial payment: 17.7}
  
(unimplemented for new categorical variables yet) we could export it to Excel list via
r.export('/home/dmitrey/Aircrafts.xls')
(see result here: https://docs.google.com/spreadsheet/ccc?key=0Ak7GVY0fCdaidGY0ZkxqeEZMV1IyT3ViZGFBS2JhUWc)
'''
