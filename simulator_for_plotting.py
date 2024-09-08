# This program is essentially an advanced version of automation mode from artifact_simulator.py

# The additional functionality is as follows:
# You're not only getting the result for the requested Crit Value, but every value below that, too.
# Basically, you get info on how long every Crit Value took to get on average.
# This allows for a Crit Value vs. Time graph to be made - that's the purpose of this program.
# The list of values that this program prints out can be copied and used in plot.py (it can replicate the graph)


import datetime
import json
import sys
import time
from pathlib import Path
from random import choices, choice

import matplotlib.pyplot as plt
import numpy as np

Path('artifact_simulator_resources', 'plots').mkdir(exist_ok=True)

# sets = ("Gladiator's Finale", "Wanderer's Troupe",                                                             # bosses
#         "Noblesse Oblige", "Bloodstained Chivalry", "Maiden Beloved", "Viridescent Venerer", "Archaic Petra",  # 1.x
#         "Retracing Bolide", "Thundersoother", "Thundering Fury", "Lavawalker", "Crimson Witch of Flames",
#         "Blizzard Strayer", "Heart of Depth", "Tenacity of the Millelith", "Pale Flame",
#         "Shimenawa's Reminiscence", "Emblem of Severed Fate", "Husk of Opulent Dreams", "Ocean-Hued Clam",     # 2.x
#         "Vermillion Hereafter", "Echoes of an Offering",
#         "Deepwood Memories", "Gilded Dreams", "Desert Pavilion Chronicle", "Flower of Paradise Lost",          # 3.x
#         "Nymph's Dream", "Vourukasha's Glow",
#         "Marechaussee Hunter", "Golden Troupe", "Song of Days Past",                                           # 4.x
#         "Nighttime Whispers in the Echoing Woods", "Fragment of Harmonic Whimsy", "Unfinished Reverie",
#         "Scroll of the Hero of Cinder City", "Obsidian Codex", )                                               # 5.x
# sort_order_sets = {set_name: len(sets)-number for number, set_name in enumerate(sets)}
# sets_short = ('    Glad    ', '   Troupe   ',
#               '  Noblesse  ', 'Bloodstained',
#               '   Maiden   ', '     VV     ',
#               '  Archaic   ', '   Bolide   ',
#               '     TS     ', '     TF     ',
#               ' Lavawalker ', '     CW     ',
#               '  Blizzard  ', '    HoD     ',
#               '    TotM    ', ' Pale Flame ',
#               " Shimenawas ", '    EoSF    ',
#               '    Husk    ', '    Clam    ',
#               ' Vermillion ', '   Echoes   ',
#               '  Deepwood  ', '   Gilded   ',
#               ' Desert Pav ', '    FoPL    ',
#               "   Nymphs   ", "Vourukasha's",
#               '     MH     ', 'GoldenTroupe',
#               '    SoDP    ', '    NWEW    ',
#               '   Whimsy   ', '  Reverie   ',
#               '   Scroll   ', '  Obsidian  ',)
# aliases_domain = {'no': '1', 'nob': '1', 'noblesse': '1', 'bennett': '1',
#                   'vv': '2', 'kazuha': '2',
#                   'maidens': '2',
#                   'ap': '3', 'petra': '3',
#                   'bolide': '3',
#                   'tf': '4', 'keqing': '4', 'razor': '4',
#                   'cw': '5',
#                   'blizzard': '6', 'ayaka': '6',
#                   'hod': '6', 'childe': '6', 'tartaglia': '6',
#                   'tom': '7', 'totm': '7', 'zl': '7', 'zhongli': '7',
#                   'eula': '7',
#                   'shim': '8', 'shime': '8', 'sr': '8', 'hu tao': '8', 'tao': '8',
#                   'emblem': '8', 'eosf': '8', 'oppa': '8', 'xl': '8', 'raiden': '8', 'xiangling': '8', 'xingqiu': '8',
#                   'xq': '8',
#                   'husk': '9',
#                   'clam': '9', 'kokomi': '9', 'kok': '9',
#                   'vermillion': '10', 'vh': '10', 'zyox': '10', 'zy0x': '10', 'xiao': '10',
#                   'echoes': '10', 'ayato': '10',
#                   'deepwood': '11', 'dm': '11', 'nahida': '11',
#                   'gilded': '11', 'gd': '11', 'alhaihtam': '11',
#                   'dpc': '12', 'scara': '12', 'wanderer': '12', 'xіangling': '12',
#                   'fopl': '12', 'flop': '12',
#                   'vg': '13', 'dehya': '13',
#                   'mh': '14', 'neuv': '14', 'neuvillette': '14', 'bat': '14',
#                   'gt': '14', 'furina': '14', 'fischl': '14',
#                   'sodp': '15', 'bird': '15', 'xianyun': '15', 'xy': '15',
#                   'navia': '15',
#                   'whimsy': '16', 'arle': '16', 'arlecchino': '16', 'father': '16', 'clorinde': '16',
#                   'emilie': '16',
#                   'natlan': '17', 'scroll': '17',
#                   'codex': '17', 'mualani': '17'
#                   }
# aliases_sets = {'glad': '1',
#                 'troupe': '2',
#                 'no': '3', 'nob': '3', 'noblesse': '3', 'bennett': '3',
#                 'maidens': '5',
#                 'vv': '6', 'kazuha': '6',
#                 'ap': '7', 'petra': '7',
#                 'bolide': '8',
#                 'tf': '10', 'keqing': '10', 'razor': '10',
#                 'cw': '12',
#                 'blizzard': '13', 'ayaka': '13',
#                 'hod': '14', 'childe': '14', 'tartaglia': '14',
#                 'tom': '15', 'totm': '15', 'zl': '15', 'zhongli': '15',
#                 'eula': '16',
#                 'shim': "17", 'shime': "17", 'sr': "17", 'hu tao': "17", 'tao': "17",
#                 'emblem': '18', 'eosf': '18', 'oppa': '18', 'xl': '18', 'raiden': '18', 'xiangling': '18', 'xingqiu': '18',
#                 'xq': '18',
#                 'husk': '19',
#                 'clam': '20', 'kokomi': '20', 'kok': '20',
#                 'vermillion': '21', 'vh': '21', 'zyox': '21', 'zy0x': '21', 'xiao': '21',
#                 'echoes': '22', 'ayato': '22',
#                 'deepwood': '23', 'dm': '23', 'nahida': '23',
#                 'gilded': '24', 'gd': '24', 'alhaihtam': '24',
#                 'dpc': '25', 'scara': '25', 'wanderer': '25', 'xіangling': '25',
#                 'fopl': '26', 'flop': '26',
#                 'vg': "28", 'dehya': "28",
#                 'mh': '29', 'neuv': '29', 'neuvillette': '29', 'bat': '29',
#                 'gt': '30', 'furina': '30', 'fischl': '30',
#                 'sodp': '31', 'bird': '31', 'xianyun': '31', 'xy': '31',
#                 'navia': '32',
#                 'whimsy': '33', 'arle': '33', 'arlecchino': '33', 'father': '33', 'clorinde': '33',
#                 'emilie': '34',
#                 'natlan': '35', 'scroll': '35',
#                 'codex': '36', 'mualani': '36'
#                 }
#
# sets_short_dict = dict(zip(sets, sets_short))
# domains = list(list(s) for s in (zip(sets[2::2], sets[3::2])))
#
# strongbox_set = choice(sets)
# domain_set = choice(domains)
# abyss_sets = sets[-2:]

