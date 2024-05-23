from z3 import *
from collections import namedtuple

def make_enum(name, items):
    items = items.split()
    sort, consts = EnumSort(name, items)
    return sort, namedtuple(f"{name}Items", items)(*consts)

def get_elems(enum):
    return [enum.constructor(i)() for i in range(enum.num_constructors())]

def make_onetoone(name, domain, codomain):
    func = Function(name, domain, codomain)
    assertions = [
        Distinct([func(x) for x in get_elems(domain)]),
        *[
            Or([func(x) == y for y in get_elems(codomain)])
            for x in get_elems(domain)
        ]]
    return func, assertions

def make_ordinal(name, enum):
    func = Function(name, enum, IntSort())
    assertions = [
        func(enum.constructor(i)()) == i+1
        for i in range(enum.num_constructors())
    ]
    return func, assertions

def get_solutions(assertions, indep_var, *dep_vars):
    solver = Solver()
    solver.add(assertions)

    solutions = []
    while solver.check() == sat:
        m = solver.model()
        solutions.append([
            (p, *[m.eval(v(p)) for v in dep_vars])
            for p in get_elems(indep_var)
        ])

        solver.add(Or([
            v(p) != m.eval(v(p))
            for p in get_elems(indep_var)
            for v in dep_vars
        ]))
    return solutions


Kid, kids = make_enum("Kid", "antony philip george luc steven")
Flavor, flavors = make_enum("Flavor", "chocolate hazelnut strawberry vanilla watermelon coconut pistachio")
Time, times = make_enum("Time", "t400 t430 t500 t530 t600")

assertions = []
time_ordinal, time_ordinal_assertions = make_ordinal("time_ordinal", Time)
assertions += time_ordinal_assertions

first_flavor, ff_assertions = make_onetoone("first_flavor", Kid, Flavor)
assertions += ff_assertions

second_flavor, sf_assertions = make_onetoone("second_flavor", Kid, Flavor)
assertions += sf_assertions

time, time_assertions = make_onetoone("time", Kid, Time)
assertions += time_assertions

assertions += [
    a
    for k in kids
    for a in [
            first_flavor(k) != flavors.coconut,
            first_flavor(k) != flavors.pistachio,
            second_flavor(k) != flavors.hazelnut,
            second_flavor(k) != flavors.vanilla,
    ]
]

def is_fruit(flavor):
    return Or(flavor == flavors.watermelon, flavor == flavors.strawberry)

def both_fruit(kid):
    return And(is_fruit(first_flavor(kid)), is_fruit(second_flavor(kid)))

assertions += [
    both_fruit(k) if k is kids.george else Not(both_fruit(k))
    for k in kids
]

george_time = time_ordinal(time(kids.george))
assertions += [
    george_time < time_ordinal(time(kids.steven)),
    george_time == time_ordinal(time(kids.luc)) + 2,
]

assertions += [
    Or(
        first_flavor(kids.philip) == flavors.watermelon,
        first_flavor(kids.philip) == flavors.vanilla,
    ),
    Or(
        second_flavor(kids.philip) == flavors.coconut,
        second_flavor(kids.philip) == flavors.chocolate,
    )
]

hazelnut_chocolate = Const("hazelnut_chocolate", Kid)
assertions += [
    first_flavor(hazelnut_chocolate) == flavors.hazelnut,
    second_flavor(hazelnut_chocolate) == flavors.chocolate,
    time_ordinal(time(hazelnut_chocolate)) + 2 == time_ordinal(time(kids.steven)),
]

t400_kid = Const("t400_kid", Kid)
assertions += [
    time(t400_kid) == times.t400,
    second_flavor(t400_kid) == flavors.pistachio,
    first_flavor(t400_kid) != flavors.vanilla,
    first_flavor(t400_kid) != flavors.watermelon,
]

t600_kid = Const("t600_kid", Kid)
assertions += [
    second_flavor(kids.steven) == flavors.strawberry,
    time(t600_kid) == times.t600,
    second_flavor(t600_kid) == flavors.coconut,
]

assertions += [
    a
    for k in kids
    for a in [
            Not(And(first_flavor(k) == flavors.chocolate, second_flavor(k) == flavors.strawberry)),
            Not(And(first_flavor(k) == flavors.strawberry, second_flavor(k) == flavors.chocolate)),
    ]
]

print(get_solutions(assertions, Kid, first_flavor, second_flavor, time))
