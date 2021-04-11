# 파이썬 - OOP Part 5. 상속과 서브 클래스(Inheitance and Subclass)
# 상속 또한 한 번 정의한 데이터를 재활용 함으로써 반복되는 코드를 줄이고자 하는 목적

# 예제 - 게임 케릭터 만들면서 확인
# 만들고자 하는 케릭터는 다음과 같다
# 클래스
#  Hero, 랭크 : 영웅, 라이프 : 300, 사이즈 : big,
#        설명 : 상위 랭크의 케릭터로써 하위 랭크의 케릭터 소환

#  Goblin, 랭크 : 병사, 라이프 : 100, 사이즈: small
#  하위 랭크의 케릭터로써 상위 랭크의 케릭터에 의해 소환

# 1. 모든 케릭터가 가지게될 속성을 갖으며 모든 클래스의 베이스가 될 Unit 클래스 제작
#    Unit 클래스를 모든 속성을 상속받는 고블린 서브 클래스 제작

class Unit(object):
    def __init__(self, rank, life, size):
        self.name = self.__class__.__name__
        self.rank = rank
        self.life = life
        self.size = size

    def show_status(self):
        print('이름: {}'.format(self.name))
        print('등급: {}'.format(self.rank))
        print('사이즈: {}'.format(self.life))
        print('라이프: {}'.format(self.size))

class Goblin(Unit):
    pass

goblin_1 = Goblin('병사', 100, 'Small')
goblin_1.show_status()

# Unit 클래스의 하위 클래스인 Goblin 클래스는 어떠한 메소드나 속성을 정의 하지 않았는데도
# Unit 클래스안에 정의한 show_status 메소드를 상속받아 사용
# 그렇다면 Goblin 클래스가 자신의 네임스페이스 안에 show_status 메소드를 가지고 있을까?

print(Goblin.__dict__)

# 확인해본 결과, show_status 메소드를 가지고 있지 않다
# 그렇다면 어떻게 호출 했을까? help()를 이용해서 Goblin 클래스가 어떻게 show_status 메소드를
# 찾았는지 알아보자

print(help(Goblin))
# | Method resolution order: | Goblin | Unit | builtin.object
# 위와 같은 문구가 나오는데, 의미는 가장 먼저 자신의 네임 스페이스에서 찾고,
# 그 다음 부모 클래스인 Unit 클래스의 네임 스페이스를 뒤지고, 마지막으로 최상 클래스인
# 내장 오브젝트 클래스의 네임 스페이스를 참조한다!

#  Methods inherited from Unit:
#  |
#  |  __init__(self, rank, life, size)
#  |
#  |  show_status(self)

# 위의 문구를 보면, __init__, show_status 함수도 상속 받았다고 나옴

# 2. Goblin 클래스의 새로운 속성인 "공격 타입"을 추가하고자 한다

class Goblin(Unit):
    def __init__(self, rank, life, size, attack_type):
        super(Goblin, self).__init__(rank, size, life)
        self.attack_type = attack_type

    def show_status(self):
        super(Goblin, self).show_status()
        print('공격 타입: {}'.format(self.attack_type))


goblin_1 = Goblin('병사', 100, 'Small', '근접 공격')
goblin_1.show_status()

# 코드를 재활용해 새로 구현하는 것을 "override" 라고 한다
# ** overloading 은 함수의 인자를 새로 정의하는 것을 의미

# 3. 고블린 클래스에 공격 메소드와 데미지 속성을 추가
#    그리고 Goblin 클래스를 상속받는 sphereGoblin 클래스를 만들고
#    sphere_type 이라는 속성을 추가

class Goblin(Unit):
    def __init__(self, rank, life, size, attack_type, damage):
        super(Goblin, self).__init__(rank, life, size)
        self.attack_type = attack_type
        self.damage = damage

    def show_status(self):
        super(Goblin,self).show_status()
        print('공격 타입 {}'.format(self.attack_type))
        # 오버라이드 메소드
        print('데미지: {}'.format(self.damage))

    def attack(self):
        print('[{}]이 공격합니다! 상대방 데미지({})'.format(self.name, self.damage))

class SphereGoblin(Goblin):
    def __init__(self, rank, size, life, attack_type, damage, sphere_type):
        super(SphereGoblin, self).__init__(rank, life, size, attack_type, damage)
        self.sphere_type = sphere_type

    def show_status(self):
        super(SphereGoblin, self).show_status()
        print('창 타입 {}'.format(self.sphere_type))

sphere_goblin_1 = SphereGoblin('병사', 'Small', 100, '레인지 공격', 10, '긴 창')
sphere_goblin_1.show_status()

# SphereGoblin 클래스는 부모 클래스인 Goblin, 할아버지 클래스인 Unit 클래스에서
# 모든 속성과 메소드를 상속받은 것을 볼 수 있음
# 4. Goblin 케릭터를 거느릴 Hero 클래스를 만들어 보자

class Hero(Unit):
    def __init__(self, rank, size, life, goblins=None):
        super(Hero, self).__init__(rank, size, life)
        if goblins is None:
            self.goblins = []
        else:
            self.goblins = goblins

    def show_own_goblins(self):
        num_of_goblins = len([x for x in self.goblins if isinstance(x, Goblin)])
        num_of_sphere_goblins = len([x for x in self.goblins if isinstance(x, SphereGoblin)])
        print('현재 영웅이 소유한 고블린은 {}명, 창 고블린은 {}명입니다.'.format(num_of_goblins, num_of_sphere_goblins))

    def make_goblins_attack(self):
        for goblin in self.goblins:
            goblin.attack()

    def add_goblins(self, new_goblins):
        for goblin in new_goblins:
            if goblin not in self.goblins:
                self.goblins.append(goblin)
            else:
                print("이미 추가된 고블린 입니다.")

    def remove_goblins(self, old_goblins):
        for goblin in old_goblins:
            try:
                self.goblins.remove(goblin)
            except:
                print('{}을 소유하고 있지 않습니다.'.format(goblin))




# 고블린 오브젝트 형성
goblin_1 = Goblin('병사', 'Small', 100, '근접 공격', 15)
goblin_2 = Goblin('병사', 'Small', 100, '근접 공격', 15)
sphere_goblin_1 = SphereGoblin('병사', 'Small', 100, '레인지 공격', 10, '긴 창')

# 영웅 오브젝트 생성 후, 고블린 오브젝트 할당
hero_1 = Hero('영웅', 'Big', 300, [goblin_1, goblin_2, sphere_goblin_1])
hero_1.show_own_goblins()
hero_1.make_goblins_attack()

# Unit 클래스를 상속하는 Hero 클래스를 만들고 __init__()을 오버라이딩
# 자신이 소유하고 있는 고블린의 수를 표시하는 메소드와 소유한 고블린이 공격을 하도록 하는 메소드도 생성

# 4. 고블린을 추가하고 없애는 메소드를 만들어보자
