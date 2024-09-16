# This program is an artifact simulator!

# You can
# 1 - Roll artifacts one-by-one as if you have unlimited resin, upgrade them, save them to your inventory etc.
# 2 - Set a Crit Value requirement and roll artifacts automatically until an artifact with enough CV is found
#     to find out how long that takes - in days and years (assuming all of your resin goes into artifact farming)
#     You can also run multiple tests and find out the average amount of time that took!

try:
    import json
    import time
    import datetime

    import numpy as np
    import matplotlib.pyplot as plt
    from colorama import init, Fore, Style
    from operator import itemgetter
    from random import choice, choices
    from math import ceil
    from pathlib import Path
    import customtkinter as ctk
    from PIL import Image
    from tkinter import Toplevel

except ModuleNotFoundError:
    print(' Run `pip install numpy matplotlib colorama customtkinter` and launch the simulator again')
    exit()

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

if not Path('res').exists():
    Path('res').mkdir(parents=True, exist_ok=True)
    print(f' {Fore.RED}Inventory sacrificed due to an update. o7{Style.RESET_ALL}')
    with open(Path('artifact_simulator_resources', 'inventory.txt'), 'w') as file:
        file.write('[]')


class Artifact:
    def __init__(self, artifact_type, mainstat, mainstat_value, threeliner, sub_stats, level, artifact_set,
                 last_upgrade="", roll_value={}):
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

    def print_stats(self, show_rv=False):

        # 311 ATK Feather (+20)
        # - HP: 418
        # - Crit DMG%: 14.8
        # - HP%: 14.6
        # - DEF%: 5.8
        print(" ", end='')
        print(self)

        for sub in self.substats:
            is_percentage = '%' in sub
            rv_num = f' ({int(self.roll_value[sub])}%)' + (self.roll_value[sub] < 100)*' ' if show_rv else ''
            print(f"{rv_num} - {sub}: {str(round(self.substats[sub], 1)) if is_percentage else round(self.substats[sub])}{f' {Fore.GREEN}(+){Style.RESET_ALL}' if sub == self.last_upgrade else ''}")

        self.last_upgrade = ""
        if show_rv:
            print(f' {Fore.CYAN}RV: {self.rv()}%{Style.RESET_ALL}')
        print()

    def upgrade(self):
        if self.level != 20:
            roll = choice(possible_rolls)

            if self.threeliner:
                self.substats[self.threeliner] = max_rolls[self.threeliner] * roll
                self.last_upgrade = self.threeliner
                self.roll_value[self.threeliner] = roll * 100
                self.threeliner = 0

            else:
                sub = choice(list(self.substats.keys()))
                self.substats[sub] += max_rolls[sub] * roll
                self.last_upgrade = sub
                self.roll_value[sub] += roll * 100

            self.level += 4
            self.mainstat_value[1] += 1

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
        return sum(self.roll_value.values())


class ArtifactEncoder(json.JSONEncoder):
    def default(self, artifact):
        return [artifact.type, artifact.mainstat, artifact.mainstat_value, artifact.threeliner, artifact.substats,
                artifact.level, artifact.set, artifact.last_upgrade, artifact.roll_value]


def choose_one(items, error_message, alias={}, blank_ok=False, skip_ok=False, what=('choice number', 'hint')):
    items_dict = dict(zip([str(ind) for ind in range(1, len(items)+1)], items))
    if isinstance(items_dict['1'], tuple) or isinstance(items_dict['1'], list):
        for item in items_dict.items():
            joined_item = ', '.join(item[1])
            print(f" {item[0]} = {joined_item}")
    else:
        for item in items_dict.items():
            print(f" {item[0]} = {item[1]}")
    skip = ' or "skip" to skip all advanced settings' if skip_ok else ''
    print(f'\n (Type 0 to exit{skip})\n')
    while True:
        new1 = input(' Your pick: ').strip()
        if what != ('choice number', 'hint') and new1.lower() in ('what', what[0], items_dict[what[0]].lower()):
            print(f' {what[1]}\n')
            continue
        if new1 in ('0', 'exit'):
            return 0
        if new1 == 'skip' and skip_ok:
            return 'skip'
        if not new1 and blank_ok:
            return 'blank'
        if new1 in items_dict or new1 in items_dict.values():
            break
        if alias and new1.lower() in alias and alias[new1] in items:
            new1 = alias[new1]
            break
        else:
            print(f' {Fore.RED}{error_message}{Style.RESET_ALL}\n')
    if isinstance(new1, str) and new1 in items_dict:
        new1 = items_dict[new1]
    return new1

# ADD NEW SETS HERE
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
set_images = ('glad.png', 'wt.png',
              'nob.png', 'bs.png', 'maiden.png', 'vv.png', 'petra.png',
              'bolide.png', 'ts.png', 'tf.png', 'lavawalker.png', 'cw.png',
              'blizzard.png', 'hod.png', 'totm.png', 'pf.png',
              'shime.png', 'eosf.png', 'husk.png', 'ohc.png', 'vh.png', 'echoes.png',
              'deepwood.png', 'gd.png', 'dpc.png', 'fopl.png', 'nymph.png', 'vg.png',
              'mh.png', 'gt.png', 'sodp.png', 'nwew.png', 'whimsy.png', 'reverie.png',
              'scroll.png', 'obsidian.png', )
