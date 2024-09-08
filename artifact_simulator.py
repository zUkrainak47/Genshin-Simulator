# This program is an artifact simulator!

# You can
# 1 - Roll artifacts one-by-one as if you have unlimited resin, upgrade them, save them to your inventory etc.
# 2 - Set a Crit Value requirement and roll artifacts automatically until an artifact with enough CV is found
#     to find out how long that takes - in days and years (assuming all of your resin goes into artifact farming)
#     You can also run multiple tests and find out the average amount of time that took!


import json
import time
import datetime

import numpy as np
import matplotlib.pyplot as plt
from colorama import init, Fore, Style
from operator import itemgetter
from random import choice, choices

from pathlib import Path

init()

# File and folder paths
file_to_move = Path('inventory.txt')
new_folder = Path('artifact_simulator_resources')
new_folder.mkdir(parents=True, exist_ok=True)

# Check if the file exists
if file_to_move.exists():
    # Define the new file path
    new_file_location = new_folder / file_to_move.name

    # Move the file
    file_to_move.rename(new_file_location)


class Artifact:
    def __init__(self, artifact_type, mainstat, mainstat_value, threeliner, sub_stats, level, artifact_set,
                 last_upgrade="", roll_value=0):
        self.type = artifact_type
        self.mainstat = mainstat
        self.mainstat_value = mainstat_value
        self.threeliner = threeliner
        self.substats = sub_stats
        self.level = level
        self.last_upgrade = last_upgrade
        self.set = artifact_set
        self.roll_value = roll_value

        if "CRIT Rate%" in self.substats:
            if self.substats["CRIT Rate%"] == 23.0:
                self.substats["CRIT Rate%"] = 22.9

    def short(self, really_short=False):
        val = (self.mainstat_value[0])[self.mainstat_value[1]]
        result = f"{val} {self.mainstat} {self.type} (+{self.level})"
        return result + ' '*(38 - len(result) - really_short*38) + f' - {sets_short_dict[self.set]} - '

    def __str__(self):
        val = (self.mainstat_value[0])[self.mainstat_value[1]]
        return f"{self.set}\n {val} {self.mainstat} {self.type} (+{self.level})"

    def subs(self):
        return {
            sub: round(self.substats[sub], 1)
            if "%" in sub else round(self.substats[sub])
            for sub in self.substats
        }

    def print_stats(self):

        # 311 ATK Feather (+20)
        # - HP: 418
        # - Crit DMG%: 14.8
        # - HP%: 14.6
        # - DEF%: 5.8
        print(" ", end='')
        print(self)

        for sub in self.substats:
            is_percentage = '%' in sub
            print(f" - {sub}: {str(round(self.substats[sub], 1)) if is_percentage else round(self.substats[sub])}{f' {Fore.GREEN}(+){Style.RESET_ALL}' if sub == self.last_upgrade else ''}")

        self.last_upgrade = ""
        print()

    def upgrade(self):
        if self.level != 20:
            roll = choice(possible_rolls)

            if self.threeliner:
                self.substats[self.threeliner] = max_rolls[
                                                     self.threeliner] * roll
                self.last_upgrade = self.threeliner
                self.threeliner = 0

            else:
                sub = choice(list(self.substats.keys()))
                self.substats[sub] += max_rolls[sub] * roll
                self.last_upgrade = sub

            self.level += 4
            self.mainstat_value[1] += 1
            self.roll_value += roll * 100

    def cv(self):
        crit_value = 0
        if "CRIT DMG%" in self.substats:
            # for eyeball:
            crit_value += round(self.substats["CRIT DMG%"], 1)
            # for cv like in akasha:
            # crit_value += self.substats["CRIT DMG%"]
        if "CRIT Rate%" in self.substats:
            # for eyeball:
            crit_value += round(self.substats["CRIT Rate%"], 1) * 2
            # for cv like in akasha:
            # crit_value += self.substats["CRIT Rate%"] * 2
        return round(crit_value, 1)

    def cv_real(self):
        crit_value = 0
        if "CRIT DMG%" in self.substats:
            # for eyeball:
            # crit_value += round(self.substats["CRIT DMG%"], 1)
            # for cv like in akasha:
            crit_value += self.substats["CRIT DMG%"]
        if "CRIT Rate%" in self.substats:
            # for eyeball:
            # crit_value += round(self.substats["CRIT Rate%"], 1) * 2
            # for cv like in akasha:
            crit_value += self.substats["CRIT Rate%"] * 2
        return round(crit_value, 1)

    def rv(self):
        return int(self.roll_value)


class ArtifactEncoder(json.JSONEncoder):
    def default(self, artifact):
        return [artifact.type, artifact.mainstat, artifact.mainstat_value, artifact.threeliner, artifact.substats,
                artifact.level, artifact.set, artifact.last_upgrade, artifact.roll_value]


def choose_one(items, error_message, alias={}):
    items_dict = dict(zip([str(ind) for ind in range(1, len(items)+1)], items))
    if isinstance(items_dict['1'], tuple) or isinstance(items_dict['1'], list):
        for item in items_dict.items():
            joined_item = ', '.join(item[1])
            print(f" {item[0]} = {joined_item}")
    else:
        for item in items_dict.items():
            print(f" {item[0]} = {item[1]}")
    print('\n (Type 0 to exit)\n')
    while True:
        new1 = input(' Your pick: ').strip()
        if new1 in ('0', 'exit'):
            return 0
        if new1 in items_dict or new1 in items_dict.values():
            break
        if alias and new1.lower() in alias:
            new1 = alias[new1]
            break
        else:
            print(f' {Fore.RED}{error_message}{Style.RESET_ALL}\n')
    if new1 in items_dict:
        new1 = items_dict[new1]
    return new1


sets = ("Gladiator's Finale", "Wanderer's Troupe",                                                             # bosses
        "Noblesse Oblige", "Bloodstained Chivalry", "Maiden Beloved", "Viridescent Venerer", "Archaic Petra",  # 1.x
        "Retracing Bolide", "Thundersoother", "Thundering Fury", "Lavawalker", "Crimson Witch of Flames",
        "Blizzard Strayer", "Heart of Depth", "Tenacity of the Millelith", "Pale Flame",
        "Shimenawa's Reminiscence", "Emblem of Severed Fate", "Husk of Opulent Dreams", "Ocean-Hued Clam",     # 2.x
        "Vermillion Hereafter", "Echoes of an Offering",
        "Deepwood Memories", "Gilded Dreams", "Desert Pavilion Chronicle", "Flower of Paradise Lost",          # 3.x
        "Nymph's Dream", "Vourukasha's Glow",
        "Marechaussee Hunter", "Golden Troupe", "Song of Days Past",                                           # 4.x
        "Nighttime Whispers in the Echoing Woods", "Fragment of Harmonic Whimsy", "Unfinished Reverie",
        "Scroll of the Hero of Cinder City", "Obsidian Codex", )                                               # 5.x
sort_order_sets = {set_name: len(sets)-number for number, set_name in enumerate(sets)}
sets_short = ('    Glad    ', '   Troupe   ',
              '  Noblesse  ', 'Bloodstained',
              '   Maiden   ', '     VV     ',
              '  Archaic   ', '   Bolide   ',
              '     TS     ', '     TF     ',
              ' Lavawalker ', '     CW     ',
              '  Blizzard  ', '    HoD     ',
              '    TotM    ', ' Pale Flame ',
              " Shimenawas ", '    EoSF    ',
              '    Husk    ', '    Clam    ',
              ' Vermillion ', '   Echoes   ',
              '  Deepwood  ', '   Gilded   ',
              ' Desert Pav ', '    FoPL    ',
              "   Nymphs   ", "Vourukasha's",
              '     MH     ', 'GoldenTroupe',
              '    SoDP    ', '    NWEW    ',
              '   Whimsy   ', '  Reverie   ',
              '   Scroll   ', '  Obsidian  ',)
aliases_domain = {'no': '1', 'nob': '1', 'noblesse': '1', 'bennett': '1',
                  'vv': '2', 'kazuha': '2',
                  'maidens': '2',
                  'ap': '3', 'petra': '3',
                  'bolide': '3',
                  'tf': '4', 'keqing': '4', 'razor': '4',
                  'cw': '5',
                  'blizzard': '6', 'ayaka': '6',
                  'hod': '6', 'childe': '6', 'tartaglia': '6',
                  'tom': '7', 'totm': '7', 'zl': '7', 'zhongli': '7',
                  'eula': '7',
                  'shim': '8', 'shime': '8', 'sr': '8', 'hu tao': '8', 'tao': '8',
                  'emblem': '8', 'eosf': '8', 'oppa': '8', 'xl': '8', 'raiden': '8', 'xiangling': '8', 'xingqiu': '8',
                  'xq': '8',
                  'husk': '9',
                  'clam': '9', 'kokomi': '9', 'kok': '9',
                  'vermillion': '10', 'vh': '10', 'zyox': '10', 'zy0x': '10', 'xiao': '10',
                  'echoes': '10', 'ayato': '10',
                  'deepwood': '11', 'dm': '11', 'nahida': '11',
                  'gilded': '11', 'gd': '11', 'alhaihtam': '11',
                  'dpc': '12', 'scara': '12', 'wanderer': '12', 'xіangling': '12',
                  'fopl': '12', 'flop': '12',
                  'vg': '13', 'dehya': '13',
                  'mh': '14', 'neuv': '14', 'neuvillette': '14', 'bat': '14',
                  'gt': '14', 'furina': '14', 'fischl': '14',
                  'sodp': '15', 'bird': '15', 'xianyun': '15', 'xy': '15',
                  'navia': '15',
                  'whimsy': '16', 'arle': '16', 'arlecchino': '16', 'father': '16', 'clorinde': '16',
                  'emilie': '16',
                  'natlan': '17', 'scroll': '17',
                  'codex': '17', 'mualani': '17'
                  }
