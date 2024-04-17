from enum import Enum
import uuid
import json
import random
import os


import CO_Skills


class RealmLevel(Enum):
    I = 0
    II = 1
    III = 2
    IV = 3
    V = 4
    VI = 5
    VII = 6
    VIII = 7
    IX = 8
    X = 9


class CultivationRealm(Enum):
    APPRENTICE = 0
    WARRIOR = 1
    MASTER = 2
    GRANDMASTER = 3
    LORD = 4
    KING = 5
    EMPEROR = 6
    SOVEREIGN = 7


class BaseCharacterStats:
    def __init__(self, realm, level):
        self.realm = realm
        self.level = level
        self.attack = 5
        self.m_attack = 0
        self.defence = 3
        self.m_defence = 0
        self.speed = 6
        self.hp = 100
        self.sp = 100
        self.mp = 100

        self.qi = 100

    def baseAttack(self):
        attack = self.attack
        if self.realm == 0 and self.level == 0:
            return attack
        if self.realm == 0 and self.level == 1:
            attack = attack + 10
            return attack
        mortal = True
        for i in range(self.realm+1):
            for j in range(10):
                if i == self.realm and j == self.level:
                    return attack
                if j == 0 and mortal is False:
                    attack = attack + (i+1)*10*10*(i+1)
                else:
                    mortal = False
                    attack = attack + (i+1)*10*(i+1)
        return attack

    def baseCultivationStat(self, base):
        return base
    
    def baseHP(self, base):
        stat = base
        if self.realm == 0 and self.level == 0:
            return stat
        if self.realm == 0 and self.level == 1:
            stat = stat + 10
            return stat
        mortal = True
        for i in range(self.realm+1):
            for j in range(10):
                if i == self.realm and j == self.level:
                    return stat
                if j == 0 and mortal is False:
                    stat = stat + (i+1)*10*10*(i+1)*2
                else:
                    mortal = False
                    stat = stat + (i+1)*10*(i+1)*2
        return stat

    def baseCombatStat(self, base):
        stat = base
        if self.realm == 0 and self.level == 0:
            return stat
        if self.realm == 0 and self.level == 1:
            stat = stat + 10
            return stat
        mortal = True
        for i in range(self.realm+1):
            for j in range(10):
                if i == self.realm and j == self.level:
                    return stat
                if j == 0 and mortal is False:
                    stat = stat + (i+1)*10*10*(i+1)
                else:
                    mortal = False
                    stat = stat + (i+1)*10*(i+1)
        return stat
    

