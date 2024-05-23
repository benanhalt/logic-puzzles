from z3 import *

solver = Solver()

Girl, girls = EnumSort("Girl", "savannah gloria carmelita".split())
savannah, gloria, carmelita = girls

Bag, bags = EnumSort("Bag", "green black yellow".split())
green, black, yellow = bags

Dest, dests = EnumSort("Dest", "france panama america".split())
france, panama, america = dests

Title, titles = EnumSort("Title", "ms_france ms_panama ms_america".split())
ms_france, ms_panama, ms_america = titles

bag = Function('bag', Girl, Bag)
solver.add(Distinct([bag(g) for g in girls]))
for g in girls:
    solver.add(Or(*[bag(g) == b for b in bags]))

dest = Function('dest', Girl, Dest)
solver.add(Distinct([dest(g) for g in girls]))
for g in girls:
    solver.add(Or(*[dest(g) == d for d in dests]))

title = Function('title', Girl, Title)
solver.add(Distinct([title(g) for g in girls]))
for g in girls:
    solver.add(Or(*[title(g) == t for t in titles]))

american = Const('american', Girl)
french = Const('french', Girl)
panamanian = Const('panamanian', Girl)
solver.add(
    title(american) == ms_america,
    dest(american) != america,

    title(french) == ms_france,
    dest(french) != france,

    title(panamanian) == ms_panama,
    dest(panamanian) != panama,
)

solver.add(
    savannah != american,
    dest(savannah) != america,
    bag(savannah) != yellow,
    bag(american) == yellow,
)

solver.add(
    bag(carmelita) != black,
)

yellow_case = Const('yellow_case', Girl)
solver.add(
    Or(
        And(dest(yellow_case) == panama, savannah == american),
        And(dest(savannah) == panama, yellow_case == american),
    )
)

solver.add(
    gloria != american,
    dest(gloria) != france,
    bag(gloria) != black,
)

print(solver.check())
print(solver.model())
