votes = {
    '바게트': ['철수', '순이'],
    '치아바타': ['하니', '유리']
}
key = '브리오슈'
who = '단이'

names = votes.get(key, [])
names.append(who)


if key in votes:
    names = votes[key]
else:
    votes[key] = names = []
names.append(who)
print(votes)

try:
    names = votes[key]
except KeyError:
    votes[key] = names = []
names.append(who)

names = votes.get(key, [])
names.append(who)

names = votes.setdefault(key, [])
names.append(who)

data = {}
key = 'foo'
value = []
data.setdefault(key, value)
print('이전 : ', data)
value.append('hello')
print('이후 : '. data)


count = counters.setdefault(key, 0)
counters[key] = count + 1