set_to_image = {set_name: Path('assets', set_image) for set_name, set_image in zip(sets, set_images)}
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
aliases_domain = {'no': ['Noblesse Oblige', 'Bloodstained Chivalry'], 'nob': ['Noblesse Oblige', 'Bloodstained Chivalry'], 'noblesse': ['Noblesse Oblige', 'Bloodstained Chivalry'], 'bennett': ['Noblesse Oblige', 'Bloodstained Chivalry'],
                  'vv': ['Maiden Beloved', 'Viridescent Venerer'], 'kazuha': ['Maiden Beloved', 'Viridescent Venerer'], 'sucrose': ['Maiden Beloved', 'Viridescent Venerer'],
                  'maidens': ['Maiden Beloved', 'Viridescent Venerer'], 'maiden': ['Maiden Beloved', 'Viridescent Venerer'],
                  'ap': ['Archaic Petra', 'Retracing Bolide'], 'petra': ['Archaic Petra', 'Retracing Bolide'],
                  'bolide': ['Archaic Petra', 'Retracing Bolide'],
                  'tf': ['Thundersoother', 'Thundering Fury'], 'keqing': ['Thundersoother', 'Thundering Fury'], 'razor': ['Thundersoother', 'Thundering Fury'],
                  'cw': ['Lavawalker', 'Crimson Witch of Flames'],
                  'blizzard': ['Blizzard Strayer', 'Heart of Depth'], 'ayaka': ['Blizzard Strayer', 'Heart of Depth'],
                  'hod': ['Blizzard Strayer', 'Heart of Depth'], 'childe': ['Blizzard Strayer', 'Heart of Depth'], 'tartaglia': ['Blizzard Strayer', 'Heart of Depth'],
                  'tom': ['Tenacity of the Millelith', 'Pale Flame'], 'totm': ['Tenacity of the Millelith', 'Pale Flame'], 'zl': ['Tenacity of the Millelith', 'Pale Flame'], 'zhongli': ['Tenacity of the Millelith', 'Pale Flame'],
                  'eula': ['Tenacity of the Millelith', 'Pale Flame'],
                  'shim': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'shime': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'sr': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'hu tao': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'tao': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'hutao': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'],
                  'emblem': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'eosf': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'oppa': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'xl': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'raiden': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'xiangling': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'xingqiu': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'xq': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'], 'yelan': ["Shimenawa's Reminiscence", 'Emblem of Severed Fate'],
                  'husk': ['Husk of Opulent Dreams', 'Ocean-Hued Clam'],
                  'clam': ['Husk of Opulent Dreams', 'Ocean-Hued Clam'], 'kokomi': ['Husk of Opulent Dreams', 'Ocean-Hued Clam'], 'kok': ['Husk of Opulent Dreams', 'Ocean-Hued Clam'],
                  'vermillion': ['Vermillion Hereafter', 'Echoes of an Offering'], 'vh': ['Vermillion Hereafter', 'Echoes of an Offering'], 'verm': ['Vermillion Hereafter', 'Echoes of an Offering'], 'peam': ['Vermillion Hereafter', 'Echoes of an Offering'], 'zyox': ['Vermillion Hereafter', 'Echoes of an Offering'], 'zy0x': ['Vermillion Hereafter', 'Echoes of an Offering'], 'xiao': ['Vermillion Hereafter', 'Echoes of an Offering'],
                  'echoes': ['Vermillion Hereafter', 'Echoes of an Offering'], 'ayato': ['Vermillion Hereafter', 'Echoes of an Offering'],
                  'deepwood': ['Deepwood Memories', 'Gilded Dreams'], 'dm': ['Deepwood Memories', 'Gilded Dreams'], 'nahida': ['Deepwood Memories', 'Gilded Dreams'],
                  'gilded': ['Deepwood Memories', 'Gilded Dreams'], 'gd': ['Deepwood Memories', 'Gilded Dreams'], 'alhaihtam': ['Deepwood Memories', 'Gilded Dreams'],
                  'dpc': ['Desert Pavilion Chronicle', 'Flower of Paradise Lost'], 'scara': ['Desert Pavilion Chronicle', 'Flower of Paradise Lost'], 'wanderer': ['Desert Pavilion Chronicle', 'Flower of Paradise Lost'], 'xіangling': ['Desert Pavilion Chronicle', 'Flower of Paradise Lost'], 'sami': ['Desert Pavilion Chronicle', 'Flower of Paradise Lost'],
                  'fopl': ['Desert Pavilion Chronicle', 'Flower of Paradise Lost'], 'flop': ['Desert Pavilion Chronicle', 'Flower of Paradise Lost'],
                  'vg': ["Nymph's Dream", "Vourukasha's Glow"], 'dehya': ["Nymph's Dream", "Vourukasha's Glow"],
                  'mh': ['Marechaussee Hunter', 'Golden Troupe'], 'neuv': ['Marechaussee Hunter', 'Golden Troupe'], 'neuvillette': ['Marechaussee Hunter', 'Golden Troupe'], 'bat': ['Marechaussee Hunter', 'Golden Troupe'],
                  'gt': ['Marechaussee Hunter', 'Golden Troupe'], 'furina': ['Marechaussee Hunter', 'Golden Troupe'], 'fischl': ['Marechaussee Hunter', 'Golden Troupe'],
                  'sodp': ['Song of Days Past', 'Nighttime Whispers in the Echoing Woods'], 'bird': ['Song of Days Past', 'Nighttime Whispers in the Echoing Woods'], 'xianyun': ['Song of Days Past', 'Nighttime Whispers in the Echoing Woods'], 'xy': ['Song of Days Past', 'Nighttime Whispers in the Echoing Woods'],
                  'navia': ['Song of Days Past', 'Nighttime Whispers in the Echoing Woods'],
                  'whimsy': ['Fragment of Harmonic Whimsy', 'Unfinished Reverie'], 'arle': ['Fragment of Harmonic Whimsy', 'Unfinished Reverie'], 'arlecchino': ['Fragment of Harmonic Whimsy', 'Unfinished Reverie'], 'father': ['Fragment of Harmonic Whimsy', 'Unfinished Reverie'], 'clorinde': ['Fragment of Harmonic Whimsy', 'Unfinished Reverie'],
                  'emilie': ['Fragment of Harmonic Whimsy', 'Unfinished Reverie'],
                  'natlan': ['Scroll of the Hero of Cinder City', 'Obsidian Codex'], 'scroll': ['Scroll of the Hero of Cinder City', 'Obsidian Codex'],
                  'codex': ['Scroll of the Hero of Cinder City', 'Obsidian Codex'], 'mualani': ['Scroll of the Hero of Cinder City', 'Obsidian Codex'],
                  }
