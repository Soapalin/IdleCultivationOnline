import json
import sys
import time
import random
import os

import Character
import CO_Skills
import GameController

class MainMenu:
    def __init__(self, player_save):
        self.player_save = player_save
        self.load_player()

        self.timestamp = time.time()


    def load_player(self):
        with open(self.player_save) as f:
            data = json.load(f)

        self.player = Character.Character(
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

    def save_player(self):
        character = self.player

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
            "skillset": character.skillset
        }

        filename = f"./characters/{character.name}_{character.id}.json"
        with open(filename, "w") as f:
            json.dump(character_details, f)



    def menu_options(self):
        return "\n===== MAIN MENU =====\n\n1. Stats\n2. Shop\n3. Alliances\n4. Explore\n5. Qi Gain\n6. Breakthrough\nChoose an option: "

    def show_stats(self):
        print("\n========== Character Stats ==========\n")
        print(f"Name: {self.player.name}")
        print("\n===== Cultivation Stats =====")
        print(f"Cultivation Realm: {Character.CultivationRealm(self.player.realm)} {Character.RealmLevel(self.player.level)}")
        # print(f"Qi: {int(self.player.qi)}/{int(self.player.max_qi)}")
        self.show_qi_gain()

        print("\n===== Combat Stats =====")
        print(f"Attack: {self.player.attack}")
        print(f"Magic Attack: {self.player.mattack}")
        print(f"Defence: {self.player.defence}")
        print(f"Magic Defence: {self.player.mdefence}")
        print(f"Speed: {self.player.speed}")
        print(f"Health Points: {self.player.max_hp}")
        print(f"Magic Points: {self.player.max_mp}")
        print(f"Stamina Points: {self.player.max_sp}")

        print("\n===== Skill Set =====")
        index = 1
        for skill in self.player.skillset:
            current_skill = CO_Skills.skill_dictionary[skill]
            print(f"{index}. {current_skill.name}")
            index += 1
        print("\n")


    def show_shop(self):
        print("Shop not available yet")


    def show_alliance(self):
        print("Alliances not available yet")


    def explore(self):
        enemy_dir = "./enemies"
        enemy_list = os.listdir(enemy_dir)

        enemy = f"enemies/{random.choice(enemy_list)}"
        gc = GameController.GameController(character=self.player_save, enemies_dir=enemy)
        gc.main()


    def calculate_qi_gain(self):
        now = time.time()
        elapsed = int(now - self.timestamp)

        gain = elapsed*self.player.idle_increase
        self.player.qi_gain(gain)

        self.timestamp = now
        return gain

    def player_cultivation(self):
        return f"{Character.CultivationRealm(self.player.realm)} {Character.RealmLevel(self.player.level)}"

    def show_player_banner(self):
        print(f"{self.player.name} | {self.player_cultivation()}")
    
    def show_qi_gain(self):
        result = "Qi: ["
        star = int((self.player.qi / self.player.max_qi)*20)
        if star > 20:
            star = 20
        for i in range(star):
            result += "*"
        for j in range(20-star):
            result += "-"
        result += f"] {int((self.player.qi / self.player.max_qi)*100)}% | {format(int(self.player.qi), ',')}/{format(int(self.player.max_qi), ',')}"
        print(result)

    def initiate_breakthrough(self):
        if self.player.can_breakthrough():
            success = self.player.breakthrough()
            if success:
                print(f"Success! You have broken through to {self.player_cultivation()} ")
                return True
            else:
                qi_backlash = 0.1*self.player.qi
                self.player.qi_loss(qi_backlash)
                print(f"Failure! You have received Qi backlash. -{int(qi_backlash)} Qi.")
                return False
        else:
            self.show_qi_gain()
            print("Cannot breakthrough due to insufficient Qi.")
            return False


    def main(self):
        while(True):
            option = input(self.menu_options())
            option = option.lower()
            self.calculate_qi_gain()
            if option in ["stat", "stats", "1"]:
                self.show_stats()
                self.save_player()
            elif option in ["shop", "2"]:
                self.show_shop()
            elif option in ["alliance", "alliances", "3"]:
                self.show_alliance()
            elif option in ["explore", "4"]:
                self.save_player()
                self.explore()
                self.load_player()
            elif option in ["gain", "qi", "qi_gain", "qi gain", "5"]:
                print("\n")
                self.show_player_banner()
                self.show_qi_gain()
                self.save_player()
            elif option in ["breakthrough", "6"]:
                success = self.initiate_breakthrough()
                print("\n")
                self.show_player_banner()
                self.show_qi_gain()
                self.save_player()
            elif option in ["exit", "0"]:
                self.save_player()
                sys.exit()


player_save = "characters/Suiren_5bc62a3c-43e1-4611-9ab6-18f33a980d03.json"
mm = MainMenu(player_save=player_save)

mm.main()