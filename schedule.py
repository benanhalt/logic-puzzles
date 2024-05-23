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

Period, periods = make_enum("Period", "first second third fourth")
Class, classes = make_enum("Class", "algebra art chem english")
Teacher, teachers = make_enum("Teacher", "mason schiller thomlinson xavier")
Room, rooms = make_enum("Room", "room112 room113 room115 room218")

period_ordinal, period_ordinal_asserts = make_ordinal("period_ordinal", Period)

cls, cls_asserts = make_onetoone("class", Period, Class)
teacher, teacher_asserts = make_onetoone("teacher", Period, Teacher)
room, room_asserts = make_onetoone("room", Period, Room)

solver = Solver()

solver.add(*period_ordinal_asserts, *cls_asserts, *teacher_asserts, *room_asserts)


room218_period = Const('room218_period', Period)
mason_period = Const('mason_period', Period)
solver.add(
    room(room218_period) == rooms.room218,
    teacher(mason_period) == teachers.mason,
    period_ordinal(room218_period) < period_ordinal(mason_period),
)

room112_period = Const('room112_period', Period)
xavier_period = Const('xavier_period', Period)
solver.add(
    room(room112_period) == rooms.room112,
    teacher(xavier_period) == teachers.xavier,
    period_ordinal(room112_period) == period_ordinal(xavier_period) + 1,
)

art_period = Const('art_period', Period)
solver.add(
    cls(art_period) == classes.art,
    room(art_period) != rooms.room112,
    cls(periods.fourth) != classes.art,
    room(periods.fourth) != rooms.room112,
)

solver.add(
    cls(periods.fourth) == classes.chem,
)

solver.add(
    Or(
        And(teacher(art_period) == teachers.thomlinson, art_period != periods.third),
        And(teacher(art_period) != teachers.thomlinson, art_period == periods.third),
    ),
)

english_period = Const('english_period', Period)
schiller_period = Const('schiller_period', Period)
solver.add(
    cls(english_period) == classes.english,
    teacher(schiller_period) == teachers.schiller,
    english_period != schiller_period,
    Or(
        And(room(english_period) == rooms.room113, schiller_period == periods.first),
        And(room(schiller_period) == rooms.room113, english_period == periods.first),
    ),
)

alg_period = Const('alg_period', Period)
solver.add(
    cls(alg_period) == classes.algebra,
    teacher(alg_period) != teachers.thomlinson,
)


def get_solutions(solver, indep_var, *dep_vars):
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        solutions.append(m)

        solver.add(Or([
            v(p) != m.eval(v(p))
            for p in get_elems(indep_var)
            for v in dep_vars
        ]))
    return solutions

print(get_solutions(solver, Period, teacher, room, cls))