artifact_types = ('Flower', 'Feather', 'Sands', 'Goblet', 'Circlet')
sands_main_stats = ('HP%', 'ATK%', 'DEF%', 'ER%', 'EM')
goblet_main_stats = ('Pyro DMG% Bonus', 'Hydro DMG% Bonus', 'Cryo DMG% Bonus',
                     'Electro DMG% Bonus', 'Anemo DMG% Bonus',
                     'Geo DMG% Bonus', 'Physical DMG% Bonus',
                     'Dendro DMG% Bonus', 'HP%', 'ATK%', 'DEF%', 'EM')
circlet_main_stats = ('HP%', 'ATK%', 'DEF%', 'EM', 'CRIT DMG%', 'CRIT Rate%',
                      'Healing Bonus')
substats = ('HP', 'ATK', 'DEF', 'HP%', 'ATK%', 'DEF%', 'ER%', 'EM',
            'CRIT Rate%', 'CRIT DMG%')
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
    'ATK': 19.45000076,
    'DEF': 23.149999,
    'HP%': 5.8335,
    'ATK%': 5.8335,
    'DEF%': 7.289999,
    'EM': 23.309999,
    'ER%': 6.4800001,
    'CRIT Rate%': 3.889999,
    'CRIT DMG%': 7.769999
}
possible_rolls = (0.7, 0.8, 0.9, 1.0)

