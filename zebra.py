from z3 import *

House, houses = EnumSort("House", "red green ivory yellow blue".split())
red_house, green_house, ivory_house, yellow_house, blue_house = houses

Nation, (england, spain, ukraine, norway, japan) = \
    EnumSort("Nation", "england spain ukraine norway japan".split())

Beverage, (coffee, tea, milk, juice, water) = \
    EnumSort("Drink", "coffee tea milk juice water".split())

Pet, (dog, snails, fox, horse, zebra) = \
    EnumSort("Pet", "dog snails fox horse zebra".split())

Smoke, (oldgold, kools, chesterfields, luckystrikes, parliaments) = \
    EnumSort("Smoke", "oldgold kools chesterfields luckystrikes parliaments".split())

nationality = Function("nationality", House, Nation)

drinks = Function("drinks", House, Beverage)

pet = Function("pet", House, Pet)

smokes = Function("smokes", House, Smoke)

house_number = Function("house_number", House, IntSort())

h, g = Consts('h g', House)

solver = Solver()
solver.add(
    # 1. There are five houses.
    ForAll(h, And(house_number(h) >= 1, house_number(h) <=5)),

    # 2. The Englishman lives in the red house.
    nationality(red_house) == england,

    # 3. The Spaniard owns the dog.
    ForAll(h, Implies(nationality(h) == spain, pet(h) == dog)),

    # 4. Coffee is drunk in the green house.
    drinks(green_house) == coffee,

    # 5. The Ukrainian drinks tea.
    ForAll(h, Implies(nationality(h) == ukraine, drinks(h) == tea)),

    # 6. The green house is immediately to the right of the ivory house.
    house_number(green_house) == house_number(ivory_house) + 1,

    # 7. The Old Gold smoker owns snails.
    ForAll(h, Implies(smokes(h) == oldgold, pet(h) == snails)),

    # 8. Kools are smoked in the yellow house.
    smokes(yellow_house) == kools,

    # 9. Milk is drunk in the middle house.
    ForAll(h, Implies(house_number(h) == 3, drinks(h) == milk)),

    # 10. The Norwegian lives in the first house.
    ForAll(h, Implies(nationality(h) == norway, house_number(h) == 1)),

    # 11. The man who smokes Chesterfields lives in the house next to the man with the fox.
    ForAll([h, g], Implies(
        And(smokes(h) == chesterfields, pet(g) == fox),
        Or(house_number(h) == house_number(g) + 1, house_number(h) == house_number(g) - 1)
    )),

    # 12. Kools are smoked in the house next to the house where the horse is kept.
    ForAll([h, g], Implies(
        And(smokes(h) == kools, pet(g) == horse),
        Or(house_number(h) == house_number(g) + 1, house_number(h) == house_number(g) - 1)
    )),

    # 13. The Lucky Strike smoker drinks orange juice.
    ForAll(h, Implies(smokes(h) == luckystrikes, drinks(h) == juice)),

    # 14. The Japanese smokes Parliaments.
    ForAll(h, Implies(nationality(h) == japan, smokes(h) == parliaments)),

    # 15. The Norwegian lives next to the blue house.
    ForAll(h, Implies(
        nationality(h) == norway,
        Or(house_number(h) == house_number(blue_house) + 1, house_number(h) == house_number(blue_house) - 1)
    )),

    # In the interest of clarity, it must be added that each of the five
    # houses is painted a different color, and their inhabitants are of
    # different national extractions, own different pets, drink different
    # beverages and smoke different brands of American cigarets [sic].
    ForAll([h, g], Implies(
        h != g,
        And(
            house_number(h) != house_number(g),
            nationality(h) != nationality(g),
            pet(h) != pet(g),
            drinks(h) != drinks(g),
            smokes(h) != smokes(g),
        )
    ))
)

# Now, who drinks water? Who owns the zebra?

the_water_house = Const("the_water_house", House)
the_zebra_house = Const("the_zebra_house", House)
solver.add(drinks(the_water_house) == water)
solver.add(pet(the_zebra_house) == zebra)

assert solver.check() == sat

model = solver.model()

print("The person who drinks water")
print(f"lives in the {model.eval(the_water_house)} house")
print(f"which is number {model.eval(house_number(the_water_house))} from the left,")
print(f"is from {model.eval(nationality(the_water_house))},")
print(f"smokes {model.eval(smokes(the_water_house))},")
print(f"and has (a) pet {model.eval(pet(the_water_house))}.\n\n")

print("The person with the zebra")
print(f"lives in the {model.eval(the_zebra_house)} house")
print(f"which is number {model.eval(house_number(the_zebra_house))} from the left,")
print(f"is from {model.eval(nationality(the_zebra_house))},")
print(f"smokes {model.eval(smokes(the_zebra_house))},")
print(f"and drinks {model.eval(drinks(the_zebra_house))}.")
