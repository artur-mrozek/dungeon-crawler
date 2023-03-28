import random
import os
from classes import Weapon, MagicalWeapon, Artifact


def shop(player):
    shop_items = []
    for i in range(5):
        item = None
        # 0 - weapon, 1 - magical_weapon, 2 - artifact
        item_type = random.randint(0, 2)

        match item_type:
            case 0:  # weapon
                weapon_names = ["Miecz", "Topór", "Włócznia", "Sztylet", "Maczuga"]
                name = random.choice(weapon_names)
                attack_power = random.randint(player.level + 10, player.level + 15)
                cost = random.randint(5, player.gold + 5)
                uses = random.randint(8, 15)
                item = Weapon(name, attack_power, cost, uses)
            case 1:  # magical_weapon
                weapon_names = ["Różdżka", "Laska"]
                name = random.choice(weapon_names)
                attack_power = random.randint(player.level, player.level + 5)
                cost = random.randint(5, player.gold + 5)
                uses = random.randint(8, 15)
                magical_power = random.randint(player.level + 10, player.level + 15)
                req_mana = random.randint(player.level + 40, player.level + 60)
                item = MagicalWeapon(name, attack_power, cost, uses, magical_power, req_mana)
            case 2:  # artifact
                artifact_names = ["Naszyjnik", "Pierścień"]
                name = random.choice(artifact_names)
                max_health = random.randint(player.level + 10, player.level + 15)
                mana = random.randint(player.level + 10, player.level + 15)
                strenght = random.randint(player.level + 10, player.level + 15)
                magical_power = random.randint(player.level + 10, player.level + 15)
                cost = random.randint(5, player.gold + 5)
                item = Artifact(name, max_health, mana, strenght, magical_power, cost)
        shop_items.append(item)

    while True:
        player.get_stats()
        player.get_equipment()
        print("Spotkałeś wędrownego handlarza...")

        counter = 1
        for item in shop_items:
            if type(item) == Weapon:
                print(
                    f"{counter} - {item.cost} złota, "
                    f"{item.name}, "
                    f"{item.attack_power} punktów ataku, "
                    f"{item.uses} użyć")
            elif type(item) == MagicalWeapon:
                print(
                    f"{counter} - {item.cost} złota, "
                    f"{item.name}, "
                    f"{item.attack_power} punktów ataku, "
                    f"{item.uses} użyć, "
                    f"{item.magical_power} mocy magicznej, "
                    f"{item.req_mana} wymaganej many")
            elif type(item) == Artifact:
                print(
                    f"{counter} - {item.cost} złota, "
                    f"{item.name}, "
                    f"{item.max_health} HP, "
                    f"{item.mana} many, "
                    f"{item.strenght} siły, "
                    f"{item.magical_power} mocy magicznej")
            counter = counter + 1
        print("0 - wyjdź")
        print(f"Złoto: {player.gold}\nWybierz przedmiot do kupienia")
        try:
            choice = int(input())
        except ValueError:
            os.system("cls")
            continue

        try:
            chosen_item = shop_items[choice - 1]
        except IndexError:
            os.system("cls")
            continue

        if choice == 0:
            os.system("cls")
            break
        else:
            if chosen_item.cost <= player.gold:
                if type(chosen_item) == Weapon or type(chosen_item) == MagicalWeapon:
                    while True:
                        os.system("cls")
                        try:
                            equip_or_to_inv = int(input(f"Kupiłeś {chosen_item.name}\n"
                                                        f"1 - Wyposaż broń\n2 - Schowaj do plecaka\n"))
                        except ValueError:
                            os.system("cls")
                            continue
                        if equip_or_to_inv == 1:
                            player.equip_weapon(chosen_item)
                            shop_items.remove(chosen_item)
                            os.system("cls")
                            break
                        elif equip_or_to_inv == 2:
                            player.equipment.append(chosen_item)
                            shop_items.remove(chosen_item)
                            os.system("cls")
                            break
                        else:
                            continue
                else:
                    player.equip_artifact(chosen_item)
                    shop_items.remove(chosen_item)
                    input(f"Kupiłeś {chosen_item.name}")
                    os.system("cls")

                player.gold = player.gold - chosen_item.cost
            else:
                print("Nie masz wystarczająco dużo złota")
                input()
                os.system("cls")