sands_main_stats_weights = (26.68, 26.66, 26.66, 10.0, 10.0)
goblet_main_stats_weights = (5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 19.25,
                             19.25, 19.0, 2.5)
circlet_main_stats_weights = (22.0, 22.0, 22.0, 4.0, 10.0, 10.0, 10.0)
substats_weights = (6, 6, 6, 4, 4, 4, 4, 4, 3, 3)


class Artifact:
    def __init__(self, artifact_type, mainstat, mainstat_value, threeliner, sub_stats, level,
                 last_upgrade="", roll_value=0):
        self.type = artifact_type
        self.mainstat = mainstat
        self.mainstat_value = mainstat_value
        self.threeliner = threeliner
        self.substats = sub_stats
        self.level = level
        self.last_upgrade = last_upgrade
        self.roll_value = roll_value

        if "CRIT Rate%" in self.substats:
            if self.substats["CRIT Rate%"] == 23.0:
                self.substats["CRIT Rate%"] = 22.9

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
        # - CRIT DMG%: 14.8
        # - HP%: 14.6
        # - DEF%: 5.8
        print(" ", end='')
        print(self)

        for sub in self.substats:
            is_percentage = '%' in sub
            print(f" - {sub}: {str(round(self.substats[sub], 1)) if is_percentage else round(self.substats[sub])}{' (+)' if sub == self.last_upgrade else ''}")

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

    def rv(self):
        return int(self.roll_value)


def take_input(defaults=(1, 50)):
    valid_exit = ('exit', "'exit'", '"exit"')
    ok1 = False
    ok2 = False
    print("\nPlease input conditions. Type 'exit' to go back to menu.\n"
          f"Leave blank to use defaults ({defaults[0]} test{'s' if defaults[0] != 1 else ''}, {defaults[1]} CV).\n")

    while not ok1:
        size = input("Number of tests to run: ")
        if size:
            if size.lower() in valid_exit:
                return 'exit', 0

            try:
                if int(size) > 0:
                    ok1 = True
                else:
                    print("Needs to be positive. Try again.\n")

            except ValueError:
                print("Needs to be an integer. Try again.\n")

        else:
            ok1 = True
            size = defaults[0]

    while not ok2:
        cv = input("Desired Crit Value: ")
        if cv:
            if cv.lower() in valid_exit:
                return 0, 'exit'

            try:
                if float(cv) > 0:
                    ok2 = True
                else:
                    print("Needs to be positive. Try again.\n")

            except ValueError:
                print("Needs to be a number. Try again.\n")

        else:
            ok2 = True
            cv = defaults[1]

    print(f"Running {int(size)} simulation{'s' if int(size) != 1 else ''}, looking for at least {min(54.5, float(cv))} CV.")
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


def create_artifact(from_where):
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
    # artifact_set = exact_source if from_where == 'strongbox' else choice(exact_source)
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

    return Artifact(art_type, mainstat, mainstat_value, threeliner, subs, 0, "", rv)


def compare_to_highest_cv(artifact, fastest, slowest, days_list, artifacts, day_number, artifact_number, cv_want,
                          only_one):
    if artifact.cv() >= min(54.5, cv_want):
        days_list.append(day_number)
        artifacts.append(artifact_number)

        if fastest[0] == 0 or day_number < fastest[0]:
            fastest = (day_number, artifact)

        if day_number > slowest[0]:
            slowest = (day_number, artifact)
        # print(artifact.subs())

        if not only_one:
            print(f'Artifacts generated: {artifact_number}')

    return fastest, slowest, days_list, artifacts, artifact.cv() >= min(54.5, cv_want)


dict_of_days_total = {0.0: 0.0}
dict_of_days_average = {0.0: 0.0}


