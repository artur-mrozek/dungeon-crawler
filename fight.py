import random
import os
from classes import Boss, Artifact


def fight(player, enemy):
    while player.health >= 0 or enemy.health >= 0:

        while True:
            if type(enemy) is not Boss:
                print(f"Walczysz z przeciwnikiem {enemy.name}\nTwoje HP: {player.health}\nTwoja mana: {player.mana}\n"
                      f"HP przeciwnika: {enemy.health}")
            else:
                print(f"Walczysz z bossem {enemy.name}\nTwoje HP: {player.health}\nTwoja mana: {player.mana}\n"
                      f"HP przeciwnika: {enemy.health}")

            try:
                choice = int(input("\n1 - Atakuj\n2 - Rzuć czar\n3 - Ulecz się\n"))
            except ValueError:
                os.system("cls")
                continue
            match choice:
                case 1:
                    player.attack(enemy)
                    break
                case 2:
                    if player.curr_magic_weapon is not None:
                        if player.mana >= player.curr_magic_weapon.req_mana:
                            player.curr_magic_weapon.magic_attack(player, enemy)
                            break
                        elif player.mana < player.curr_magic_weapon.req_mana:
                            print("Nie masz wystaczająco dużo many")
                            input()
                            os.system("cls")
                            continue
                    else:
                        print("Nie posiadasz magicznej broni")
                        input()
                        os.system("cls")
                        continue
                case 3:
                    if player.health == player.max_health:
                        input("Masz już maksymalną ilość zdrowia")
                        os.system("cls")
                        continue
                    healed = False
                    for item in player.equipment:
                        if type(item) == Artifact:
                            item.heal(player)
                            healed = True
                            break
                    if not healed:
                        print("Nie posiadasz żadnych artefaktów, które mogłyby cię uleczyć")
                        input()
                        os.system("cls")
                        continue
                    else:
                        break
                case _:
                    os.system("cls")
                    continue

        if enemy.health <= 0:
            input("Przeciwnik pokonany!")
            os.system("cls")
            break

        if type(enemy) == Boss:
            chance = random.uniform(0.0, 10.0)
            if chance <= 2.5:
                enemy.super_attack(player)
            else:
                enemy.attack(player)
        else:
            enemy.attack(player)

        if player.health <= 0:
            break

        input()
        os.system("cls")

    if enemy.health <= 0:
        player.mana = player.max_mana
        return True
    else:
        return False
