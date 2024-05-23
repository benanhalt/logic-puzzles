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

solver = Solver()

# In the interest of clarity, it must be added that each of the five
# houses is painted a different color, and their inhabitants are of
# different national extractions, own different pets, drink different
# beverages and smoke different brands of American cigarets [sic].
solver.add(Distinct([house_number(h) for h in houses]))
solver.add(Distinct([nationality(h) for h in houses]))
solver.add(Distinct([pet(h) for h in houses]))
solver.add(Distinct([drinks(h) for h in houses]))
solver.add(Distinct([smokes(h) for h in houses]))


# 1. There are five houses.
solver.add([
    And(house_number(h) >= 1, house_number(h) <=5)
    for h in houses
])

# 2. The Englishman lives in the red house.
solver.add(nationality(red_house) == england)

# 3. The Spaniard owns the dog.
the_spaniards_house = Const("the_spaniards_house", House)
solver.add(nationality(the_spaniards_house) == spain)
solver.add(pet(the_spaniards_house) == dog)

# 4. Coffee is drunk in the green house.
solver.add(drinks(green_house) == coffee)

# 5. The Ukrainian drinks tea.
the_ukrainians_house = Const("the_ukrainians_house", House)
solver.add(nationality(the_ukrainians_house) == ukraine)
solver.add(drinks(the_ukrainians_house) == tea)

# 6. The green house is immediately to the right of the ivory house.
solver.add(house_number(green_house) == house_number(ivory_house) + 1)

# 7. The Old Gold smoker owns snails.
the_oldgold_house = Const("the_oldgold_house", House)
solver.add(smokes(the_oldgold_house) == oldgold)
solver.add(pet(the_oldgold_house) == snails)

# 8. Kools are smoked in the yellow house.
solver.add(smokes(yellow_house) == kools)

# 9. Milk is drunk in the middle house.
the_middle_house = Const("the_middle_house", House)
solver.add(house_number(the_middle_house) == 3)
solver.add(drinks(the_middle_house) == milk)

# 10. The Norwegian lives in the first house.
the_first_house = Const("the_first_house", House)
solver.add(house_number(the_first_house) == 1)
solver.add(nationality(the_first_house) == norway)

# 11. The man who smokes Chesterfields lives in the house next to the man with the fox.
the_chesterfield_house = Const("the_chesterfield_house", House)
the_fox_house = Const("the_fox_house", House)
solver.add(smokes(the_chesterfield_house) == chesterfields)
solver.add(pet(the_fox_house) == fox)
solver.add(
    Or(
        house_number(the_fox_house) == house_number(the_chesterfield_house) + 1,
        house_number(the_fox_house) == house_number(the_chesterfield_house) - 1,
    )
)

# 12. Kools are smoked in the house next to the house where the horse is kept.
the_kools_house = Const("the_kools_house", House)
the_horse_house = Const("the_horse_house", House)
solver.add(smokes(the_kools_house) == kools)
solver.add(pet(the_horse_house) == horse)
solver.add(
    Or(
        house_number(the_horse_house) == house_number(the_kools_house) + 1,
        house_number(the_horse_house) == house_number(the_kools_house) - 1,
    )
)

# 13. The Lucky Strike smoker drinks orange juice.
the_luckystrikes_house = Const("the_luckystrikes_house", House)
solver.add(smokes(the_luckystrikes_house) == luckystrikes)
solver.add(drinks(the_luckystrikes_house) == juice)

# 14. The Japanese smokes Parliaments.
the_japanese_house = Const("the_japanese_house", House)
solver.add(nationality(the_japanese_house) == japan)
solver.add(smokes(the_japanese_house) == parliaments)

# 15. The Norwegian lives next to the blue house.
the_norwegian_house = Const("the_norwegian_house", House)
solver.add(nationality(the_norwegian_house) == norway)
solver.add(
    Or(
        house_number(the_norwegian_house) == house_number(blue_house) + 1,
        house_number(the_norwegian_house) == house_number(blue_house) - 1,
    )
)

# Now, who drinks water? Who owns the zebra?

the_water_house = Const("the_water_house", House)
the_zebra_house = Const("the_zebra_house", House)
solver.add(drinks(the_water_house) == water)
solver.add(pet(the_zebra_house) == zebra)

# In the interest of clarity, it must be added that each of the five
# houses is painted a different color, and their inhabitants are of
# different national extractions, own different pets, drink different
# beverages and smoke different brands of American cigarets [sic].
solver.add(Distinct([nationality(h) for h in houses]))
solver.add(Distinct([drinks(h) for h in houses]))
solver.add(Distinct([pet(h) for h in houses]))
solver.add(Distinct([smokes(h) for h in houses]))
solver.add(Distinct([house_number(h) for h in houses]))

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
