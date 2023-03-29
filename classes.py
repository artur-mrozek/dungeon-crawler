import random
import os


class Player:
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.strenght = 20
        self.magical_power = 20
        self.level = 1
        self.gold = 0
        self.equipment = []
        self.curr_weapon = None
        self.curr_magic_weapon = None

    def attack(self, enemy):
        enemy.health = enemy.health - self.strenght
        print(f"Zadałeś {self.strenght} obrażeń przeciwnikowi {enemy.name}, zostało mu {enemy.health} HP")
        if self.curr_weapon is not None:
            self.curr_weapon.uses = self.curr_weapon.uses - 1
            if self.curr_weapon.uses <= 0:
                self.curr_weapon.weapon_break(self)

    def equip_weapon(self, weapon):
        if type(weapon) == MagicalWeapon:
            if self.mana >= weapon.req_mana:
                if self.curr_magic_weapon is not None:
                    self.equipment.append(self.curr_magic_weapon)
                    self.remove_weapon(self.curr_magic_weapon)
                    self.curr_magic_weapon = None
                self.magical_power = self.magical_power + weapon.magical_power
                self.strenght = self.strenght + weapon.attack_power
                self.curr_magic_weapon = weapon
            else:
                print("Nie masz wytarczająco dużo many")
        if type(weapon) == Weapon:
            if self.curr_weapon is not None:
                self.equipment.append(self.curr_weapon)
                self.remove_weapon(self.curr_weapon)
                self.curr_weapon = None
            self.curr_weapon = weapon
            self.strenght = self.strenght + weapon.attack_power

    def remove_weapon(self, weapon):
        if type(weapon) == Weapon:
            self.strenght = self.strenght - weapon.attack_power
            self.curr_weapon = None
        if type(weapon) == MagicalWeapon:
            self.magical_power = self.magical_power - weapon.magical_power
            self.strenght = self.strenght - self.curr_magic_weapon.attack_power
            self.curr_magic_weapon = None

    def equip_artifact(self, artifact):
        self.max_health = self.max_health + artifact.max_health
        self.health = self.max_health
        self.max_mana = self.max_mana + artifact.mana
        self.mana = self.max_mana
        self.strenght = self.strenght + artifact.strenght
        self.magical_power = self.magical_power + artifact.magical_power
        self.equipment.append(artifact)

    def open_equipment(self):
        i = 0
        items = ""
        for item in self.equipment:
            items.join(f"{i}: {item} ")

    def lvl_up(self):
        self.level = self.level + 1
        self.max_health = self.max_health + random.randint(40, 60)
        self.max_mana = self.max_mana + random.randint(10, 15)
        self.strenght = self.strenght + random.randint(10, 15)
        self.magical_power = self.magical_power + random.randint(10, 15)
        self.health = self.max_health
        self.mana = self.max_mana
        print("Otrzymałeś kolejny poziom, twoje statystyki wzrastają, a życie i mana regenerują się...")
        self.get_stats()
        self.get_equipment()

    def get_curr_weapon(self):
        if self.curr_weapon is None:
            return "Brak"
        else:
            return self.curr_weapon

    def get_curr_maigc_weapon(self):
        if self.curr_magic_weapon is None:
            return "Brak"
        else:
            return self.curr_magic_weapon

    def get_equipment(self):
        print("Ekwipunek: ")
        counter = 1
        if self.equipment:
            for item in self.equipment:
                if type(item) == Weapon:
                    print(f"{counter} - {item.name}, Atak: {item.attack_power}, Wytrzymałość: {item.uses}")
                elif type(item) == MagicalWeapon:
                    print(f"{counter} - {item.name}, Atak: {item.attack_power}, Moc Magiczna: {item.magical_power}, "
                          f"Wymagagana mana: {item.req_mana}, "
                          f"Wytrzymałość: {item.uses}")
                else:
                    print(f"{counter} - {item.name}, HP: {item.max_health}, Mana: {item.mana}, Siła: {item.strenght}, "
                          f"Moc magiczna: {item.magical_power}")
                counter = counter + 1
        else:
            print("Pusty")
        print("")

    def get_stats(self):
        print(f"HP: {self.health}/{self.max_health}\n"
              f"Mana: {self.mana}/{self.max_mana}\n"
              f"Siła: {self.strenght}\n"
              f"Moc magiczna: {self.magical_power}\n"
              f"LVL: {self.level}\n"
              f"Złoto: {self.gold}")

        if self.curr_weapon is not None:
            print(
                  f"Broń biała: {self.get_curr_weapon().name}, "
                  f"Atak: {self.get_curr_weapon().attack_power}, "
                  f"Wytrzymałość: {self.get_curr_weapon().uses}")
        else:
            print("Broń biała:" + self.get_curr_weapon())

        if self.curr_magic_weapon is not None:
            print(
                  f"Broń magiczna: {self.get_curr_maigc_weapon().name}, "
                  f"Atak: {self.get_curr_maigc_weapon().attack_power}, "
                  f"Moc Magiczna: {self.get_curr_maigc_weapon().magical_power}, "
                  f"Wymagagana mana: {self.get_curr_maigc_weapon().req_mana}, "
                  f"Wytrzymałość: {self.get_curr_maigc_weapon().uses}\n")
        else:
            print("Broń magiczna:" + self.get_curr_maigc_weapon() + "\n")