aliases_sets = {'glad': '1',
                'troupe': '2',
                'no': '3', 'nob': '3', 'noblesse': '3', 'bennett': '3',
                'maidens': '5',
                'vv': '6', 'kazuha': '6',
                'ap': '7', 'petra': '7',
                'bolide': '8',
                'tf': '10', 'keqing': '10', 'razor': '10',
                'cw': '12',
                'blizzard': '13', 'ayaka': '13',
                'hod': '14', 'childe': '14', 'tartaglia': '14',
                'tom': '15', 'totm': '15', 'zl': '15', 'zhongli': '15',
                'eula': '16',
                'shim': "17", 'shime': "17", 'sr': "17", 'hu tao': "17", 'tao': "17",
                'emblem': '18', 'eosf': '18', 'oppa': '18', 'xl': '18', 'raiden': '18', 'xiangling': '18', 'xingqiu': '18',
                'xq': '18',
                'husk': '19',
                'clam': '20', 'kokomi': '20', 'kok': '20',
                'vermillion': '21', 'vh': '21', 'zyox': '21', 'zy0x': '21', 'xiao': '21',
                'echoes': '22', 'ayato': '22',
                'deepwood': '23', 'dm': '23', 'nahida': '23',
                'gilded': '24', 'gd': '24', 'alhaihtam': '24',
                'dpc': '25', 'scara': '25', 'wanderer': '25', 'xіangling': '25',
                'fopl': '26', 'flop': '26',
                'vg': "28", 'dehya': "28",
                'mh': '29', 'neuv': '29', 'neuvillette': '29', 'bat': '29',
                'gt': '30', 'furina': '30', 'fischl': '30',
                'sodp': '31', 'bird': '31', 'xianyun': '31', 'xy': '31',
                'navia': '32',
                'whimsy': '33', 'arle': '33', 'arlecchino': '33', 'father': '33', 'clorinde': '33',
                'emilie': '34',
                'natlan': '35', 'scroll': '35',
                'codex': '36', 'mualani': '36'
                }

sets_short_dict = dict(zip(sets, sets_short))
domains = list(list(s) for s in (zip(sets[2::2], sets[3::2])))
# print(domains)
artifact_types = ('Flower', 'Feather', 'Sands', 'Goblet', 'Circlet')
sands_main_stats = ('HP%', 'ATK%', 'DEF%', 'ER%', 'EM')
goblet_main_stats = ('Pyro DMG% Bonus', 'Hydro DMG% Bonus', 'Cryo DMG% Bonus',
                     'Electro DMG% Bonus', 'Anemo DMG% Bonus',
                     'Geo DMG% Bonus', 'Physical DMG% Bonus',
                     'Dendro DMG% Bonus', 'HP%', 'ATK%', 'DEF%', 'EM')
circlet_main_stats = ('HP%', 'ATK%', 'DEF%', 'EM', 'CRIT DMG%', 'CRIT Rate%',
                      'Healing Bonus')
substats = ('HP', 'ATK', 'DEF', 'HP%', 'ATK%', 'DEF%', 'ER%', 'EM', 'CRIT Rate%', 'CRIT DMG%')
type_to_main_stats = dict(zip(artifact_types, (('HP'), ('ATK'), sands_main_stats, goblet_main_stats, circlet_main_stats)))
flower_stats = (717, 1530, 2342, 3155, 3967, 4780)
feather_stats = (47, 100, 152, 205, 258, 311)
hp_atk_dmg_stats = (7.0, 14.9, 22.8, 30.8, 38.7, 46.6)
def_stats = (8.7, 18.6, 28.6, 38.5, 48.4, 58.3)
em_stats = (28, 60, 91, 123, 155, 187)
er_stats = (7.8, 16.6, 25.4, 34.2, 43.0, 51.8)
healing_bonus_stats = (5.4, 11.5, 17.6, 23.7, 29.8, 35.9)
crit_rate_stats = (4.7, 9.9, 15.2, 20.5, 25.8, 31.1)
crit_dmg_stats = (9.3, 19.9, 30.5, 41.0, 51.6, 62.2)
max_rolls = {
    'HP': 298.75,
    'ATK': 19.4501,
    'DEF': 23.1499,
    'HP%': 5.83333,
    'ATK%': 5.83333,
    'DEF%': 7.2899,
    'EM': 23.3099,
    'ER%': 6.4801,
    'CRIT Rate%': 3.8899,
    'CRIT DMG%': 7.7699
}
possible_rolls = (0.7, 0.8, 0.9, 1.0)
possible_cvs = [i / 10 for i in range(545)]

sands_main_stats_weights = (26.68, 26.66, 26.66, 10.0, 10.0)
goblet_main_stats_weights = (5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 19.25,
                             19.25, 19.0, 2.5)
circlet_main_stats_weights = (22.0, 22.0, 22.0, 4.0, 10.0, 10.0, 10.0)
substats_weights = (6, 6, 6, 4, 4, 4, 4, 4, 3, 3)


def take_input(defaults=(1, 50)):
    valid_exit = ('exit', "'exit'", '"exit"', '0', 'O')
    ok1 = False
    ok2 = False
    print("\n Please input conditions. Type 0 to go back.\n"
          f" Leave blank to use defaults ({defaults[0]} test{'s' if defaults[0] != 1 else ''}, {defaults[1]} CV).\n")

    while not ok1:
        size = input(" Number of tests to run: ")
        if size:
            if size.lower() in valid_exit:
                return 'exit', 0

            if size.isnumeric():
                ok1 = True
            else:
                print(f" {Fore.RED}Needs to be an integer. Try again{Style.RESET_ALL}\n")

        else:
            ok1 = True
            size = defaults[0]
    sss = 's' if int(size) != 1 else ''
    print(f' Ok, will run {Fore.LIGHTCYAN_EX}{int(size)}{Style.RESET_ALL} test{sss}\n')
    while not ok2:
        cv = input(" Desired Crit Value: ")
        if cv:
            if cv.lower() in valid_exit:
                return 0, 'exit'

            try:
                float(cv)
                ok2 = True

            except ValueError:
                print(f" {Fore.RED}Needs to be a number. Try again{Style.RESET_ALL}\n")

        else:
            ok2 = True
            cv = defaults[1]

    print(f' Ok, will look for at least {Fore.LIGHTCYAN_EX}{min(54.5, float(cv))}{Style.RESET_ALL} cv\n')
    print(f" Running {Fore.LIGHTCYAN_EX}{int(size)}{Style.RESET_ALL} simulation{'s' if int(size) != 1 else ''}, looking for at least {Fore.LIGHTCYAN_EX}{min(54.5, float(cv))}{Style.RESET_ALL} CV.")
    return size, cv


def get_main_stat_value(mainstat):
    if mainstat == 'HP':
        return [flower_stats, 0]
    elif mainstat == 'ATK':
        return [feather_stats, 0]
    elif mainstat in ('Pyro DMG% Bonus', 'Hydro DMG% Bonus', 'Cryo DMG% Bonus',
                      'Electro DMG% Bonus', 'Anemo DMG% Bonus',
                      'Geo DMG% Bonus', 'Physical DMG% Bonus',
                      'Dendro DMG% Bonus', 'HP%', 'ATK%'):
        return [hp_atk_dmg_stats, 0]
    elif mainstat == 'DEF%':
        return [def_stats, 0]
    elif mainstat == 'ER%':
        return [er_stats, 0]
    elif mainstat == 'EM':
        return [em_stats, 0]
    elif mainstat == 'Healing Bonus%':
        return [healing_bonus_stats, 0]
    elif mainstat == 'CRIT Rate%':
        return [crit_rate_stats, 0]
    else:
        return [crit_dmg_stats, 0]


last = 0
def transmute(preset=[]):
    if preset:
        artifact_type, main_stat, sub_stat_1, sub_stat_2, artifact_set = preset
        subs_pool = [sub for sub in substats if sub != main_stat]
        # print(f' {Fore.YELLOW}{artifact_type.capitalize()} selected.{Style.RESET_ALL}')
        # print(f' {Fore.YELLOW}Main Stat - {main_stat} selected.{Style.RESET_ALL}')
        # print(f' {Fore.YELLOW}{sub_stat_1} and {sub_stat_2} selected.{Style.RESET_ALL}')
        print(f' {Fore.YELLOW}Creating a {artifact_set} {main_stat} {artifact_type} with {sub_stat_1} and {sub_stat_2}.{Style.RESET_ALL}')

    else:
        print(f" {Fore.CYAN}Choose artifact set:{Style.RESET_ALL}")
        artifact_set = choose_one(sets, "That's not a set that is available! Try again", aliases_sets)
        if not artifact_set:
            print(f' {Fore.LIGHTMAGENTA_EX}Ok, not transmuting artifact anymore{Style.RESET_ALL}\n')
            return 0, last
        print(f' {Fore.YELLOW}{artifact_set} selected.{Style.RESET_ALL}')


        print(f"\n {Fore.CYAN}Choose type of artifact:{Style.RESET_ALL}")

        # type_dict = dict(zip([str(x+1) for x in range(len(artifact_types))], artifact_types))
        # for i in type_dict.items():
        #     print(f" {i[0]} = {i[1]}")
        # print('\n (Type 0 to exit)\n')
        # while True:
        #     artifact_type = input(' Your pick: ').strip().lower()
        #     if artifact_type in ('0', 'exit'):
        #         break
        #     if artifact_type in type_dict or artifact_type in type_dict.values():
        #         break
        #     else:
        #         print(f' {Fore.RED}Please input either the number or the name of the Artifact Type of choice{Style.RESET_ALL}\n')
        # if artifact_type in ('0', 'exit'):

        artifact_type = choose_one(artifact_types, 'Please input either the number or the name of the Artifact Type of choice')
        if not artifact_type:
            print(f' {Fore.LIGHTMAGENTA_EX}Ok, not transmuting artifact anymore{Style.RESET_ALL}\n')
            return 0, last
        print(f' {Fore.YELLOW}{artifact_type.capitalize()} selected.{Style.RESET_ALL}')
        if artifact_type == 'Flower':
            main_stat = 'HP'
        elif artifact_type == 'Feather':
            main_stat = 'ATK'
        else:
            main_stats = type_to_main_stats[artifact_type]
            print(f"\n {Fore.CYAN}Choose artifact Main Stat:{Style.RESET_ALL}")

            # main_stats_dict = dict(zip([str(x+1) for x in range(len(main_stats))], main_stats))
            # for i in main_stats_dict.items():
            #     print(f" {i[0]} = {i[1]}")
            # print('\n (Type 0 to exit)\n')
            # while True:
            #     main_stat = input(' Your pick: ').strip().lower()
            #     if main_stat in ('0', 'exit'):
            #         break
            #     if main_stat in main_stats_dict or main_stat in main_stats_dict.values():
            #         break
            #     else:
            #         print(f' {Fore.RED}Please input either the number or the name of the Main Stat of choice{Style.RESET_ALL}\n')
            # if main_stat in ('0', 'exit'):

            main_stat = choose_one(main_stats, 'Please input either the number or the name of the Main Stat of choice')
            if not main_stat:
                print(f' {Fore.LIGHTMAGENTA_EX}Ok, not transmuting artifact anymore{Style.RESET_ALL}\n')
                return 0, last
        print(f' {Fore.YELLOW}Main Stat - {main_stat} selected.{Style.RESET_ALL}')
        print()

        subs_pool = [sub for sub in substats if sub != main_stat]
        subs_dict = dict(enumerate(subs_pool, start=1))
        print(f" {Fore.CYAN}Choose two artifact Sub Stats (separate with space):{Style.RESET_ALL}")
        for i in subs_dict.items():
            print(f" {i[0]} = {i[1]}")
        print('\n (Type 0 to exit)\n')
        while True:
            subs = input(' Your pick: ').strip().lower().split()
            if (len(subs) == 1 and subs[0] == '0') or (len(subs) == 4 and subs[0] == 'exit'):
                break
            if len(subs) != 2:
                print(f' {Fore.RED}Please input two numbers corresponding to artifact Sub Stats of choice SEPARATED BY SPACE{Style.RESET_ALL}\n')
                continue
            sub_stat_1, sub_stat_2 = subs
            if sub_stat_1.isnumeric() and sub_stat_2.isnumeric() and sub_stat_1 != sub_stat_2:
                sub_stat_1, sub_stat_2 = int(sub_stat_1), int(sub_stat_2)
            else:
                print(f' {Fore.RED}Please input TWO DIFFERENT NUMBERS corresponding to artifact Sub Stats of choice separated by space{Style.RESET_ALL}\n')
                continue
            if sub_stat_1 in subs_dict and sub_stat_2 in subs_dict:
                break
            else:
                print(f' {Fore.RED}Please input two numbers CORRESPONDING TO ARTIFACT SUB STATS of choice separated by space{Style.RESET_ALL}\n')
        if subs[0] in ('0', 'exit'):
            print(f' {Fore.LIGHTMAGENTA_EX}Ok, not transmuting artifact anymore{Style.RESET_ALL}\n')
            return 0, last
        sub_stat_1 = subs_dict[sub_stat_1]
        sub_stat_2 = subs_dict[sub_stat_2]
        print(f' {Fore.YELLOW}{sub_stat_1} and {sub_stat_2} selected.{Style.RESET_ALL}')
        preset = [artifact_type, main_stat, sub_stat_1, sub_stat_2, artifact_set]

    fourliner = choices((1, 0), weights=(1, 2))[0]

    sub_stat_1_roll = choice(possible_rolls)
    sub_stat_2_roll = choice(possible_rolls)
    rv = sub_stat_1_roll*100 + sub_stat_2_roll*100

    subs = {sub_stat_1: max_rolls[sub_stat_1]*sub_stat_1_roll, sub_stat_2: max_rolls[sub_stat_2]*sub_stat_2_roll}
    subs_weights = dict(zip(substats, substats_weights))

    if main_stat in subs_weights:
        subs_weights.pop(main_stat)

    subs_weights.pop(sub_stat_1)
    subs_weights.pop(sub_stat_2)
    subs_pool.remove(sub_stat_1)
    subs_pool.remove(sub_stat_2)

    for _i in range(1 + fourliner):
        roll = choice(possible_rolls)
        sub = choices(subs_pool, weights=list(subs_weights.values()))[0]
        subs_weights.pop(sub)
        subs_pool.remove(sub)
        subs[sub] = max_rolls[sub] * roll
        rv += roll * 100
    print()
    threeliner = choices(subs_pool, weights=list(subs_weights.values()))[0] if not fourliner else 0
    return Artifact(artifact_type, main_stat, get_main_stat_value(main_stat), threeliner, subs, 0, artifact_set, "", rv), preset


