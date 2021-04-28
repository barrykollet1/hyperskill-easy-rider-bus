import itertools

for a, b in zip(itertools.product(main_courses, desserts, drinks), itertools.product(price_main_courses, price_desserts, price_drinks)):
    if sum(b) <= 30:
        print(*a, sum(b))
