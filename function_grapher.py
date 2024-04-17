import matplotlib.pyplot as plt
from enum import Enum
import math


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



class FuncGraph:
    def __init__(self):
        pass


    def graph_one_func(self,x, y, name):
        plt.plot(x, y, label = name)


    def cultivation_increase(self):
        idle = []
        tap = []
        tapBreakthrough = []
        qi = []
        hours = []
        x = [i for i in range(0, 80)]

        idleIncrease = 1
        tapIncrease = 3
        maxQi = 250
        totalDays = 0
        mortal = True

        for cultivation in range(8):
            for level in range(10):
                print(f"{CultivationRealm(cultivation)} ({cultivation}) | {RealmLevel(level)}")
                if level == 0 and mortal is False:
                    maxQi = maxQi*2.8 + 2500
                    idleIncrease = idleIncrease + (cultivation * 10 + 20)/10
                    tapIncrease = tapIncrease + (cultivation * 10 + 20)/10
                else:
                    idleIncrease = idleIncrease + (cultivation * 10 + (20-level))/10
                    tapIncrease = tapIncrease + (cultivation * 10 + (20-level))/10
                    maxQi = maxQi * 1.1 + 1000
                    mortal = False

                print(f"idleIncrease: {idleIncrease}")
                print(f"tapIncrease: {tapIncrease}")
                print(f"maxQi: {maxQi:,}")
                print(f"Minutes taken to breakthrough: {(maxQi/idleIncrease)/60}")
                print(f"Hours taken to breakthrough: {((maxQi/idleIncrease)/60/60):,}")
                print(f"Days taken to breakthrough: {((maxQi/idleIncrease)/60/60/24):,}")
                print(f"Taps taken to breakthrough: {(maxQi/tapIncrease):,}\n")
                idle.append(idleIncrease)
                tap.append(tapIncrease)
                tapBreakthrough.append(maxQi/tapIncrease)
                qi.append(maxQi)
                hours.append((maxQi/idleIncrease)/60/60)
                totalDays += (maxQi/idleIncrease)/60/60/24

        print(f"Total Days: {totalDays:,}")
        print(f"Total Years: {(totalDays/365)}")

        plt.plot(x, idle, 1, label="idle")
        plt.plot(x, tap, 1, label="tap")
        plt.plot(x, qi, 1, label="qi")
        plt.plot(x, hours, 1, label="hours")
        plt.plot(x, tapBreakthrough, label="tapBreakthrough")
        plt.yscale("log")
        plt.legend()
        plt.title('Log values graph')
        plt.show()

        plt.plot(x, idle, 2, label="idle")
        plt.plot(x, tap, 2, label="tap")
        plt.plot(x, qi, 2, label="qi")
        plt.plot(x, hours, 2, label="hours")
        plt.legend()
        plt.title('Raw values graph')
        plt.tight_layout()
        plt.show()


    def combat_stat_increase(self):
        attack = 5
        m_attack = 0
        defence = 3
        m_defence = 0
        speed = 6
        hp = 100


        hp_list = []
        attack_list = []
        m_attack_list = []
        m_defence_list = []
        defence_list = []
        speed_list = []
        x = [i for i in range(0,80)]
        mortal = True

        for cultivation in range(8):
            for level in range(10):
                print(f"{CultivationRealm(cultivation)} ({cultivation}) | {RealmLevel(level)}")
                if level == 0 and mortal is False:
                    attack = attack + (cultivation+1)*10*10*(cultivation+1)
                    m_attack = m_attack + (cultivation+1)*10*10*(cultivation+1)
                    defence = defence + (cultivation+1)*10*10*(cultivation+1)
                    m_defence = m_defence + (cultivation+1)*10*10*(cultivation+1)
                    speed = speed + (cultivation+1)*10*10*(cultivation+1)
                    hp = (hp + (cultivation+1)*10*10*(cultivation+1))*2
                else:
                    mortal = False
                    attack = attack + (cultivation+1)*10*(cultivation+1)
                    m_attack = m_attack + (cultivation+1)*10*(cultivation+1)
                    defence = defence + (cultivation+1)*10*(cultivation+1)
                    m_defence = m_defence + (cultivation+1)*10*(cultivation+1)
                    speed = speed + (cultivation+1)*10*(cultivation+1)
                    hp = hp + (cultivation+1)*10*(cultivation+1)*2

                print(f"attack: {attack}")
                print(f"defence: {defence}")
                print(f"m_attack: {m_attack}")
                print(f"m_defence: {m_defence}")
                print(f"speed: {speed}")
                print(f"hp: {hp}")
                attack_list.append(attack)
                m_attack_list.append(m_attack)
                m_defence_list.append(m_defence)
                defence_list.append(defence)
                speed_list.append(speed)
                hp_list.append(hp)

        plt.plot(x, attack_list,  label="attack")
        plt.plot(x, m_attack_list,  label="m_attack")
        plt.plot(x, defence_list,  label="defence")
        plt.plot(x, m_defence_list,  label="m_defence")
        plt.plot(x, speed_list,  label="speed")
        plt.plot(x, hp_list,  label="hp")
        plt.yscale("log")
        plt.legend()
        plt.show()


    def exp_gain_increase(self):
        gain_percentage = 1/10

        for cultivation in range(8):
            for level in range(10):
                print(f"{CultivationRealm(cultivation)} ({cultivation}) | {RealmLevel(level)}")
                percentage = 2/((cultivation+1)*10+level)
                print(f"percentage gain; {percentage*100}")

        


    def main(self):
        # self.cultivation_increase()
        # self.combat_stat_increase()
        self.exp_gain_increase()


funcgraph = FuncGraph()
funcgraph.main()