def load_inventory():
    try:
        with open(Path('artifact_simulator_resources', 'inventory.txt')) as file:
            data = file.read()
        inv = json.loads(data)
        inv = [Artifact(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]) for a in inv]
        inv = sort_inventory(inv)
        if False in [a.set in sets for a in inv]:
            print(f' {Fore.RED}Some artifacts have invalid sets. Clearing inventory{Style.RESET_ALL}')
            with open(Path('artifact_simulator_resources', 'inventory.txt'), 'w') as file:
                file.write('[]')
            return []
        return inv

    except FileNotFoundError:
        with open(Path('artifact_simulator_resources', 'inventory.txt'), 'w') as file:
            file.write('[]')
        return []

    except IndexError:
        print(f' {Fore.RED}Your artifacts have been sacrificed to the Artifact Muncher\n'
              f' This is most likely due to your artifacts not having a set, which\n'
              f' is a new artifact trait I added in an update. Old artifacts\n'
              f' are no longer possible to be read from the save file :smoge:')
        with open(Path('artifact_simulator_resources', 'inventory.txt'), 'w') as file:
            file.write('[]')
        return []


def load_settings():
    global settings, source, resin_max
    try:
        with open(Path('artifact_simulator_resources', 'settings.txt')) as file:
            data = file.read()
        settings = json.loads(data)
        if (len(settings) == 2) and isinstance(settings, list):
            artifact_source, resin_maximum = settings
            if (
              (len(artifact_source) != 2) or  # length must be 2
              not isinstance(artifact_source, list) or  # must be a tuple
              not  # if neither of the following three cases is true, settings are invalid:
              (  # first item included in domains and 2nd item = 'domain'
                ((artifact_source[0] in domains) and (artifact_source[1] == 'domain')) or
                 # first item included in sets and 2nd item = 'strongbox'
                (artifact_source[0] in sets and (artifact_source[1] == 'strongbox')) or
                 # first item is a list of first two items in sets and 2nd item = 'boss'
                (artifact_source[0] == list(sets[:2]) and (artifact_source[1] == 'boss'))
              )
            ):
                print(f' {Fore.RED}Invalid settings, setting to default{Style.RESET_ALL}')
                settings = [[domains[-1], 'domain'], 180]
                save_settings_to_file()
            elif not isinstance(resin_maximum, int) or resin_maximum < 180 or resin_maximum > 1000:
                print(f' {Fore.RED}Invalid settings, setting to default{Style.RESET_ALL}')
                settings = [[domains[-1], 'domain'], 180]
                save_settings_to_file()
    except FileNotFoundError:
        settings = [[domains[-1], 'domain'], 180]
        save_settings_to_file()
    except:
        print(f' {Fore.RED}Failed to load settings, setting to default{Style.RESET_ALL}')
        settings = [[domains[-1], 'domain'], 180]
        save_settings_to_file()
    source, resin_max = settings


def create_artifact(full_source):
    exact_source, from_where = full_source
    art_type = choice(artifact_types)
    rv = 0

    if art_type == 'Flower':
        mainstat = 'HP'
    elif art_type == 'Feather':
        mainstat = 'ATK'
    elif art_type == 'Sands':
        mainstat = choices(sands_main_stats,
                           weights=sands_main_stats_weights)[0]
    elif art_type == 'Goblet':
        mainstat = choices(goblet_main_stats,
                           weights=goblet_main_stats_weights)[0]
    else:
        mainstat = choices(circlet_main_stats,
                           weights=circlet_main_stats_weights)[0]

    mainstat_value = get_main_stat_value(mainstat)
    fourliner_weights = (1, 4) if from_where == 'domain' else (1, 2)  # 20% or 33.33% chance for artifact to be 4-liner
    artifact_set = exact_source if from_where == 'strongbox' else choice(exact_source)
    fourliner = choices((1, 0), weights=fourliner_weights)[0]
    subs = {}

    subs_pool = list(substats)
    subs_weights = list(substats_weights)

    if mainstat in subs_pool:
        subs_weights.remove(subs_weights[subs_pool.index(mainstat)])
        subs_pool.remove(mainstat)

    for _i in range(3 + fourliner):
        roll = choice(possible_rolls)
        sub = choices(subs_pool, weights=subs_weights)[0]
        subs_weights.remove(subs_weights[subs_pool.index(sub)])
        subs_pool.remove(sub)
        subs[sub] = max_rolls[sub] * roll
        rv += roll * 100

    threeliner = choices(subs_pool, weights=subs_weights)[0] if not fourliner else 0

    return Artifact(art_type, mainstat, mainstat_value, threeliner, subs, 0, artifact_set, "", rv)


# ccc = 0
# aaamount = 100000000
# for i in range(aaamount):
#     if i % 1000000 == 0:
#         print(i)
#     a = create_artifact('domain')
#     if not a.threeliner and "CRIT Rate%" in a.substats and "CRIT DMG%" in a.substats:
#         ccc += 1
# print(f' {ccc / aaamount * 100}%')


def create_and_roll_artifact(arti_source, highest_cv=0, silent=False):
    artifact = create_artifact(arti_source)

    if not highest_cv and not silent:
        artifact.print_stats()

    for j in range(5):
        artifact.upgrade()
        if not highest_cv and not silent:
            artifact.print_stats()

    if highest_cv and artifact.cv() > highest_cv:
        highest_cv = artifact.cv()
        if not silent:
            print(f' Day {day}: {artifact.cv()} CV ({artifact.short()}) - {artifact.subs()}')

    if silent:
        artifact.last_upgrade = ""

    return artifact, highest_cv


def upgrade_to_next_tier(artifact, do_we_print=True, extra_space=False):
    if artifact.level == 20:
        if do_we_print:
            print(f" {Fore.LIGHTMAGENTA_EX}Artifact already at +20{Style.RESET_ALL}\n")

    else:
        if do_we_print:
            print(f' {Fore.LIGHTMAGENTA_EX}Upgrading...{Style.RESET_ALL}')
            if extra_space:
                print()

        artifact.upgrade()

        if do_we_print:
            artifact.print_stats()
        else:
            artifact.last_upgrade = ''


def upgrade_to_max_tier(artifact, do_we_print=2, extra_space=False):  # 2 - print everything
    if artifact.level == 20 and do_we_print >= 1:  # 1 - print only status and last upgrade
        print(f" {Fore.LIGHTMAGENTA_EX}Artifact already at +20{Style.RESET_ALL}\n")  # 0 - dont print

    else:
        if do_we_print >= 1:
            print(f' {Fore.LIGHTMAGENTA_EX}Upgrading to +20...{Style.RESET_ALL}')
            if extra_space:
                print()

        while artifact.level < 20:
            artifact.upgrade()
            if do_we_print == 2:
                artifact.print_stats()

        if do_we_print == 1:
            artifact.print_stats()
        artifact.last_upgrade = ''


def save_inventory_to_file(artifacts):
    with open(Path('artifact_simulator_resources', 'inventory.txt'), 'w') as f:
        f.write(json.dumps(artifacts, cls=ArtifactEncoder, separators=(',', ':')))


def save_settings_to_file():
    with open(Path('artifact_simulator_resources', 'settings.txt'), 'w') as f:
        f.write(json.dumps(settings, cls=ArtifactEncoder, separators=(',', ':')))


