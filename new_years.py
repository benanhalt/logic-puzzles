from z3 import *

solver = Solver()

Wife, wives = EnumSort("Wife", "cindy mary pauline susan".split())
(cindy, mary, pauline, susan) = wives

Husband, husbands = EnumSort("Husband", "george mick stanley todd".split())
(george, mick, stanley, todd) = husbands

Resolution, resolutions = EnumSort("Resolution", "car cook island weight".split())
(car, cook, island, weight) = resolutions

Name, names = EnumSort("Name", "clark douglas humphrey stills".split())
(clark, douglas, humphrey, stills) = names

wife = Function('wife', Name, Wife)
solver.add(Distinct([wife(n) for n in names]))
for n in names:
    solver.add(Or(*[wife(n) == w for w in wives]))

husband = Function('husband', Name, Husband)
solver.add(Distinct([husband(n) for n in names]))
for n in names:
    solver.add(Or(*[husband(n) == h for h in husbands]))

resolution = Function('resolution', Name, Resolution)
solver.add(Distinct([resolution(n) for n in names]))
for n in names:
    solver.add(Or(*[resolution(n) == r for r in resolutions]))

name_clue1 = Const('name_clue1', Name)
solver.add(
    husband(name_clue1) == todd,
    resolution(name_clue1) == cook
)

solver.add(
    husband(clark) != george,
    resolution(clark) == island,
)

for n in names:
    solver.add(Not(And(wife(n) == mary, husband(n) == mick)))

name_clue3 = Const('name_clue3', Name)
solver.add(Not(And(husband(name_clue3) == stanley, resolution(name_clue3) == car)))

solver.add(
    wife(douglas) == cindy,
    resolution(douglas) != weight,
)

for n in names:
    solver.add(Not(And(wife(n) == susan, husband(n) == george)))

solver.add(
    resolution(stills) == car,
    husband(humphrey) == todd,
    wife(stills) != pauline,
    wife(humphrey) != pauline,
)

solver.add(
    husband(stills) == stanley,
    wife(stills) != susan,
)

