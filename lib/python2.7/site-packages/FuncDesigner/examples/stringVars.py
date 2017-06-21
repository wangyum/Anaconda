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

aircraftsData = [
                # name; price (millions Euro); lifting capacity (tons)
                ('AN-15', 15, 15), 
                ('AN-30', 30, 30), 
                ('AN-70', 50, 45),
                ('AN-124', 200, 170),
                ('AN-138', 130, 140),
                ('AN-140', 145, 147),
                ('AN-148', 150, 160), 
                ('AN-225', 240, 230)
                ]

enginesData = [
               #name, price (millions Euro), efficiency (%)
               ('Ivchenko AI-14', 1.4, 30.1), 
               ('Ivchenko AI-26', 2.6, 32.2),
               ('MotorSich MD-18T', 1.8, 31.5),
               ('MotorSich MS400', 2.1, 33.4),
               ('MotorSich D-436TP', 2.4, 34.2),
               ('MotorSich D-27', 2.7, 35.7)
               ]

#aircraftPrice, enginePrice, aircraftCapacity, engineEfficiency = \
#oovars('aircraft price', 'engine price', 'aircraft capacity','engine efficiency')

aircraftPrice, enginePrice, aircraftCapacity, engineEfficiency = [oovar() for i in range(4)]

# interalg will work much faster if we define domain for these discrete variables
aircraftPrice.domain = [elem[1] for elem in aircraftsData] # 15, 30, 50,..., 240
# alternatively we could use numpy arrays and slices
enginePrice.domain = [elem[1] for elem in enginesData] # 1.4, 2.6, ...
aircraftCapacity.domain = [elem[2] for elem in aircraftsData] # 15, 30, ..., 230
engineEfficiency.domain = [elem[2] for elem in enginesData] # 30.1, 32.2, ..., 35.7

# suppose that we can chose Fuel Octane Number as a continuous variable 
FuelOctaneNumber = oovar('Fuel Octane Number') 

aircraftNames = [elem[0] for elem in aircraftsData] # ['AN-15', 'AN-30', ..., 'AN-225']
engineNames = [elem[0] for elem in enginesData] # ['Ivchenko AI-14', ..., 'MotorSich D-27']

# let's create 2 categorical variables:
aircraft = oovar('aircraft', domain = aircraftNames)
engine = oovar('engine', domain = engineNames) 

# suppose fuel consumption is 
fuelConsumption = 4000 / (engineEfficiency * FuelOctaneNumber) 
# suppose annual profit is
annualProfit = (20 - aircraftPrice - fuelConsumption)('annual profit')
# define initial payment
initialPayment = (aircraftPrice + enginePrice)('initial payment')

constraints = [
               FuelOctaneNumber > 30, FuelOctaneNumber < 105, 
               OR([(aircraft == Name) & (aircraftPrice == Price) & (aircraftCapacity == Capacity) for Name, Price, Capacity in aircraftsData]),
               OR([(engine == Engine) & (enginePrice == Price) & (engineEfficiency == Efficiency) for Engine, Price, Efficiency in enginesData]),
               
              # suppose for AN-15 FuelOctaneNumber has to be less than 100
               ifThen(aircraft == 'AN-15', FuelOctaneNumber < 100), 
               # suppose for AN-140 only MotorSich MD-18T, Ivchenko AI-14 or MotorSich D-436TP are suitable
               ifThen(aircraft == 'AN-140', 
                      (engine == 'MotorSich MD-18T') | (engine == 'Ivchenko AI-14') | (engine == 'MotorSich D-436TP')), 
               # suppose for AN-138 engine MotorSich D-27 is not suitable; we could use  
               #ifThen(aircraft == 'AN-138', engine != 'MotorSich D-27'), 
               # but let's assign it via NAND ("not and"), see FuncDesigner or interalg doc for  other funcs like AND, XOR, NOR etc
               NAND(aircraft == 'AN-138', engine == 'MotorSich D-27'), 
               # suppose for MotorSich MS400 fuelConsumption has to be at least 15.8:
               # we can use synonim "IMPLICATION" for ifThen:
               IMPLICATION(engine == 'MotorSich MS400', fuelConsumption >= 15.8), 
               # suppose only Ivchenko AI-14 and MotorSich MD-18T can use fuel with octane number < 50:
               ifThen(FuelOctaneNumber < 50, (engine == 'MotorSich MS400') | (engine == 'MotorSich MD-18T')), 
               # suppose for AN-225 FuelOctaneNumber has to be at least 80 and fuelConsumption should be between 1.5 and 15
               #ifThen(aircraft == 'AN-225', FuelOctaneNumber > 80, fuelConsumption > 1.5, fuelConsumption < 15)
               ifThen(aircraft == 'AN-225', FuelOctaneNumber > 80 ,  fuelConsumption > 1.5, fuelConsumption < 15)
               ]