def sort_inventory(artifacts):
    return sorted(artifacts, key=lambda x: (sort_order_type[x.type], sort_order_sets[x.set], sort_order_mainstat[x.mainstat], -x.level))


def sort_daily(artifacts):
    # return sorted(artifacts, key=lambda x: (sort_order_sets[x.set], -sort_order_type[x.type], -sort_order_mainstat[x.mainstat]))
    return sorted(artifacts, key=lambda x: (sort_order_sets[x.set], sort_order_type[x.type],  sort_order_mainstat[x.mainstat]))[::-1]  # yes there is a reason i didn't use reverse=True


def compare_to_highest_cv(artifact, fastest, slowest, days_list, artifacts, day_number, artifact_number, cv_want,
                          only_one):
    if artifact.cv() >= min(54.5, cv_want):
        days_list.append(day_number)
        artifacts.append(artifact_number)

        if fastest[0] == 0 or day_number < fastest[0]:
            fastest = (day_number, artifact_number, artifact)

        if day_number > slowest[0]:
            slowest = (day_number, artifact_number, artifact)
        # print(artifact.subs())

        if not only_one:
            print(f' Artifacts generated: {Fore.MAGENTA}{artifact_number}{Style.RESET_ALL}')

    return fastest, slowest, days_list, artifacts, artifact.cv() >= min(54.5, cv_want)


def print_inventory(list_of_artifacts, indexes_to_print=None):
    first = '-'*44
    second = '-'*68
    flowers =  f'--- {Fore.LIGHTCYAN_EX}Flowers{Style.RESET_ALL} ----'
    feathers = f'--- {Fore.LIGHTCYAN_EX}Feathers{Style.RESET_ALL} ---'
    sands =    f'---- {Fore.LIGHTCYAN_EX}Sands{Style.RESET_ALL} -----'
    goblets =  f'--- {Fore.LIGHTCYAN_EX}Goblets{Style.RESET_ALL} ----'
    circlets = f'--- {Fore.LIGHTCYAN_EX}Circlets{Style.RESET_ALL} ---'
    t_map = {'Flower': flowers, 'Feather': feathers, 'Sands': sands, 'Goblet': goblets, 'Circlet': circlets}
    if indexes_to_print is None:
        needed_indexes = range(len(list_of_artifacts))
    else:
        for current_index in indexes_to_print:
            if current_index == -1 or current_index >= len(artifact_list):
                print(f' {Fore.RED}No artifact with index "{current_index + 1}" in your inventory.', end='')
                if len(artifact_list) >= 1:
                    print(f' Indexes go from 1 to {len(artifact_list)}{Style.RESET_ALL}\n')
                else:
                    print()
                    print_empty_inv()
                raise StopIteration

        needed_indexes = indexes_to_print

    print(f" {Fore.LIGHTMAGENTA_EX}Inventory:{Style.RESET_ALL}\n")
    t1 = list_of_artifacts[needed_indexes[0]].type
    extra_lines = (len(str(needed_indexes[0] + 1))-1)*'-'
    print(f'{extra_lines}{first}{t_map[t1]}{second}')

    for this_index in range(len(needed_indexes)):
        current_index = int(needed_indexes[this_index])

        if this_index != 0:
            t_last = list_of_artifacts[needed_indexes[this_index - 1]].type
            t_now = list_of_artifacts[needed_indexes[this_index]].type

            if t_now != t_last:
                extra_lines = (len(str(current_index + 1))-1)*'-'
                print(f'{extra_lines}{first}{t_map[t_now]}{second}')

        print(f' #{current_index + 1}) {list_of_artifacts[current_index].short()} {list_of_artifacts[current_index].subs()}')


def print_progress_bar(ind, total, bar_len=36, title='Please wait'):
    '''
    index is expected to be 0 based index.
    0 <= index < total
    '''
    percent_done = (ind+1)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'\r {title}: [{done_str}{togo_str}] - {percent_done}% done', end='')


def get_indexes(user_input):
    if ',' in user_input:  # if , in input
        idxs = user_input.split(',')  # split by commas
        # print(idxs)
        case = 'comma'

        for idx in range(len(idxs)):  # for every part separated by ,
            this_index = idxs[idx]

            if this_index == '':
                print(f' {Fore.RED}Try removing the space between the indexes (if applicable){Style.RESET_ALL}\n')
                raise StopIteration

            if '-' in this_index:  # if it has -
                if len(this_index.split('-')) == 2:  # and there's only one -
                    this_index = this_index.split('-')  # split by -

                    if this_index[0].isnumeric() and this_index[1].isnumeric():  # if the range is correct
                        this_index[0] = int(this_index[0])
                        this_index[1] = int(this_index[1])
                        if this_index[0] <= this_index[1]:
                            # replace the part with the range instead
                            idxs[idx] = [_ for _ in range(this_index[0], this_index[1] + 1)]

                        else:
                            print(f" {Fore.RED}\"{this_index}\" doesn't seem like a correct range{Style.RESET_ALL}\n")
                            raise StopIteration

                    else:
                        print(
                            f" {Fore.RED}Index \"{this_index[0] if not this_index[0].isnumeric() else this_index[1]}\" is non-numeric{Style.RESET_ALL}\n")
                        raise StopIteration

                else:
                    print(
                        f" {Fore.RED}Index \"{this_index}\" is incorrect, the range must consist of two numbers separated by \"-\"{Style.RESET_ALL}\n")
                    raise StopIteration

            elif not this_index.isnumeric():
                print(f" {Fore.RED}Index \"{this_index}\" is non-numeric", end='')

                if '[' in this_index:
                    print(f'. {Fore.LIGHTMAGENTA_EX}Remove the parentheses{Style.RESET_ALL}\n')
                else:
                    print(f'\n{Style.RESET_ALL}')

                raise StopIteration

        idxs = flatten_list(idxs)

    elif '-' in user_input:
        if len(user_input.split('-')) == 2:
            this_index = user_input.split('-')

            # if the range is correct
            if this_index[0].isnumeric() and this_index[1].isnumeric():  # if the range is correct
                this_index[0] = int(this_index[0])
                this_index[1] = int(this_index[1])
                if this_index[0] <= this_index[1]:
                    # replace the part with the range instead
                    idxs = [_ for _ in range(this_index[0], this_index[1] + 1)]

                else:
                    print(f' {Fore.RED}"{this_index}" doesn\'t seem like a correct range{Style.RESET_ALL}\n')
                    raise StopIteration

            else:
                print(f' {Fore.RED}Index "{this_index[0] if not this_index[0].isnumeric() else this_index[1]}" is non-numeric',
                      end='')

                if '[' in this_index[0]:
                    print(f'. {Fore.LIGHTMAGENTA_EX}Remove the parentheses{Style.RESET_ALL}\n')
                else:
                    print(f'\n{Style.RESET_ALL}')

                raise StopIteration

        else:
            print(f' Index "{user_input}" is incorrect, the range must consist of two numbers separated by "-"\n')
            raise StopIteration
        # print('flatten?', idxs)
        # idxs = flatten_list(idxs)

        case = 'range'

    else:
        if user_input.isnumeric():
            idxs = [user_input]

        else:
            print(f' {Fore.RED}Index "{user_input}" is non-numeric{Style.RESET_ALL}\n')
            raise StopIteration

        case = 'index'

    # print(list(map(int, idxs)))
    return list(map(int, idxs)), case


def print_empty_inv():
    print(f' {Fore.LIGHTMAGENTA_EX}Inventory is empty{Style.RESET_ALL}\n'
          f' try "r 5" to save 5 random artifacts or "s" to save the generated one\n')


def print_help():
    print(
        '\n' + '=' * 44 + f' {Fore.LIGHTCYAN_EX}CONTROLS{Style.RESET_ALL} ' + '=' * 44 + '\n'  # aliases included next to each command
        '\n'
        '--------------------------------- ACTIONS WITH GENERATED ARTIFACT --------------------------------\n'
        '\n'
        f' {Fore.LIGHTCYAN_EX}a{Style.RESET_ALL} = show generated artifact\n'  # artifact
        '\n'
        f' {Fore.BLUE}rv{Style.RESET_ALL} = show its roll value\n'   # rv
        f' {Fore.BLUE}cv{Style.RESET_ALL} = show its crit value\n'       # cv
        f' {Fore.BLUE}+{Style.RESET_ALL} = upgrade it to next tier\n'     # a+, a +
        f' {Fore.BLUE}++{Style.RESET_ALL} = upgrade it to +20\n'          # a++, a ++
        '\n'
        f' {Fore.BLUE}s{Style.RESET_ALL} = save to inventory (shows index of artifact if it is already saved)\n'        # save
        f' {Fore.BLUE}del{Style.RESET_ALL} = remove/delete from inventory\n'  # d, delete, rm, remove
        f'\n'
        f' {Fore.LIGHTCYAN_EX}r{Style.RESET_ALL} = re-roll artifact\n'
        f' {Fore.LIGHTCYAN_EX}r{Fore.BLUE} ++{Style.RESET_ALL} = re-roll and upgrade to +20\n'  # r ++
        f' {Fore.LIGHTCYAN_EX}r {Fore.MAGENTA}[number]{Style.RESET_ALL} = re-roll and save a given number of artifacts to the inventory\n'
        f' {Fore.LIGHTCYAN_EX}r {Fore.MAGENTA}[number]{Fore.BLUE} ++{Style.RESET_ALL} = re-roll, +20, and save a given number of artifacts to the inventory\n'
        f'\n'
        f' {Fore.LIGHTCYAN_EX}log{Style.RESET_ALL} = view artifact log (10 most recent artifacts generated)\n'
        f' {Fore.LIGHTCYAN_EX}log-{Fore.BLUE} [number]{Style.RESET_ALL} = move back in the artifact log\n'
        f' {Fore.LIGHTCYAN_EX}log+{Fore.BLUE} [number]{Style.RESET_ALL} = move forward in the artifact log\n'
        f'\n'
        '------------------------------------- ACTIONS WITH INVENTORY -------------------------------------\n'
        '\n'
        f' {Fore.LIGHTCYAN_EX}inv{Style.RESET_ALL} = show inventory\n'  # inventory
        # this is true for every other inventory command too
        '\n'
        f' {Fore.CYAN}inv {Fore.MAGENTA}[indexes]{Style.RESET_ALL} = view artifacts from inventory. Using 1 index also selects the artifact\n'
        f' {Fore.CYAN}inv {Fore.MAGENTA}[indexes]{Fore.BLUE} +/++/cv/rv/del{Style.RESET_ALL} = perform action with artifacts from the inventory (pick one)\n'
        '\n'
        f' {Fore.GREEN}VALID INDEXING:{Style.RESET_ALL} inv 3 | inv 1,4 | inv 1-5 | inv 9,2-6 | inv 5-35\n'
        f' {Fore.RED}INVALID INDEXING:{Style.RESET_ALL} inv [8,9] | inv 7.9 | inv 3, 2 | inv 3 - 8 | inv 4,6-2\n'
        f' NOTE: Indexes may change after deletion or upgrading of artifacts due to inventory sorting\n'
        '\n'
        f' {Fore.CYAN}inv {Fore.BLUE}size{Style.RESET_ALL} = view amount of artifacts in inventory\n'  # inv len/inv length
        f' {Fore.CYAN}inv {Fore.BLUE}cv{Style.RESET_ALL} = show artifact with highest crit value\n'
        f' {Fore.CYAN}inv {Fore.BLUE}rv{Style.RESET_ALL} = show artifact with highest roll value\n'
        f' {Fore.CYAN}inv {Fore.BLUE}load{Style.RESET_ALL} = load updates made to inventory.txt\n'
        f' {Fore.CYAN}inv {Fore.BLUE}c{Style.RESET_ALL} = clear inventory\n'  # aliases for 'c': clear, clr
        '\n'
        '----------------------------------------- OTHER COMMANDS ----------------------------------------\n'
        '\n'
        f' {Fore.LIGHTCYAN_EX}auto{Style.RESET_ALL} = enter Automation Mode\n'  # auto
        f' {Fore.LIGHTCYAN_EX}plot{Style.RESET_ALL} = generate a number of artifacts and plot their Crit Values\n'
        '\n'
        f' {Fore.LIGHTCYAN_EX}tr{Style.RESET_ALL} = transmute artifact\n'  # transmute
        f' {Fore.LIGHTCYAN_EX}daily {Fore.BLUE}save{Style.RESET_ALL} = spend daily resin in a domain of choice, save if specified\n'  # daily s
        '\n'
        f' {Fore.LIGHTCYAN_EX}resin{Style.RESET_ALL} = change amount of daily resin\n'
        f' {Fore.LIGHTCYAN_EX}source{Style.RESET_ALL} = view current source\n'
        f' {Fore.CYAN}domain{Style.RESET_ALL} = change artifact source to domain\n'
        f' {Fore.CYAN}strongbox{Style.RESET_ALL} = change artifact source to strongbox\n'
        f' {Fore.CYAN}boss{Style.RESET_ALL} = change artifact source to bosses\n'
        '\n'
        f' {Fore.LIGHTCYAN_EX}0{Style.RESET_ALL} = exit Artifact Simulator\n'  # 0, menu
        '\n'
        '==================================================================================================\n'
        )