class Character:
    def __init__(self, id, name, att, matt, defence, mdefence, speed, hp, stamina, magica, qi, realm, level, skillset, max_qi=None, idle_increase=None, tap_incrase=None):
        self.id = id
        self.name = name
        self.attack = att
        self.mattack = matt
        self.defence = defence
        self.mdefence = mdefence
        self.speed = speed

        self.max_hp = hp
        self.max_sp = stamina
        self.max_mp = magica

        self.hp = hp
        self.sp = stamina
        self.mp = magica

        self.qi = qi
        self.realm = realm
        self.level = level
        if max_qi is None:
            self.max_qi  = self.maxQiPerLevel()
        
        if idle_increase is None:
            self.idle_increase = self.calculate_idle()
        else:
            self.idle_increase = idle_increase

        if tap_incrase is None:
            self.tap_increase = self.calculate_tap()
        else:
            self.tap_increase = tap_incrase

        self.skillset = skillset

    
    def receive_damage(self, damage):
        self.hp = self.hp - damage
        return self.is_dead()

    def is_dead(self):
        if self.hp > 0:
            return False
        else: 
            return True
        
    def qi_gain(self, gain):
        self.qi = self.qi + gain
    
    def qi_loss(self, loss):
        if loss >=  self.qi:
            self.qi = 0
        else:
            self.qi = self.qi - loss

    def can_breakthrough(self):
        if self.qi >= self.max_qi:
            return True
        else:
            return False
        
    def breakthrough(self):
        if RealmLevel(self.level)  == RealmLevel.X:
            self.realm = self.realm + 1
            self.level = 0
            self.all_stat_increase(major=True)
        else:
            self.level = self.level + 1 
            self.all_stat_increase(major=False)

        self.qi = self.qi - self.max_qi 
        self.max_qi = self.maxQiPerLevel()
        self.idle_increase = self.calculate_idle()
        self.tap_increase = self.calculate_tap()
        return True
    
    def all_stat_increase(self, major=False):
        cultivation = self.realm
        if major is True:
            self.attack  = self.attack + (cultivation+1)*10*10*(cultivation+1)
            self.mattack = self.mattack + (cultivation+1)*10*10*(cultivation+1)
            self.defence = self.defence + (cultivation+1)*10*10*(cultivation+1)
            self.mdefence = self.mdefence + (cultivation+1)*10*10*(cultivation+1)
            self.speed = self.speed + (cultivation+1)*10*10*(cultivation+1)
            self.max_hp = (self.max_hp + (cultivation+1)*10*10*(cultivation+1))*2
            self.max_sp = self.max_sp + (cultivation+1)*10*(cultivation+1)*2
            self.max_mp = self.max_sp + (cultivation+1)*10*(cultivation+1)*2
            self.hp = self.max_hp
            self.sp = self.max_sp
            self.mp = self.max_mp
        else:
            self.attack  = self.attack + (cultivation+1)*10*(cultivation+1)
            self.mattack = self.mattack + (cultivation+1)*10*(cultivation+1)
            self.defence = self.defence + (cultivation+1)*10*(cultivation+1)
            self.mdefence = self.mdefence + (cultivation+1)*10*(cultivation+1)
            self.speed = self.speed + (cultivation+1)*10*(cultivation+1)
            self.max_hp = self.max_hp + (cultivation+1)*10*(cultivation+1)*2
            self.max_sp = self.max_sp + (cultivation+1)*10*(cultivation+1)*2
            self.max_mp = self.max_sp + (cultivation+1)*10*(cultivation+1)*2
            self.hp = self.max_hp
            self.sp = self.max_sp
            self.mp = self.max_mp


    def calculate_idle(self):
        idleIncrease = 1
        mortal = True
        for i in range(self.realm+1):
            for j in range(10):
                if i == self.realm and j == self.level:
                    return idleIncrease
                if j == 0 and mortal is False:
                    idleIncrease = idleIncrease + (i * 10 + 20)/10
                else:
                    mortal = False
                    idleIncrease = idleIncrease + (i * 10 + (20-j))/10

        return idleIncrease
    
    def calculate_tap(self):
        tapIncrease = 3
        mortal = True
        for i in range(self.realm+1):
            for j in range(10):
                if i == self.realm and j == self.level:
                    return tapIncrease
                if j == 0 and mortal is False:
                    tapIncrease = tapIncrease + (i * 10 + 20)/10
                else:
                    mortal = False
                    tapIncrease = tapIncrease + (i * 10 + (20-j))/10

        return tapIncrease

    def maxQiPerLevel(self):
        maxQi = 250
        mortal = True
        for i in range(self.realm+1):
            for j in range(10):
                if i == self.realm and j == self.level:
                    return maxQi
                if j == 0 and mortal is False:
                    maxQi = maxQi*2.8 + 2500
                else:
                    mortal = False
                    maxQi = maxQi * 1.1 + 1000

        return maxQi
        