def create_and_roll_artifact(arti_source, highest_cv, cv_want, d):
    artifact = create_artifact(arti_source)

    for j in range(5):
        artifact.upgrade()

    a_cv = artifact.cv()

    if a_cv > highest_cv:
        if highest_cv == 0:
            dict_of_days_total[0] += 1

        for q in range(int(highest_cv * 10) + 1, int(min(a_cv * 10, cv_want * 10)) + 1):
            if q / 10 in dict_of_days_total:
                dict_of_days_total[q / 10] += d
            else:
                dict_of_days_total[q / 10] = d

        highest_cv = a_cv

    return artifact, highest_cv


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

    if num == 12:  # yes this is spaghetti code.
        if len(result[result <= 55]) <= num:
            return insert_average(result, num)
    else:
        if len(result) <= num:
            return insert_average(result, num)

    return result[result <= 55] if num == 12 else result


def plot_this(plot_cv, plot_days, range_cv, amount_of_tests, desired_cv, endless=True):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    if len(plot_cv) == 1:
        ax[0].scatter(plot_cv, plot_days, color='red', label='Single Point')
        ax[1].scatter(plot_cv, plot_days, color='red', label='Single Point')
    else:
        ax[0].plot(plot_cv, plot_days, label='Data')
        ax[1].plot(plot_cv, plot_days, label='Data')

    # Plot for the False value (left subplot)
    ax[0].set_title('Regular')
    ax[0].set_xlabel("Crit Value")
    ax[0].set_ylabel("Days to reach CV")
    ax[0].tick_params(axis='x', rotation=60)  # Rotate x-axis labels

    # Plot for the True value (right subplot)
    ax[1].set_title('Logarithmic')
    ax[1].set_xlabel("Crit Value")
    ax[1].set_yscale('log')
    ax[1].tick_params(axis='x', rotation=60)  # Rotate x-axis labels

    for a in ax:
        a.grid(True)

    ax[0].set_xticks(insert_average(ax[0].get_xticks(), 12))
    ax[0].set_yticks(insert_average(ax[0].get_yticks(), 11))
    ax[1].set_xticks(insert_average(ax[1].get_xticks(), 12))

    fig.suptitle(f"Average time to reach Crit Value (sample size = {amount_of_tests:,})")
    plt.tight_layout()
    # plt.grid()

    if int(range_cv[0]) == range_cv[0]:
        from_cv = max(int(range_cv[0]), 0)
    else:
        from_cv = max(range_cv[0], 0)

    is_int = int(desired_cv) if int(desired_cv) == desired_cv else desired_cv

    if int(range_cv[1]) == range_cv[1]:
        to_cv = min(int(range_cv[1]), is_int)
    else:
        to_cv = min(range_cv[1], is_int)
    plt.savefig(Path('artifact_simulator_resources', 'plots', f'(Days distribution) {amount_of_tests} sample size', f'Plot of {from_cv}CV to {to_cv}CV (size = {amount_of_tests}).png'),
                dpi=900)

    print("Here you go. This was also saved as a .png file.")
    if endless:
        print("(To continue, close the graph if this is the last line you see)")
    plt.show()

    if endless:
        print("\nYou can plot another graph now if you want.\n")