class Enemy:
    def __init__(self, name, health, strenght):
        self.name = name
        self.health = health
        self.strenght = strenght

    def attack(self, player):
        dmg = self.strenght + random.randint(player.level * 2, player.level * 3)
        player.health = player.health - dmg
        print(f"Przeciwnik {self.name} zadał ci {dmg} obrażeń, zostało ci {player.health} HP")


class Boss(Enemy):
    def __init__(self, name, health, strenght, super_attack_power):
        super().__init__(name, health, strenght)
        self.super_attack_power = super_attack_power

    def super_attack(self, player):
        player.health = player.health - (self.super_attack_power * 2)
        print(f"Boss {self.name} zadał ci {self.strenght * 2} obrażeń super atakiem, zostało ci {player.health} HP")


class Weapon:
    def __init__(self, name, attack_power, cost, uses):
        self.name = name
        self.attack_power = attack_power
        self.cost = cost
        self.uses = uses

    def weapon_break(self, player):
        player.remove_weapon(self)

        input("Twoja broń uległa zniszczeniu")

        while True:
            if player.equipment:
                os.system("cls")
                print("Twoja broń uległa zniszczeniu")
                player.get_equipment()
                print("0 - Wyjdź")

                try:
                    choice = int(input("Wybierz nową broń z ekwipunku:\n"))
                except ValueError:
                    os.system("cls")
                    continue

                if choice == 0:
                    os.system("cls")
                    break

                try:
                    new_weapon = player.equipment[choice - 1]
                except IndexError:
                    os.system("cls")
                    continue

                if type(new_weapon) != type(self):
                    input("To nie jest broń!")
                    os.system("cls")
                    continue

                if type(new_weapon) == Weapon:
                    player.curr_weapon = new_weapon
                else:
                    player.curr_magic_weapon = new_weapon
                player.equipment.remove(new_weapon)
                input("Wyposażyłeś nową broń")
                os.system("cls")
                break
            else:
                break


class MagicalWeapon(Weapon):
    def __init__(self, name, attack_power, cost, uses, magical_power, req_mana):
        super().__init__(name, attack_power, cost, uses)
        self.magical_power = magical_power
        self.req_mana = req_mana

    def magic_attack(self, player, enemy):
        if player.mana >= self.req_mana:
            enemy.health = enemy.health - player.magical_power
            player.mana = player.mana - self.req_mana
            self.uses = self.uses - 1
            print(f"Zadałeś {player.magical_power} obrażeń przeciwnikowi {enemy.name}, "
                  f"zostało mu {enemy.health} HP")
            if self.uses <= 0:
                self.weapon_break(player)
        else:
            print("Nie masz wystarczająco dużo many")


class Artifact:
    def __init__(self, name, max_health, mana, strenght, magical_power, cost):
        self.name = name
        self.max_health = max_health
        self.mana = mana
        self.strenght = strenght
        self.magical_power = magical_power
        self.cost = cost

    def heal(self, player):
        counter = 0
        for item in player.equipment:
            if type(item) == Artifact:
                counter = counter + 1
        if counter > 0:
            if player.health + self.max_health < player.health:
                player.health = player.health + self.max_health
                input(f"Artefakt uleczył cię o {counter} HP")
            else:
                player.health = player.max_health
                input(f"Artefakt w pełni cię uleczył")