class CreateCharacter:
    def __init__(self, path=None):
        if path is None:
            self.path = ""
        else: 
            self.path = path

    def createRandomCharacter(self, name, realm=None, level=None, qi=None, attack=None, defence=None, m_attack=None, m_defence=None, speed=None, hp=None, sp=None, mp=None, skillset=None):
        id = str(uuid.uuid4())
        if realm is None:
            realm = random.randint(0,8)
        if level is None:
            level = random.randint(0,10)
        base = BaseCharacterStats(realm,level)
        if qi is None:
            factor = random.uniform(0.8, 1.5)
            qi = base.baseCultivationStat(base.qi) * factor

        if attack is None:
            factor = random.uniform(0.8, 1.5)
            attack = base.baseCombatStat(base.attack) * factor

        if defence is None:
            factor = random.uniform(0.8, 1.5)
            defence = base.baseCombatStat(base.defence) * factor

        if m_attack is None:
            factor = random.uniform(0.8, 1.5)
            m_attack = base.baseCombatStat(base.m_attack) * factor

        if m_defence is None:
            factor = random.uniform(0.8, 1.5)
            m_defence = base.baseCombatStat(base.m_defence) * factor

        if speed is None:
            factor = random.uniform(0.8, 1.5)
            speed = base.baseCombatStat(base.speed) * factor

        if hp is None:
            factor = random.uniform(0.8, 1.5)
            hp = base.baseHP(base.hp) * factor

        if sp is None:
            factor = random.uniform(0.8, 1.5)
            sp = base.baseCombatStat(base.sp) * factor

        if mp is None:
            factor = random.uniform(0.8, 1.5)
            mp = base.baseCombatStat(base.mp) * factor

        if skillset is None:
            skillset = []
            for i in range(4):
                skillset.append(random.randint(0, len(CO_Skills.skill_dictionary)-1))

        character_details = {
            "id": id,
            "name": name,
            "realm": realm,
            "level": level,
            "qi": int(qi),
            "attack": int(attack),
            "defence": int(defence),
            "magicAttack": int(m_attack),
            "magicDefence": int(m_defence),
            "speed": int(speed),
            "hp": int(hp),
            "sp": int(sp),
            "mp": int(mp),
            "skillset": skillset

        }

        filename = f"{name}_{id}.json"

        with open(os.path.join(self.path, filename), "w") as f:
            json.dump(character_details, f)

    def createFromCMD(self):
        print("===== Character Creation Center =====")
        print("Leave blank if you'd like it to be randomised")
        name = input("Name of Character: ")
        id = input("Character ID:")
        if id == "":
            id = str(uuid.uuid4())
            print(id)

        print("=== Stats ===")
        realm = input("Cultivation Realm (0-7): ")
        level = input("Cultivation Level (1-10):")
        qi = input("Qi Reserve: ")

        attack = input("Attack: ")
        defence = input("Defence: ")
        m_attack = input("Magic Attack: ")
        m_defence = input("Magic Defence: ")
        speed = input("Speed: ")


        hp = input("Health: ")
        sp = input("Stamina: ")
        mp = input("Magica: ")


        print("=== Skillset ===")
        skillset = []
        for i in range(6):
            skillset.append(input(f"Move {i+1}: "))

        print("=== Moves ===\n" + "\n".join(skillset))
        filename = f"{name}_{id}.json"
        print(f"Saving to {filename}...")

        character_details = {
            "id": id,
            "name": name,
            "realm": realm,
            "level": level,
            "qi": qi,
            "attack": attack,
            "defence": defence,
            "magicAttack": m_attack,
            "magicDefence": m_defence,
            "speed": speed,
            "hp": hp,
            "sp": sp,
            "mp": mp,

        }

        with open(filename, "w") as f:
            json.dump(character_details, f)




# base = BaseCharacterStats(realm=0, level=0)
# print(base.baseCombatStat(base=base.attack))
# base = BaseCharacterStats(realm=0, level=1)
# print(base.baseCombatStat(base=base.attack))
# base = BaseCharacterStats(realm=0, level=2)
# print(base.baseCombatStat(base=base.attack))
# base = BaseCharacterStats(realm=0, level=3)
# print(base.baseCombatStat(base=base.attack))



# create = CreateCharacter()
# create.createRandomCharacter("Suiren", realm=0, level=0)
# create.createRandomCharacter("Zangetsu", realm=0, level=0)
# create.createFromCMD()

