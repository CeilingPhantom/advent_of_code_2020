def a(lines):
    ingredient_appearances = {}
    allergen_possiblities = {}
    for line in lines:
        ingredients, allergens = line.split(" (contains ")
        ingredients = ingredients.split()
        for ingredient in ingredients:
            try:
                ingredient_appearances[ingredient] += 1
            except KeyError:
                ingredient_appearances[ingredient] = 1
        allergens = allergens[:-1].split(", ")
        for allergen in allergens:
            try:
                allergen_possiblities[allergen].intersection_update(ingredients)
            except KeyError:
                allergen_possiblities[allergen] = set(ingredients)
    nonallergen_ingredients = set(ingredient_appearances.keys())
    for _, ingredients in allergen_possiblities.items():
        nonallergen_ingredients.difference_update(ingredients)
    return sum(ingredient_appearances[ingredient] for ingredient in nonallergen_ingredients)

def b(lines):
    allergen_possiblities = {}
    for line in lines:
        ingredients, allergens = line.split(" (contains ")
        ingredients = ingredients.split()
        allergens = allergens[:-1].split(", ")
        for allergen in allergens:
            try:
                allergen_possiblities[allergen].intersection_update(ingredients)
            except KeyError:
                allergen_possiblities[allergen] = set(ingredients)
    # sort allergens alphabetically
    allergens_sorted = sorted(allergen_possiblities.keys())

    # determine which ingredient contains what allergen
    allergen_ingredient_dict = {}
    allergens_sorted_cp = allergens_sorted[:]
    while allergens_sorted_cp:
        i = 0
        allergen = allergens_sorted_cp[i]
        curr_determined_ingredients = allergen_ingredient_dict.values()
        diff = allergen_possiblities[allergen].difference(curr_determined_ingredients)
        while len(diff) != 1:
            i += 1
            allergen = allergens_sorted_cp[i]
            curr_determined_ingredients = allergen_ingredient_dict.values()
            diff = allergen_possiblities[allergen].difference(curr_determined_ingredients)
        allergen_ingredient_dict[allergens_sorted_cp[i]] = diff.pop()
        allergens_sorted_cp.pop(i)
    
    # get ingredients sorted by alphabetical order of allergens
    allergen_ingredients_sorted = []
    for allergen in allergens_sorted:
        allergen_ingredients_sorted.append(allergen_ingredient_dict[allergen])
    return ",".join(allergen_ingredients_sorted)

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))