def insert_average(arr, num):
    if (num != 12) and (arr[-1] - arr[-2] <= 1):
        return arr
    arr = arr[arr >= 0]
    # Calculate the number of elements in the output array
    n = arr.shape[0]
    # Create an array to hold the result, initially twice the size of the input array
    result = np.empty(2 * n - 1)
    # Fill the odd indices with the original elements of the array
    result[::2] = arr
    # Fill the even indices with the average of adjacent elements

    result[1::2] = (arr[:-1] + arr[1:]) / 2

    if len(result) <= num:
        return insert_average(result, num)

    return result


def plot_that(plot_cv):
    amount_of_artifacts = sum(plot_cv)
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].bar(possible_cvs, plot_cv, label='Data')
    ax[1].plot(possible_cvs, plot_cv, label='Data')
    # Plot for the False value (left subplot)
    ax[0].set_title('Regular')
    ax[0].set_xlabel("Crit Value")
    ax[0].set_ylabel("Number of artifacts")
    ax[0].tick_params(axis='x', rotation=60)  # Rotate x-axis labels

    # Plot for the True value (right subplot)
    ax[1].set_title('Logarithmic')
    ax[1].set_xlabel("Crit Value")
    ax[1].set_yscale('log')
    ax[1].tick_params(axis='x', rotation=60)  # Rotate x-axis labels

    for a in ax:
        a.grid(True)

    ax[0].set_xticks(possible_cvs[::20])
    ax[0].set_yticks(insert_average(ax[0].get_yticks(), 11))
    ax[1].set_xticks(possible_cvs[::20])
    s = 's' if amount_of_artifacts > 1 else ''
    ap = 's' if amount_of_artifacts == 1 else ''
    fig.suptitle(f"Crit Value distribution of {amount_of_artifacts:,} artifact{s}")
    plt.tight_layout()
    # plt.grid()
    Path('artifact_simulator_resources', 'plots', f'(CV distribution) {amount_of_artifacts} sample size').mkdir(parents=True, exist_ok=True)
    plt.savefig(Path('artifact_simulator_resources', 'plots', f'(CV distribution) {amount_of_artifacts} sample size', f"Plot of {amount_of_artifacts} artifact{s}'{ap} CV{s} at {str(datetime.datetime.now())[:-7].replace(":", "-")}.png"),
                dpi=900)

    print(" Here you go. This was also saved as a .png file.\n")
    plt.show()


def flatten_list(nested_list):  # thanks saturncloud.io
    def flatten(lst):
        for item in lst:
            if isinstance(item, list):
                flatten(item)
            else:
                flat_list.append(item)

    flat_list = []
    flatten(nested_list)
    return flat_list


def print_menu():
    print('\n' + '=' * 30 + " MENU " + '=' * 30 + '\n')
    print(" 0 = exit Artifact Simulator\n"
          " 1 = roll one artifact at a time\n"
          " 2 = roll artifacts until a certain CV is reached\n")


def show_index_changes(old_list, new_list):
    # ty chatgpt this is actually a cool approach
    index_differences = []
    artifact_map = {artifact: i for i, artifact in enumerate(new_list)}

    for i, artifact in enumerate(old_list):
        try:
            if artifact != new_list[i]:
                index_differences.append((artifact_map.get(artifact, -1), i))
        except IndexError:
            index_differences.append((artifact_map.get(artifact, -1), i))

    if index_differences:
        counter = 0
        print(f' {Fore.LIGHTMAGENTA_EX}SOME INVENTORY INDEXES CHANGED:{Style.RESET_ALL}')
        for new, old in index_differences[::-1]:
            if new+1 == 0:
                continue
            counter += 1
            print(f' {old + 1} -> {new + 1}', end='')
            if counter >= 5:
                print('...')
                print(f' Check your inventory to see all {len(index_differences)} changes')
                break
            print()
        print()


sort_order_type = {'Flower': 0, 'Feather': 1, 'Sands': 2, 'Goblet': 3, 'Circlet': 4}
sort_order_mainstat = {'ATK': 0,
                       'HP': 1,
                       'CRIT DMG%': 2, 'CRIT Rate%': 3,
                       'EM': 4,
                       'Pyro DMG% Bonus': 5, 'Hydro DMG% Bonus': 6, 'Cryo DMG% Bonus': 7, 'Electro DMG% Bonus': 8,
                       'Anemo DMG% Bonus': 9, 'Dendro DMG% Bonus': 10, 'Geo DMG% Bonus': 11, 'Physical DMG% Bonus': 12,
                       'ER%': 13,
                       'Healing Bonus': 14,
                       'ATK%': 15,
                       'HP%': 16,
                       'DEF%': 17,
                       }
valid_help = ['help', "'help'", '"help"']
valid_picks = ['0', 'exit', '1', '2']


print(f'\n==================== {Fore.LIGHTCYAN_EX}LOADING ARTIFACT SIMULATOR{Style.RESET_ALL} ==================\n')

try:
    artifact_list = load_inventory()
    print(f' {Fore.LIGHTGREEN_EX}Loaded inventory successfully!{Style.RESET_ALL}')
    # print_inventory(artifact_list)
    # print()
except json.decoder.JSONDecodeError:
    print(f' {Fore.RED}Something off with inventory file. Clearing inventory.txt{Style.RESET_ALL}')
    artifact_list = []
    save_inventory_to_file(artifact_list)
    print(f' {Fore.LIGHTGREEN_EX}Inventory cleared{Style.RESET_ALL}')

load_settings()
print(f' {Fore.LIGHTGREEN_EX}Loaded settings successfully!{Style.RESET_ALL}')

# while True:
#     print_menu()
#
#     while True:
#         automate = input('Your pick: ').strip()
#         if automate.lower() in valid_picks:
#             break
#         else:
#             print('Commands are 0, 1 or 2\n')
#
#     print('Exiting...\n' if automate in ('0', 'exit') else '')
print()
print(f'======================== {Fore.LIGHTCYAN_EX}ARTIFACT SIMULATOR{Style.RESET_ALL} ======================')

print(f'\n Type {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL} for the list of commands\n')
art = create_artifact(source)
artifact_log = [art]
art.print_stats()


def print_log():
    for this_index in range(1, len(artifact_log) + 1):
        color = Fore.GREEN if art == artifact_log[-this_index] else ''
        index_to_show = this_index if not artifact_log[-this_index] in artifact_list else '#' + str(artifact_list.index(artifact_log[-this_index]) + 1)
        print(f' {color}{index_to_show}) {artifact_log[-this_index].short()} {artifact_log[-this_index].subs()}{Style.RESET_ALL}')
    print()


