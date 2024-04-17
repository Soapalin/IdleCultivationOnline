import os
import json
import random
import sys

import Character
import CO_Skills



class GameController:
    def __init__(self, character, allies_dir=None, enemies_dir=None):
        self.battlename = "BATTLE"
        self.character = character

        if allies_dir is not None:
            self.allies_dir = allies_dir
        else:
            self.allies_dir = ""

        if enemies_dir is not None:
            self.enemies_dir = enemies_dir
        else:
            self.enemies_dir = ""


    def load_ally_from_file(self):
        pass

    def load_enemy_from_file(self):
        with open(self.enemies_dir) as f:
            data = json.load(f)

        self.enemy = Character.Character(
            id = data['id'],
            name = data['name'],
            att = data['attack'],
            matt = data['magicAttack'],
            defence = data['defence'],
            mdefence = data['magicDefence'],
            speed = data['speed'],
            hp = data['hp'],
            stamina = data['sp'],
            magica = data['mp'],
            qi = data["qi"],
            realm = data["realm"],
            level = data["level"],
            skillset = data["skillset"]
        )

    def load_char_from_file(self):
        with open(self.character) as f:
            data = json.load(f)

        self.main_character = Character.Character(
            id = data['id'],
            name = data['name'],
            att = int(data['attack']),
            matt = int(data['magicAttack']),
            defence = int(data['defence']),
            mdefence = int(data['magicDefence']),
            speed = int(data['speed']),
            hp = int(data['hp']),
            stamina = int(data['sp']),
            magica = int(data['mp']),
            qi = int(data["qi"]),
            realm = int(data["realm"]),
            level = int(data["level"]),
            skillset = data["skillset"]
        )

    def create_battle(self):
        self.battlename = input("Battle Name: ")
        self.allies_nb = input("Number of Allies: ")
        for i in range(self.allies_nb):
            file = ""
            while(file != "" and not os.path.exists(file)):
                file = input(f"Ally{i} Filename: ")
            self.allies.append([])

        self.enemies_nb = input("Number of Enemies: ")

    def health_bar(self, character):
        result = character.name + ": ["
        hp_ratio = int((int(character.hp) / int(character.max_hp)) *10)
        # print(f"hp_ratio: {character.hp}/{character.max_hp} * 10")
        if hp_ratio > 10:
            hp_ratio = 10
        if hp_ratio < 0:
            hp_ratio = 0
        for i in range(hp_ratio):
            result += "*"

        for j in range(10 - hp_ratio):
            result += "-"

        result += f"] {int(character.hp)}/{int(character.max_hp)}"

        return result


    def player_options(self):
        print("Actions available:")
        index = 1
        for skill in self.main_character.skillset:
            print(f"{index}. {CO_Skills.skill_dictionary[skill].name}")
            index += 1

    def damage_calculator(self, skill, attacker, defender):
        skill_id_used = attacker.skillset[int(skill)-1] # SkillsID
        skill_used = CO_Skills.skill_dictionary[skill_id_used] # Skill
        if skill_id_used == CO_Skills.SkillsID.NO_SKILL:
            return 0

        print("\n")
        print(f"{attacker.name} used {skill_used.name}!")

        phys_damage_reduction = defender.defence/((skill_used.attack/100+1)*attacker.attack)
        phys_damage = skill_used.attack+attacker.attack - (skill_used.attack+attacker.attack)*phys_damage_reduction
        if phys_damage < 0:
            phys_damage = 0 
        print(f"phys_damage: {phys_damage}")

        magic_damage_reduction = defender.mdefence/((skill_used.mattack/100+1)*attacker.mattack)
        magic_damage = skill_used.mattack+attacker.mattack - (skill_used.mattack+attacker.mattack)*magic_damage_reduction
        print(f"magic_damage: {magic_damage}")
        if magic_damage < 0:
            magic_damage = 0 

        damage = phys_damage + magic_damage


        print(f"{attacker.name} dealt {int(damage)} to {defender.name}")
        return damage

    def buff_calculator(self, skill, attacker, defender):
        pass

    def qi_rewards(self, winner, loser):
        enumerator = (loser.realm+1)*10+(loser.level+1)
        denominator = (winner.realm+1)*10+(winner.level+1)
        # print(f"e/d: {enumerator}/{denominator}")
        percentage = (2/denominator) * (enumerator/denominator)
        # print(percentage)
        return winner.max_qi * percentage

    def save_character(self, character, dir):
        character_details = {
            "id": character.id,
            "name": character.name,
            "realm": character.realm,
            "level": character.level,
            "qi": int(character.qi),
            "attack": int(character.attack),
            "defence": int(character.defence),
            "magicAttack": int(character.mattack),
            "magicDefence": int(character.mdefence),
            "speed": int(character.speed),
            "hp": int(character.max_hp),
            "sp": int(character.max_sp),
            "mp": int(character.max_mp),
            "skillset": character.skillset,
        }

        filename = f"./{dir}/{character.name}_{character.id}.json"
        with open(filename, "w") as f:
            json.dump(character_details, f)

    def save_progress(self):
        self.save_character(self.main_character, "characters")
        self.save_character(self.enemy, "enemies")

    def show_progression_bar(self, ratio):
        nb_of_cross = int(ratio*20)
        result = "Qi: ["
        for i in range(nb_of_cross):
            result += "*"
        for j in range(20-nb_of_cross):
            result += "-"
        result += f"] {int(ratio*100)}%"
        print(result)


    def check_battle_outcome(self):
        if self.enemy.is_dead():
            print("\n===== BATTLE OUTCOME =====\n")
            print(f"{self.health_bar(self.main_character)} vs {self.health_bar(self.enemy)}")
            gain = self.qi_rewards(self.main_character, self.enemy)
            print(f"{self.enemy.name} was slain. You have received {int(gain)} Qi.")
            self.main_character.qi_gain(gain)

            if self.main_character.can_breakthrough():
                self.main_character.breakthrough()
                print(f"Congratulations! You have broken through to {Character.CultivationRealm(self.main_character.realm)} {Character.RealmLevel(self.main_character.level)}")
            print(f"Qi: {int(self.main_character.qi)}/{int(self.main_character.max_qi)}")
            self.show_progression_bar(self.main_character.qi/self.main_character.max_qi)
            return True

        if self.main_character.is_dead():
            print("===== BATTLE OUTCOME =====")
            print(f"{self.health_bar(self.main_character)} vs {self.health_bar(self.enemy)}")
            loss = 0.05*self.main_character.qi
            self.main_character.qi_loss(loss)
            print(f"You were killed by {self.enemy.name}. You have lost {int(loss)} Qi.")
            gain = self.qi_rewards(self.enemy, self.main_character)
            self.enemy.qi_gain(gain)
            self.save_progress()
            return True

        return False

    def main(self):
        self.load_ally_from_file()
        self.load_enemy_from_file()
        self.load_char_from_file()
        print(f"===== {self.battlename} =====")
        print(f"===== {self.main_character.name} vs {self.enemy.name} =====")

        print(f"Enemy Strength: {Character.CultivationRealm(self.enemy.realm)} {Character.RealmLevel(self.enemy.level)}")

        round_index = 1
        finished = False
        while(not self.main_character.is_dead() and not self.enemy.is_dead()):
            print(f"\n===== ROUND {round_index} =====\n")
            print(f"{self.health_bar(self.main_character)} vs {self.health_bar(self.enemy)}")
            self.player_options()
            action = input("What do you want to do (1-4): ")
            while action not in ["1", "2", "3", "4"]:
                action = input("What do you want to do (1-4): ")
            if self.main_character.speed > self.enemy.speed:
                damage = self.damage_calculator(action, self.main_character, self.enemy)
                self.enemy.receive_damage(damage)
                finished = self.check_battle_outcome()
                if not finished:
                    enemy_action = random.randint(1,4)
                    damage = self.damage_calculator(enemy_action, self.enemy, self.main_character)
                    self.main_character.receive_damage(damage)
            else:
                enemy_action = random.randint(1,4)
                damage = self.damage_calculator(enemy_action, self.enemy, self.main_character)
                self.main_character.receive_damage(damage)
                finished = self.check_battle_outcome()
                if not finished:
                    damage = self.damage_calculator(action, self.main_character, self.enemy)
                    self.enemy.receive_damage(damage)

            if finished is False:
                self.check_battle_outcome()
            round_index += 1


        self.save_progress()


# main_c = "characters/Suiren_75f1a6f5-2733-4d02-8808-98db180ab739.json"
# gc = GameController(character=main_c, enemies_dir=enemy)
# gc.main()