def remainder(number, divisor):
    return number % divisor


assert remainder(20, 7) == 6


remainder(20, 7)
remainder(20, divisor=7)
remainder(divisor=7, number=20)

my_kwargs = {
    "number": 20,
    "divisor": 7
}

remainder(** my_kwargs)

my_kwargs = {
    "divisor": 7
}

remainder(number=20, ** my_kwargs)