if __name__ == "__main__":
    sample_size, cv_desired = take_input((100, 50))

    if sample_size == 'exit' or cv_desired == 'exit':
        print("Exiting program")
        sys.exit()

    sample_size, cv_desired = int(sample_size), float(cv_desired)
    days_it_took_to_reach_desired_cv = []
    artifacts_generated = []
    Path('artifact_simulator_resources', 'plots', f'(Days distribution) {sample_size} sample size').mkdir(parents=True, exist_ok=True)

    low = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))
    high = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))

    sample_size_is_one = sample_size == 1
    start = time.perf_counter()

    for i in range(sample_size):
        c = 0
        day = 0
        highest = 0
        total_generated = 0
        inventory = 0
        flag = False

        if (i + 1) % 25 == 0:
            print("\nResults so far:")

            for dd in dict_of_days_total:
                dict_of_days_average[dd] = round(dict_of_days_total[dd] / i, 2)

            print('Dict:', dict_of_days_average)
            print('List:', list(dict_of_days_average.values()))
            print()

        print(f'Now running simulation {i + 1}...', end=' ')
        while not flag:
            day += 1
            # print(f'new day {day}')

            if day % 10000 == 0:
                print(f'Day {day} - still going')

            if day % 30 == 0:  # 4 artifacts from abyss every 30 days
                for k in range(4):
                    inventory += 1
                    total_generated += 1
                    art, highest = create_and_roll_artifact('abyss', highest, cv_desired, day)
                    low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                        compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv, artifacts_generated,
                                              day, total_generated, cv_desired, sample_size_is_one))
                    if flag:
                        break
                if flag:
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
                inventory += amount[0]

                for k in range(amount[0]):
                    art, highest = create_and_roll_artifact("domain", highest, cv_desired, day)
                    low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                        compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv, artifacts_generated,
                                              day, total_generated, cv_desired, sample_size_is_one))
                    if flag:
                        break
                if flag:
                    break

            else:
                while inventory >= 3:
                    # print(f'strongbox {inventory}')
                    inventory -= 2
                    total_generated += 1
                    art, highest = create_and_roll_artifact("strongbox", highest, cv_desired, day)
                    low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                        compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv, artifacts_generated,
                                              day, total_generated, cv_desired, sample_size_is_one))
                    if flag:
                        break
                # print(f'{inventory} left in inventory')

    end = time.perf_counter()
    days = round(sum(days_it_took_to_reach_desired_cv) / sample_size, 2)

    if sample_size > 1:
        print(f'\nOut of {sample_size} simulations, it took an average of {days} days ({round(days / 365.25, 2)} years) to reach {cv_desired} CV.')
        print(f'Fastest - {low[0]} days: {low[1].subs()}')
        print(f'Slowest - {high[0]} days ({round(high[0] / 365.25, 2)} years): {high[1].subs()}')
    else:
        print(f'It took {low[0]} days (or {round(high[0] / 365.25, 2)} years)!')

    print(f'Total artifacts generated: {sum(artifacts_generated)}')

    run_time = end - start
    to_hours = time.strftime("%T", time.gmtime(run_time))
    decimals = f'{(run_time % 1):.3f}'

    print(f'\nThe simulation{"s" if sample_size > 1 else ""} took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
    print(f'Performance: {round(sum(artifacts_generated) / run_time / 1000, 2)} artifacts per ms')
    # print(run_time)

    for i in dict_of_days_total:
        dict_of_days_average[i] = round(dict_of_days_total[i] / sample_size, 2)

    days_for_plotting = list(dict_of_days_average.values())
    cv_for_plotting = np.arange(cv_desired * 10 + 1) / 10

    print('Dict:', dict_of_days_average)
    print('List:', days_for_plotting)
    print()

    with open(Path('artifact_simulator_resources', 'plots', f'(Days distribution) {sample_size} sample size', f'{cv_desired}CV - {sample_size} at {str(datetime.datetime.now())[:-7].replace(":", "-")}.txt'), 'w') as file:
        file.write(json.dumps(days_for_plotting))

    plot_this(cv_for_plotting, days_for_plotting, [0.0, cv_desired], sample_size, cv_desired)

    first_time = True
    while True:
        print('What CV range would you like to see the plot for?')

        if first_time:
            print('Leave blank to use the entire range. Type "exit" to quit.')
            print('Example: 20.5:45')
            first_time = False

        user_cmd = input('Range: ')
        if user_cmd:
            if user_cmd in ('exit', "'exit'", '"exit"', '0'):
                break

            try:
                cv_range = list(map(float, user_cmd.split(':')))
                if (cv_range[0] > cv_desired or
                        cv_range[1] < 0 or
                        cv_range[1] < cv_range[0]):
                    print('Invalid range, try again\n')
                    continue

            except:
                print('Invalid, try again\n')
                continue

        else:
            cv_range = [0.0, cv_desired]

        days_plot = days_for_plotting[max(int(cv_range[0] * 10), 0):min(int(cv_range[1] * 10 + 1), int(cv_desired * 10 + 1))]
        cv_plot = cv_for_plotting[max(int(cv_range[0] * 10), 0):min(int(cv_range[1] * 10 + 1), int(cv_desired * 10 + 1))]

        print()
        print('Values:', days_plot)
        print()

        plot_this(cv_plot, days_plot, cv_range, sample_size, cv_desired)

    print('\nThank you for using Artifact Simulator (plotting edition)')