while True:
    user_command = input(' Command: ').lower().strip()
    if user_command in valid_help:
        print_help()

    elif '"' in user_command or "'" in user_command:
        print(f' {Fore.LIGHTMAGENTA_EX}Remove the quotation marks{Style.RESET_ALL}\n')
        continue

    elif user_command in ('exit', '0'):
        print(' Exiting Artifact Simulator...')
        break

    elif user_command in ('automate', 'auto'):
        print(' Entering Automation Mode...\n')
        print('='*25 + f' {Fore.LIGHTCYAN_EX}AUTOMATION MODE{Style.RESET_ALL} ' + '='*24)
        sample_size, cv_desired = take_input()

        if sample_size == 'exit' or cv_desired == 'exit':
            print(" Going back to normal mode...")
            print()
            print('=' * 27 + f' {Fore.LIGHTCYAN_EX}NORMAL MODE{Style.RESET_ALL} ' + '=' * 26)
            print()
            continue
        else:
            sample_size, cv_desired = int(sample_size), float(cv_desired)

        days_it_took_to_reach_desired_cv = []
        artifacts_generated = []
        absolute_generated_domain = 0
        absolute_generated_strongbox = 0
        absolute_generated_abyss = 0
        win_generated_domain = 0
        win_generated_strongbox = 0
        win_generated_abyss = 0
        low = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0, ''))
        high = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0, ''))
        start = time.perf_counter()
        sample_size_is_one = sample_size == 1
        abyss_sets = sets[-2:]
        for i in range(sample_size):
            strongbox_set = choice(sets)
            domain_set = choice(domains)
            joined_domain = ', '.join(domain_set)
            c = 0
            day = 0
            highest = 0.1
            total_generated = 0
            inventory = 0
            flag = False
            print(f'\n {Fore.LIGHTMAGENTA_EX}Simulation {i + 1}{Style.RESET_ALL}:' if sample_size > 1 else '')
            print(f' Strongbox set: {Fore.MAGENTA}{strongbox_set}{Style.RESET_ALL}\n Abyss sets: {Fore.MAGENTA}{abyss_sets[0]}, {abyss_sets[1]}{Style.RESET_ALL}\n Domain: {Fore.MAGENTA}{joined_domain}{Style.RESET_ALL}\n')

            while not flag:
                day += 1

                if day % 10000 == 0:
                    print(f' {Fore.MAGENTA}Day {day} - still going{Style.RESET_ALL}')

                if day % 30 == 0:  # 4 artifacts from abyss every 30 days
                    for k in range(4):
                        inventory += 1
                        total_generated += 1
                        absolute_generated_abyss += 1
                        art, highest = create_and_roll_artifact([abyss_sets, "abyss"], highest)
                        low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                            compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv,
                                                  artifacts_generated,
                                                  day, total_generated, cv_desired, sample_size_is_one))
                        if flag:
                            break
                    if flag:
                        win_generated_abyss += 1
                        break
                resin = 180

                if day % 7 == 1:  # 1 transient resin from tubby every monday
                    resin += 60

                while resin and not flag:
                    # print('domain run')
                    resin -= 20
                    amount = choices((1, 2), weights=(28, 2))  # 6.66% chance for 2 artifacts
                    # if amount[0] == 2:
                    #     print('lucky!')
                    total_generated += amount[0]
                    absolute_generated_domain += amount[0]
                    inventory += amount[0]
                    for k in range(amount[0]):
                        art, highest = create_and_roll_artifact([domain_set, "domain"], highest)
                        low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                            compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv,
                                                  artifacts_generated,
                                                  day, total_generated, cv_desired, sample_size_is_one))
                        if flag:
                            break
                    if flag:
                        win_generated_domain += 1
                        break

                else:
                    while inventory >= 3:
                        # print(f'strongbox {inventory}')
                        inventory -= 2
                        total_generated += 1
                        absolute_generated_strongbox += 1
                        art, highest = create_and_roll_artifact([strongbox_set, "strongbox"], highest)
                        low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                            compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv,
                                                  artifacts_generated,
                                                  day, total_generated, cv_desired, sample_size_is_one))
                        if flag:
                            win_generated_strongbox += 1
                            break
                    # print(f'{inventory} left in inventory')

        end = time.perf_counter()
        run_time = end - start
        to_hours = time.strftime("%T", time.gmtime(run_time))
        decimals = f'{(run_time % 1):.3f}'

        print()
        days = round(sum(days_it_took_to_reach_desired_cv) / sample_size, 2)

        if sample_size > 1:
            print(f' Out of {sample_size} simulations, it took an average of {Fore.LIGHTCYAN_EX}{days}{Style.RESET_ALL} days ({round(days / 365.25, 2)} years) to reach at least {cv_desired} CV.')
            print(f' Fastest - {Fore.GREEN}{low[0]} day{"s" if low[0] > 1 else ""}{Style.RESET_ALL} - artifact #{low[1]}: {low[2].short(True)}{low[2].subs()}')
            print(f' Slowest - {Fore.RED}{high[0]} day{"s" if high[0] > 1 else ""} ({round(high[0] / 365.25, 2)} years){Style.RESET_ALL} - artifact #{high[1]}: {high[2].short(True)}{high[2].subs()}')
            print()
            print(f' Out of {sample_size} winning artifacts {Fore.LIGHTCYAN_EX}{win_generated_domain}{Style.RESET_ALL} were from domains, {Fore.LIGHTCYAN_EX}{win_generated_strongbox}{Style.RESET_ALL} from strongbox and {Fore.LIGHTCYAN_EX}{win_generated_abyss}{Style.RESET_ALL} from abyss.')
        else:
            print(f' It took {Fore.LIGHTCYAN_EX}{low[0]} days{Style.RESET_ALL} (or {round(high[0] / 365.25, 2)} years)!')

        print(f' Total artifacts generated: {Fore.MAGENTA}{sum(artifacts_generated)}{Style.RESET_ALL} (Domains: {Fore.CYAN}{absolute_generated_domain}{Style.RESET_ALL}, Strongbox: {Fore.CYAN}{absolute_generated_strongbox}{Style.RESET_ALL}, Abyss: {Fore.CYAN}{absolute_generated_abyss}{Style.RESET_ALL})\n')
        print(f' The simulation{"s" if sample_size > 1 else ""} took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
        print(f' Performance: {round(sum(artifacts_generated) / run_time / 1000, 2)} artifacts per ms')
        print()
        print('=' * 27 + f' {Fore.LIGHTCYAN_EX}NORMAL MODE{Style.RESET_ALL} ' + '=' * 26)
        print()

    elif user_command == 'plot':
        f = True
        print(' This allows you to generate a number of artifacts and plot the Crit Values of those artifacts!\n'
              f' Artifacts are generated from your currently active source (type {Fore.CYAN}source{Style.RESET_ALL} to check)\n')
        while True:
            num = input(' How many artifacts to generate: ').strip()
            if num == '0':
                print(f' {Fore.LIGHTMAGENTA_EX}Ok, no longer plotting (insert racoon gif){Style.RESET_ALL}\n')
                f = False
                break
            elif num == 'source':
                print(f' Current source is {source[1].capitalize()}\n')
            elif num.isnumeric():
                num = int(num)
                break
            else:
                print(f' {Fore.RED}Please input a number{Style.RESET_ALL}\n')
        if f:
            print()
            cvs = {i: 0 for i in possible_cvs}
            progress_bar_number = num//1000
            for i in range(num):
                art, _ = create_and_roll_artifact(source, 0, True)
                cvs[art.cv_real()] += 1
                print_progress_bar(i // progress_bar_number, num // progress_bar_number)
            print(f"\r {Fore.LIGHTGREEN_EX}Generation complete - 100%{Style.RESET_ALL}" + ' '*47+'\n')
            # plt.bar(cvs.keys(), cvs.values())
            # plt.show()
            print(' Ok!')
            print(' Raw values:', cvs)
            plot_that(cvs.values())


    elif user_command in ('+', 'a+', 'a +'):
        if art in artifact_list:
            old_index = artifact_list.index(art)
            upgrade_to_next_tier(art, True, True)

            artifact_list_new = sort_inventory(artifact_list)
            new_index = artifact_list_new.index(art)
            show_index_changes(artifact_list, artifact_list_new)

            artifact_list = artifact_list_new
            save_inventory_to_file(artifact_list)

            if old_index != new_index:
                print(f' New inventory index: #{new_index+1}\n')
        else:
            upgrade_to_next_tier(art, True, True)

    elif user_command in ('++', 'a++', 'a ++'):
        if art in artifact_list:
            old_index = artifact_list.index(art)
            upgrade_to_max_tier(art, 2, True)

            artifact_list_new = sort_inventory(artifact_list)
            new_index = artifact_list_new.index(art)
            show_index_changes(artifact_list, artifact_list_new)

            artifact_list = artifact_list_new
            save_inventory_to_file(artifact_list)

            if old_index != new_index:
                print(f' New inventory index: #{new_index+1}\n')
        else:
            upgrade_to_max_tier(art, 2, True)

    elif user_command == 'r':
        print(f' {Fore.LIGHTMAGENTA_EX}Re-rolling...{Style.RESET_ALL}\n')
        art = create_artifact(source)
        artifact_log.append(art)
        if len(artifact_log) > 10:
            log_start = len(artifact_log)-10
            artifact_log = artifact_log[log_start:]
        art.print_stats()

    elif user_command in ('r++', 'r ++'):
        print(f' {Fore.LIGHTMAGENTA_EX}Re-rolling and upgrading...{Style.RESET_ALL}\n')
        art, _ = create_and_roll_artifact(source)
        artifact_log.append(art)
        if len(artifact_log) > 10:
            log_start = len(artifact_log)-10
            artifact_log = artifact_log[log_start:]

    elif 'log-' in user_command:
        if user_command[:4] == 'log-':
            inp = user_command.split()
            if len(inp) == 2:
                if inp[1].isnumeric():
                    back = int(inp[1])
                else:
                    print(f' {Fore.RED}"{inp[1]}" is not a number{Style.RESET_ALL}\n')
                    continue
            else:
                back = 1
            if art in artifact_log:
                if artifact_log.index(art) - back >= 0:
                    art = artifact_log[artifact_log.index(art) - back]
                    # print(f' {Fore.LIGHTGREEN_EX}Ok, moved back {back} artifact{"s" if back != 1 else ""} inside of the artifact log{Style.RESET_ALL}\n')
                    print_log()
                    print(f' {Fore.CYAN}Selected artifact:{Style.RESET_ALL}')
                    art.print_stats()
                elif artifact_log.index(art) != 0:
                    art = artifact_log[0]
                    print(f' {Fore.LIGHTMAGENTA_EX}Not enough artifacts in the log to move back {back} spot{"s" if back != 1 else ""}{Style.RESET_ALL}\n'
                          f' {Fore.MAGENTA}Moved back to the start of the artifact log instead{Style.RESET_ALL}\n')
                    print_log()
                    print(f' {Fore.CYAN}Selected artifact:{Style.RESET_ALL}')
                    art.print_stats()
                else:
                    print(f' {Fore.LIGHTMAGENTA_EX}You\'re already at the beginning of the artifact log!{Style.RESET_ALL}\n')
            else:
                art = artifact_log[-1]
                print_log()
                print(f' {Fore.CYAN}Selected artifact:{Style.RESET_ALL}')
                art.print_stats()
        else:
            print(f' {Fore.RED}Command must start with "log-" to move back inside of the artifact log!{Style.RESET_ALL}\n')

    elif 'log+' in user_command:
        if user_command[:4] == 'log+':
            inp = user_command.split()
            if len(inp) == 2:
                if inp[1].isnumeric():
                    forward = int(inp[1])
                else:
                    print(f' {Fore.RED}"{inp[1]}" is not a number{Style.RESET_ALL}\n')
                    continue
            else:
                forward = 1
            if art in artifact_log:
                if artifact_log.index(art) + forward < len(artifact_log):
                    art = artifact_log[artifact_log.index(art) + forward]
                    # print(f' {Fore.LIGHTGREEN_EX}Ok, moved forward {forward} artifact{"s" if forward != 1 else ""} inside of the artifact log{Style.RESET_ALL}\n')
                    print_log()
                    print(f' {Fore.CYAN}Selected artifact:{Style.RESET_ALL}')
                    art.print_stats()
                elif artifact_log.index(art) != len(artifact_log) - 1:
                    art = artifact_log[-1]
                    print(f' {Fore.LIGHTMAGENTA_EX}Not enough artifacts in the log to move forward {forward} spot{"s" if forward != 1 else ""}{Style.RESET_ALL}\n'
                          f' {Fore.MAGENTA}Moved to the end of the artifact log instead{Style.RESET_ALL}\n')
                    print_log()
                    print(f' {Fore.CYAN}Selected artifact:{Style.RESET_ALL}')
                    art.print_stats()
                else:
                    print(f' {Fore.LIGHTMAGENTA_EX}You\'re already at the end of the artifact log!{Style.RESET_ALL}\n')
            else:
                art = artifact_log[-1]
                print_log()
                print(f' {Fore.CYAN}Selected artifact:{Style.RESET_ALL}')
                art.print_stats()
        else:
            print(f' {Fore.RED}Command must start with "log+" to move forward inside of the artifact log!{Style.RESET_ALL}\n')

    elif user_command == 'log':
        print_log()

    elif user_command[:2] == 'r ':
        if '++' in user_command:
            if len(user_command.split()) == 3:
                _, cmd, _ = user_command.split()
            else:
                print(f' {Fore.RED}Nuh uh. Only put one number between r and ++{Style.RESET_ALL}\n')
                continue

            if cmd.isnumeric():
                cmd = int(cmd)
                s = len(artifact_list)
                artifact_list_old = artifact_list.copy()

                for i in range(cmd):
                    if s < 100000:
                        art, _ = create_and_roll_artifact(source, 0, True)
                        artifact_list.append(art)
                        s += 1
                    else:
                        print(f' {Fore.RED}Inventory full (100k artifacts).\n'
                              f' {Fore.LIGHTMAGENTA_EX}Delete some artifacts first to continue saving.\n'
                              f' You may still generate artifacts without saving them.{Style.RESET_ALL}\n')
                        cmd = i
                        break

                artifact_list = sort_inventory(artifact_list)
                save_inventory_to_file(artifact_list)

                print(f' {Fore.LIGHTGREEN_EX}{cmd} new +20 artifact{"s" if cmd > 1 else ""} added to inventory. {len(artifact_list)} artifact{"s" if len(artifact_list) != 1 else ""} in inventory{Style.RESET_ALL}\n')
                show_index_changes(artifact_list_old, artifact_list)
                continue
                # print_inventory(artifact_list)
                # print()

            else:
                print(f' {Fore.RED}{cmd} is not a valid number{Style.RESET_ALL}\n')
                continue

        else:
            if len(user_command.split()) == 2:
                _, cmd = user_command.split()
            else:
                print(f' {Fore.RED}Nuh uh. Only put one number after r{Style.RESET_ALL}\n')
                continue

            if cmd.isnumeric():
                cmd = int(cmd)

                s = len(artifact_list)
                artifact_list_old = artifact_list.copy()

                for i in range(cmd):
                    if s < 100000:
                        art = create_artifact(source)
                        artifact_list.append(art)
                        s += 1
                    else:
                        print(f' {Fore.RED}Inventory full (100k artifacts).\n'
                              f' {Fore.LIGHTMAGENTA_EX}Delete some artifacts first to continue saving.\n'
                              f' You may still generate artifacts without saving them.{Style.RESET_ALL}\n')
                        cmd = i
                        break

                artifact_list = sort_inventory(artifact_list)
                save_inventory_to_file(artifact_list)

                print(f' {Fore.LIGHTGREEN_EX}{cmd} new +0 artifact{"s" if cmd > 1 else ""} added to inventory\n {len(artifact_list)} artifact{"s" if len(artifact_list) != 1 else ""} in inventory{Style.RESET_ALL}\n')
                show_index_changes(artifact_list_old, artifact_list)
                continue
                # print_inventory(artifact_list)
                # print()

            else:
                print(f' {Fore.RED}{cmd} is not a valid number{Style.RESET_ALL}\n')
                continue

    elif user_command in ('s', 'save'):
        if art not in artifact_list:
            if len(artifact_list) < 100000:
                artifact_list.append(art)
                len_artifact_list = len(artifact_list)

                artifact_list = sort_inventory(artifact_list)
                save_inventory_to_file(artifact_list)

                print(f' {Fore.LIGHTGREEN_EX}Saved (#{artifact_list.index(art)+1}) - {len_artifact_list} artifact{"s" if len_artifact_list > 1 else ""} in inventory{Style.RESET_ALL}\n')
            else:
                print(f' {Fore.RED}Inventory full (100k artifacts).\n'
                      f' {Fore.LIGHTMAGENTA_EX}Delete some artifacts first to continue saving.\n'
                      f' You may still generate artifacts without saving them.{Style.RESET_ALL}\n')
        else:
            print(f' {Fore.LIGHTMAGENTA_EX}Already saved this artifact - #{artifact_list.index(art)+1}{Style.RESET_ALL}\n')

    elif user_command in ('d', 'del', 'delete', 'rm', 'remove'):
        if art in artifact_list:
            artifact_list.remove(art)
            len_artifact_list = len(artifact_list)

            save_inventory_to_file(artifact_list)
            print(f' {Fore.LIGHTGREEN_EX}Removed - {len_artifact_list} artifact{"s" if len_artifact_list != 1 else ""} in inventory{Style.RESET_ALL}\n')

        else:
            print(f' {Fore.LIGHTMAGENTA_EX}This artifact is not in your inventory{Style.RESET_ALL}\n')

    elif 'inv' in user_command:
        user_command = user_command.split()
        if user_command[0] not in ('inv', 'inventory'):
            print(f' {Fore.LIGHTMAGENTA_EX}Inventory commands must start with "inv".\n'
                  f' If you want to pass any arguments, you must put a space after "inv"{Style.RESET_ALL}.\n')
            continue

        if len(user_command) == 1:
            if len(artifact_list) == 0:
                print_empty_inv()

            else:
                print_inventory(artifact_list)
                print()

        elif len(user_command) == 3:  # e.g. "inv 1 +" or "inv 1,2,4 +" or "inv 2-5 d"
            _, chosen_numbers, cmd = user_command
            flag = True

            try:
                indexes, operation = get_indexes(chosen_numbers)
            except StopIteration:
                continue

            for i in indexes:
                if int(i) > len(artifact_list) or int(i) == 0:
                    flag = False
                    print(f' {Fore.RED}No artifact with index "{i}" in your inventory.', end='')
                    if len(artifact_list) >= 1:
                        print(f' Indexes go from 1 to {len(artifact_list)}{Style.RESET_ALL}\n')
                    else:
                        print()
                        print_empty_inv()
                    break

            if flag:  # if all given indexes are valid
                indexes = list(map(lambda x: x - 1, map(int, indexes)))  # transform them
                if len(indexes) == 1:  # if one index, we print every upgrade
                    do_print = 2
                elif len(indexes) <= 25:  # if no more than 25, we print the results for every one
                    do_print = 1
                else:  # otherwise, we don't print because that takes too much time and space on the screen
                    do_print = 0

                if len(indexes) > 1:  # if there's more than 1 index
                    if len(indexes) <= 25:
                        if cmd in ('+', '++'):
                            print('\n')  # two blank lines
                        if cmd in ('cv', 'rv'):
                            print()

                    # make a new list containing all the artifacts in question
                    arti_list = itemgetter(*indexes)(artifact_list)

                else:  # otherwise, make a list containing 1 artifact
                    arti_list = [artifact_list[indexes[0]]]  # because we need a list object to iterate
                    if cmd in ('+', '++'):
                        print()

                if cmd in ('d', 'del', 'delete', 'rm', 'remove'):
                    artifact_list_old = artifact_list.copy()

                # then iterate this list and execute command
                for index, iterative_index in zip(indexes, range(len(arti_list))):
                    if cmd == '+':
                        if do_print:
                            print(f' #{index + 1})', end='')
                        upgrade_to_next_tier(arti_list[iterative_index], do_print)
                        old_index = artifact_list.index(arti_list[iterative_index])

                    elif cmd == '++':
                        if do_print:
                            print(f' #{index + 1})', end='')
                        upgrade_to_max_tier(arti_list[iterative_index], do_print)
                        old_index = artifact_list.index(arti_list[iterative_index])

                    elif cmd == 'rv':
                        print(f' #{index + 1}) RV: {arti_list[iterative_index].rv()}%')

                    elif cmd == 'cv':
                        print(f' #{index + 1}) CV: {arti_list[iterative_index].cv()}')

                    elif cmd in ('d', 'del', 'delete', 'rm', 'remove'):
                        if arti_list[iterative_index] in artifact_list:
                            artifact_list.remove(arti_list[iterative_index])

                    else:
                        print(f' {Fore.RED}"{cmd}" is not a valid command{Style.RESET_ALL}\n')

                if cmd in ('d', 'del', 'delete', 'rm', 'remove'):
                    save_inventory_to_file(artifact_list)
                    print(f' {Fore.LIGHTGREEN_EX}Artifact{"s" if len(indexes) > 1 else ""} removed{Style.RESET_ALL}\n')
                    show_index_changes(artifact_list_old, artifact_list)

                if cmd in ('+', '++'):
                    if not do_print:
                        print(f" {Fore.LIGHTGREEN_EX}Done! Artifacts upgraded{Style.RESET_ALL}")

                    if len(indexes) != 1:
                        artifact_list_new = sort_inventory(artifact_list)
                        show_index_changes(artifact_list, artifact_list_new)

                        artifact_list = artifact_list_new
                        save_inventory_to_file(artifact_list)

                        print()

                    else:
                        artifact_list_new = sort_inventory(artifact_list)
                        show_index_changes(artifact_list, artifact_list_new)

                        artifact_list = artifact_list_new
                        save_inventory_to_file(artifact_list)

                        new_index = artifact_list_new.index(arti_list[iterative_index])

                        if old_index != new_index:
                            print(f' New inventory index: #{new_index + 1}\n')

                if cmd in ('cv', 'rv'):
                    print()

        elif len(user_command) == 2:  # e.g. "inv 2" or "inv 1-5,7"
            _, cmd = user_command
            if ',' in cmd or '-' in cmd:

                try:
                    indexes, operation = get_indexes(cmd)
                except StopIteration:
                    continue

                indexes = list(map(lambda x: x - 1, map(int, indexes)))
                # print(indexes)
                indexes = sorted(list(set(indexes)))

                if len(artifact_list) > 0:
                    try:
                        print_inventory(artifact_list, indexes)
                        print()
                    except StopIteration:
                        continue

                else:
                    print_empty_inv()

            elif cmd.isnumeric():
                cmd = int(cmd)

                if cmd <= len(artifact_list) and cmd != 0:
                    print()
                    art = artifact_list[int(cmd) - 1]
                    artifact_list[int(cmd) - 1].print_stats()

                else:
                    print(f' {Fore.RED}No artifact with index "{cmd}" in your inventory.', end='')

                    if len(artifact_list) >= 1:
                        print(f' Indexes go from 1 to {len(artifact_list)}{Style.RESET_ALL}\n')
                    else:
                        print()
                        print_empty_inv()

            elif cmd in ('clear', 'clr', 'c'):
                artifact_list.clear()
                save_inventory_to_file(artifact_list)
                print(f' {Fore.LIGHTGREEN_EX}Inventory cleared{Style.RESET_ALL}\n')

            elif cmd == 'cv':
                big_cv = max(artifact_list, key=lambda x: x.cv())
                print(f' #{artifact_list.index(big_cv) + 1}) {big_cv} - {big_cv.subs()}')
                print(f' CV: {big_cv.cv()}')
                print()

            elif cmd == 'rv':
                big_rv = max(artifact_list, key=lambda x: x.rv())
                print(f' #{artifact_list.index(big_rv) + 1}) {big_rv} - {big_rv.subs()}')
                print(f' RV: {big_rv.rv()}%')
                print()

            elif cmd in ('size', 'len', 'length'):
                print(
                    f' {len(artifact_list)} artifact{"s" if len(artifact_list) != 1 else ""} in inventory',
                    end='')
                if len(artifact_list) > 0:
                    print(':')
                    flower_count = 0
                    feather_count = 0
                    sands_count = 0
                    goblet_count = 0
                    circlet_count = 0
                    for i in artifact_list:
                        if i.type == 'Flower':
                            flower_count += 1
                        elif i.type == 'Feather':
                            feather_count += 1
                        elif i.type == 'Sands':
                            sands_count += 1
                        elif i.type == 'Goblet':
                            goblet_count += 1
                        else:
                            circlet_count += 1
                    print(f' {flower_count} Flower{"s" if flower_count != 1 else ""}\n'
                          f' {feather_count} Feather{"s" if feather_count != 1 else ""}\n'
                          f' {sands_count} Sands\n'
                          f' {goblet_count} Goblet{"s" if goblet_count != 1 else ""}\n'
                          f' {circlet_count} Circlet{"s" if circlet_count != 1 else ""}\n')
                else:
                    print('\n')

            elif cmd == 'load':
                try:
                    artifact_list = load_inventory()
                    print(f' {Fore.LIGHTGREEN_EX}Loaded inventory successfully!{Style.RESET_ALL}')
                    if len(artifact_list) == 0:
                        print(f' {Fore.LIGHTMAGENTA_EX}Inventory is empty{Style.RESET_ALL}')
                    else:
                        if len(artifact_list) <= 25:
                            print()
                            print_inventory(artifact_list)
                    print()

                except json.decoder.JSONDecodeError:
                    print(f' {Fore.RED}Something off with inventory file. Clearing inventory.txt{Style.RESET_ALL}')
                    artifact_list = []
                    save_inventory_to_file(artifact_list)
                    print(f' {Fore.LIGHTGREEN_EX}Inventory cleared{Style.RESET_ALL}\n')

            else:
                print(f' {Fore.RED}"{cmd}" is not a valid inventory command or index{Style.RESET_ALL}\n')
        else:
            print(f' {Fore.RED}You did something wrong.\n'
                  f' If you tried inputting multiple indexes, remove spaces between them{Style.RESET_ALL}\n')

    elif user_command in ('transmute', 'tr'):
        print()
        art, last = transmute()
        if art:
            artifact_log.append(art)
            if len(artifact_log) > 10:
                log_start = len(artifact_log) - 10
                artifact_log = artifact_log[log_start:]
            art.print_stats()
            print(f' {Fore.CYAN}Tip: Type "re" to create an artifact using the same preset!{Style.RESET_ALL}\n')

    elif user_command == 're':
        if last:
            art, last = transmute(last)
            artifact_log.append(art)
            if len(artifact_log) > 10:
                log_start = len(artifact_log) - 10
                artifact_log = artifact_log[log_start:]
            art.print_stats()
        else:
            print(f' {Fore.RED}Run "transmute" first{Style.RESET_ALL}\n')

    elif user_command == 'domain':
        # unsure why i added this lol felt like coming up with aliases
        print(f'\n {Fore.CYAN}Choose new domain (some aliases are supported):{Style.RESET_ALL}')
        new_source = [choose_one(domains, "That's not a domain that is available!\n Please input a number corresponding to the domain of choice", aliases_domain), 'domain']
        if new_source[0]:
            settings = [new_source, resin_max]
            save_settings_to_file()
            source = new_source
            joined_source = ', '.join(source[0])
            print(f' Source set to Domain: {Fore.LIGHTGREEN_EX}{joined_source}{Style.RESET_ALL}\n')
        else:
            print(f' {Fore.LIGHTMAGENTA_EX}Ok, no longer choosing domain{Style.RESET_ALL}\n')

    elif user_command == 'strongbox':
        print(f'\n {Fore.CYAN}Choose new artifact set (some aliases are supported):{Style.RESET_ALL}')
        new_source = [choose_one(sets, "That's not a set that is available! Try again", aliases_sets), 'strongbox']
        if new_source[0]:
            settings = [new_source, resin_max]
            save_settings_to_file()
            source = new_source
            print(f' Source set to Strongbox: {Fore.LIGHTGREEN_EX}{source[0]}{Style.RESET_ALL}\n')
        else:
            print(f' {Fore.LIGHTMAGENTA_EX}Ok, no longer choosing strongbox{Style.RESET_ALL}\n')

    elif user_command == 'boss':
        settings = [[(sets[0], sets[1]), 'boss'], resin_max]
        save_settings_to_file()
        source = settings[0]
        joined_source = ', '.join(source[0])
        print(f' Source set to Boss: {Fore.LIGHTGREEN_EX}{joined_source}{Style.RESET_ALL}\n')

    elif user_command == 'source':
        if source[1] == 'strongbox':
            print(f' Current source is Strongbox: {Fore.LIGHTGREEN_EX}{source[0]}{Style.RESET_ALL}\n')
        else:
            joined_source = ', '.join(source[0])
            print(f' Current source is {source[1].capitalize()}: {Fore.LIGHTGREEN_EX}{joined_source}{Style.RESET_ALL}\n')

    elif user_command == 'resin':
        print(f' {Fore.CYAN}Choose how much resin you use per day{Style.RESET_ALL} (180 default, {resin_max} current)\n')
        print(' (Type 0 to exit)\n')
        while True:
            try:
                max_resin = int(input(' Resin: '))
            except ValueError:
                print(f' {Fore.RED}Must be a number. Try again{Style.RESET_ALL}\n')
                continue
            if not max_resin:
                print(f' {Fore.LIGHTMAGENTA_EX}Ok, no longer choosing resin per day{Style.RESET_ALL}\n')
                break
            if max_resin < 180:
                print(f' {Fore.RED}Must be >= 180. Try again{Style.RESET_ALL}\n')
                continue
            if max_resin > 1000:
                print(f" {Fore.RED}Alright man, let's keep this reasonable. No more than 1000. Try again{Style.RESET_ALL}\n")
                continue
            resin_max = max_resin - max_resin % 20
            print(f' {Fore.LIGHTGREEN_EX}Daily resin set to {resin_max}{Style.RESET_ALL}\n')
            settings[1] = resin_max
            save_settings_to_file()
            break

    elif user_command[:5] == 'daily':
        if user_command.split() in (['daily', 's'], ['daily', 'save']):
            save = True
        elif user_command == 'daily':
            save = False
        else:
            print(f' {Fore.RED}You did something wrong.{Style.RESET_ALL}\n')
            continue
        print(f'\n {Fore.CYAN}Choose a domain (some aliases are supported):{Style.RESET_ALL}')
        domain_set = [choose_one(domains, "That's not a domain that is available!\n Please input a number corresponding to the domain of choice", aliases_domain), 'domain']
        if domain_set[0]:
            runs = resin_max//20
            artifact_log = []
            amount = 0
            save_success_message = ''
            save_success = True
            while runs:
                runs -= 1
                amount += choices((1, 2), weights=(28, 2))[0]  # 6.66% chance for 2 artifacts
            for k in range(amount):
                art = create_artifact(domain_set)
                artifact_log.append(art)
                if save:
                    if len(artifact_list) < 100000:
                        artifact_list.append(art)
                    else:
                        save_success = False
            artifact_log = sort_daily(artifact_log)
            if save:
                artifact_list = sort_inventory(artifact_list)
                save_inventory_to_file(artifact_list)
                if save_success:
                    save_success_message = f' {Fore.LIGHTGREEN_EX}Saving successful! {len(artifact_list)} artifact{"s" if len(artifact_list) != 1 else ""} in inventory{Style.RESET_ALL}\n'
                else:
                    print(f' {Fore.RED}Saving of one or more artifacts unsuccessful, inventory full (100k){Style.RESET_ALL}\n')

            print(f' {Fore.LIGHTCYAN_EX}Daily {resin_max} resin spent successfully! You got {amount} artifacts!{Style.RESET_ALL}')
            print(save_success_message, end='')
            print(f' You can move up and down in the list by typing log+ and log- (optional number after, e.g. "log- 5")\n')
            art = artifact_log[-1]
            print_log()

        else:
            print(f' {Fore.LIGHTMAGENTA_EX}Ok, not spending daily resin anymore{Style.RESET_ALL}\n')

    elif user_command in ('a rv', 'rv'):
        print(f' RV: {art.rv()}%\n')

    elif user_command in ('a cv', 'cv'):
        print(f' CV: {art.cv()}\n')

    elif user_command in ('artifact', 'a'):
        print()
        art.print_stats()

    else:
        print(f' Try {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL}\n')

if __name__ == '__main__':
    print('\n==================================================================')
    print('\n Thank you for using Artifact Simulator')
