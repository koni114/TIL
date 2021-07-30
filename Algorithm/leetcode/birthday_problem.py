import random
TRIALS = 100000    #- 10만번 실험
same_birthdays = 0 #- 생일이 같은 실험의 수

#- 10만 번 실험 진행
for _ in range(TRIALS):
    birthdays = []
    for i in range(23):
        birthday = random.randint(1, 365)
        if birthday in birthdays:
            same_birthdays += 1
            break
        birthdays.append(birthday)

print(f"{same_birthdays / TRIALS * 100}%")
