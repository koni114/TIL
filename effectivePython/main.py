fresh_fruit = {
    '사과': 10,
    '바나나': 8,
    '레몬': 5
}

fresh_fruit

def make_lemonade(count):
    print("레모네이드를 만들어냅니다!")

def out_of_stuck(count):
    print("재고 소진!")


count = fresh_fruit.get('레몬', 0)
if count:
    make_lemonade(count)
else:
    out_of_stuck(count)


if count := fresh_fruit.get('레몬', 0):
    make_lemonade(count)
else:
    out_of_stuck(count)