# if you have defined aircraftPrice etc variables as discrete (via domain parameter), you can omit using tol
# elseware it's very recommended (e.g. (aircraftPrice == Price)(tol = 0.5); default tol is 10^-6

# alternatively you could use
# ifThen(aircraft == Name, (aircraftPrice == Price) & (aircraftCapacity == Capacity))
# or OR([(aircraft == Name) & (aircraftPrice == Price) & (aircraftCapacity == Capacity) for Name, Price, Capacity in aircraftsData]), 
# but formew way is works many times faster

# start point can have any coords, even infiasibl, but for soma difficault problems a good start point matters for time elapsed
startPoint = {aircraft:'AN-70', aircraftCapacity: 0.5, 
              engine:'MotorSich D-436TP', engineEfficiency: 4, 
              FuelOctaneNumber:80, enginePrice: 10, aircraftPrice: 100}

solver='interalg'
# or this solver with some non-default parameters:
#solver=oosolver('interalg', maxIter = 1000, maxNodes = 1000, maxActiveNodes = 15, sigma = 0.2, maxActiveNodes = 15)

# for variables without assigned lb <= x <= ub 
# +/-implicitBounds have to be used (or LB,UB, if implicitBounds is tuple (LB,UB))
# e.g. implicitBounds = (1, 2000) 
# we have provided lb and ub for FuelOctaneNumber, for discrete and bool variables they are not required

# we could define ordinary nonlinear problem:
p = NLP(annualProfit, startPoint, constraints = constraints, goal = 'max', fTol = 0.05)
# but let's consider multiextremum problem: search for minimal initial payment and maximal annual profit
objectives = [
              # function, required accuracy, goal
              annualProfit, 0.05,'max', 
              initialPayment, 0.05, 'min'
              ]  
p = MOP(objectives, startPoint, constraints = constraints)
r = p.solve(solver, plot = False, iprint = 1, maxIter  = 400)

''' results for notebook Intel Atom 2 GHz:
------------------------- OpenOpt 0.38 -------------------------
solver: interalg   problem: unnamed    type: MOP   goal: weak Pareto front
 iter   front length   income   outcome   
 ...
istop: 1001 (all solutions have been obtained)
Solver:   Time Elapsed = 12.69  CPU Time Elapsed = 12.3
4 solutions have been obtained
'''
# to view list of solutions you could use print(r.solutions), it has 3 entries like
#{aircraft price: 15.0, engine price: 2.7000000000000002, aircraft capacity: 15.0, engine efficiency: 35.700000000000003, 
#Fuel Octane Number: 99.680126627924992, aircraft: 'AN-15', engine: 'MotorSich D-27', annual profit: 3.8759563042551157, initial payment: 17.7}
# we could export it to Excel list via
# r.export('/home/dmitrey/Aircrafts.xls')
# (see result here: https://docs.google.com/spreadsheet/ccc?key=0Ak7GVY0fCdaidGY0ZkxqeEZMV1IyT3ViZGFBS2JhUWc)
