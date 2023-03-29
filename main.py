import random
import os
from classes import Player, Enemy, Boss, Weapon, MagicalWeapon
from fight import fight
from shop import shop


def main():
    os.system("cls")
    enemy_names = ["Ork wojownik", "Ork szaman", "Ork łucznik", "Gobiln", "Wielki pająk", "Bandyta"]
    player = Player()

    for dung_lvl in range(1, 5):
        print(f"Wchodzisz do lochu nr {dung_lvl},\nTwoje statystyki to: ")

        player.get_stats()
        player.get_equipment()

        input()
        os.system("cls")

        rooms = range(1, random.randint(4, 6))
        for curr_room in rooms:
            print(f"Wchodzisz do pokoju nr {curr_room}")

            input()
            os.system("cls")

            if curr_room != len(rooms):
                enemy_health = (dung_lvl + curr_room + player.level) * (dung_lvl * 8)
                enemy_strenght = (dung_lvl + curr_room + player.level) * (dung_lvl * 2)
                enemy = Enemy(random.choice(enemy_names), enemy_health, enemy_strenght)
            else:
                enemy_health = (dung_lvl + curr_room + player.level) * (dung_lvl * 10)
                enemy_strenght = (dung_lvl + curr_room + player.level) * (dung_lvl * 2)
                enemy_super_attack_power = (dung_lvl + curr_room + player.level) * (dung_lvl * 2)
                enemy = Boss(random.choice(enemy_names), enemy_health, enemy_strenght, enemy_super_attack_power)

            win = fight(player, enemy)

            if win:
                found_gold = dung_lvl + curr_room + random.randint(3, 10)
                player.gold = player.gold + found_gold
                print(f"Znalazłeś {found_gold} złota")
                player.lvl_up()
                input()
                os.system("cls")
                continue
            else:
                break

        if player.health <= 0:
            break

        input(f"Ukończyłeś loch nr {dung_lvl}")

        if dung_lvl != 4:
            shop(player)

    if player.health <= 0:
        print("Nie żyjesz")
    else:
        print("Gratulacje, wygrałeś!")
    input()


if __name__ == "__main__":
    main()
