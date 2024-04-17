from enum import IntEnum, Enum


class SkillsID(IntEnum):
    NO_SKILL = 0
    PALM_STRIKE = 1
    SWORD_STRIKE = 2
    MINOR_QI_STRIKE = 3
    MAJOR_QI_STRIKE = 4
    FLYING_KICK = 5
    QI_RAY = 6
    SWORD_DANCE = 7


    def __int__(self):
        return self.value

class Skill:
    def __init__(self, id, name, ccost, taboo, scost, mcost, acc, attack, defence, mattack, mdefence, speed, buff_func):
        self.id = id
        self.name = name
        self.cultivation_cost = ccost
        self.is_taboo = taboo
        self.stamina_cost = scost
        self.magic_cost = mcost
        self.accuracy = acc
        self.attack = attack
        self.defence = defence
        self.mattack = mattack
        self.mdefence = mdefence
        self.speed = speed
        self.buff_debuff_func = buff_func


class Skillset():
    def __init__(self):
        self.MAX_NUMBER_OF_SKILLS = 6
        self.skillset = [None] * self.MAX_NUMBER_OF_SKILLS

class Buff:
    class Subject:
        SELF = "SELF"
        ENEMY = "ENEMY"

    class Attribute:
        ATT = "ATT"
        MATT = "ATT"

    def __init__(self, subject, attribute, multiplier, duration):
        self.subject = subject # SELF or ENEMY
        self.attribute = attribute # what attribute is being buffed or debuffed
        self.multiplier = multiplier # <1 is a debuff, >1 is a buff
        self.duration = duration # how many turns. If zero, last until end of fight

class BuffList(Enum):
    SELF_ATT_PLUS = "ATT_PLUS" # increase attack until end of 
    SELF_ATT_PLUS_1_LOW = 1
    SELF_ATT_PLUS_2_MID = 2
    # SELF_ATT_PLUS_3_HIGH = 3
    SELF_ATT_PLUS_3_HIGH = Buff(Buff.Subject.SELF, Buff.Attribute.ATT, 1.5, 3)



skill_dictionary = [
    #     ID                                Name                    ccost   taboo     scost    mcost    acc    att    def    matt    mdef    speed    buff/debuff (function)
    Skill(SkillsID.NO_SKILL,                "None",                 0,      False,    0,       0,       0,     0,     0,     0,      0,      0,       None),
    Skill(SkillsID.PALM_STRIKE,             "PALM_STRIKE",          0,      False,    20,      10,      1,     10,    0,     5,      0,      1.2,     None),
    Skill(SkillsID.SWORD_STRIKE,            "SWORD_STRIKE",         0,      False,    30,      20,      1,     30,    0,     10,      0,      1.2,     None),
    Skill(SkillsID.MINOR_QI_STRIKE,         "MINOR_QI_STRIKE",      0,      False,    30,      20,      1,     10,    0,     30,     0,      1.2,     None),
    Skill(SkillsID.MAJOR_QI_STRIKE,         "MAJOR_QI_STRIKE",      0,      False,    30,      20,      1,     10,    0,     50,     0,      1.2,     None),
    Skill(SkillsID.FLYING_KICK,             "FLYING_KICK",          0,      False,    20,      20,      1,     25,    0,     0,      0,      1.2,     None),
    Skill(SkillsID.QI_RAY,                  "QI_RAY",               0,      False,    20,      20,      1,     0,     0,     80,     0,      1.2,     None),
    # Skill(SkillsID.SWORD_DANCE,             "SWORD_DANCE",          0,      False,    20,      20,      1,     0,     0,     0,      0,      1.2,     None),
]