aliases_sets = {'glad': "Gladiator's Finale",
                'troupe': "Wanderer's Troupe",
                'no': "Noblesse Oblige", 'nob': "Noblesse Oblige", 'noblesse': "Noblesse Oblige", 'bennett': "Noblesse Oblige",
                'maidens': "Maiden Beloved", 'maiden': "Maiden Beloved",
                'vv': "Viridescent Venerer", 'kazuha': "Viridescent Venerer", 'sucrose': "Viridescent Venerer",
                'ap': "Archaic Petra", 'petra': "Archaic Petra",
                'bolide': "Retracing Bolide",
                'tf': "Thundering Fury", 'keqing': "Thundering Fury", 'razor': "Thundering Fury",
                'cw': "Crimson Witch of Flames",
                'blizzard': "Blizzard Strayer", 'ayaka': "Blizzard Strayer",
                'hod': "Heart of Depth", 'childe': "Heart of Depth", 'tartaglia': "Heart of Depth",
                'tom': "Tenacity of the Millelith", 'totm': "Tenacity of the Millelith", 'zl': "Tenacity of the Millelith", 'zhongli': "Tenacity of the Millelith",
                'eula': "Pale Flame",
                'shim': "Shimenawa's Reminiscence", 'shime': "Shimenawa's Reminiscence", 'sr': "Shimenawa's Reminiscence", 'hu tao': "Shimenawa's Reminiscence", 'tao': "Shimenawa's Reminiscence", 'hutao': "Shimenawa's Reminiscence",
                'emblem': "Emblem of Severed Fate", 'eosf': "Emblem of Severed Fate", 'oppa': "Emblem of Severed Fate", 'xl': "Emblem of Severed Fate", 'raiden': "Emblem of Severed Fate", 'xiangling': "Emblem of Severed Fate", 'xingqiu': "Emblem of Severed Fate",
                'xq': "Emblem of Severed Fate", 'yelan': "Emblem of Severed Fate",
                'husk': "Husk of Opulent Dreams",
                'clam': "Ocean-Hued Clam", 'kokomi': "Ocean-Hued Clam", 'kok': "Ocean-Hued Clam",
                'vermillion': "Vermillion Hereafter", 'vh': "Vermillion Hereafter", 'verm': "Vermillion Hereafter", 'peam': "Vermillion Hereafter", 'zyox': "Vermillion Hereafter", 'zy0x': "Vermillion Hereafter", 'xiao': "Vermillion Hereafter",
                'echoes': "Echoes of an Offering", 'ayato': "Echoes of an Offering",
                'deepwood': "Deepwood Memories", 'dm': "Deepwood Memories", 'nahida': "Deepwood Memories",
                'gilded': "Gilded Dreams", 'gd': "Gilded Dreams", 'alhaihtam': "Gilded Dreams",
                'dpc': "Desert Pavilion Chronicle", 'scara': "Desert Pavilion Chronicle", 'wanderer': "Desert Pavilion Chronicle", 'xіangling': "Desert Pavilion Chronicle", 'sami': "Desert Pavilion Chronicle",
                'fopl': "Flower of Paradise Lost", 'flop': "Flower of Paradise Lost",
                'vg': "Vourukasha's Glow", 'dehya': "Vourukasha's Glow",
                'mh': "Marechaussee Hunter", 'neuv': "Marechaussee Hunter", 'neuvillette': "Marechaussee Hunter", 'bat': "Marechaussee Hunter",
                'gt': "Golden Troupe", 'furina': "Golden Troupe", 'fischl': "Golden Troupe",
                'sodp': "Song of Days Past", 'bird': "Song of Days Past", 'xianyun': "Song of Days Past", 'xy': "Song of Days Past",
                'navia': "Nighttime Whispers in the Echoing Woods",
                'whimsy': "Fragment of Harmonic Whimsy", 'arle': "Fragment of Harmonic Whimsy", 'arlecchino': "Fragment of Harmonic Whimsy", 'father': "Fragment of Harmonic Whimsy", 'clorinde': "Fragment of Harmonic Whimsy",
                'emilie': "Unfinished Reverie",
                'natlan': "Scroll of the Hero of Cinder City", 'scroll': "Scroll of the Hero of Cinder City",
                'codex': "Obsidian Codex", 'mualani': "Obsidian Codex",
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
type_to_main_stats = dict(zip(artifact_types, (('HP',), ('ATK',), sands_main_stats, goblet_main_stats, circlet_main_stats)))
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
    valid_exit = ['exit', "'exit'", '"exit"']
    ok1 = False
    ok2 = False
    print('\n Please input conditions. Type "exit" to go back\n'
          f" Leave blank to use defaults ({defaults[0]} test{'s' if defaults[0] != 1 else ''}, {defaults[1]} CV)\n")

    while not ok1:
        size = input(" Number of tests to run: ")
        if size:
            if size.lower() in valid_exit+['0']:
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
# last_auto = 0
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
    rv = {sub_stat_1: sub_stat_1_roll * 100, sub_stat_2: sub_stat_2_roll * 100}

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
        rv[sub] = roll * 100
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
    rv = {}

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
        rv[sub] = roll * 100

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
    # highest_cv is only 0 when it's not passed
    artifact = create_artifact(arti_source)

    if not highest_cv and not silent:
        artifact.print_stats()

    for j in range(5):
        artifact.upgrade()
        if not highest_cv and not silent:
            artifact.print_stats()
    art_cv = artifact.cv()
    if (highest_cv and art_cv > highest_cv and
            (set_requirement == 'none' or artifact.set == set_requirement) and
            (type_requirement == 'none' or artifact.type == type_requirement) and
            (main_stat_requirement == 'none' or artifact.mainstat == main_stat_requirement) and
            (sub_stat_mode != '0' or not sub_stat_requirement or all(i in artifact.substats for i in sub_stat_requirement)) and
            (not rv_requirement or sum([i[1] for i in artifact.roll_value.items() if i[0] in sub_stat_requirement]) >= rv_requirement)):
        # even if highest_cv is supposed to be set to 0 it's set to 1
        highest_cv = art_cv + (art_cv == 0)
        if not silent:
            print(f'\r Day {day}: {art_cv} CV - {artifact.short()} {artifact.subs()}')

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


def compare_to_wanted_cv(artifact, fastest, slowest, days_list, artifacts, day_number, artifact_number, cv_want,
                         only_one):
    new_winner = ((artifact.cv() >= min(54.5, cv_want)) and
                  (set_requirement == 'none' or artifact.set == set_requirement) and
                  (type_requirement == 'none' or artifact.type == type_requirement) and
                  (main_stat_requirement == 'none' or artifact.mainstat == main_stat_requirement) and
                  (sub_stat_mode != '0' or not sub_stat_requirement or all(i in artifact.substats for i in sub_stat_requirement)) and
                  (not rv_requirement or sum([i[1] for i in artifact.roll_value.items() if i[0] in sub_stat_requirement]) >= rv_requirement))
    if new_winner:
        days_list.append(day_number)
        artifacts.append(artifact_number)

        if fastest[0] == 0 or artifact_number < fastest[1]:
            fastest = (day_number, artifact_number, artifact)

        if artifact_number > slowest[1]:
            slowest = (day_number, artifact_number, artifact)
        # print(artifact.subs())
        if rv_requirement:
            print(f' {Fore.LIGHTCYAN_EX}{int(sum([i[1] for i in artifact.roll_value.items() if i[0] in sub_stat_requirement]))}% RV{Style.RESET_ALL} ({int(artifact.rv())}% Total)')
        if not only_one:
            print(f' Artifacts generated: {Fore.LIGHTMAGENTA_EX}{artifact_number}{Style.RESET_ALL}')

    return fastest, slowest, days_list, artifacts, new_winner


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
    exact_time = str(datetime.datetime.now())[:-7].replace(":", "-")
    plt.savefig(Path('artifact_simulator_resources', 'plots', f'(CV distribution) {amount_of_artifacts} sample size', f"Plot of {amount_of_artifacts} artifact{s}'{ap} CV{s} at {exact_time}.png"),
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


# GUI FUNCTIONS
def update_button_state():
    """Updates the state of the transmute button and controls the enabling/disabling of substat checkboxes."""
    selected_substats = sum([var.get() for var in substat_vars])

    # Enable/disable the transmute button based on the number of selected substats
    if selected_substats == 2:
        transmute_button.configure(state="normal")
        # Disable all checkboxes that are not selected
        for i, var in enumerate(substat_vars):
            if not var.get():
                substat_checkboxes[i].configure(state="disabled")
    else:
        transmute_button.configure(state="disabled")
        # Enable all checkboxes
        for i, var in enumerate(substat_vars):
            # Only enable checkboxes that don't match the main stat
            if substats[i] != main_stat_var.get():
                substat_checkboxes[i].configure(state="normal")


def on_transmute():
    global art, last, art_update
    """Handles the transmute button click event."""
    artifact_set = artifact_set_var.get()
    artifact_type = artifact_type_var.get()
    main_stat = main_stat_var.get()
    selected_substats = [substats[i] for i, var in enumerate(substat_vars) if var.get()]
    preset = [artifact_type, main_stat] + selected_substats + [artifact_set]
    art, last = transmute(preset)
    art_update = True
    app.withdraw()
    app.quit()


def disable_close_button():
    app.withdraw()
    app.quit()


def update_main_stats(*args):
    """Updates the list of available main stats based on artifact type and updates the substat checkboxes."""
    artifact_type = artifact_type_var.get()
    new_main_stats = type_to_main_stats.get(artifact_type, [])

    # Update the Main Stat dropdown
    main_stat_menu.configure(values=new_main_stats)
    main_stat_var.set(new_main_stats[0])  # Set the first main stat in the list

    # Call the function to update substat checkboxes
    update_substat_checkboxes()


def update_substat_checkboxes(*args):
    """Updates the substat checkboxes, disabling the ones that match the selected main stat."""
    main_stat = main_stat_var.get()

    for i, substat in enumerate(substats):
        if substat == main_stat:
            # Disable substat if it matches the main stat
            substat_checkboxes[i].configure(state="disabled")
            substat_vars[i].set(False)  # Ensure it's unticked
        else:
            # Enable other substats
            substat_checkboxes[i].configure(state="normal")

    # Check if more than two substats are selected
    update_button_state()


def choose_artifact_set(set_name, image):
    """Handles the selection of an artifact set from the dropdown."""
    artifact_set_var.set(set_name)
    artifact_set_button.configure(image=image, text=set_name)
    dropdown_window.destroy()


def open_artifact_set_dropdown():
    """Opens a scrollable dropdown to select an artifact set."""
    global dropdown_window
    dropdown_window = Toplevel(app)
    dropdown_window.geometry("400x800")  # Adjust size as needed

    scrollable_frame = ctk.CTkScrollableFrame(dropdown_window, width=230, height=350)
    scrollable_frame.pack(fill="both", expand=True, padx=2, pady=2)

    for artifact_set, image in set_to_image.items():
        btn_image = ctk.CTkImage(Image.open(image), size=(26, 26))
        btn = ctk.CTkButton(scrollable_frame, text=artifact_set, image=btn_image, compound="left",
                            command=lambda a_set=artifact_set, img=btn_image: choose_artifact_set(a_set, img))
        btn.pack(padx=10, pady=5)


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
        print('='*50 + f' {Fore.LIGHTCYAN_EX}AUTOMATION MODE{Style.RESET_ALL} ' + '='*50)
        sample_size, cv_desired = take_input()

        if sample_size == 'exit' or cv_desired == 'exit':
            print(" Going back to normal mode...")
            print()
            print('=' * 52 + f' {Fore.LIGHTCYAN_EX}NORMAL MODE{Style.RESET_ALL} ' + '=' * 52)
            print()
            continue
        else:
            sample_size, cv_desired = int(sample_size), float(cv_desired)
            print(f' Ok, will look for at least {Fore.LIGHTCYAN_EX}{min(54.5, cv_desired)}{Style.RESET_ALL} cv\n')

        print(f' Would you like to view {Fore.CYAN}advanced settings{Style.RESET_ALL}? (leave blank to skip and use defaults, type 0 to exit)')
        while True:
            yesno = input(' Y/n: ').strip().lower()
            if not yesno or yesno == 'n':
                advanced = False
                print(' Ok, using defaults\n')
                break
            if yesno == '0':
                break
            if yesno == 'y':
                advanced = True
                break
            else:
                print(f' {Fore.RED}Please enter either y or n{Style.RESET_ALL}\n')

        if yesno == '0':
            print(" Going back to normal mode...")
            print()
            print('=' * 52 + f' {Fore.LIGHTCYAN_EX}NORMAL MODE{Style.RESET_ALL} ' + '=' * 52)
            print()
            continue

        auto_source = 'Domains, Strongbox, Abyss'
        domain_use = 1
        strongbox_use = 1
        abyss_use = 1
        auto_domain = 'random'
        auto_strongbox = 'random'
        set_requirement = 'none'
        type_requirement = 'none'
        main_stat_requirement = 'none'
        sub_stat_requirement = []
        rv_requirement = 0
        sub_stat_mode = "2"

        exited = False
        if advanced:
            skipped = False
            print(f'\n {Fore.CYAN}Where would you like your artifacts to come from?{Style.RESET_ALL} (leave blank to use default)')
            # ARTIFACT SOURCE CHOICE
            auto_source = choose_one(['Only Domains', 'Only Strongbox', 'Domains, Strongbox, Abyss'], 'Please choose a valid option (1, 2 or 3)!', {}, True, True)

            if not auto_source:  # user input 0
                exited = True

            elif auto_source == 'skip':
                auto_source = 'Domains, Strongbox, Abyss'
                print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                skipped = True

            elif auto_source == 'blank':
                auto_source = 'Domains, Strongbox, Abyss'
                print(f' {Fore.LIGHTMAGENTA_EX}Setting default: Domains, Strongbox, Abyss{Style.RESET_ALL}\n')

            else:
                if auto_source == 'Only Domains':
                    strongbox_use = 0
                    abyss_use = 0

                elif auto_source == 'Only Strongbox':
                    domain_use = 0
                    abyss_use = 0

                print(f' {Fore.LIGHTMAGENTA_EX}Source set to {auto_source}{Style.RESET_ALL}\n')

            everysim = ' for every simulation' if sample_size > 1 else ''
            if not exited and not skipped and domain_use:  # DOMAIN CHOICE (IF DOMAINS ARE USED)
                print(f' {Fore.CYAN}Choose a domain for your artifacts{Style.RESET_ALL} (leave blank to randomize)')
                auto_domain = choose_one(domains, "That's not a domain that is available!\n Please input a number corresponding to the domain of choice", aliases_domain, True, True)
                if auto_domain == 'blank':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, will choose a random domain{everysim}{Style.RESET_ALL}\n')
                    auto_domain = 'random'
                elif not auto_domain:
                    exited = True
                elif auto_domain == 'skip':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                    auto_domain = 'random'
                    skipped = True
                else:
                    print(f' {Fore.LIGHTMAGENTA_EX}Domain: {auto_domain[0]}, {auto_domain[1]}{Style.RESET_ALL}\n')

            if not exited and not skipped and strongbox_use:  # STRONGBOX SET CHOICE (IF STRONGBOX IS USED)
                print(f' {Fore.CYAN}Choose a strongbox set for your artifacts{Style.RESET_ALL} (leave blank to randomize)')
                auto_strongbox = choose_one(sets, "That's not a set that is available! Try again", aliases_sets, True, True)
                if auto_strongbox == 'blank':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, will choose a random strongbox set{everysim}{Style.RESET_ALL}\n')
                    auto_strongbox = 'random'
                elif not auto_strongbox:
                    exited = True
                elif auto_strongbox == 'skip':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                    auto_strongbox = 'random'
                    skipped = True
                else:
                    print(f' {Fore.LIGHTMAGENTA_EX}Strongbox set: {auto_strongbox}{Style.RESET_ALL}\n')

            if not exited and not skipped:
                print(f' {Fore.CYAN}Do your artifacts need to be a specific type?{Style.RESET_ALL} (leave blank to set no requirements)')
                type_requirement = choose_one(artifact_types, "That's not a type that is available! Try again", {}, True, True)
                if type_requirement == 'blank':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, no artifact type requirement{Style.RESET_ALL}\n')
                    type_requirement = 'none'
                elif not type_requirement:
                    exited = True
                elif type_requirement == 'skip':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                    type_requirement = 'none'
                    skipped = True
                else:
                    print(f' {Fore.LIGHTMAGENTA_EX}Artifact type requirement: {type_requirement}{Style.RESET_ALL}\n')

            if not exited and not skipped and type_requirement not in ('none', 'Feather', 'Flower'):
                print(f' {Fore.CYAN}Do your artifacts need to have a specific Main Stat?{Style.RESET_ALL} (leave blank to set no requirements)')
                eligible_mains = list(type_to_main_stats[type_requirement])
                if cv_desired > 46.6 and type_requirement == 'Circlet':
                    eligible_mains.remove('CRIT Rate%')
                    eligible_mains.remove('CRIT DMG%')
                main_stat_requirement = choose_one(eligible_mains, "That's not a stat that is available! Try again", {}, True, True)
                if main_stat_requirement == 'blank':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, no Main Stat requirement{Style.RESET_ALL}\n')
                    main_stat_requirement = 'none'
                elif not main_stat_requirement:
                    exited = True
                elif main_stat_requirement == 'skip':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                    main_stat_requirement = 'none'
                    skipped = True
                else:
                    print(f' {Fore.LIGHTMAGENTA_EX}Artifact type requirement: {main_stat_requirement}{Style.RESET_ALL}\n')

            if not exited and not skipped:
                print(f' {Fore.CYAN}Do your artifacts need to have specific Sub Stats?{Style.RESET_ALL} (leave blank to set no requirements)')
                sub_stat_mode_options = ['Yes, I want to choose Sub Stats, ALL of which must be present in my artifact (max 4)',
                                         'Yes, I want to choose Sub Stats only to base the RV requirement off of',
                                         "No, I don't want to choose Sub Stats",
                                         "WHAT DOES THE 2ND OPTION MEAN???"]
                sub_stat_mode = choose_one(sub_stat_mode_options, "Choose one of the options please. Try again", blank_ok=True, skip_ok=True, what=('4', 'https://youtu.be/aaj7lAzC4zs\n https://raw.githubusercontent.com/zUkrainak47/Genshin-Simulator/main/assets/explanation_by_keijo.png'))
                if sub_stat_mode in sub_stat_mode_options:
                    sub_stat_mode = str(sub_stat_mode_options.index(sub_stat_mode))
                if not sub_stat_mode:
                    exited = True
                    break
                if sub_stat_mode in ('blank', "2"):
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, no Sub Stats requirement{Style.RESET_ALL}\n')
                    sub_stat_mode = "2"
                elif sub_stat_mode == 'skip':
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                    sub_stat_mode = "2"
                    skipped = True

            if not exited and not skipped and sub_stat_mode != "2":
                print(f' {Fore.CYAN}Ok, choose the Sub Stats!{Style.RESET_ALL} (leave blank to set no requirements)')
                eligible_subs = [x for x in substats if x != main_stat_requirement]
                if type_requirement == 'Feather':
                    eligible_subs.remove('ATK')
                if type_requirement == 'Flower':
                    eligible_subs.remove('HP')
                subs_dict = dict(zip([str(ind) for ind in range(1, len(eligible_subs) + 1)], eligible_subs))
                for item in subs_dict.items():
                    print(f" {item[0]} = {item[1]}")
                print('\n (Type 0 to exit or "skip" to skip all advanced settings)\n')
                while True:
                    sub_stat_requirement = input(' Your pick: ').split()

                    if not sub_stat_requirement:
                        sub_stat_requirement = []
                        print(f' {Fore.LIGHTMAGENTA_EX}Ok, no Sub Stats requirement{Style.RESET_ALL}\n')
                        break

                    if sub_stat_requirement[0] in ('0', 'exit'):
                        exited = True
                        break

                    elif sub_stat_requirement[0] == 'skip':
                        sub_stat_requirement = []
                        print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                        skipped = True
                        break

                    if len(sub_stat_requirement) > 4 and sub_stat_mode == "0":
                        print(f' {Fore.RED}Please input up to 4 sub stats! Try again{Style.RESET_ALL}\n')
                        continue

                    if all((i in subs_dict) or (i in subs_dict.values()) for i in sub_stat_requirement):
                        for i in range(len(sub_stat_requirement)):
                            if sub_stat_requirement[i] in subs_dict:
                                sub_stat_requirement[i] = subs_dict[sub_stat_requirement[i]]
                        if len(set(sub_stat_requirement)) != len(sub_stat_requirement):
                            print(f' {Fore.RED}Please input different sub stats :){Style.RESET_ALL}\n')

                            '''
                            impossible to hit cv requirement if
                            atk hp atk% hp%    1 cv
                            atk hp atk%       47 cv
                            atk hp atk% crit  47 cv
                            '''
                        elif ((len(sub_stat_requirement) == 4 and 'CRIT DMG%' not in sub_stat_requirement and 'CRIT Rate%' not in sub_stat_requirement and cv_desired > 0) or
                              (len(sub_stat_requirement) == 3 and 'CRIT DMG%' not in sub_stat_requirement and 'CRIT Rate%' not in sub_stat_requirement and cv_desired > 46.6) or
                              (len(sub_stat_requirement) == 4 and ('CRIT DMG%' not in sub_stat_requirement or 'CRIT Rate%' not in sub_stat_requirement) and cv_desired > 46.6)):
                            print(f' {Fore.RED}Impossible to hit CV requirement with the chosen Sub Stats.\n Choose a different set of Sub Stats or a different CV requirement{Style.RESET_ALL}\n')
                        else:
                            joined_subs_requirement = ', '.join(sub_stat_requirement)
                            print(f' {Fore.LIGHTMAGENTA_EX}Sub Stat requirement: {joined_subs_requirement}{Style.RESET_ALL}\n')
                            break
                    else:
                        print(f' {Fore.RED}Please input Sub Stats separated by space! Try again{Style.RESET_ALL}\n')

            if not exited and not skipped and sub_stat_requirement:
                print(f' {Fore.CYAN}Do you want to set a minimum combined RV requirement for the chosen Sub Stats?{Style.RESET_ALL} (leave blank to set no requirement)')
                rv_needed_for_cv_req = max(ceil(cv_desired / 7.8 - 1 - ("CRIT DMG%" not in sub_stat_requirement or "CRIT Rate%" not in sub_stat_requirement)) * 100, 0)
                # print(rv_needed_for_cv_req)
                max_rv_for_given_stats = 900 - (4 - len(sub_stat_requirement))*100 - rv_needed_for_cv_req * ('CRIT Rate%' not in sub_stat_requirement and 'CRIT DMG%' not in sub_stat_requirement) #+ (cv_desired > 46.6) * ('CRIT Rate%' in sub_stat_requirement and 'CRIT DMG%' in sub_stat_requirement) * 100
                # print(max_rv_for_given_stats)
                # at_least_one_crit_required = ('CRIT Rate%' in sub_stat_requirement or 'CRIT DMG%' in sub_stat_requirement) * min(rv_needed_for_cv_req - 100, 0)
                # both_crits_required = ('CRIT Rate%' in sub_stat_requirement and 'CRIT DMG%' in sub_stat_requirement) * (rv_needed_for_cv_req != 0) * 100
                # max_possible_rv_requirement = remaining_rv_for_other_stats + at_least_one_crit_required + both_crits_required
                max_possible_rv_requirement = max_rv_for_given_stats
                rv_s = 's' if len(sub_stat_requirement) > 1 else ''
                while True:
                    rv_requirement = input(' Your pick: ')
                    if not rv_requirement:
                        print(f' {Fore.LIGHTMAGENTA_EX}Ok, no RV requirement{Style.RESET_ALL}\n')
                        rv_requirement = 0
                        break

                    elif rv_requirement == '0':
                        print(f' {Fore.LIGHTCYAN_EX}Really not sure how to treat this lmao, did you mean 0 RV or exit?{Style.RESET_ALL}\n'
                              ' Type "exit" to exit. Type "zero" or leave blank to set 0 RV\n')

                    elif rv_requirement == 'zero':
                        print(f' {Fore.LIGHTMAGENTA_EX}RV requirement: 0%{Style.RESET_ALL}\n')
                        rv_requirement = 0
                        break

                    elif rv_requirement == 'exit':
                        exited = True
                        break

                    elif rv_requirement == 'skip':
                        print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                        rv_requirement = 0
                        skipped = True
                        break

                    elif rv_requirement.isnumeric():
                        rv_requirement = int(rv_requirement)
                        if rv_requirement > max_possible_rv_requirement:
                            print(f' {Fore.RED}Max RV requirement for the chosen Sub Stat{rv_s} is {max_possible_rv_requirement}. Try again{Style.RESET_ALL}\n')
                        else:
                            print(f' {Fore.LIGHTMAGENTA_EX}RV requirement: {rv_requirement}%{Style.RESET_ALL}\n')
                            break

                    else:
                        print(f' {Fore.RED}Please input a number! Try again{Style.RESET_ALL}\n')

            # ask for set requirement only if
            # - a domain is chosen
            # - source is not strongbox only
            if not exited and not skipped and auto_domain != 'random' and auto_source != 'Only Strongbox':
                # - either strongbox is not used
                if not strongbox_use:
                    print(f' {Fore.CYAN}Does your artifact need to be from a specific set?{Style.RESET_ALL} (leave blank to set no requirements)')
                    set_requirement = choose_one(auto_domain, "That's not a set that is available! Try again", aliases_sets, True, True)
                    if set_requirement == 'blank':
                        print(f' {Fore.LIGHTMAGENTA_EX}Ok, no artifact set requirement{Style.RESET_ALL}\n')
                        set_requirement = 'none'
                    elif not set_requirement:
                        exited = True
                    elif set_requirement == 'skip':
                        print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                        set_requirement = 'none'
                        skipped = True
                    else:
                        print(f' {Fore.LIGHTMAGENTA_EX}Artifact set requirement: {set_requirement}{Style.RESET_ALL}\n')

                # - or strongbox set is one of the domain sets
                elif auto_strongbox in auto_domain:
                    print(f' {Fore.CYAN}Do you need your artifact to be a {auto_strongbox} piece?{Style.RESET_ALL} (leave blank to set no requirements)')

                    while True:
                        yesno = input(' Y/n: ').strip().lower()
                        if not yesno or yesno == 'n':
                            set_requirement = 'none'
                            print(f' {Fore.LIGHTMAGENTA_EX}Ok, no artifact set requirement{Style.RESET_ALL}\n')
                            break
                        if yesno == 'y':
                            set_requirement = auto_strongbox
                            print(f' {Fore.LIGHTMAGENTA_EX}Artifact set requirement: {set_requirement}{Style.RESET_ALL}\n')
                            break
                        if yesno in ('0', 'exit'):
                            exited = True
                            break
                        elif yesno == 'skip':
                            set_requirement = 'none'
                            skipped = True
                            print(f' {Fore.LIGHTMAGENTA_EX}Ok, skipping advanced settings. Using defaults for unset settings{Style.RESET_ALL}\n')
                            break
                        else:
                            print(f' {Fore.RED}Please enter either y or n{Style.RESET_ALL}\n')

        if exited:
            print(" Going back to normal mode...")
            print()
            print('=' * 52 + f' {Fore.LIGHTCYAN_EX}NORMAL MODE{Style.RESET_ALL} ' + '=' * 52)
            print()
            continue

        print('=' * 117)
        print()
        print(f" Running {Fore.LIGHTCYAN_EX}{int(sample_size)}{Style.RESET_ALL} simulation{'s' if int(sample_size) != 1 else ''}, looking for at least {Fore.LIGHTCYAN_EX}{min(54.5, float(cv_desired))}{Style.RESET_ALL} CV")
        if advanced:
            information = f" Source: {Fore.LIGHTCYAN_EX}{auto_source}{Style.RESET_ALL}"
            if sample_size > 1 or auto_domain == 'random':
                if auto_source in ('Domains, Strongbox, Abyss', 'Only Domains'):
                    information += f'\n Domains will be {Fore.CYAN}randomized{Style.RESET_ALL}' if auto_domain == 'random' else f'\n Domain: {Fore.LIGHTCYAN_EX}{auto_domain[0]}, {auto_domain[1]}{Style.RESET_ALL}'
            if sample_size > 1 or auto_strongbox == 'random':
                if auto_source in ('Domains, Strongbox, Abyss', 'Only Strongbox'):
                    information += f'\n Strongbox set will be {Fore.CYAN}randomized{Style.RESET_ALL}' if auto_strongbox == 'random' else f'\n Strongbox set: {Fore.LIGHTCYAN_EX}{auto_strongbox}{Style.RESET_ALL}'
            color1 = Fore.LIGHTCYAN_EX if type_requirement != 'none' else Fore.CYAN
            information += f"\n Artifact type requirement: {color1}{type_requirement}{Style.RESET_ALL}"
            if type_requirement not in ('none', 'Flower', 'Feather'):
                color2 = Fore.LIGHTCYAN_EX if main_stat_requirement != 'none' else Fore.CYAN
                information += f"\n Main Stat requirement: {color2}{main_stat_requirement}{Style.RESET_ALL}"
            color3 = Fore.LIGHTCYAN_EX if sub_stat_requirement else Fore.CYAN
            joined_subs_requirement = ', '.join(sub_stat_requirement) if sub_stat_requirement else 'none'
            information += f"\n Sub Stat requirements: {color3}{joined_subs_requirement}{Style.RESET_ALL}"
            if sub_stat_requirement:
                color4 = Fore.LIGHTCYAN_EX if rv_requirement else Fore.CYAN
                information += f"\n Roll Value requirement for chosen Sub Stats: {color4}{rv_requirement}%{Style.RESET_ALL}"
            if auto_domain != 'random' and auto_source != 'Only Strongbox' and (auto_strongbox in auto_domain or not strongbox_use):
                information += f'\n {Fore.CYAN}No{Style.RESET_ALL} artifact set requirement' if set_requirement == 'none' else f'\n Artifact set requirement: {Fore.LIGHTCYAN_EX}{set_requirement}{Style.RESET_ALL}'
            print(information)

        days_it_took_to_reach_desired_cv = []
        artifacts_generated = []
        absolute_generated_domain = 0
        absolute_generated_strongbox = 0
        absolute_generated_abyss = 0
        win_generated_domain = 0
        win_generated_strongbox = 0
        win_generated_abyss = 0
        low = (0, 0, Artifact('this', 'needs', 'to', 'be', 'done', 0, ''))
        high = (0, 0, Artifact('this', 'needs', 'to', 'be', 'done', 0, ''))
        start = time.perf_counter()
        sample_size_is_one = sample_size == 1
        abyss_sets = sets[-2:]
        if abyss_use and set_requirement != 'none' and set_requirement not in abyss_sets:
            abyss_use = 0
            print(f" {Fore.RED}Abyss will be skipped since neither {abyss_sets[0]} nor {abyss_sets[1]} fit the artifact set requirement{Style.RESET_ALL}")

        for i in range(sample_size):
            strongbox_set = choice(sets) if auto_strongbox == 'random' else auto_strongbox
            domain_set = choice(domains) if auto_domain == 'random' else auto_domain

            joined_domain = ', '.join(domain_set)
            c = 0
            day = 0
            highest = -0.1
            total_generated = 0
            inventory = 0
            flag = False
            print(f'\n\n {Fore.YELLOW}Simulation {i + 1}{Style.RESET_ALL}:' if sample_size > 1 else '\n')
            # if domain_use:
            #     print(f' Domain: {Fore.MAGENTA}{joined_domain}{Style.RESET_ALL}')
            # if strongbox_use:
            #     print(f' Strongbox set: {Fore.MAGENTA}{strongbox_set}{Style.RESET_ALL}')
            # if abyss_use:
            #     print(f' Abyss sets: {Fore.MAGENTA}{abyss_sets[0]}, {abyss_sets[1]}{Style.RESET_ALL}')
            if domain_use and auto_domain == 'random':
                print(f' Domain: {Fore.MAGENTA}{joined_domain}{Style.RESET_ALL}')
            if strongbox_use and auto_strongbox == 'random':
                print(f' Strongbox set: {Fore.MAGENTA}{strongbox_set}{Style.RESET_ALL}')
            if (auto_domain == 'random') or (auto_strongbox == 'random'):
                print()

            while not flag:
                day += 1

                if day % 10000 == 0:
                    print(f'\r {Fore.MAGENTA}Day {day} - still going{Style.RESET_ALL}', end='')

                if day % 30 == 0:  # 4 artifacts from abyss every 30 days
                    for k in range(4):
                        inventory += 1
                        if abyss_use:
                            total_generated += 1
                            absolute_generated_abyss += 1
                            art, highest = create_and_roll_artifact([abyss_sets, "abyss"], highest)
                            low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                                compare_to_wanted_cv(art, low, high, days_it_took_to_reach_desired_cv,
                                                     artifacts_generated,
                                                     day, total_generated, cv_desired, sample_size_is_one))
                            if flag:
                                break
                    if flag:
                        win_generated_abyss += 1
                        break

                if not flag:
                    resin = resin_max + (day % 7 == 1) * 60  # 1 transient resin from tubby every monday

                    while resin:
                        # print('domain run')
                        resin -= 20
                        amount = choices((1, 2), weights=(28, 2))  # 6.66% chance for 2 artifacts
                        # if amount[0] == 2:
                        #     print('lucky!')
                        inventory += amount[0]
                        if domain_use:
                            absolute_generated_domain += amount[0]
                            for k in range(amount[0]):
                                total_generated += 1
                                art, highest = create_and_roll_artifact([domain_set, "domain"], highest)
                                low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                                    compare_to_wanted_cv(art, low, high, days_it_took_to_reach_desired_cv,
                                                         artifacts_generated,
                                                         day, total_generated, cv_desired, sample_size_is_one))
                                if flag:
                                    break
                            if flag:
                                win_generated_domain += 1
                                break

                if strongbox_use and not flag:
                    while inventory >= 3:
                        # print(f'strongbox {inventory}')
                        inventory -= 2
                        total_generated += 1
                        absolute_generated_strongbox += 1
                        art, highest = create_and_roll_artifact([strongbox_set, "strongbox"], highest)
                        low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                            compare_to_wanted_cv(art, low, high, days_it_took_to_reach_desired_cv,
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
            print(f'\n Out of {sample_size} simulations, it took an average of {Fore.LIGHTCYAN_EX}{days}{Style.RESET_ALL} days ({round(days / 365.25, 2)} years) to reach at least {cv_desired} CV')
            print(f' Fastest - {Fore.GREEN}{low[0]} day{"s" if low[0] > 1 else ""}{Style.RESET_ALL} - artifact #{low[1]}: {low[2].short(True)}{low[2].subs()}')
            print(f' Slowest - {Fore.RED}{high[0]} day{"s" if high[0] > 1 else ""} ({round(high[0] / 365.25, 2)} years){Style.RESET_ALL} - artifact #{high[1]}: {high[2].short(True)}{high[2].subs()}')
            print()
            word = 'were' if win_generated_domain != 1 else 'was'
            print(f' Out of {sample_size} winning artifacts {Fore.LIGHTCYAN_EX}{win_generated_domain}{Style.RESET_ALL} {word} from domains, {Fore.LIGHTCYAN_EX}{win_generated_strongbox}{Style.RESET_ALL} from strongbox and {Fore.LIGHTCYAN_EX}{win_generated_abyss}{Style.RESET_ALL} from abyss boxes.')
        else:
            day_s = 'days' if low[0] != 1 else 'day'
            print(f'\n It took {Fore.LIGHTCYAN_EX}{low[0]} {day_s}{Style.RESET_ALL} (or {round(high[0] / 365.25, 2)} years)!')
            print()
            win_source = 'a domain' if win_generated_domain else 'the strongbox' if win_generated_strongbox else 'an abyss box'
            print(f' The winning artifact was from {Fore.LIGHTCYAN_EX}{win_source}{Style.RESET_ALL}')

        print(f' Total artifacts generated: {Fore.LIGHTMAGENTA_EX}{sum(artifacts_generated):,}{Style.RESET_ALL} (Domains: {Fore.CYAN}{absolute_generated_domain:,}{Style.RESET_ALL} | Strongbox: {Fore.CYAN}{absolute_generated_strongbox:,}{Style.RESET_ALL} | Abyss: {Fore.CYAN}{absolute_generated_abyss:,}{Style.RESET_ALL})\n')
        if advanced and sample_size > 1:
            print(' Conditions:')
            print(information)
            print()
        print(f' The simulation{"s" if sample_size > 1 else ""} took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
        print(f' Performance: {round(sum(artifacts_generated) / run_time / 1000, 2)} artifacts per ms')
        print()
        print('=' * 52 + f' {Fore.LIGHTCYAN_EX}NORMAL MODE{Style.RESET_ALL} ' + '=' * 52)
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
                art, _ = create_and_roll_artifact(source, silent=True)
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
                        art, _ = create_and_roll_artifact(source, silent=True)
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
                # print(f' #{artifact_list.index(big_rv) + 1}) {big_rv} - {big_rv.subs()}')
                # print(f' RV: {big_rv.rv()}%')
                print()
                big_rv.print_stats(True)

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
        # print()
        # art, last = transmute()
        art_update = False
        # Initialize the tkinter window
        if "app" not in globals():
            app = ctk.CTk()
            app.protocol("WM_DELETE_WINDOW", disable_close_button)
        else:
            app.deiconify()
        app.title("Artifact Transmutation")

        # Artifact Set Dropdown (Custom)
        artifact_set_var = ctk.StringVar(value=sets[0])
        button_image = ctk.CTkImage(Image.open(set_to_image[sets[0]]), size=(26, 26))
        artifact_set_button = ctk.CTkButton(app, text=sets[0], image=button_image,
                                            compound="left", command=open_artifact_set_dropdown)
        artifact_set_button.grid(row=0, column=1, padx=10, pady=10)

        # Artifact Type Dropdown
        artifact_type_var = ctk.StringVar(value=artifact_types[0])
        artifact_type_var.trace_add("write", update_main_stats)
        artifact_type_label = ctk.CTkLabel(app, text="Artifact Type")
        artifact_type_label.grid(row=1, column=0, padx=10, pady=10)
        artifact_type_menu = ctk.CTkOptionMenu(app, variable=artifact_type_var, values=artifact_types)
        artifact_type_menu.grid(row=1, column=1, padx=10, pady=10)

        # Main Stat Dropdown
        main_stat_var = ctk.StringVar(value=type_to_main_stats[artifact_types[0]][0])
        main_stat_var.trace_add("write",
                                update_substat_checkboxes)  # Track changes in main stat to update substat checkboxes
        main_stat_label = ctk.CTkLabel(app, text="Main Stat")
        main_stat_label.grid(row=2, column=0, padx=10, pady=10)
        main_stat_menu = ctk.CTkOptionMenu(app, variable=main_stat_var, values=type_to_main_stats[artifact_types[0]])
        main_stat_menu.grid(row=2, column=1, padx=10, pady=10)

        # Sub Stats Checkboxes
        substat_vars = [ctk.BooleanVar() for _ in substats]
        substat_checkboxes = []
        substat_label = ctk.CTkLabel(app, text="Choose 2 Sub Stats")
        substat_label.grid(row=3, column=0, padx=10, pady=10)

        for i, substat in enumerate(substats):
            checkbox = ctk.CTkCheckBox(app, text=substat, variable=substat_vars[i], command=update_button_state)
            checkbox.grid(row=4 + i % 5, column=i // 5, columnspan=2, padx=100, pady=5)
            substat_checkboxes.append(checkbox)  # Keep track of checkboxes to enable/disable them later

        # Transmute Button (initially disabled)
        transmute_button = ctk.CTkButton(app, text="Transmute", command=on_transmute, state="disabled")
        transmute_button.grid(row=4 + len(substats), column=0, columnspan=2, padx=10, pady=20)

        # Initialize by disabling substat checkboxes based on the initial main stat
        update_substat_checkboxes()

        # Run the application
        app.mainloop()

        if art_update:
            artifact_log.append(art)
            if len(artifact_log) > 10:
                log_start = len(artifact_log) - 10
                artifact_log = artifact_log[log_start:]
            art.print_stats()
            print(f' {Fore.CYAN}Tip: Type "re" to create an artifact using the same preset!{Style.RESET_ALL}\n')
            art_update = False
        else:
            print(f' {Fore.RED}Aborted{Style.RESET_ALL}\n')

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
        # print(f' RV: {art.rv()}%\n')
        print()
        art.print_stats(True)

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
