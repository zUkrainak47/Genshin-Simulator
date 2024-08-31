import json
from random import choice, choices
from colorama import init, Fore, Style
from pathlib import Path
import sys
import importlib
import os

from pathlib import Path


try:
    os.environ['replit']
    replit = True
    # if replit:
        # print('\n Running in replit!')
except KeyError:
    replit = False
    # print('\n Not running in replit!')


print(f'\n===================== {Fore.LIGHTCYAN_EX}LOADING WISH SIMULATOR{Style.RESET_ALL} =====================\n')
init()
Path('banner_info').mkdir(parents=True, exist_ok=True)


def save_character_history_to_file():
    with open(Path('banner_info', 'character_wish_history.txt'), 'w') as f:
        f.write(json.dumps(wish_history["character"], separators=(',', ':')))


def save_weapon_history_to_file():
    with open(Path('banner_info', 'weapon_wish_history.txt'), 'w') as f:
        f.write(json.dumps(wish_history["weapon"], separators=(',', ':')))


def save_standard_history_to_file():
    with open(Path('banner_info', 'standard_wish_history.txt'), 'w') as f:
        f.write(json.dumps(wish_history["standard"], separators=(',', ':')))


def save_chronicled_history_to_file():
    with open(Path('banner_info', 'chronicled_wish_history.txt'), 'w') as f:
        f.write(json.dumps(wish_history["chronicled"], separators=(',', ':')))


saving_dict = {"character": save_character_history_to_file,
               "weapon": save_weapon_history_to_file,
               "standard": save_standard_history_to_file,
               "chronicled": save_chronicled_history_to_file}


def load_history():
    try:
        with open(Path('banner_info', 'character_wish_history.txt')) as file:
            data = file.read()
        character_history = json.loads(data)
        with open(Path('banner_info', 'weapon_wish_history.txt')) as file:
            data = file.read()
        weapon_history = json.loads(data)
        with open(Path('banner_info', 'standard_wish_history.txt')) as file:
            data = file.read()
        standard_history = json.loads(data)
        with open(Path('banner_info', 'chronicled_wish_history.txt')) as file:
            data = file.read()
        chronicled_history = json.loads(data)
        for i in character_history + weapon_history + standard_history + chronicled_history:
            if i not in number_to_item_dict:
                raise ValueError

        return character_history, weapon_history, standard_history, chronicled_history

    except FileNotFoundError:
        global wish_history
        wish_history = {"character": [], "weapon": [], "standard": [],  "chronicled": []}
        save_character_history_to_file()
        save_weapon_history_to_file()
        save_chronicled_history_to_file()
        save_standard_history_to_file()
        return [], [], [], []


def save_character_distribution_to_file():
    with open(Path('banner_info', 'character_distribution.txt'), 'w') as f:
        f.write(json.dumps(character_distribution, separators=(',', ':')))


def save_weapon_distribution_to_file():
    with open(Path('banner_info', 'weapon_distribution.txt'), 'w') as f:
        f.write(json.dumps(weapon_distribution, separators=(',', ':')))


def save_info_to_file(pity, count_, five_count_, four_count_, unique_five_char_count_, unique_five_weap_count_, unique_four_weap_count_, gacha_system):
    with open(Path('banner_info', 'info.txt'), 'w') as f:
        f.write(json.dumps([pity, count_, five_count_, four_count_, unique_five_char_count_, unique_five_weap_count_, unique_four_weap_count_, gacha_system], separators=(',', ':')))


def save_banner_to_file():
    with open(Path('banner_info', 'banner.txt'), 'w') as f:
        f.write(json.dumps(user_banner_input, separators=(',', ':')))


def save_archive_to_file(cons, refs):

    numeric_indexes_c = [character.num for character in cons]
    numeric_indexes_w = [weapon.num for weapon in refs]
    new_dict_c = dict(zip(numeric_indexes_c, list(cons.values())))
    new_dict_w = dict(zip(numeric_indexes_w, list(refs.values())))
    with open(Path('banner_info', 'archive.txt'), 'w') as f:
        data = (new_dict_c, new_dict_w)
        f.write(json.dumps(data, separators=(',', ':')))


banner_types = ["character", "weapon", "standard", "chronicled"]


def load_info():
    try:
        with open(Path('banner_info', 'info.txt')) as file:
            data = file.read()
        pity_and_other_info = json.loads(data)
        return pity_and_other_info

    except FileNotFoundError:
        pities_ = {
            'character': [0, 0, False, False, 0, [0, 0, 0]],
            'weapon': [0, 0, 0, False, False, [0, 0, 0]],
            'standard': [0, 0, 0, 0, [0, 0, 0]],
            'chronicled': [0, 0, False, [0, 0, 0]]
        }
        with open(Path('banner_info', 'info.txt'), 'w') as file:
            info = [pities_, 0, 0, 0, 0, 0, 0, "new"]
            file.write(json.dumps(info, separators=(',', ':')))
        return info


def load_banner():  # always returns a valid banner
    global user_banner_input
    try:  # if can read, read.
        with open(Path('banner_info', 'banner.txt')) as file:
            data = file.read()
        user_banner_input = json.loads(data)
        check_for_banner_mismatch_and_save()  # make sure what was read is a valid banner and save variables
    except FileNotFoundError:  # if can't read, set to default
        user_banner_input = ['character', 'tao-3']
        save_new_banner_of_choice()


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(kk): vv for kk, vv in x.items()}
    return x


def load_distribution():
    global character_distribution, weapon_distribution
    try:
        with open(Path('banner_info', 'character_distribution.txt')) as file:
            data = file.read()
        character_distribution = json.loads(data, object_hook=jsonKeys2int)

    except:
        character_distribution = {i: 0 for i in range(1, 91)}
        character_distribution[100] = 0
        save_character_distribution_to_file()

    try:
        with open(Path('banner_info', 'weapon_distribution.txt')) as file:
            data = file.read()
        weapon_distribution = json.loads(data, object_hook=jsonKeys2int)

    except:
        weapon_distribution = {i: 0 for i in range(1, 78)}
        weapon_distribution[100] = 0
        save_weapon_distribution_to_file()

    print(Fore.LIGHTGREEN_EX + ' Loaded distribution successfully!' + Style.RESET_ALL)


def load_archive():
    try:
        with open(Path('banner_info', 'archive.txt')) as file:
            data = file.read()
        archive = json.loads(data, object_hook=jsonKeys2int)

        indexes_c = [number_to_item_dict[i] for i in archive[0]]
        indexes_w = [number_to_item_dict[i] for i in archive[1]]
        new_dict_c = dict(zip(indexes_c, list(archive[0].values())))
        new_dict_w = dict(zip(indexes_w, list(archive[1].values())))
        return new_dict_c, new_dict_w

    except FileNotFoundError:
        with open(Path('banner_info', 'archive.txt'), 'w') as file:
            file.write("[{}, {}]")
        return {}, {}


def set_defaults():
    global wish_history, constellations, refinements, pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count, gacha_system

    wish_history = {"character": [], "weapon": [], "standard": [], "chronicled": []}
    save_character_history_to_file()
    save_weapon_history_to_file()
    save_chronicled_history_to_file()
    save_standard_history_to_file()

    constellations, refinements = {}, {}
    save_archive_to_file(constellations, refinements)

    pities = {'character': [0, 0, False, False, 0, [0, 0, 0]],
              # 5-star pity / 4-star pity / 5-star guarantee / 4-star guarantee
              'weapon': [0, 0, 0, False, False, [0, 0, 0]],
              # 5-star pity / 4-star pity / epitomized path / last 5 star was standard? / 4-star guarantee
              'standard': [0, 0, 0, 0, [0, 0, 0]],
              # wishes since last [5-star char / 5-star weapon / 4-star char / 4-star weapon]
              'chronicled': [0, 0, False, [0, 0, 0]]
              # 5-star pity / 4-star pity / 5-star guarantee
              # last item is [total pull count, 5-star count, 4-star count]
              }
    count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count, gacha_system = 0, 0, 0, 0, 0, 0, "new"
    save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                      unique_four_weap_count, gacha_system)
    print(Fore.LIGHTGREEN_EX + " Everything cleared!" + Style.RESET_ALL)


def check_for_banner_mismatch_and_save():  # given any user_banner_input, makes sure it's valid
    global user_banner_input  # ['type', 'banner_id']
    if not isinstance(user_banner_input, list) and len(user_banner_input) != 2:  # if not even a list, set default
        user_banner_input = ['character', 'tao-3']
        save_new_banner_of_choice()
        return

    banner_type = user_banner_input[0]

    if banner_type == 'standard':  # ['standard']
        save_new_banner_of_choice()
        return

    if banner_type not in ['character', 'weapon', 'chronicled']:
        # ['something', 'tao-3']
        print(Fore.RED + ' Banner mismatch detected, setting to default' + Style.RESET_ALL)
        user_banner_input = ['character', 'tao-3']
        save_new_banner_of_choice()
        return

    # left only ['character', 'weapon', 'chronicled']

    banner_id = user_banner_input[1]
    if banner_type == 'character':
        # ["character", "tao-4"]

        if banner_id not in character_banner_list:
            print(Fore.RED + ' Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return

    elif banner_type == 'weapon':
        # ["weapon", ["Staff of Homa - Aqua Simulacra", "Staff of Homa"]]

        if banner_id[0] not in weapon_banner_list:
            # ["weapon", ["something", "Staff of Homa"]]
            print(Fore.RED + ' Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return
        if banner_id[1] not in [s.name for s in weapon_banner_list[banner_id[0]][0][:2]]:
            # ["weapon", ["Staff of Homa - Aqua Simulacra", "Mistsplitter Reforged"]]
            print(Fore.RED + ' Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return

    else:  # ['chronicled', ['mondstadt-1', 'Jean']]
        if banner_id[0] not in chronicled_banner_list:
            # ['chronicled', ['mondstadt-8', 'Jean']]
            print(Fore.RED + ' Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return

        chron_banner = chronicled_banner_list[banner_id[0]]
        valids = ([i.name for i in chron_banner['characters']['5-stars']] +
                  [i.name for i in chron_banner['weapons']['5-stars']])
        if banner_id[1] not in valids:
            # ['chronicled', ['mondstadt-1', 'Furina']]
            print(Fore.RED + ' Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return

    save_new_banner_of_choice()
    return


# source: https://stackoverflow.com/a/61433559, though slightly modified because it didn't work
def print_progress_bar(index, total, bar_len=36, title='Please wait'):
    '''
    index is expected to be 0 based index.
    0 <= index < total
    '''
    percent_done = (index+1)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'\r {title}: [{done_str}{togo_str}] - {percent_done}% done', end='')


class Character:
    def __init__(self, name, region, vision, weapon, version, rarity, unique_number):
        self.name = name
        self.region = region
        self.vision = vision
        self.weapon = weapon
        self.version = version
        self.rarity = rarity
        self.num = unique_number


class Weapon:
    def __init__(self, name, weapon_type, rarity, unique_number):
        self.name = name
        self.weapon_type = weapon_type
        self.rarity = rarity
        self.num = unique_number


# ADD NEW CHARACTERS HERE
characters_dict = {
    "Amber": Character("Amber", "Mondstadt", "Pyro", "Bow", 1.0, 4, 13),
    "Barbara": Character("Barbara", "Mondstadt", "Hydro", "Catalyst", 1.0, 4, 14),
    "Beidou": Character("Beidou", "Liyue", "Electro", "Claymore", 1.0, 4, 15),
    "Bennett": Character("Bennett", "Mondstadt", "Pyro", "Sword", 1.0, 4, 16),
    "Chongyun": Character("Chongyun", "Liyue", "Cryo", "Claymore", 1.0, 4, 17),
    "Diluc": Character("Diluc", "Mondstadt", "Pyro", "Claymore", 1.0, 5, 18),
    "Fischl": Character("Fischl", "Mondstadt", "Electro", "Bow", 1.0, 4, 19),
    "Jean": Character("Jean", "Mondstadt", "Anemo", "Sword", 1.0, 5, 20),
    "Kaeya": Character("Kaeya", "Mondstadt", "Cryo", "Sword", 1.0, 4, 21),
    "Keqing": Character("Keqing", "Liyue", "Electro", "Sword", 1.0, 5, 22),
    "Klee": Character("Klee", "Mondstadt", "Pyro", "Catalyst", 1.0, 5, 23),
    "Lisa": Character("Lisa", "Mondstadt", "Electro", "Catalyst", 1.0, 4, 24),
    "Mona": Character("Mona", "Mondstadt", "Hydro", "Catalyst", 1.0, 5, 25),
    "Ningguang": Character("Ningguang", "Liyue", "Geo", "Catalyst", 1.0, 4, 26),
    "Noelle": Character("Noelle", "Mondstadt", "Geo", "Claymore", 1.0, 4, 27),
    "Qiqi": Character("Qiqi", "Liyue", "Cryo", "Sword", 1.0, 5, 28),
    "Razor": Character("Razor", "Mondstadt", "Electro", "Claymore", 1.0, 4, 29),
    "Sucrose": Character("Sucrose", "Mondstadt", "Anemo", "Catalyst", 1.0, 4, 30),
    "Venti": Character("Venti", "Mondstadt", "Anemo", "Bow", 1.0, 5, 31),
    "Xiangling": Character("Xiangling", "Liyue", "Pyro", "Polearm", 1.0, 4, 32),
    "Xingqiu": Character("Xingqiu", "Liyue", "Hydro", "Sword", 1.0, 4, 33),
    "Diona": Character("Diona", "Mondstadt", "Cryo", "Bow", 1.1, 4, 34),
    "Tartaglia": Character("Tartaglia", "Snezhnaya", "Hydro", "Bow", 1.1, 5, 35),
    "Xinyan": Character("Xinyan", "Liyue", "Pyro", "Claymore", 1.1, 4, 36),
    "Zhongli": Character("Zhongli", "Liyue", "Geo", "Polearm", 1.1, 5, 37),
    "Albedo": Character("Albedo", "Mondstadt", "Geo", "Sword", 1.2, 5, 38),
    "Ganyu": Character("Ganyu", "Liyue", "Cryo", "Bow", 1.2, 5, 39),
    "Hu Tao": Character("Hu Tao", "Liyue", "Pyro", "Polearm", 1.3, 5, 40),
    "Xiao": Character("Xiao", "Liyue", "Anemo", "Polearm", 1.3, 5, 41),
    "Rosaria": Character("Rosaria", "Mondstadt", "Cryo", "Polearm", 1.4, 4, 42),
    "Eula": Character("Eula", "Mondstadt", "Cryo", "Claymore", 1.5, 5, 43),
    "Yanfei": Character("Yanfei", "Liyue", "Pyro", "Catalyst", 1.5, 4, 44),
    "Kaedehara Kazuha": Character("Kazuha", "Inazuma", "Anemo", "Sword", 1.6, 5, 45),
    "Kamisato Ayaka": Character("Ayaka", "Inazuma", "Cryo", "Sword", 2.0, 5, 46),
    "Sayu": Character("Sayu", "Inazuma", "Anemo", "Claymore", 2.0, 4, 47),
    "Yoimiya": Character("Yoimiya", "Inazuma", "Pyro", "Bow", 2.0, 5, 48),
    "Aloy": Character("Aloy", "None", "Cryo", "Bow", 2.1, 4.5, 49),
    "Kujou Sara": Character("Kujou Sara", "Inazuma", "Electro", "Bow", 2.1, 4, 50),
    "Raiden Shogun": Character("Raiden Shogun", "Inazuma", "Electro", "Polearm", 2.1, 5, 51),
    "Sangonomiya Kokomi": Character("Kokomi", "Inazuma", "Hydro", "Catalyst", 2.1, 5, 52),
    "Thoma": Character("Thoma", "Inazuma", "Pyro", "Polearm", 2.2, 4, 53),
    "Arataki Itto": Character("Itto", "Inazuma", "Geo", "Claymore", 2.3, 5, 54),
    "Gorou": Character("Gorou", "Inazuma", "Geo", "Bow", 2.3, 4, 55),
    "Shenhe": Character("Shenhe", "Liyue", "Cryo", "Polearm", 2.4, 5, 56),
    "Yun Jin": Character("Yun Jin", "Liyue", "Geo", "Polearm", 2.4, 4, 57),
    "Yae Miko": Character("Yae Miko", "Inazuma", "Electro", "Catalyst", 2.5, 5, 58),
    "Kamisato Ayato": Character("Ayato", "Inazuma", "Hydro", "Sword", 2.6, 5, 59),
    "Kuki Shinobu": Character("Kuki Shinobu", "Inazuma", "Electro", "Sword", 2.7, 4, 60),
    "Yelan": Character("Yelan", "Liyue", "Hydro", "Bow", 2.7, 5, 61),
    "Shikanoin Heizou": Character("Heizou", "Inazuma", "Anemo", "Catalyst", 2.8, 4, 62),
    "Collei": Character("Collei", "Sumeru", "Dendro", "Bow", 3.0, 4, 63),
    "Dori": Character("Dori", "Sumeru", "Electro", "Claymore", 3.0, 4, 64),
    "Tighnari": Character("Tighnari", "Sumeru", "Dendro", "Bow", 3.0, 5, 65),
    "Candace": Character("Candace", "Sumeru", "Hydro", "Polearm", 3.1, 4, 66),
    "Cyno": Character("Cyno", "Sumeru", "Electro", "Polearm", 3.1, 5, 67),
    "Nilou": Character("Nilou", "Sumeru", "Hydro", "Sword", 3.1, 5, 68),
    "Layla": Character("Layla", "Sumeru", "Cryo", "Sword", 3.2, 4, 69),
    "Nahida": Character("Nahida", "Sumeru", "Dendro", "Catalyst", 3.2, 5, 70),
    "Faruzan": Character("Faruzan", "Sumeru", "Anemo", "Bow", 3.3, 4, 71),
    "Wanderer": Character("Wanderer", "Sumeru", "Anemo", "Catalyst", 3.3, 5, 72),
    "Alhaitham": Character("Alhaitham", "Sumeru", "Dendro", "Sword", 3.4, 5, 73),
    "Yaoyao": Character("Yaoyao", "Liyue", "Dendro", "Polearm", 3.4, 4, 74),
    "Dehya": Character("Dehya", "Sumeru", "Pyro", "Claymore", 3.5, 5, 75),
    "Mika": Character("Mika", "Mondstadt", "Cryo", "Polearm", 3.5, 4, 76),
    "Baizhu": Character("Baizhu", "Liyue", "Dendro", "Catalyst", 3.6, 5, 77),
    "Kaveh": Character("Kaveh", "Sumeru", "Dendro", "Claymore", 3.6, 4, 78),
    "Kirara": Character("Kirara", "Inazuma", "Dendro", "Sword", 3.7, 4, 79),
    "Freminet": Character("Freminet", "Fontaine", "Cryo", "Claymore", 4.0, 4, 80),
    "Lynette": Character("Lynette", "Fontaine", "Anemo", "Sword", 4.0, 4, 81),
    "Lyney": Character("Lyney", "Fontaine", "Pyro", "Bow", 4.0, 5, 82),
    "Neuvillette": Character("Neuvillette", "Fontaine", "Hydro", "Catalyst", 4.1, 5, 83),
    "Wriothesley": Character("Wriothesley", "Fontaine", "Cryo", "Catalyst", 4.1, 5, 84),
    "Charlotte": Character("Charlotte", "Fontaine", "Cryo", "Catalyst", 4.2, 4, 85),
    "Furina": Character("Furina", "Fontaine", "Hydro", "Sword", 4.2, 5, 86),
    "Chevreuse": Character("Chevreuse", "Fontaine", "Pyro", "Polearm", 4.3, 4, 87),
    "Navia": Character("Navia", "Fontaine", "Geo", "Claymore", 4.3, 5, 88),
    "Gaming": Character("Gaming", "Liyue", "Pyro", "Claymore", 4.4, 4, 89),
    "Xianyun": Character("Xianyun", "Liyue", "Anemo", "Catalyst", 4.4, 5, 90),
    "Chiori": Character("Chiori", "Inazuma", "Geo", "Sword", 4.5, 5, 91),
    "Arlecchino": Character("Arlecchino", "Snezhnaya", "Pyro", "Polearm", 4.6, 5, 92),
    "Sethos": Character("Sethos", "Sumeru", "Electro", "Bow", 4.7, 4, 93),
    "Clorinde": Character("Clorinde", "Fontaine", "Electro", "Sword", 4.7, 5, 94),
    "Sigewinne": Character("Sigewinne", "Fontaine", "Hydro", "Bow", 4.7, 5, 95),
    "Emilie": Character("Emilie", "Fontaine", "Dendro", "Polearm", 4.8, 5, 96),
    "Mualani": Character("Mualani", "Natlan", "Hydro", "Catalyst", 5.0, 5, 97),
    "Kachina": Character("Kachina", "Natlan", "Geo", "Polearm", 5.0, 4, 98),
    #"Kinich": Character("Emilie", "Natlan", "Dendro", "Claymore", 5.0, 5, 99),
    #"Xilonen": Character("Xilonen", "Natlan", "Geo", "Sword", 5.1, 5, 100),
}


# ADD NEW WEAPONS HERE
weapons_dict = {
    "A Thousand Floating Dreams": Weapon("A Thousand Floating Dreams", "Catalyst", 5, 300),
    "Akuoumaru": Weapon("Akuoumaru", "Claymore", 4, 301),
    "Alley Hunter": Weapon("Alley Hunter", "Bow", 4, 302),
    "Amos' Bow": Weapon("Amos' Bow", "Bow", 5, 303),
    "Aqua Simulacra": Weapon("Aqua Simulacra", "Bow", 5, 304),
    "Aquila Favonia": Weapon("Aquila Favonia", "Sword", 5, 305),
    "Absolution": Weapon("Absolution", "Sword", 5, 306),

    "Beacon of the Reed Sea": Weapon("Beacon of the Reed Sea", "Claymore", 5, 330),
    "Black Tassel": Weapon("Black Tassel", "Polearm", 3, 1),
    "Bloodtainted Greatsword": Weapon("Bloodtainted Greatsword", "Claymore", 3, 2),

    "Calamity Queller": Weapon("Calamity Queller", "Polearm", 5, 360),
    "Cashflow Supervision": Weapon("Cashflow Supervision", "Catalyst", 5, 361),
    "Cool Steel": Weapon("Cool Steel", "Sword", 3, 3),
    "Crane's Echoing Call": Weapon("Crane's Echoing Call", "Catalyst", 5, 363),
    "Crimson Moon's Semblance": Weapon("Crimson Moon's Semblance", "Polearm", 5, 364),

    "Debate Club": Weapon("Debate Club", "Claymore", 3, 4),
    "Dragon's Bane": Weapon("Dragon's Bane", "Polearm", 4, 391),

    "Elegy for the End": Weapon("Elegy for the End", "Bow", 5, 420),
    "Emerald Orb": Weapon("Emerald Orb", "Catalyst", 3, 5),
    "Engulfing Lightning": Weapon("Engulfing Lightning", "Polearm", 5, 422),
    "Everlasting Moonglow": Weapon("Everlasting Moonglow", "Catalyst", 5, 423),
    "Eye of Perception": Weapon("Eye of Perception", "Catalyst", 4, 424),

    "Favonius Codex": Weapon("Favonius Codex", "Catalyst", 4, 450),
    "Favonius Greatsword": Weapon("Favonius Greatsword", "Claymore", 4, 451),
    "Favonius Lance": Weapon("Favonius Lance", "Polearm", 4, 452),
    "Favonius Sword": Weapon("Favonius Sword", "Sword", 4, 453),
    "Favonius Warbow": Weapon("Favonius Warbow", "Bow", 4, 454),
    "Ferrous Shadow": Weapon("Ferrous Shadow", "Claymore", 3, 6),
    "Freedom-Sworn": Weapon("Freedom-Sworn", "Sword", 5, 456),
    # "Fang of the Mountain King": Weapon("Fang of the Mountain King", "Claymore", 5, 457),

    "Haran Geppaku Futsu": Weapon("Haran Geppaku Futsu", "Sword", 5, 510),
    "Harbinger of Dawn": Weapon("Harbinger of Dawn", "Sword", 3, 7),
    "Hunter's Path": Weapon("Hunter's Path", "Bow", 4, 512),

    "Jadefall's Splendor": Weapon("Jadefall's Splendor", "Catalyst", 5, 570),

    "Kagura's Verity": Weapon("Kagura's Verity", "Catalyst", 5, 600),
    "Key of Khaj-Nisut": Weapon("Key of Khaj-Nisut", "Sword", 5, 601),

    "Light of Foliar Incision": Weapon("Light of Foliar Incision", "Sword", 5, 630),
    "Lion's Roar": Weapon("Lion's Roar", "Sword", 4, 631),
    "Lithic Blade": Weapon("Lithic Blade", "Claymore", 4, 632),
    "Lithic Spear": Weapon("Lithic Spear", "Polearm", 4, 633),
    "Lost Prayer to the Sacred Winds": Weapon("Lost Prayer to the Sacred Winds", "Catalyst", 5, 634),
    "Lumidouce Elegy": Weapon("Lumidouce Elegy", "Polearm", 5, 635),

    "Magic Guide": Weapon("Magic Guide", "Catalyst", 3, 8),
    "Makhaira Aquamarine": Weapon("Makhaira Aquamarine", "Claymore", 4, 661),
    "Memory of Dust": Weapon("Memory of Dust", "Catalyst", 5, 662),
    "Mistsplitter Reforged": Weapon("Mistsplitter Reforged", "Sword", 5, 663),
    "Mitternachts Waltz": Weapon("Mitternachts Waltz", "Bow", 4, 664),
    "Mouun's Moon": Weapon("Mouun's Moon", "Bow", 4, 665),

    "Polar Star": Weapon("Polar Star", "Bow", 5, 750),
    "Portable Power Saw": Weapon("Portable Power Saw", "Claymore", 4, 751),
    "Primordial Jade Cutter": Weapon("Primordial Jade Cutter", "Sword", 5, 752),
    "Primordial Jade Winged-Spear": Weapon("Primordial Jade Winged-Spear", "Polearm", 5, 753),
    "Prospector's Drill": Weapon("Prospector's Drill", "Polearm", 4, 754),
    # "Peak Patrol Song": Weapon("Peak Patrol Song", "Sword", 5, 755),

    "Rainslasher": Weapon("Rainslasher", "Claymore", 4, 810),
    "Range Gauge": Weapon("Range Gauge", "Bow", 4, 811),
    "Raven Bow": Weapon("Raven Bow", "Bow", 3, 9),
    "Redhorn Stonethresher": Weapon("Redhorn Stonethresher", "Claymore", 5, 813),
    "Rust": Weapon("Rust", "Bow", 4, 814),

    "Sacrificial Bow": Weapon("Sacrificial Bow", "Bow", 4, 840),
    "Sacrificial Fragments": Weapon("Sacrificial Fragments", "Catalyst", 4, 841),
    "Sacrificial Greatsword": Weapon("Sacrificial Greatsword", "Claymore", 4, 842),
    "Sacrificial Sword": Weapon("Sacrificial Sword", "Sword", 4, 843),
    "Sharpshooter's Oath": Weapon("Sharpshooter's Oath", "Bow", 3, 10),
    "Skyrider Sword": Weapon("Skyrider Sword", "Sword", 3, 11),
    "Skyward Atlas": Weapon("Skyward Atlas", "Catalyst", 5, 846),
    "Skyward Blade": Weapon("Skyward Blade", "Sword", 5, 847),
    "Skyward Harp": Weapon("Skyward Harp", "Bow", 5, 848),
    "Skyward Pride": Weapon("Skyward Pride", "Claymore", 5, 849),
    "Skyward Spine": Weapon("Skyward Spine", "Polearm", 5, 850),
    "Slingshot": Weapon("Slingshot", "Bow", 3, 12),
    "Song of Broken Pines": Weapon("Song of Broken Pines", "Polearm", 5, 852),
    "Splendor of Tranquil Waters": Weapon("Splendor of Tranquil Waters", "Sword", 5, 853),
    "Staff of Homa": Weapon("Staff of Homa", "Polearm", 5, 854),
    "Staff of the Scarlet Sands": Weapon("Staff of the Scarlet Sands", "Polearm", 5, 855),
    "Summit Shaper": Weapon("Summit Shaper", "Sword", 5, 856),
    "Silvershower Heartstrings": Weapon("Silvershower Heartstrings", "Bow", 5, 857),
    "Surf's Up": Weapon("Surf's Up", "Catalyst", 5, 858),

    "The Alley Flash": Weapon("The Alley Flash", "Sword", 4, 870),
    "The Bell": Weapon("The Bell", "Claymore", 4, 871),
    "The Dockhand's Assistant": Weapon("The Dockhand's Assistant", "Sword", 4, 872),
    "The First Great Magic": Weapon("The First Great Magic", "Bow", 5, 873),
    "The Flute": Weapon("The Flute", "Sword", 4, 874),
    "The Stringless": Weapon("The Stringless", "Bow", 4, 875),
    "The Unforged": Weapon("The Unforged", "Claymore", 5, 876),
    "The Widsith": Weapon("The Widsith", "Catalyst", 4, 877),
    "Thrilling Tales of Dragon Slayers": Weapon("Thrilling Tales of Dragon Slayers", "Catalyst", 3, 0),
    "Thundering Pulse": Weapon("Thundering Pulse", "Bow", 5, 879),
    "Tome of the Eternal Flow": Weapon("Tome of the Eternal Flow", "Catalyst", 5, 880),
    "Tulaytullah's Remembrance": Weapon("Tulaytullah's Remembrance", "Catalyst", 5, 881),

    "Uraku Misugiri": Weapon("Uraku Misugiri", "Sword", 5, 900),

    "Verdict": Weapon("Verdict", "Claymore", 5, 930),
    "Vortex Vanquisher": Weapon("Vortex Vanquisher", "Polearm", 5, 587),

    "Wandering Evenstar": Weapon("Wandering Evenstar", "Catalyst", 4, 960),
    "Wavebreaker's Fin": Weapon("Wavebreaker's Fin", "Polearm", 4, 961),
    "Wine and Song": Weapon("Wine and Song", "Catalyst", 4, 962),
    "Wolf's Gravestone": Weapon("Wolf's Gravestone", "Claymore", 5, 963),

    "Xiphos' Moonlight": Weapon("Xiphos' Moonlight", "Sword", 4, 990)
}


def number_to_item():
    result = {}
    for item in list(characters_dict.values()) + list(weapons_dict.values()):
        result[item.num] = item
    return result


number_to_item_dict = number_to_item()


amount_of_five_stars = sum([i.rarity == 5 for i in characters_dict.values()]) + 1  # add 1 for aloy who has 4.5 rarity
amount_of_four_stars = len(characters_dict) - amount_of_five_stars


# thank you chatgpt for helping me convert paimon moe to this

# need to explicitly state, sometimes gets changed
standard_5_star_characters = [characters_dict[char] for char in ("Jean", "Qiqi", "Mona", "Diluc", "Keqing", "Tighnari", "Dehya")]
standard_5_star_weapons = ["Primordial Jade Winged-Spear", "Skyward Blade", "Skyward Spine",  # always unchanged
                           "Skyward Harp", "Skyward Pride", "Skyward Atlas", "Aquila Favonia",
                           "Wolf's Gravestone", "Amos' Bow", "Lost Prayer to the Sacred Winds"]
standard_4_star_characters = [  # automated these guys cuz they change every patch and i dont wanna update it every time
    characters_dict[char] for char in characters_dict if
    characters_dict[char].rarity == 4 and characters_dict[char].name not in ("Amber", "Kaeya", "Lisa")
]
standard_4_star_weapons = [  # always unchanged
    "The Widsith", "Sacrificial Fragments", "Rust", "Sacrificial Sword", "Favonius Greatsword",
    "Rainslasher", "Dragon's Bane", "The Flute", "Favonius Codex", "Sacrificial Greatsword",
    "Favonius Warbow", "Favonius Lance", "Favonius Sword", "Lion's Roar", "Sacrificial Bow",
    "Eye of Perception", "The Stringless", "The Bell"
]
three_star_weapons = [  # always unchanged
    "Black Tassel",
    "Bloodtainted Greatsword",
    "Cool Steel",
    "Debate Club",
    "Emerald Orb",
    "Ferrous Shadow",
    "Harbinger of Dawn",
    "Magic Guide",
    "Raven Bow",
    "Sharpshooter's Oath",
    "Skyrider Sword",
    "Slingshot",
    "Thrilling Tales of Dragon Slayers"
]


amount_of_five_star_weapons = sum([i.rarity == 5 for i in weapons_dict.values()])
amount_of_three_star_weapons = len(three_star_weapons)
amount_of_four_star_weapons = len(weapons_dict) - amount_of_five_star_weapons - amount_of_three_star_weapons


# ADD NEW CHARACTER BANNERS HERE
character_banner_list = {  # thank you, @shilva on discord for typing this out BY HAND WHAT THE HELL DID U DO BRO
    "venti-1": (["Venti", "Barbara", "Fischl", "Xiangling"], 1.0),
    "klee-1": (["Klee", "Xingqiu", "Noelle", "Sucrose"], 1.0),
    "tartaglia-1": (["Tartaglia", "Diona", "Beidou", "Ningguang"], 1.1),
    "zhongli-1": (["Zhongli", "Xinyan", "Razor", "Chongyun"], 1.1),
    "albedo-1": (["Albedo", "Fischl", "Sucrose", "Bennett"], 1.2),
    "ganyu-1": (["Ganyu", "Xiangling", "Xingqiu", "Noelle"], 1.2),
    "xiao-1": (["Xiao", "Diona", "Beidou", "Xinyan"], 1.3),
    "keqing-1": (["Keqing", "Ningguang", "Bennett", "Barbara"], 1.3),
    "tao-1": (["Hu Tao", "Xingqiu", "Xiangling", "Chongyun"], 1.3),
    "venti-2": (["Venti", "Sucrose", "Razor", "Noelle"], 1.4),
    "tartaglia-2": (["Tartaglia", "Rosaria", "Barbara", "Fischl"], 1.4),
    "zhongli-2": (["Zhongli", "Yanfei", "Noelle", "Diona"], 1.5),
    "eula-1": (["Eula", "Xinyan", "Xingqiu", "Beidou"], 1.5),
    "klee-2": (["Klee", "Barbara", "Sucrose", "Fischl"], 1.6),
    "kazuha-1": (["Kaedehara Kazuha", "Rosaria", "Bennett", "Razor"], 1.6),
    "ayaka-1": (["Kamisato Ayaka", "Ningguang", "Chongyun", "Yanfei"], 2.0),
    "yoimiya-1": (["Yoimiya", "Sayu", "Diona", "Xinyan"], 2.0),
    "shogun-1": (["Raiden Shogun", "Kujou Sara", "Xiangling", "Sucrose"], 2.1),
    "kokomi-1": (["Sangonomiya Kokomi", "Rosaria", "Beidou", "Xingqiu"], 2.1),
    "tartaglia-3": (["Tartaglia", "Ningguang", "Chongyun", "Yanfei"], 2.2),
    "tao-2": (["Hu Tao", "Thoma", "Diona", "Sayu"], 2.2),
    "albedo-2": (["Albedo", "Bennett", "Noelle", "Rosaria"], 2.3),
    "eula-2": (["Eula", "Bennett", "Noelle", "Rosaria"], 2.3),
    "itto-1": (["Arataki Itto", "Gorou", "Barbara", "Xiangling"], 2.3),
    "shenhe-1": (["Shenhe", "Yun Jin", "Ningguang", "Chongyun"], 2.4),
    "xiao-2": (["Xiao", "Yun Jin", "Ningguang", "Chongyun"], 2.4),
    "zhongli-3": (["Zhongli", "Xingqiu", "Beidou", "Yanfei"], 2.4),
    "ganyu-2": (["Ganyu", "Xingqiu", "Beidou", "Yanfei"], 2.4),
    "miko-1": (["Yae Miko", "Fischl", "Diona", "Thoma"], 2.5),
    "shogun-2": (["Raiden Shogun", "Bennett", "Xinyan", "Kujou Sara"], 2.5),
    "kokomi-2": (["Sangonomiya Kokomi", "Bennett", "Xinyan", "Kujou Sara"], 2.5),
    "ayato-1": (["Kamisato Ayato", "Sucrose", "Xiangling", "Yun Jin"], 2.6),
    "venti-3": (["Venti", "Sucrose", "Xiangling", "Yun Jin"], 2.6),
    "ayaka-2": (["Kamisato Ayaka", "Razor", "Rosaria", "Sayu"], 2.6),
    "yelan-1": (["Yelan", "Barbara", "Yanfei", "Noelle"], 2.7),
    "xiao-3": (["Xiao", "Barbara", "Yanfei", "Noelle"], 2.7),
    "itto-2": (["Arataki Itto", "Kuki Shinobu", "Chongyun", "Gorou"], 2.7),
    "kazuha-2": (["Kaedehara Kazuha", "Shikanoin Heizou", "Ningguang", "Thoma"], 2.8),
    "klee-3": (["Klee", "Shikanoin Heizou", "Ningguang", "Thoma"], 2.8),
    "yoimiya-2": (["Yoimiya", "Bennett", "Xinyan", "Yun Jin"], 2.8),
    "tighnari-1": (["Tighnari", "Collei", "Diona", "Fischl"], 3.0),
    "zhongli-4": (["Zhongli", "Collei", "Diona", "Fischl"], 3.0),
    "ganyu-3": (["Ganyu", "Dori", "Sucrose", "Xingqiu"], 3.0),
    "kokomi-3": (["Sangonomiya Kokomi", "Dori", "Sucrose", "Xingqiu"], 3.0),
    "cyno-1": (["Cyno", "Candace", "Kuki Shinobu", "Sayu"], 3.1),
    "venti-4": (["Venti", "Candace", "Kuki Shinobu", "Sayu"], 3.1),
    "nilou-1": (["Nilou", "Barbara", "Beidou", "Xiangling"], 3.1),
    "albedo-3": (["Albedo", "Barbara", "Beidou", "Xiangling"], 3.1),
    "nahida-1": (["Nahida", "Razor", "Noelle", "Bennett"], 3.2),
    "yoimiya-3": (["Yoimiya", "Razor", "Noelle", "Bennett"], 3.2),
    "miko-2": (["Yae Miko", "Layla", "Thoma", "Shikanoin Heizou"], 3.2),
    "tartaglia-4": (["Tartaglia", "Layla", "Thoma", "Shikanoin Heizou"], 3.2),
    "wanderer-1": (["Wanderer", "Faruzan", "Gorou", "Yanfei"], 3.3),
    "itto-3": (["Arataki Itto", "Faruzan", "Gorou", "Yanfei"], 3.3),
    "shogun-3": (["Raiden Shogun", "Rosaria", "Sayu", "Kujou Sara"], 3.3),
    "ayato-2": (["Kamisato Ayato", "Rosaria", "Sayu", "Kujou Sara"], 3.3),
    "alhaitham-1": (["Alhaitham", "Yaoyao", "Yun Jin", "Xinyan"], 3.4),
    "xiao-4": (["Xiao", "Yaoyao", "Yun Jin", "Xinyan"], 3.4),
    "tao-3": (["Hu Tao", "Xingqiu", "Ningguang", "Beidou"], 3.4),
    "yelan-2": (["Yelan", "Xingqiu", "Ningguang", "Beidou"], 3.4),
    "dehya-1": (["Dehya", "Bennett", "Barbara", "Collei"], 3.5),
    "cyno-2": (["Cyno", "Bennett", "Barbara", "Collei"], 3.5),
    "shenhe-2": (["Shenhe", "Diona", "Sucrose", "Mika"], 3.5),
    "ayaka-3": (["Kamisato Ayaka", "Diona", "Sucrose", "Mika"], 3.5),
    "nahida-2": (["Nahida", "Kuki Shinobu", "Dori", "Layla"], 3.6),
    "nilou-2": (["Nilou", "Kuki Shinobu", "Dori", "Layla"], 3.6),
    "baizhu-1": (["Baizhu", "Kaveh", "Candace", "Fischl"], 3.6),
    "ganyu-4": (["Ganyu", "Kaveh", "Candace", "Fischl"], 3.6),
    "yoimiya-4": (["Yoimiya", "Kirara", "Yun Jin", "Chongyun"], 3.7),
    "miko-3": (["Yae Miko", "Kirara", "Yun Jin", "Chongyun"], 3.7),
    "alhaitham-2": (["Alhaitham", "Shikanoin Heizou", "Xiangling", "Yaoyao"], 3.7),
    "kazuha-3": (["Kaedehara Kazuha", "Shikanoin Heizou", "Xiangling", "Yaoyao"], 3.7),
    "eula-3": (["Eula", "Mika", "Razor", "Thoma"], 3.8),
    "klee-4": (["Klee", "Mika", "Razor", "Thoma"], 3.8),
    "kokomi-4": (["Sangonomiya Kokomi", "Faruzan", "Rosaria", "Yanfei"], 3.8),
    "wanderer-2": (["Wanderer", "Faruzan", "Rosaria", "Yanfei"], 3.8),
    "lyney-1": (["Lyney", "Lynette", "Bennett", "Barbara"], 4.0),
    "yelan-3": (["Yelan", "Lynette", "Bennett", "Barbara"], 4.0),
    "zhongli-5": (["Zhongli", "Freminet", "Sayu", "Noelle"], 4.0),
    "tartaglia-5": (["Tartaglia", "Freminet", "Sayu", "Noelle"], 4.0),
    "neuvillette-1": (["Neuvillette", "Fischl", "Xingqiu", "Diona"], 4.1),
    "tao-4": (["Hu Tao", "Fischl", "Xingqiu", "Diona"], 4.1),
    "wriothesley-1": (["Wriothesley", "Chongyun", "Thoma", "Dori"], 4.1),
    "venti-5": (["Venti", "Chongyun", "Thoma", "Dori"], 4.1),
    "furina-1": (["Furina", "Charlotte", "Collei", "Beidou"], 4.2),
    "baizhu-2": (["Baizhu", "Charlotte", "Collei", "Beidou"], 4.2),
    "cyno-3": (["Cyno", "Kirara", "Kuki Shinobu", "Xiangling"], 4.2),
    "ayato-3": (["Kamisato Ayato", "Kirara", "Kuki Shinobu", "Xiangling"], 4.2),
    "navia-1": (["Navia", "Sucrose", "Rosaria", "Candace"], 4.3),
    "ayaka-4": (["Kamisato Ayaka", "Sucrose", "Rosaria", "Candace"], 4.3),
    "shogun-4": (["Raiden Shogun", "Chevreuse", "Kujou Sara", "Bennett"], 4.3),
    "yoimiya-5": (["Yoimiya", "Chevreuse", "Kujou Sara", "Bennett"], 4.3),
    "xianyun-1": (["Xianyun", "Gaming", "Faruzan", "Noelle"], 4.4),
    "nahida-3": (["Nahida", "Gaming", "Faruzan", "Noelle"], 4.4),
    "xiao-5": (["Xiao", "Yaoyao", "Xinyan", "Ningguang"], 4.4),
    "miko-4": (["Yae Miko", "Yaoyao", "Xinyan", "Ningguang"], 4.4),
    "chiori-1": (["Chiori", "Gorou", "Yun Jin", "Dori"], 4.5),
    "itto-4": (["Arataki Itto", "Gorou", "Yun Jin", "Dori"], 4.5),
    "neuvillette-2": (["Neuvillette", "Barbara", "Xingqiu", "Yanfei"], 4.5),
    "kazuha-4": (["Kaedehara Kazuha", "Barbara", "Xingqiu", "Yanfei"], 4.5),
    "arlecchino-1": (["Arlecchino", "Freminet", "Lynette", "Xiangling"], 4.6),
    "lyney-2": (["Lyney", "Freminet", "Lynette", "Xiangling"], 4.6),
    "baizhu-3": (["Baizhu", "Layla", "Faruzan", "Beidou"], 4.6),
    "wanderer-3": (["Wanderer", "Layla", "Faruzan", "Beidou"], 4.6),
    "clorinde-1": (["Clorinde", "Sethos", "Bennett", "Thoma"], 4.7),
    "alhaitham-3": (["Alhaitham", "Sethos", "Bennett", "Thoma"], 4.7),
    "sigewinne-1": (["Sigewinne", "Noelle", "Rosaria", "Gaming"], 4.7),
    "furina-2": (["Furina", "Noelle", "Rosaria", "Gaming"], 4.7),
    "navia-2": (["Navia", "Ningguang", "Kaveh", "Kirara"], 4.8),
    "nilou-3": (["Nilou", "Ningguang", "Kaveh", "Kirara"], 4.8),
    "yelan-4": (["Yelan", "Razor", "Xiangling", "Yanfei"], 4.8),
    "emilie-1": (["Emilie", "Razor", "Xiangling", "Yanfei"], 4.8),
    "kazuha-5": (["Kazuha", "Bennett", "Xinyan", "Kachina"], 5.0),
    "mualani-1": (["Mualani", "Bennett", "Xinyan", "Kachina"], 5.0),
    # "": (["", "", "", ""], 5.0),
    # "kinich-1": (["Kinich", "", "", ""], 5.0),
    # "": (["", "", "", ""], 5.1),
    # "xilonen-1": (["Xilonen", "", "", ""], 5.1),

    # "": (["", "", "", ""], ),
}


# ADD NEW WEAPON BANNERS HERE
weapon_banner_list = {
    "Aquila Favonia - Amos' Bow": (["Aquila Favonia", "Amos' Bow", "The Flute", "The Bell", "The Widsith", "The Stringless", "Favonius Lance"], 1.0),
    "Lost Prayer to the Sacred Winds - Wolf's Gravestone": (["Lost Prayer to the Sacred Winds", "Wolf's Gravestone", "Sacrificial Sword", "Sacrificial Bow", "Sacrificial Fragments", "Sacrificial Fragments", "Dragon's Bane"], 1.0),
    "Memory of Dust - Skyward Harp": (["Memory of Dust", "Skyward Harp", "The Flute", "Rainslasher", "Eye of Perception", "Rust", "Favonius Lance"], 1.1),
    "Vortex Vanquisher - The Unforged": (["Vortex Vanquisher", "The Unforged", "Lion's Roar", "The Bell", "Favonius Codex", "Favonius Warbow", "Dragon's Bane"], 1.1),
    "Summit Shaper - Skyward Atlas": (["Summit Shaper", "Skyward Atlas", "Favonius Sword", "Favonius Greatsword", "Favonius Lance", "Sacrificial Fragments", "The Stringless"], 1.2),
    "Skyward Pride - Amos' Bow": (["Skyward Pride", "Amos' Bow", "Sacrificial Sword", "The Bell", "Dragon's Bane", "Eye of Perception", "Favonius Warbow"], 1.2),
    "Primordial Jade Cutter - Primordial Jade Winged-Spear": (["Primordial Jade Cutter", "Primordial Jade Winged-Spear", "The Flute", "Sacrificial Greatsword", "Rust", "Eye of Perception", "Favonius Lance"], 1.3),
    "Staff of Homa - Wolf's Gravestone": (["Staff of Homa", "Wolf's Gravestone", "Lithic Blade", "Lithic Spear", "Lion's Roar", "Sacrificial Bow", "The Widsith"], 1.3),
    "Elegy for the End - Skyward Blade": (["Elegy for the End", "Skyward Blade", "The Alley Flash", "Wine and Song", "Favonius Greatsword", "Favonius Warbow", "Dragon's Bane"], 1.4),
    "Skyward Harp - Lost Prayer to the Sacred Winds": (["Skyward Harp", "Lost Prayer to the Sacred Winds", "Alley Hunter", "Favonius Sword", "Sacrificial Greatsword", "Favonius Codex", "Favonius Lance"], 1.4),
    "Summit Shaper - Memory of Dust": (["Summit Shaper", "Memory of Dust", "Lithic Blade", "Lithic Spear", "The Flute", "Eye of Perception", "Sacrificial Bow"], 1.5),
    "Song of Broken Pines - Aquila Favonia": (["Song of Broken Pines", "Aquila Favonia", "Sacrificial Sword", "Rainslasher", "Dragon's Bane", "Sacrificial Fragments", "Rust"], 1.5),
    "Skyward Pride - Lost Prayer to the Sacred Winds": (["Skyward Pride", "Lost Prayer to the Sacred Winds", "Mitternachts Waltz", "Lion's Roar", "The Bell", "Favonius Lance", "The Widsith"], 1.6),
    "Freedom-Sworn - Skyward Atlas": (["Freedom-Sworn", "Skyward Atlas", "The Alley Flash", "Wine and Song", "Alley Hunter", "Dragon's Bane", "Favonius Greatsword"], 1.6),
    "Mistsplitter Reforged - Skyward Spine": (["Mistsplitter Reforged", "Skyward Spine", "Sacrificial Greatsword", "Favonius Lance", "Favonius Codex", "Favonius Sword", "The Stringless"], 2.0),
    "Thundering Pulse - Skyward Blade": (["Thundering Pulse", "Skyward Blade", "Sacrificial Sword", "Rainslasher", "Dragon's Bane", "Sacrificial Fragments", "Favonius Warbow"], 2.0),
    "Engulfing Lightning - The Unforged": (["Engulfing Lightning", "The Unforged", "Lion's Roar", "The Bell", "Favonius Lance", "The Widsith", "Sacrificial Bow"], 2.1),
    "Everlasting Moonglow - Primordial Jade Cutter": (["Everlasting Moonglow", "Primordial Jade Cutter", "The Flute", "Favonius Greatsword", "Dragon's Bane", "Favonius Codex", "The Stringless"], 2.1),
    "Polar Star - Memory of Dust": (["Polar Star", "Memory of Dust", "Akuoumaru", "Favonius Sword", "Favonius Lance", "Eye of Perception", "Rust"], 2.2),
    "Staff of Homa - Elegy for the End": (["Staff of Homa", "Elegy for the End", "Wavebreaker's Fin", "Mouun's Moon", "Sacrificial Sword", "Rainslasher", "The Widsith"], 2.2),
    "Freedom-Sworn - Song of Broken Pines": (["Freedom-Sworn", "Song of Broken Pines", "Wine and Song", "Alley Hunter", "Lion's Roar", "Sacrificial Greatsword", "Dragon's Bane"], 2.3),
    "Redhorn Stonethresher - Skyward Harp": (["Redhorn Stonethresher", "Skyward Harp", "The Alley Flash", "Mitternachts Waltz", "The Bell", "Favonius Lance", "Sacrificial Fragments"], 2.3),
    "Calamity Queller - Primordial Jade Winged-Spear": (["Calamity Queller", "Primordial Jade Winged-Spear", "Lithic Spear", "The Flute", "Favonius Greatsword", "The Widsith", "Favonius Warbow"], 2.4),
    "Vortex Vanquisher - Amos' Bow": (["Vortex Vanquisher", "Amos' Bow", "Lithic Blade", "Favonius Sword", "Dragon's Bane", "Favonius Codex", "Sacrificial Bow"], 2.4),
    "Kagura's Verity - Primordial Jade Cutter": (["Kagura's Verity", "Primordial Jade Cutter", "Wavebreaker's Fin", "Sacrificial Sword", "Rainslasher", "Eye of Perception", "The Stringless"], 2.5),
    "Engulfing Lightning - Everlasting Moonglow": (["Engulfing Lightning", "Everlasting Moonglow", "Akuoumaru", "Mouun's Moon", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments"], 2.5),
    "Haran Geppaku Futsu - Elegy for the End": (["Haran Geppaku Futsu", "Elegy for the End", "The Flute", "Sacrificial Greatsword", "Dragon's Bane", "The Widsith", "Rust"], 2.6),
    "Mistsplitter Reforged - The Unforged": (["Mistsplitter Reforged", "The Unforged", "Favonius Sword", "The Bell", "Favonius Lance", "Favonius Codex", "Favonius Warbow"], 2.6),
    "Aqua Simulacra - Primordial Jade Winged-Spear": (["Aqua Simulacra", "Primordial Jade Winged-Spear", "Lithic Spear", "Eye of Perception", "Favonius Greatsword", "Sacrificial Bow", "Sacrificial Sword"], 2.7),
    "Redhorn Stonethresher - Memory of Dust": (["Redhorn Stonethresher", "Memory of Dust", "Lithic Blade", "Lion's Roar", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"], 2.7),
    "Freedom-Sworn - Lost Prayer to the Sacred Winds": (["Freedom-Sworn", "Lost Prayer to the Sacred Winds", "The Alley Flash", "Mitternachts Waltz", "Rainslasher", "Favonius Lance", "The Widsith"], 2.8),
    "Thundering Pulse - Summit Shaper": (["Thundering Pulse", "Summit Shaper", "Wine and Song", "Alley Hunter", "The Flute", "Sacrificial Greatsword", "Dragon's Bane"], 2.8),
    "Hunter's Path - Vortex Vanquisher": (["Hunter's Path", "Vortex Vanquisher", "Favonius Sword", "The Bell", "Favonius Lance", "Favonius Codex", "The Stringless"], 3.0),
    "Everlasting Moonglow - Amos' Bow": (["Everlasting Moonglow", "Amos' Bow", "Sacrificial Sword", "Favonius Greatsword", "Dragon's Bane", "Eye of Perception", "Rust"], 3.0),
    "Staff of the Scarlet Sands - Elegy for the End": (["Staff of the Scarlet Sands", "Elegy for the End", "Makhaira Aquamarine", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments", "Favonius Warbow"], 3.1),
    "Key of Khaj-Nisut - Primordial Jade Cutter": (["Key of Khaj-Nisut", "Primordial Jade Cutter", "Xiphos' Moonlight", "Wandering Evenstar", "Rainslasher", "Dragon's Bane", "Sacrificial Bow"], 3.1),
    "A Thousand Floating Dreams - Thundering Pulse": (["A Thousand Floating Dreams", "Thundering Pulse", "The Flute", "Sacrificial Greatsword", "Favonius Lance", "The Widsith", "Rust"], 3.2),
    "Kagura's Verity - Polar Star": (["Kagura's Verity", "Polar Star", "Favonius Sword", "The Bell", "Dragon's Bane", "Favonius Codex", "The Stringless"], 3.2),
    "Tulaytullah's Remembrance - Redhorn Stonethresher": (["Tulaytullah's Remembrance", "Redhorn Stonethresher", "Wavebreaker's Fin", "Sacrificial Sword", "Favonius Greatsword", "Eye of Perception", "Favonius Warbow"], 3.3),
    "Engulfing Lightning - Haran Geppaku Futsu": (["Engulfing Lightning", "Haran Geppaku Futsu", "Akuoumaru", "Mouun's Moon", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments"], 3.3),
    "Light of Foliar Incision - Primordial Jade Winged-Spear": (["Light of Foliar Incision", "Primordial Jade Winged-Spear", "Lithic Spear", "The Flute", "Rainslasher", "The Widsith", "Sacrificial Bow"], 3.4),
    "Staff of Homa - Aqua Simulacra": (["Staff of Homa", "Aqua Simulacra", "Lithic Blade", "Favonius Sword", "Dragon's Bane", "Favonius Codex", "Rust"], 3.4),
    "Beacon of the Reed Sea - Staff of the Scarlet Sands": (["Beacon of the Reed Sea", "Staff of the Scarlet Sands", "The Alley Flash", "Alley Hunter", "Sacrificial Greatsword", "Dragon's Bane", "Eye of Perception"], 3.5),
    "Calamity Queller - Mistsplitter Reforged": (["Calamity Queller", "Mistsplitter Reforged", "Wine and Song", "Sacrificial Sword", "The Bell", "Favonius Lance", "Favonius Warbow"], 3.5),
    "A Thousand Floating Dreams - Key of Khaj-Nisut": (["A Thousand Floating Dreams", "Key of Khaj-Nisut", "Xiphos' Moonlight", "Favonius Greatsword", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"], 3.6),
    "Jadefall's Splendor - Amos' Bow": (["Jadefall's Splendor", "Amos' Bow", "Makhaira Aquamarine", "Wandering Evenstar", "Lion's Roar", "Favonius Lance", "Sacrificial Bow"], 3.6),
    "Thundering Pulse - Kagura's Verity": (["Thundering Pulse", "Kagura's Verity", "Akuoumaru", "The Flute", "Dragon's Bane", "The Widsith", "Rust"], 3.7),
    "Light of Foliar Incision - Freedom-Sworn": (["Light of Foliar Incision", "Freedom-Sworn", "Favonius Codex", "Favonius Sword", "Mouun's Moon", "Sacrificial Greatsword", "Wavebreaker's Fin"], 3.7),
    "Song of Broken Pines - Lost Prayer to the Sacred Winds": (["Song of Broken Pines", "Lost Prayer to the Sacred Winds", "The Alley Flash", "Alley Hunter", "Rainslasher", "Favonius Lance", "Eye of Perception"], 3.8),
    "Everlasting Moonglow - Tulaytullah's Remembrance": (["Everlasting Moonglow", "Tulaytullah's Remembrance", "Wine and Song", "Lion's Roar", "The Bell", "Dragon's Bane", "Favonius Warbow"], 3.8),
    "The First Great Magic - Aqua Simulacra": (["The First Great Magic", "Aqua Simulacra", "Sacrificial Sword", "Favonius Greatsword", "Favonius Lance", "Sacrificial Fragments", "Sacrificial Bow"], 4.0),
    "Vortex Vanquisher - Polar Star": (["Vortex Vanquisher", "Polar Star", "The Flute", "Sacrificial Greatsword", "Dragon's Bane", "The Widsith", "Rust"], 4.0),
    "Tome of the Eternal Flow - Staff of Homa": (["Tome of the Eternal Flow", "Staff of Homa", "The Dockhand's Assistant", "Portable Power Saw", "Mitternachts Waltz", "Favonius Lance", "Favonius Codex"], 4.1),
    "Cashflow Supervision - Elegy for the End": (["Cashflow Supervision", "Elegy for the End", "Prospector's Drill", "Range Gauge", "Favonius Sword", "Rainslasher", "Eye of Perception"], 4.1),
    "Splendor of Tranquil Waters - Jadefall's Splendor": (["Splendor of Tranquil Waters", "Jadefall's Splendor", "Sacrificial Sword", "The Bell", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"], 4.2),
    "Staff of the Scarlet Sands - Haran Geppaku Futsu": (["Staff of the Scarlet Sands", "Haran Geppaku Futsu", "Lion's Roar", "Favonius Greatsword", "Favonius Lance", "The Widsith", "Favonius Warbow"], 4.2),
    "Verdict - Mistsplitter Reforged": (["Verdict", "Mistsplitter Reforged", "Akuoumaru", "Mouun's Moon", "The Flute", "Dragon's Bane", "Favonius Codex"], 4.3),
    "Engulfing Lightning - Thundering Pulse": (["Engulfing Lightning", "Thundering Pulse", "Wavebreaker's Fin", "Favonius Sword", "Rainslasher", "Eye of Perception", "Rust"], 4.3),
    "Crane's Echoing Call - A Thousand Floating Dreams": (["Crane's Echoing Call", "A Thousand Floating Dreams", "Lithic Spear", "Sacrificial Sword", "Sacrificial Greatsword", "Sacrificial Fragments", "Sacrificial Bow"], 4.4),
    "Kagura's Verity - Primordial Jade Winged-Spear": (["Kagura's Verity", "Primordial Jade Winged-Spear", "Lithic Blade", "Lion's Roar", "Favonius Lance", "The Widsith", "The Stringless"], 4.4),
    "Uraku Misugiri - Redhorn Stonethresher": (["Uraku Misugiri", "Redhorn Stonethresher", "The Alley Flash", "Alley Hunter", "The Bell", "Dragon's Bane", "Favonius Codex"], 4.5),
    "Tome of the Eternal Flow - Freedom-Sworn": (["Tome of the Eternal Flow", "Freedom-Sworn", "Wine and Song", "Mitternachts Waltz", "The Flute", "Favonius Greatsword", "Favonius Lance"], 4.5),
    "Crimson Moon's Semblance - The First Great Magic": (["Crimson Moon's Semblance", "The First Great Magic", "The Dockhand's Assistant", "Portable Power Saw", "Dragon's Bane", "Eye of Perception", "Favonius Warbow"], 4.6),
    "Tulaytullah's Remembrance - Jadefall's Splendor": (["Tulaytullah's Remembrance", "Jadefall's Splendor", "Prospector's Drill", "Range Gauge", "Favonius Sword", "Rainslasher", "Sacrificial Fragments"], 4.6),
    "Absolution - Light of Foliar Incision": (["Absolution", "Light of Foliar Incision", "Lithic Spear", "Sacrificial Sword", "Sacrificial Greatsword", "The Widsith", "The Stringless"], 4.7),
    "Silvershower Heartstrings - Splendor of Tranquil Waters": (["Silvershower Heartstrings", "Splendor of Tranquil Waters", "Sacrificial Bow", "Lion's Roar", "Favonius Codex", "Lithic Blade", "Favonius Lance"], 4.7),
    "Verdict - Key of Khaj-Nisut": (["Verdict", "Key of Khaj-Nisut", "Xiphos' Moonlight", "Rust", "Eye of Perception", "Dragon's Bane", "The Bell"], 4.8),
    "Aqua Simulacra - Lumidouce Elegy": (["Aqua Simulacra", "Lumidouce Elegy", "Favonius Warbow", "The Flute", "Favonius Lance", "Wandering Evenstar", "Makhaira Aquamarine"], 4.8),
    "Surf's Up - Freedom-Sworn": (["Surf's Up", "Freedom-Sworn", "Favonius Greatsword", "Favonius Sword", "The Stringless", "Sacrificial Fragments", "Dragon's Bane"], 5.0),

    # "": (["", "", "", "", "", "", ""], ),
}


# ADD NEW CHRONICLED BANNERS HERE
chronicled_banner_list = {
    'mondstadt-1': {
        'characters': {
            '5-stars': [characters_dict[i] for i in ['Albedo', 'Diluc', 'Eula', 'Jean', 'Klee', 'Mona']],
            '4-stars': [characters_dict[i] for i in ['Amber', 'Barbara', 'Bennett', 'Diona', 'Fischl', 'Kaeya',
                                                     'Lisa', 'Mika', 'Noelle', 'Razor', 'Rosaria', 'Sucrose']]},

        'weapons': {
            '5-stars': [weapons_dict[i] for i in ['Aquila Favonia', 'Beacon of the Reed Sea', "Hunter's Path",
                                                  'Lost Prayer to the Sacred Winds', 'Skyward Atlas', 'Skyward Blade',
                                                  'Skyward Harp', 'Skyward Pride', 'Skyward Spine',
                                                  'Song of Broken Pines', "Wolf's Gravestone"]],
            '4-stars': [weapons_dict[i] for i in ["Alley Hunter", "Dragon's Bane", "Eye of Perception",
                                                  "Favonius Codex", "Favonius Greatsword", "Favonius Lance",
                                                  "Favonius Sword", "Favonius Warbow", "Lion's Roar",
                                                  "Mitternachts Waltz", "Rainslasher", "Rust", "Sacrificial Bow",
                                                  "Sacrificial Fragments", "Sacrificial Greatsword",
                                                  "Sacrificial Sword", "The Alley Flash", "The Bell", "The Flute",
                                                  "The Stringless", "The Widsith", "Wine and Song"]]}
    }
}


# replace strings with objects in lists of banners
for banner in character_banner_list:
    for i in range(len(character_banner_list[banner][0])):
        character_banner_list[banner][0][i] = characters_dict[character_banner_list[banner][0][i]]

for banner in weapon_banner_list:
    for i in range(len(weapon_banner_list[banner][0])):
        weapon_banner_list[banner][0][i] = weapons_dict[weapon_banner_list[banner][0][i]]


# replace strings with objects in lists of weapons
for i in range(len(standard_5_star_weapons)):
    standard_5_star_weapons[i] = weapons_dict[standard_5_star_weapons[i]]

for i in range(len(standard_4_star_weapons)):
    standard_4_star_weapons[i] = weapons_dict[standard_4_star_weapons[i]]

for i in range(len(three_star_weapons)):
    three_star_weapons[i] = weapons_dict[three_star_weapons[i]]


# standard_characters = standard_5_star_characters + standard_4_star_characters
# standard_weapons = standard_5_star_weapons + standard_4_star_weapons

def save_new_banner_of_choice():  # needs user_banner_input and pities to work
    # saves variables needed for wish making based on new banner
    # call this function after changing user_banner_input explicitly IF SURE that the banner is valid
    # if in doubt about new banner being valid, call check_for_banner_mismatch_and_save()
    # load_banner() already calls check_for_banner_mismatch_and_save() which calls save_new_banner_of_choice()

    global banner_of_choice, legal_standard_four_stars, legal_standard_five_stars, pity_info
    if user_banner_input[0] == 'character':  # ['character', 'tao-4']
        banner_of_choice = (
            user_banner_input[0],
            character_banner_list[user_banner_input[1]][0],
            character_banner_list[user_banner_input[1]][1])

        legal_standard_four_stars = [s for s in standard_4_star_characters if
                                     (s not in banner_of_choice[1] and (s.version < banner_of_choice[2] or s.version == 1.0))]
        legal_standard_five_stars = [s for s in standard_5_star_characters if
                                     (s not in banner_of_choice[1] and (s.version < banner_of_choice[2] or s.version == 1.0))]

    elif user_banner_input[0] == 'weapon':  # ['weapon', ['Staff of Homa - Aqua Simulacra', 'Staff of Homa']]
        banner_of_choice = (  # ['weapon', featured weapon list, banner version, chosen epitomized path weapon]
            user_banner_input[0],
            weapon_banner_list[user_banner_input[1][0]][0],
            weapon_banner_list[user_banner_input[1][0]][1],
            weapons_dict[user_banner_input[1][1]])

        legal_standard_four_stars = [s for s in standard_4_star_characters if
                                     (s.version < banner_of_choice[2] or s.version == 1.0)]
        legal_standard_five_stars = [s for s in standard_5_star_weapons if s not in banner_of_choice[1]]

    elif user_banner_input[0] == 'standard':  # ['standard']
        banner_of_choice = (
            user_banner_input[0],
        )
        legal_standard_four_stars = standard_4_star_characters + list(map(lambda x: characters_dict[x], ['Lisa', 'Amber', 'Kaeya']))
        legal_standard_five_stars = standard_5_star_characters

    elif user_banner_input[0] == 'chronicled':  # ['chronicled', ['mondstadt-1', 'Jean']]
        chosen_type = 'characters' if user_banner_input[1][1] in characters_dict else 'weapons'

        banner_of_choice = (
            user_banner_input[0],
            chronicled_banner_list[user_banner_input[1][0]],
            characters_dict[user_banner_input[1][1]] if chosen_type == 'characters' else weapons_dict[user_banner_input[1][1]])

        legal_standard_four_stars = (banner_of_choice[1]['characters']['4-stars'],  # 4-star characters
                                     banner_of_choice[1]['weapons']['4-stars'])  # 4-star weapons

        legal_standard_five_stars = [i for i in banner_of_choice[1][chosen_type]['5-stars']
                                     # every item that's a 5-star of the same type as the chosen 5-star
                                     if i.name != user_banner_input[1][1]]  # that isn't the chosen item

        # for context, user_banner_input has ['chronicled', ['mondstadt-1', 'Jean']] structure
        # legal_standard_five_stars is the list of characters you can lose your 5050 to

        # first, I determine the chronicled banner of choice based on user_banner_input[1][0] and save it to
        # banner_of_choice[1]

        # then, I determine the type of the item user has chosen: if user_banner_input[1][1] in characters_dict, it's
        # a character (set t to 'characters'), otherwise it's a weapon (set t to 'weapons').

        # I extract the list of featured characters or weapons based on t
        # I take index 0 of that list because I got [5-star items, 4-star items], and I need the 5-star ones

        # I then choose the ones whose name does not equal to user_banner_input[1][1] (since you can't lose your 5050 to
        # the item that you chose) and add them to a list

    pity_info = pities[banner_of_choice[0]]
    save_banner_to_file()


def print_pity(counter, pity_, c5, c4):
    print("\n" + "="*24 + " PITY INFORMATION " + "="*24)
    if pity_[0] < 10 and pity_[1] < 10:
        insert1, insert2 = '', ''
    else:
        insert1 = ' ' * (pity_[0] < 10)
        insert2 = ' ' * (pity_[1] < 10)
    if user_banner_input[0] == 'character':
        fifty = "you're on a 50/50"  # python 3.10 breaks if I just put this into the f-string
        print(f' {Fore.YELLOW}5★{Style.RESET_ALL} pity = {pity_[0]},{insert1} {fifty if not pity_[2] else "next is guaranteed to be featured"}')
        print(f' {Fore.MAGENTA}4★{Style.RESET_ALL} pity = {pity_[1]},{insert2} {fifty if not pity_[3] else "next is guaranteed to be featured"}')
    elif user_banner_input[0] == 'chronicled':
        fifty = "you're on a 50/50"  # python 3.10 breaks if I just put this into the f-string
        print(f' {Fore.YELLOW}5★{Style.RESET_ALL} pity = {pity_[0]}, {fifty if not pity_[2] else "next is guaranteed to be featured"}')
        print(f' {Fore.MAGENTA}4★{Style.RESET_ALL} pity = {pity_[1]}')
    elif user_banner_input[0] == 'weapon':
        was_standard = 'was standard' if pity_[3] else 'was not standard'
        epitomized_ = f"epitomized points: {pity_[2]}, last {was_standard}"
        seventyfive = "you're on a 75/25"
        print(f' {Fore.YELLOW}5★{Style.RESET_ALL} pity = {pity_[0]},{insert1} {epitomized_ if pity_[2] < 2-(gacha_system == 'new') else "next is guaranteed to be featured"}')
        print(f' {Fore.MAGENTA}4★{Style.RESET_ALL} pity = {pity_[1]},{insert2} {seventyfive if not pity_[4] else "next is guaranteed to be featured"}')
    elif user_banner_input[0] == 'standard':
        print(f' {Fore.YELLOW}5★ character{Style.RESET_ALL} pity = {pity_[0]}\n'
              f' {Fore.YELLOW}5★ weapon{Style.RESET_ALL}    pity = {pity_[1]}')
        print(f' {Fore.MAGENTA}4★ character{Style.RESET_ALL} pity = {pity_[2]}\n'
              f' {Fore.MAGENTA}4★ weapon{Style.RESET_ALL}    pity = {pity_[3]}')
        if pity_[0] >= 180 or pity_[1] >= 180:
            print(f' Next {Fore.YELLOW}5★ item{Style.RESET_ALL} is guaranteed to be a {"character" if pity_[0] >= 180 else "weapon"}')
        if pity_[2] >= 20 or pity_[3] >= 20:
            print(f' Next {Fore.MAGENTA}4★ item{Style.RESET_ALL} is guaranteed to be a {"character" if pity_[2] >= 20 else "weapon"}')
    print(f' {pity_[-1][0]:,} pull{"s" if pity_[-1][0] != 1 else ""} done on the {user_banner_input[0]} banner')
    print(f' Out of them {Fore.YELLOW}{pity_[-1][1]:,} five-star{"s" if c5 != 1 else ""}{Style.RESET_ALL} and {Fore.MAGENTA}{pity_[-1][2]:,} four-star{"s" if c4 != 1 else ""}{Style.RESET_ALL}\n')
    if counter:
        print(f' {counter:,} pull{"s" if counter != 1 else ""} done on all banners combined (${int(round(counter/50.5, 1) * 100):,})')
        print(f' Out of them {Fore.YELLOW}{c5:,} five-star{"s" if c5 != 1 else ""}{Style.RESET_ALL} and {Fore.MAGENTA}{c4:,} four-star{"s" if c4 != 1 else ""}{Style.RESET_ALL}')

    # print('\n==================================================================')


def print_character_archive():
    out = ''
    global sorted_constellations
    if user_banner_input[0] != 'standard':
        sorted_constellations = sorted(list(constellations.items()),
                                       key=lambda x: (x[0].rarity, x[0] in banner_of_choice[1], x[0] not in standard_5_star_characters, x[1]), reverse=True)
    else:
        sorted_constellations = sorted(list(constellations.items()),
                                       key=lambda x: (x[0].rarity, x[0] not in standard_5_star_characters, x[1]), reverse=True)
    if sorted_constellations:
        out += ("\n\n" + "="*24 + f" {Fore.CYAN}CHARACTER ARCHIVE{Style.RESET_ALL} " + "="*24 + '\n')
        out += f" {len(constellations)}/{len(characters_dict)} characters ({unique_five_char_count}/{amount_of_five_stars} {Fore.YELLOW}5★{Style.RESET_ALL}, {len(constellations) - unique_five_char_count}/{amount_of_four_stars} {Fore.MAGENTA}4★{Style.RESET_ALL})\n"
        for a in sorted_constellations:
            out += f' {color_map[a[0].rarity]}c{a[1]} {color_map_light[a[0].rarity]}{a[0].name}{Style.RESET_ALL}\n'
        out += Style.RESET_ALL
    return out


def print_weapon_archive(extra_indent=False):
    out = ''
    global sorted_refinements
    if user_banner_input[0] != 'standard':
        sorted_refinements = sorted(list(refinements.items()),
                                    key=lambda x: (x[0].rarity, x[0] in banner_of_choice[1], x[0] not in standard_5_star_weapons, x[1]), reverse=True)
    else:
        sorted_refinements = sorted(list(refinements.items()),
                                    key=lambda x: (x[0].rarity, x[0] not in standard_5_star_weapons, x[1]), reverse=True)
    if sorted_refinements:
        if extra_indent:
            out += "\n\n"
        out += ("="*26 + f" {Fore.CYAN}WEAPON ARCHIVE{Style.RESET_ALL} " + "="*25 + '\n')
        out += f" {len(refinements)}/{len(weapons_dict)} gacha weapons ({unique_five_weap_count}/{amount_of_five_star_weapons} {Fore.YELLOW}5★{Style.RESET_ALL}, {unique_four_weap_count}/{amount_of_four_star_weapons} {Fore.MAGENTA}4★{Style.RESET_ALL}, {len(refinements) - unique_five_weap_count - unique_four_weap_count}/{amount_of_three_star_weapons} {Fore.BLUE}3★{Style.RESET_ALL})\n"
        for a in sorted_refinements:
            out += f' {color_map[a[0].rarity]}r{a[1]} {color_map_light[a[0].rarity]}{a[0].name}{Style.RESET_ALL}\n'
        out += Style.RESET_ALL
    return out


def print_full_inventory():
    chars_inv = print_character_archive()
    if chars_inv:
        print(chars_inv)
        weap_inv = print_weapon_archive()
        if weap_inv:
            print(weap_inv)
    else:
        weap_inv = print_weapon_archive(True)
        if weap_inv:
            print(weap_inv)
        else:
            print(f' {Fore.MAGENTA}Character/weapon archive empty!{Style.RESET_ALL}\n')


def print_inventory_box_partial(ttt, extra_indent=False):
    out = ''
    if ttt == 'character':
        counters = constellations
        item_dict = characters_dict
        letter = 'c'
        title = "\n\n" + "=" * 45 + f" {Fore.CYAN}CHARACTER ARCHIVE{Style.RESET_ALL} " + "=" * 44

    else:
        counters = refinements
        item_dict = weapons_dict
        letter = 'r'
        title = "\n" * extra_indent + "\n" + "=" * 46 + f" {Fore.CYAN}WEAPON ARCHIVE{Style.RESET_ALL} " + "=" * 46

    if user_banner_input[0] != 'standard':
        sorted_items = sorted(list(counters.items()),
                                       key=lambda x: (x[0].rarity, x[0] in banner_of_choice[1], x[1]), reverse=True)
    else:
        sorted_items = sorted(list(counters.items()),
                                       key=lambda x: (x[0].rarity, x[1]), reverse=True)
    if sorted_items:
        out += title + '\n\n'
        t = f"{len(counters)}/{len(item_dict)} {ttt}s ({unique_five_char_count}/{amount_of_five_stars} {Fore.YELLOW}5★{Style.RESET_ALL}, {len(counters) - unique_five_char_count}/{amount_of_four_stars} {Fore.MAGENTA}4★{Style.RESET_ALL})"
        extra = (104 - len(t) + 18) // 2  # +10 to account for the color change
        out += (" " + ' ' * extra + t + '\n\n')

        # max_length = max(len(s) for s in strings)
        cell_width = 20

        # Calculate the number of lines needed
        num_lines = (len(sorted_items) + 4) // 5

        # Print top border
        out += ' +'
        for j in range(5):
            out += ('-' * cell_width + '+')
        out += '\n'

        # Iterate through lines
        for i in range(num_lines):
            # Print the horizontal borders
            out += ' |                    |                    |                    |                    |                    |\n'

            out += ' |'
            for j in range(5):
                if i * 5 + j < len(sorted_items):
                    placeholder = sorted_items[i * 5 + j][0].name.split()
                    counter_ = 0
                    for k in range(len(placeholder)):
                        if counter_ + len(placeholder[k]) + 1 <= 16:
                            counter_ += len(placeholder[k]) + 1
                        else:
                            to_print = k
                            break
                    else:
                        to_print = len(placeholder)
                    printing = (' '.join(placeholder[:to_print]))
                    padded_string = ' ' * ((20-len(printing))//2) + color_map_light[sorted_items[i * 5 + j][0].rarity] + printing + Style.RESET_ALL + ' ' * (20 - ((20-len(printing))//2) - len(printing))
                    out += (padded_string + '|')
                else:
                    out += (' ' * cell_width + '|')
            out += '\n'

            out += ' |'
            for j in range(5):
                if i * 5 + j < len(sorted_items):
                    placeholder = sorted_items[i * 5 + j][0].name.split()
                    counter_ = 0
                    for k in range(len(placeholder)):
                        if counter_ + len(placeholder[k]) + 1 <= 16:
                            counter_ += len(placeholder[k]) + 1
                        else:
                            to_print = k
                            break
                    else:
                        to_print = len(placeholder)
                    printing = (' '.join(placeholder[to_print:]))
                    padded_string = ' ' * ((20-len(printing))//2) + color_map_light[sorted_items[i * 5 + j][0].rarity] + printing + Style.RESET_ALL + ' ' * (20 - ((20-len(printing))//2) - len(printing))
                    out += (padded_string + '|')
                else:
                    out += (' ' * cell_width + '|')
            out += '\n'

            out += ' |                    |                    |                    |                    |                    |\n'

            out += ' |'
            for j in range(5):
                if i * 5 + j < len(sorted_items):
                    padded_string = ' ' * ((19-len(str(sorted_items[i * 5 + j][1])))//2) + color_map[sorted_items[i * 5 + j][0].rarity] + letter + str(sorted_items[i * 5 + j][1]) + Style.RESET_ALL + ' ' * (19 - ((19-len(str(sorted_items[i * 5 + j][1])))//2) - len(str(sorted_items[i * 5 + j][1])))
                    out += (padded_string + '|')
                else:
                    out += (' ' * cell_width + '|')
            out += '\n'

            out += ' |                    |                    |                    |                    |                    |\n'

            # Print the horizontal border between lines
            out += ' +'
            for j in range(5):
                out += ('-' * cell_width + '+')
            out += '\n'
        # out += '\n'
    return out


def print_inventory_box():
    chars_inv = print_inventory_box_partial('character')

    if chars_inv:
        print(chars_inv)
        weap_inv = print_inventory_box_partial('weapon')
        if weap_inv:
            print(weap_inv)
    else:
        weap_inv = print_inventory_box_partial('weapon', True)
        if weap_inv:
            print(weap_inv)
        else:
            print(f' {Fore.MAGENTA}Character/weapon archive empty!{Style.RESET_ALL}\n')

    # if not print_inventory_box_partial('character'):
    #     if not print_inventory_box_partial('weapon'):
    #         print(f' {Fore.MAGENTA}Character/weapon archive empty!{Style.RESET_ALL}')
    # else:
    #     print_inventory_box_partial('weapon')
    # print()


def print_history_page():  # no idea how this works anymore
    print_from = -((page - 1) * 25) - 1
    print_to = -(min(page * 25, len(wish_history[banner_of_choice[0]]))) - 1
    cc = -print_from - 1
    print(Style.RESET_ALL + '    ' + '-' * 58)
    for number in wish_history[banner_of_choice[0]][print_from:print_to:-1]:
        cc += 1
        print(color_map[number_to_item_dict[number].rarity] + f'    {cc}.{" " if len(str(cc)) < len(str(-print_to - 1)) else ""}',
              number_to_item_dict[number].name)
    print(Style.RESET_ALL + '    ' + '-' * 58)
    print(f'\n    (Page {page}/{num_of_pages})\n')


try:
    pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count, gacha_system = load_info()
    print(Fore.LIGHTGREEN_EX + ' Loaded additional information successfully!' + Style.RESET_ALL)
    info_ok = True
except:
    print(Fore.RED + ' Something off with info file. Clearing everything...' + Style.RESET_ALL)
    info_ok = False


if info_ok:
    try:  # if I extract this into a method pycharm stops seeing all the variables assigned
        cchar, wweap, sstd, cchron = load_history()
        wish_history = {"character": cchar, "weapon": wweap, "standard": sstd, "chronicled": cchron}
        print(Fore.LIGHTGREEN_EX + ' Loaded wish history successfully!' + Style.RESET_ALL)
        history_ok = True
    except:
        print(Fore.RED + ' Something off with wish history files. Clearing everything...' + Style.RESET_ALL)
        history_ok = False


if info_ok and history_ok:
    try:
        constellations, refinements = load_archive()
        print(Fore.LIGHTGREEN_EX + ' Loaded archive successfully!' + Style.RESET_ALL)
        archive_ok = True
    except:
        print(Fore.RED + ' Something off with archive file. Clearing everything...' + Style.RESET_ALL)
        archive_ok = False


if not (info_ok and history_ok and archive_ok):
    set_defaults()


# try:
load_banner()
print(Fore.LIGHTGREEN_EX + ' Loaded banner information successfully!' + Style.RESET_ALL)
# except:
#     print(Fore.RED + ' Something off with banner file. Setting to default...' + Style.RESET_ALL)
#     user_banner_input = ['character', 'tao-3']
#     save_new_banner_of_choice()


load_distribution()


# print([c in standard_characters for c in character_banner_list["venti-1"]])


def get_weights(num):
    #            win/loss/Capturing Radiance
    # 0 losses = 50/50/0
    # 1 loss   = 50/50/0
    # 2 losses = 50/25/25
    # 3 losses = 50/0/50
    return [50, 50 - max((num-1), 0)*25, max((num-1), 0)*25]

def make_pull(banner_info, pity):
    five_star_chance, four_star_chance = get_chances(banner_info[0], pity)
    rarity = 5 if choices((True, False), (five_star_chance, 100 - five_star_chance))[0] \
        else 4 if choices((True, False), (four_star_chance, 100 - four_star_chance))[0] else 3

    if banner_info[0] == 'character':  # banner_info = ['character', banner dictionary, banner version]
        consecutive_losses = pity[4]
        # print(consecutive_losses)
        featured_five_star = banner_info[1][0]
        featured_four_stars = banner_info[1][1:]
        if rarity == 5:
            character_distribution[pity[0] + 1] += 1
            # print(f' {Style.RESET_ALL}{five_star_chance}')
            if pity[2]:  # if guaranteed
                result = [featured_five_star, pity[0] + 1]  # give featured 5-star character
                pity[2] = False  # change guaranteed to false
                result.append(2)  # log that guarantee took place
            else:  # if not guaranteed
                # choose if win 50/50
                if gacha_system == 'new':
                    result = [choices(((featured_five_star, False), (choice(legal_standard_five_stars), False), (featured_five_star, True)), get_weights(consecutive_losses)), pity[0] + 1]
                else:
                    result = [choices(((featured_five_star, False), (choice(legal_standard_five_stars), False))), pity[0] + 1]
                # print(result)
                result[0], radiance = result[0][0][0], result[0][0][1]
                # print(result)
                if radiance:
                    print(f' {Fore.LIGHTMAGENTA_EX}CAPTURING RADIANCE ACTIVATED ({get_weights(consecutive_losses)[-1]}%){Style.RESET_ALL}')
                if result[0] != featured_five_star:  # if didnt win 50/50
                    pity[2] = True  # set guarantee to true
                    pity[4] += 1    # consecutive loss counter
                    result.append(0)  # log if you won or not
                else:
                    pity[4] = 0
                    result.append(1)
            pity[0] = 0
            pity[1] += 1

        elif rarity == 4:
            # print(f' {Style.RESET_ALL}{four_star_chance}')
            if pity[3]:  # if guaranteed
                result = [choice(featured_four_stars), pity[1] + 1]  # give a featured 4-star character
                pity[3] = False  # change guaranteed to false
                result.append(2)  # log that guarantee took place
            else:  # if not guaranteed
                # choose what to give from different pools
                result = [choice(choices((featured_four_stars, legal_standard_four_stars, standard_4_star_weapons), [2, 1, 1])[0]), pity[1] + 1]
                if result[0] not in featured_four_stars:  # if 50/50 lost
                    pity[3] = True  # set guarantee to true
                result.append(int(result[0] in featured_four_stars))  # log if you won or not
            pity[0] += 1
            pity[1] = 0

        elif rarity == 3:
            result = [choice(three_star_weapons), 0, 7]
            pity[0] += 1
            pity[1] += 1

    elif banner_info[0] == 'chronicled':  # banner_info = ['chronicled', banner dictionary, Chronicled Path item]
        featured_five_star = banner_info[2]
        if rarity == 5:
            character_distribution[pity[0] + 1] += 1
            # print(f' {Style.RESET_ALL}{five_star_chance}')
            if pity[2]:  # if guaranteed
                result = [featured_five_star, pity[0] + 1]  # give featured 5-star character
                pity[2] = False  # change guaranteed to false
                result.append(2)  # log that guarantee took place
            else:  # if not guaranteed
                # choose if win 50/50
                result = [choice((featured_five_star, choice(legal_standard_five_stars))), pity[0] + 1]
                pity[2] = (result[0] != featured_five_star)  # if didn't win 50/50 set guarantee to true
                result.append(int(result[0] == featured_five_star))  # log if you won or not
            pity[0] = 0
            pity[1] += 1

        elif rarity == 4:
            result = [choice(choice((legal_standard_four_stars[0], legal_standard_four_stars[1]))), pity[1] + 1, 7]
            pity[0] += 1
            pity[1] = 0

        elif rarity == 3:
            result = [choice(three_star_weapons), 0, 7]
            pity[0] += 1
            pity[1] += 1

    elif banner_info[0] == 'weapon':  # ['weapon', featured weapon list, banner version, chosen epitomized path weapon]
        featured_five_star = banner_info[3]
        other_five_star = banner_info[1][0] if banner_info[1][0] != featured_five_star else banner_info[1][1]
        if rarity == 5:
            weapon_distribution[pity[0] + 1] += 1
            if pity[2] < 2-(gacha_system == 'new'):  # 'weapon': [0, 0, 0, False, False] - 5-star pity, 4-star pity, epitomized path, last 5-star was standard, last 4-star was standard
                if pity[3]:  # if last 5-star was a standard one
                    result = [choice((featured_five_star, other_five_star)), pity[0] + 1]  # give one of the rate-ups
                    pity[3] = False  # set last 5-star to not be standard
                    if result[0] == featured_five_star:
                        result.append((3, pity[2]))  # last standard, not full epitomized path, win
                        pity[2] = 0  # set epitomized path back to 0
                    else:
                        result.append((4, pity[2]))  # last standard, not full epitomized path, loss
                        pity[2] += 1  # +1 to epitomized path
                else:  # if it wasn't standard
                    # give one based on 37.5/37.5/25 rule
                    result = [choices((featured_five_star, other_five_star, choice(legal_standard_five_stars)), [3, 3, 2])[0], pity[0] + 1]
                    if result[0] == featured_five_star:  # if won
                        result.append((5, pity[2]))  # last not standard, not full epitomized path, win
                        pity[2] = 0
                    else:  # if not won
                        pity[3] = result[0] in legal_standard_five_stars  # log if what was lost to is standard
                        result.append((6, pity[2]))  # last not standard, not full epitomized path, loss
                        pity[2] += 1
            else:
                result = [featured_five_star, pity[0] + 1, 2]
                pity[2] = 0  # set epitomized path back to 0
                pity[3] = False  # set last 5-star to not standard
            pity[0] = 0  # set 5-star pity to 0
            pity[1] += 1  # increase 4-star pity by 1

        elif rarity == 4:
            if pity[4]:
                result = [choice(banner_info[1][2:]), pity[1] + 1, 2]
                pity[4] = False
            else:
                result = [choice(choices((banner_info[1][2:], legal_standard_four_stars), [3, 1])[0]), pity[1] + 1]
                result.append(int(result[0] in banner_info[1]))
                pity[4] = result[0] in legal_standard_four_stars
            pity[0] += 1
            pity[1] = 0

        elif rarity == 3:
            result = [choice(three_star_weapons), 0, 7]
            pity[0] += 1
            pity[1] += 1

    elif banner_info[0] == 'standard':
        if rarity == 5:
            character_distribution[min(pity[0], pity[1]) + 1] += 1
            if pity[0] >= 180:
                result = [choice(legal_standard_five_stars), f'{pity[1] + 1} ({pity[0] + 1})', 2]
                pity[0] = 0
                pity[1] += 1
                pity[2] += 1
                pity[3] += 1
            elif pity[1] >= 180:
                result = [choice(standard_5_star_weapons), f'{pity[0] + 1} ({pity[1] + 1})', 2]
                pity[0] += 1
                pity[1] = 0
                pity[2] += 1
                pity[3] += 1
            else:
                result = [choice(choice((legal_standard_five_stars, standard_5_star_weapons)))]
                got = int(result[0] in standard_5_star_weapons)  # 0 if character, 1 if weapon
                if pity[got] > pity[1 - got]:
                    result.extend([f'{pity[1 - got] + 1} ({pity[got] + 1})', 7])
                else:
                    result.extend([f'{pity[got] + 1}', 7])
                pity[got] = 0
                pity[1 - got] += 1
                pity[2] += 1
                pity[3] += 1

        elif rarity == 4:
            if pity[2] >= 20:
                result = [choice(legal_standard_four_stars), f'{pity[3] + 1} ({pity[2] + 1})', 2]
                pity[0] += 1
                pity[1] += 1
                pity[2] = 0
                pity[3] += 1
            elif pity[3] >= 20:
                result = [choice(standard_4_star_weapons), f'{pity[2] + 1} ({pity[3] + 1})', 2]
                pity[0] += 1
                pity[1] += 1
                pity[2] += 1
                pity[3] = 0
            else:
                result = [choice(choice((legal_standard_four_stars, standard_4_star_weapons)))]
                got = int(result[0] in standard_4_star_weapons) + 2  # 2 if character, 3 if weapon
                if pity[got] > pity[5 - got]:
                    result.extend([f'{pity[5 - got] + 1} ({pity[got] + 1})', 7])
                else:
                    result.extend([f'{pity[got] + 1}', 7])
                pity[0] += 1
                pity[1] += 1
                pity[got] = 0
                pity[5 - got] += 1

        elif rarity == 3:
            result = [choice(three_star_weapons), 0, 7]
            pity[0] += 1
            pity[1] += 1
            pity[2] += 1
            pity[3] += 1
        # print(pity[0], pity[1], pity[2], pity[3])

    wish_history[banner_info[0]].append(result[0].num)
    pities[banner_info[0]] = pity
    return result


def get_chances(banner_type, pity):  # returns (% to get 5 star, % to get 4 star)
    if banner_type in ('character', 'chronicled'):  # + 1 here to check the number of the next pull you're making
        five_star_chance = max(0, pity[0] + 1 - 73) * 6 + 0.6  # every pull above 73 adds 6%
        four_star_chance = 100 if pity[1] + 1 >= 10 else (56.1 if pity[1] + 1 == 9 else 5.1)
        # 10+ pity = 4 star in case of no 5 star, 9 pity = 56.1% chance, <9 = 5.6%

    elif banner_type == 'weapon':
        five_star_chance = max(0, pity[0] + 1 - 62) * 7 + 0.7
        four_star_chance = 100 if pity[1] + 1 >= 9 else (66 if pity[1] + 1 == 8 else 6)

    elif banner_type == 'standard':
        five_star_chance = max(0, min(pity[0], pity[1]) + 1 - 73) * 6 + 0.6  # every pull above 73 adds 6%
        four_star_chance = 100 if min(pity[2], pity[3]) + 1 >= 10 else (56.1 if min(pity[2], pity[3]) + 1 == 9 else 5.1)

    return five_star_chance, four_star_chance


three_stars = '(   ★ ★ ★   )'
four_stars = '(  ★ ★ ★ ★  )'
five_stars = '( ★ ★ ★ ★ ★ )'
color_map = {3: Fore.BLUE, 4: Fore.MAGENTA, 4.5: Fore.RED, 5: Fore.YELLOW}
# color_map_light = {3: Fore.LIGHTBLUE_EX, 4: Fore.LIGHTMAGENTA_EX, 5: Fore.LIGHTYELLOW_EX}
color_map_light = color_map
win_map = {0: f'[{Fore.RED}L{Style.RESET_ALL}] ',
           1: f'[{Fore.LIGHTCYAN_EX}W{Style.RESET_ALL}] ',
           2: f'[{Fore.LIGHTGREEN_EX}G{Style.RESET_ALL}] ',
           (3, 0): f'[{Fore.LIGHTCYAN_EX}S0W{Style.RESET_ALL}] ',
           (3, 1): f'[{Fore.LIGHTCYAN_EX}S1W{Style.RESET_ALL}] ',
           (4, 0): f'[{Fore.RED}S0L{Style.RESET_ALL}] ',
           (4, 1): f'[{Fore.RED}S1L{Style.RESET_ALL}] ',
           (5, 0): f'[{Fore.LIGHTCYAN_EX}N0W{Style.RESET_ALL}] ',
           (5, 1): f'[{Fore.LIGHTCYAN_EX}N1W{Style.RESET_ALL}] ',
           (6, 0): f'[{Fore.RED}N0L{Style.RESET_ALL}] ',
           (6, 1): f'[{Fore.RED}N1L{Style.RESET_ALL}] ',
           7: ''
           }
verbose_threshold = 3
messaged = False  # has wish history limit warning been shown?

print(f'\n========================= {Fore.LIGHTCYAN_EX}WISH SIMULATOR{Style.RESET_ALL} =========================\n')
print(f' Type {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL} for the list of commands\n')


def print_banner(t1):
    if t1 == 'Chosen':
        t2 = 'B'
    elif t1 == 'Current':
        t2 = 'Current b'
    elif t1 == 'New':
        t2 = 'New b'
    else:
        t2 = '???'
    if user_banner_input[0] != 'standard':
        print()
    print(f' {t1} banner type: {Fore.CYAN}{user_banner_input[0]}{Style.RESET_ALL}')
    if banner_of_choice[0] == 'character':
        print(f' {t2}anner ID: {user_banner_input[1]}')
        for i in banner_of_choice[1]:
            print(f' {color_map[i.rarity]}{i.rarity}★ {i.name}{Style.RESET_ALL}')
    elif banner_of_choice[0] == 'weapon':
        print(f' {t2}anner ID: {user_banner_input[1][0]}\n Epitomized Path: {color_map[5]}{user_banner_input[1][1]}{Style.RESET_ALL}\n')
        for i in banner_of_choice[1]:
            print(f' {color_map[i.rarity]}{i.rarity}★ {i.name}{Style.RESET_ALL}')
    elif banner_of_choice[0] == 'chronicled':
        print(f' {t2}anner ID: {user_banner_input[1][0]}\n Chronicled Path: {color_map[5]}{user_banner_input[1][1]}{Style.RESET_ALL}')


not_first = False
while True:
    wished_by_viz = False
    if not_first:
        last_banner = user_command == 'banner'
    else:
        last_banner = False
    not_first = True
    user_command = input('\n Command: ').lower().strip()
    if not user_command:
        print(f' Try {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL}\n')
        continue
    if user_command in ('0', 'exit'):
        print(' Exiting Wish Simulator...')
        break

    if user_command in ['help', "'help'", '"help"']:
        print('\n' +
              '=' * 28 + f" {Fore.LIGHTCYAN_EX}CONTROLS{Style.RESET_ALL} " + '=' * 28 + '\n'
              '\n'
              f' {Fore.BLUE}numbers in [] are optional{Style.RESET_ALL}\n\n'
              f' {Fore.LIGHTCYAN_EX}number{Style.RESET_ALL} = do a number of pulls\n'
              f' {Fore.LIGHTCYAN_EX}banner{Style.RESET_ALL} = view current banner\n'
              f' {Fore.LIGHTCYAN_EX}change{Style.RESET_ALL} = choose a different banner\n\n'
              f' {Fore.LIGHTCYAN_EX}system{Style.RESET_ALL} = choose a gacha system (new system introduced in v5.0)\n\n'
              f' {Fore.LIGHTCYAN_EX}pity{Style.RESET_ALL} = view pity related information\n'
              f' {Fore.LIGHTCYAN_EX}aloy{Style.RESET_ALL} = unlock/remove Aloy!!!\n'
              f' {Fore.LIGHTCYAN_EX}inv{Style.RESET_ALL} = view character/weapon archive as list\n'
              f' {Fore.LIGHTCYAN_EX}inv box{Style.RESET_ALL} = view character/weapon archive as boxes\n'
              f' {Fore.LIGHTCYAN_EX}h{Style.RESET_ALL} = view wish history, commands to interact with it:\n'
              f' \t{Fore.LIGHTMAGENTA_EX}n {Fore.BLUE}[number]{Style.RESET_ALL} = go forward a number of pages,\n'
              f' \t{Fore.LIGHTMAGENTA_EX}p {Fore.BLUE}[number]{Style.RESET_ALL} = go back a number of pages,\n'
              f' \t{Fore.LIGHTMAGENTA_EX}number{Style.RESET_ALL} = go to page,\n'
              f' \t{Fore.LIGHTMAGENTA_EX}e{Style.RESET_ALL} = exit\n\n'
              f' {Fore.LIGHTCYAN_EX}dist{Style.RESET_ALL} = view distribution of 5-star items per pity\n'
              f' {Fore.LIGHTCYAN_EX}viz{Style.RESET_ALL} = plot a "Distribution of 5★ items per pity" graph\n\n'
              f' {Fore.LIGHTCYAN_EX}clear{Style.RESET_ALL} = clear wish history, pity, archive\n'
              f' {Fore.LIGHTCYAN_EX}load{Style.RESET_ALL} = load updates made to files located in ./banner_info/\n'
              f' {Fore.RED}It is not encouraged to introduce changes to the files yourself\n'
                        f' as they work together in tandem and by changing a file, chaos is\n'
                        f' introduced which may or may not cause unpredictable behavior!{Style.RESET_ALL}\n'
              f'\n'
              f' {Fore.LIGHTCYAN_EX}0{Style.RESET_ALL} = exit Wish Simulator\n'
              f'\n' +
              '=' * 66 +
              '\n')
        continue

    if 'number' in user_command:
        print(f' real funny, input an actual number tho. just type {Fore.CYAN}10{Style.RESET_ALL} to do 10 wishes\n')
        continue

    if user_command == 'aloy':
        if number_to_item_dict[49] not in constellations:
            constellations[number_to_item_dict[49]] = 0
            unique_five_char_count += 1
            save_archive_to_file(constellations, refinements)
            save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                              unique_four_weap_count, gacha_system)
            print(f"{Fore.RED} Aloy{Fore.LIGHTGREEN_EX} claimed!{Style.RESET_ALL}\n")
        else:
            del constellations[number_to_item_dict[49]]
            unique_five_char_count -= 1
            save_archive_to_file(constellations, refinements)
            save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                              unique_four_weap_count, gacha_system)
            print(f"{Fore.RED} Aloy {Fore.LIGHTGREEN_EX}removed :({Style.RESET_ALL}\n")
        continue

    if user_command == 'banner':
        print_banner('Chosen')
        print()
        continue

    if user_command == 'change':
        if user_banner_input[0] == 'weapon' and pity_info[2]:
            print(f'\n {Fore.RED}NOTE: YOUR EPITOMIZED PATH WILL RESET IF YOU CHANGE THE BANNER\n'
                  f' (You own {pity_info[2]} Epitomized Point{"s" if pity_info[2] != 1 else ""}){Style.RESET_ALL}')
        elif user_banner_input[0] == 'chronicled' and pity_info[2]:
            print(f'\n {Fore.RED}NOTE: YOUR CHRONICLED PATH WILL RESET IF YOU CHANGE THE BANNER\n'
                  f' (You own 1 Chronicled Point){Style.RESET_ALL}')
        if not last_banner:
            print_banner('Current')
        print()
        m = {"1": "character", "2": "weapon", "3": "chronicled", "4": "standard"}
        print(f" {Fore.CYAN}Choose type of new banner:{Style.RESET_ALL}")
        for i in m.items():
            print(f" {i[0]} = {i[1]}")
        print('\n (Type 0 to exit)\n')
        while True:
            new1 = input(' Your pick: ').strip().lower()
            if new1 in ('0', 'exit'):
                break
            if new1 in m or new1 in m.values():
                break
            else:
                print(f' {Fore.RED}Please input either the number or the name of the banner type of choice{Style.RESET_ALL}\n')
        if new1 in ('0', 'exit'):
            print(f' {Fore.LIGHTMAGENTA_EX}Ok, not changing banner anymore{Style.RESET_ALL}\n')
            continue
        if new1 in m:
            new1 = m[new1]
        print(f' {Fore.YELLOW}{new1.capitalize()} banner selected.{Style.RESET_ALL}')

        if new1 == 'standard':
            user_banner_input = [new1]

        else:
            print(f'\n {Fore.CYAN}Choose the banner!{Style.RESET_ALL}\n'
                  ' List of available banners:\n')

            if new1 == 'character':
                m = {str(q): w for q, w in zip(range(1, len(character_banner_list)+1), character_banner_list.keys())}
                for i in m.items():
                    first = f" {i[0]} = {i[1]}"
                    print(" " + first + ' ' * (21-len(first)) + '(' + str(character_banner_list[i[1]][1]) + ')')

                print('\n (Type 0 to exit)\n')

                while True:
                    new2 = input(' Choose one: ').strip().lower()
                    if new2 in ('0', 'exit'):
                        break
                    if new2 not in m and new2 not in m.values():
                        print(f" {Fore.RED}That's not a banner that's available! Try again{Style.RESET_ALL}\n")
                    else:
                        if new2 in m:
                            new2 = m[new2]
                        print(f" Ok, {Fore.YELLOW}{new2}{Style.RESET_ALL} selected")
                        break

                if new2 in ('0', 'exit'):
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, not changing banner anymore{Style.RESET_ALL}\n')
                    continue
                user_banner_input = [new1, new2]

            elif new1 == 'chronicled':
                m = {str(q): w for q, w in zip(range(1, len(chronicled_banner_list)+1), chronicled_banner_list.keys())}
                for i in m.items():
                    print(f" {i[0]} = {i[1]}")
                print('\n (Type 0 to exit)\n')

                while True:
                    new2 = input(' Choose one: ').strip().lower()
                    if new2 in ('0', 'exit'):
                        break
                    if new2 not in m and new2 not in m.values():
                        print(f" {Fore.RED}That's not a banner that's available! Try again{Style.RESET_ALL}\n")
                    else:
                        if new2 in m:
                            new2 = m[new2]
                        print(f" Ok, {Fore.YELLOW}{new2}{Style.RESET_ALL} selected")
                        break

                if new2 in ('0', 'exit'):
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, not changing banner anymore{Style.RESET_ALL}\n')
                    continue
                print(f'\n {Fore.CYAN}Choose your Chronicled Path now!{Style.RESET_ALL}\n'
                      f' List of available options:\n')
                options = ([i.name for i in chronicled_banner_list[new2]['characters']['5-stars']] +
                           [i.name for i in chronicled_banner_list[new2]['weapons']['5-stars']])
                m = {str(q): w for q, w in zip(range(1, len(options)+1), options)}
                for i in m.items():
                    print(f" {i[0]} = {Fore.YELLOW}{i[1]}{Style.RESET_ALL}")
                print('\n (Type 0 to exit)\n')

                while True:
                    new3 = input(' Choose one: ').strip()
                    if new3 in ('0', 'exit'):
                        break
                    if new3 not in m and new3 not in m.values():
                        print(f" {Fore.RED}That's not a valid pick! Try again\n"
                              f" {Fore.LIGHTMAGENTA_EX}Please make sure the capitalization matches{Style.RESET_ALL}\n")
                    else:
                        if new3 in m:
                            new3 = m[new3]
                        print(f" Ok, {Fore.YELLOW}{new3}{Style.RESET_ALL} selected")
                        break

                if new3 in ('0', 'exit'):
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, not choosing Chronicled Path anymore{Style.RESET_ALL}\n')
                    continue
                user_banner_input = [new1, [new2, new3]]

            elif new1 == 'weapon':
                m = {str(q): w for q, w in zip(range(1, len(weapon_banner_list)+1), weapon_banner_list.keys())}
                for i in m.items():
                    first = f" {i[0]} = {i[1]}"
                    print(" " + first + ' ' * (62-len(first)) + '(' + str(weapon_banner_list[i[1]][1]) + ')')
                    # just learned that ljust and rjust exist, leaving this comment here for later

                # print('\n'.join(i for i in weapon_banner_list))
                print('\n (Type 0 to exit)\n')

                while True:
                    new2 = input(' Choose one: ').strip()
                    if new2 in ('0', 'exit'):
                        break
                    if new2 not in m and new2 not in m.values():
                        print(f" {Fore.RED}That's not a banner that's available! Try again\n"
                              f" {Fore.LIGHTMAGENTA_EX}Please make sure the capitalization matches{Style.RESET_ALL}\n")
                    else:
                        if new2 in m:
                            new2 = m[new2]
                        print(f" Ok, {Fore.YELLOW}{new2}{Style.RESET_ALL} selected")
                        break

                if new2 in ('0', 'exit'):
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, not changing banner anymore{Style.RESET_ALL}\n')
                    continue
                print(f'\n {Fore.CYAN}Choose your Epitomized Path now!{Style.RESET_ALL}\n'
                      f' List of available options:\n')
                m = {"1": weapon_banner_list[new2][0][0].name, "2": weapon_banner_list[new2][0][1].name}
                for i in m.items():
                    print(f" {i[0]} = {Fore.YELLOW}{i[1]}{Style.RESET_ALL}")
                print('\n (Type 0 to exit)\n')

                while True:
                    new3 = input(' Choose one: ').strip()
                    if new3 in ('0', 'exit'):
                        break
                    if new3 not in m and new3 not in m.values():
                        print(f" {Fore.RED}That's not a valid pick! Try again\n"
                              f" {Fore.LIGHTMAGENTA_EX}Please make sure the capitalization matches{Style.RESET_ALL}\n")
                    else:
                        if new3 in m:
                            new3 = m[new3]
                        print(f" Ok, {Fore.YELLOW}{new3}{Style.RESET_ALL} selected")
                        break

                if new3 in ('0', 'exit'):
                    print(f' {Fore.LIGHTMAGENTA_EX}Ok, not choosing Epitomized Path anymore{Style.RESET_ALL}\n')
                    continue
                user_banner_input = [new1, [new2, new3]]

        pities['weapon'][2] = 0
        pities['chronicled'][2] = False
        save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                          unique_four_weap_count, gacha_system)
        save_new_banner_of_choice()
        print_banner('New')
        print()
        continue

    if user_command == 'balls':  # hello dear reader
        print()                  # this is kaeya from genshin impact!
        print('''?????????7?YG#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@&&&&&&&@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&##BGGBBGG5J77???????
?????????JG#&&&&&&&&&&&&&&&&&&&@@@@&&&&&&&&&&&&&&&&&&&&@@&&&@&&&&&&@@@&&@&&&&&&&&&&&##&&#####&&&&&&&&#&BGPG#B#B5?7??????
???7???JP#&&&&&&&&&&&&&&&&&@@@@@@@&&&&&&&&&#############&&&&&&&&&&&&@@@&@&&&&&&&&&&&&&&&&&######&&&&&&&&#G55G#&#5???????
7777?JYB&&&&&&&&&&&&&&&&&@@@&&&&&&&&&&&&&&##############&&#&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&&&&&&#&&&&&&&&&#BG5B##B5?7????
??J5PB#&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&###BPPG5?7???
BB#&&&&&&&&&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@&&&&@@&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&G55GGY?7??
&&&&&&&&&&&&&&&&&&&&&&@@##&@@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@&&&@&&&&&&&##&&###&&&&&&&&&&&&&&&&&&#BP5PGP?7??
&&&&&&&&&&&&&&&&&&&&&&&&&&@@&&&&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@@&&&&&&&&&&&&&&&&&##&&&&&&&&&&&&&&&&#BPPGY?7??
&&&&&&&&&&&&&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&@&&&&&&&&&&###&&&&@@@@@&&&&#BG5J??777
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&####&&&&&&&&&&&&&&&@@&&&&&&&&&&&&&@@&&&&&&&&&&&&&&###&&&&&&&&&&&#GJ?7???
&&&&&&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&######&&&&&&&&&&&&&&&&&&&&&&&&&&@@&&@&&&&&&&@@@&&&&&&&##&&@@&&&&#BG5J??J
&&&&&&&&&&&@&&@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&###&###&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@&&&&&&&&&&@&&&@&&&&&&&&&&&&&&&&#GGP555
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#############BBB###&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&##BBBG
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&#####BBBBBB###&&&&&&&&&&&&&&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&BP5
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&###BB####&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&&&&&&&&&&&#&##
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#BB##&&&&&&&&&&#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&###&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&##BB#&&&##&&&&&&&&&&&&&&&&&&&&&&&&&&@##&&&&&#B##&&&&&&&&&&###&&&#&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#BB##&#####&&&###&&&&##&&&&&&&&&&&&&&&#BB&&#&BGGBB#&&&&&&&&&&&&&&&####&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&##B#######&&&####&&&&#####&&&&&&&&&&&&&BGB&&BBGP55PGB#&&&&&&&&&&&#&&####&##&&&&@&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#BBB####&&&####&&&&&&#BB###&&&&&&&&&&&&#GPB#&#GP5YYY5GB#&&&&&&&&&&&##&&&&&&&##&&&&@&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&##BB#&&&&&&&##&&&&&&&&#BB##&&&&&#&&&&&&&BG5G#&#B5JJY5PB####&&&&&&&&&&&#&&&#&&&&##&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&##BB#&&#&&&&&&&&&&&&&&#BB##&&&&&##&&&&&&#G5YGB##BPY5G##BPPGGB#&&&&&&&&&&&#####&&&&#&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&##&#BB&&&&&&&&&&&&&&&&&&###&&&&&&&&&&&&&&#BPJYGB#BB###BG5YYYY5PB##&&&&&&&&&&&&&#&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&#&&BB#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#GY?5B##&&#G5YJJJJJYYY5GB#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&#&&#BB#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#B5JYG#&&#B5J???JJJJJYYYY5GB#&&&&&&&&&&&&&&&&&&&&&@&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&#GB&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&BP5PB&&#BP5J????JJJJJJJJYYY5B#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&#BG#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#BB##&&#GP5YJ?????JJJJJJJJYYYYPB#&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&#BB#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&##BBBBGGP5Y???????JJJJJJJYYYYYYPB#&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&#B#&&&#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&BGPPGPPGGP5J????????JJJJJJJYYYYYYYPB#&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&#&#B#&&&#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#GP55555PGP5YJ????????JJJJJJJJJJYYYYY5PG###&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&#B#&&&&&@&&@&&&&&&&#&&&&&&&&&&&&&&&#BP5YJYY5GGPYJ???????????????JJJJJJYYYY55PGB##&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&#B#&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&#BBP5Y?JYY5GP5YJ??????????????JJY55PPPPPGGGGPPGGBB#&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&#B&&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&#GYJJJYY5PP55YJJJJJJJJJJJYY55PGGGGBBB#&&&&&#BBGGPGB#&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&###&#&&&@&&&&&&&&&&&&&&&&&&&&&&&&&###GYY5Y5PP555YYYYY555PPGB###################BBBGPPG#&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&###&&#&&&&&&&&&&&&&&&&&&&&&&&&&&&&###&#P55PP5555YY55PBB###&&&&&&&&&&&#BBBBGGPPPPPGGP55G#&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&###&&##&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#&#BP55555YYY5PPGB###&&&&&&@@@##&@&##&&&##BGGGGPP55G#@&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&##&&&#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&##&#BP555YJYY5PGGBB#BBBBBP5G#&#BB##GYYPB#&&###BPP555G&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&##&&&##&&&&&&&&&&&&&&&&&&&&&&&&&&&&###&#BP5YJJJJYY5PGGGPPGPP5YJJYPPGGG5J?J5PGBBBGGP555Y5B&&&&&&&&##&@&&&&&&&&
&&&&&&&&&&&B#&&&#&&&&&&&&&&&&&&&&&&&&&&&&&&&#&&&&#BBPYJJ??JJY5PP5YY5555555YYYYYYYYY555PGGP55YYYYYY5B&&&&&&&##&&&&&&&&&&&
&&&&&&&&&&#B&&&##&&&&&&&&&&&&&&&&&&&&&&&&&&&#&&&#BGGPYJJ???JY5555Y555Y55555555Y5YYY555555YYYYYYYYYG#&#&&&&&#&&&&&&&&&@&#
&&&&&&&&&&##&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#GP55PP5YJJ?JJY555YJJJYJJYYYYYYYYYYYYYYYJJJJJJJJYYYYB##&&&&&##&&&&&&&&&@#Y
&&&&&&&&&#B#&&&&&@&&&&&&&&&&&&&&&&&&&&&&&&&&#G55555P5YJJ???JJY55YJJJJJJJJJJJJJJJJJJJJJJJJJJJJJYYYPB##&&&&&&#&&&&&&&&@&G7
&&&&&&&@#GG#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&BPYYY555555YJJ???JJY55YYJJJJ?JJJJJJJJJJJJJJJJJJJJJJJYYYG###&&&&&&&&&&&&&&&&GJ!
&&&&&&&@&BG&&&#&&&&&&&&&&&&&&&&&&&&&&&&&B5JJJJYY55555YJJ?7??JY55YYJJJJJ?????JJJJJJJJJJJJJJJJJYYYPB###&&&&&&&&&&&&&&#GY77
&&&&&&&&&##&&&#&&&&&&&&&&##&&&&&&&&&&#PYJ??JJYY555555YJJ?7??JYY55YJJJJJ????????JJ?JJJJJJJJJJJJY5BBB#&&&&&&&&&&&&&&BGY777
&&&&&&&&&&#&&&&&&&&&&&&&&BP5PPGGGBGPYJJ????JJY5555555YJJ????JJY55YYJJJJ?JJ??????J??JJJJJJJJJYY5GGGB#&&&&&&&&&&&@&BBJ7777
&&&&&&&&&##&&&&&&@&&&&&&#PYJJJJJJJ???J????JJYY55PP555YJ?????JJYY5YYYJJJJJJJJ????????JJJJJJJYYYPGGGB#&&&&&#&&&&@#BBJ77777
&&&&&&&@&##&&&&&&&&&&&##BYJJJJJJ????J????JJYY5PPPPP55YJ?????JJYYYYYYYJJJJJJJJ?????JJJJJJJYYY55PPGGB&&&&&#&&&&&#BBY!77777
#&&&&&&&&#B&&&&&&&&&&###PYJJJJJJJJJJJJJJJJJY5PP55P555YJ?777?JJYYYYYYYYJJJJJJ?????JJJJJJJYYY555PPGG#&&&#B&&&&&##GY?777777
B#&&&&&&&&#&&&&&&&&&&##B5YYYJJJJJJJJJJJJJJJY5P555P55YJJ?77??JJJYYYYYYYJJJJJJ??JJJJJJJJYYYYY55PPGGG#&&&#&&&&&#&5?JJ777777
BB#&&&&&&&##&&&&&&&&&##BP5YYYYJJJJJJJJJJJJJY5PPPPPPP5YJJJJJJYY5555555YJJ??JJJJJJJJJJJYYYYY55PPGGGG#&&&&&&&&#&G?7Y?777777
PGB#&&&&&&##&&&&&&&&&##GP55YYYYYJJJJJJJJJJJJ5PB#####BGGPPPPPGBBBBBBG5JJ????JJJJJJJJJJYYYY555PPPGGB#&&&&&&&#BG5?7J?777777
YPBB#&&&&&&#&&&&&&&&###GP55555YYYYYJJJJJJJYYYY5PPGGBBBBBBBBBBBGGGGP5YJJ????JJJJJJJJJYYYYY555PPPPG#&&&&&&&#B5PY?7J7777777
JYPGB&&&&&&#&&&&&&&###BGPPP5555YYYYJYYJJJJJYYYYYY5555PPPGGP5555555YYJJJJJJJJJJJJJJJJYYYY55555PPPB&&&&&&&&BPYGJ7?Y?777777
JJY5G#&#&&&#&&&&&&&###BPPPPP555YYYYJYYYYYYYYYYJYYYYYYYYY55YYYYYYYYYJJJJJJJJJJJJJJJJYYYY555555PPG&&##&&&#BPYP5?7?Y7777777
??JY5GB##&&&&&&&&&####BPPPPPP555YYYYYYYYYYYYYYYJJYYYJJJYY5YJJJJJJYJJJJJJJJJJJJJYYYYYY55555555PG#&##&&&&BG55P?77?J7777777
???JY5GBB#&&&&&&&&####GPPPPPPP55YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYJJJJYYYYYYYYYYYY555555PPG####&&&##GPPP5?77??7777777
???JJYPGGB&&&&&&&#&###GPPPPPPP55Y55555PGGGGGBBBBGGGGGGGPPPGGGGGGGGGGGGPPPPPPP5YYYYYY555555PPGB##GB&&#GGPGGPJ777?77777777
77??JJ555G#&&&&&&####BBGPPPPPPP55YYYYY5PGBBBBGGGPGGGGGBBBBBBBGGGGGGGGBBGGGP555YYYYY55P55PPPGBB#B5#@#5YPPGPY?77?777777777
J?7?JJYJJ5#&&&&&###BBBBGGGPGGGP55YYYYJJY5PPPGPPPP5YYYYY5555YYYYY5555555YYYYYYYYYY555PPPPPPGGBBB5B@#5?YJPPYJ7777777777777
B5J7?JY?7YB&&&&&###5JPBGGGGGGGGP5555YYYYY5PPPPPPPPP55YYYYYYYYY55555555YYYYYYYYYY55PPPPPPPGBG55GG&&57?5YPYJ?7777777777777
GYYJ77??7?P&&&&&&#BY?YG#BGGGGGGGP55555555555PPPPPPPPPPP555555555555555YYYYYYYYY555PPPPPGGB#5JYG#&G?7JYJYJ??7777777777777
Y777777?7?5#&#####G5JJP##BGGGPPPPP55555555555PPPPPPGGGGGGGGGPPPPP5555YYYYYYYY5555PPPPPGGBB#PY5#&BY77JJ7JJ??7777777777777
777777777?5B###BGBG5??5###BBGGPPPPP55555555555555555PPPPPPPPP555YYYYYYYYYYYY55555PPPGGBBBBBP5P##5?77?J777777777777777777
77777?777?YP##P55PG5?7Y#BBBBBBGGPPPP5555YYYYYYYYYYYYYYJJYYYJJJJJJJJJJJYYYYY55555PPGGBBBBBBBG5PBBY?77??777777777777777777
?7777??77?J5#GJ??YP5J7YBBBBBBBBBBGPPP5555YYYYYYYYYYJJJJJJJJJJJJJJJJJJJYYYY5YY55PGGBBBBGGGGGGGGBGPY?7??777777777777777777
?777?7????J5B5?7?JJ5J7YBBBBBBBBBBBBGGPP5555YYYYYYYJJJJJJJJJJJJJJJJJJJYYY55YY5PGGBBBGGGPPGGGGB##BBBPJ?7777777777777777777
J?????7?????5Y?7?JJJ?7YBBGGGGGGGBBBBBGGPP5555YYYYYYYJJJJJJJJJJJJJJYYYYYYYY5PGGBBBGGPPPPPPPGGB#&#BB#B5YJ77777777777777777
#G5??J??77!!?J?7?JJ?77YGGGGGPGGGGGBB#BBBGGPP5555YYYYYYYYYJJJYYYJYYYYYYYY5PGBBBBGPPP5555PPPPGB&&#BB#BG5P5Y?77777777777777
#&&B5?7777?JJJJ??Y?77?YGGGGPPPPPGGGGBBB##BBGPP5555555YYYYYYYYYYYYY55555PGBBBBGPP55555555PPPG#&&#BB###G5PP5?7?77777777777
BB#&#GJ7!?YYJJ?JYJ??J5GGGGPPPPPPPPGGGGGBB###BBGPPPPP5555555555555PPPGBB#BBGGPPP5555555555PPG#&&##BB###GPGGPJ?77777777777
PGB##B#5!7YYJ?JYYY5PGGGGGGPPPPPPPPPPGGGGBBBBB##BBBGGGGGGGGGGGGGBBB###BBGGPPP5555555555Y55PPB#&###BB####GGGG5Y?????777777
''')
        continue

    if user_command == 'ballshd':
        print()
        print(
'''^^^^^~~~~~^^^^^~~~~~~~~^^^^^:^^~~^^^:::~^^!~5GB#BBPBB&&####BGPPPPPP5555PPPPPPP5J??JY5G###PY?7!!!!!~~~^^^^^^~~~~~~~~!!!!7
^^^^^~~~^^:::::^^~~~^^^^^^:^^^^~~^^^^~!JJJYYBBBBB#B&&&####BBBBGG5YYY5PPPGGBBBBBBGPP555PG####PJ7!~~~~^^^^^^^^~~^^^~^^~~!!
^^^^^^^^::::::::^^^^^:^^^^^^^^~~!7?YPGBB######BBB#&&&&&&&&#&#BGPGBGPPPPGGGBB#######&&&&##&&&&#5777~^^^:::^^^^^^^^^^^~~~~
^^^^^^^^^^^^^^::^^^^^:::^^^^~!7JPGBBBB##########BB##&&&&&&&&#BB#&##BGGPPPPPPPPGGGB#&##GGY?YY5G#GJ!!!~^^:::^^:::^^^^~~^^^
^^^^^^^^^^^:::^^^^^^::^^^^~!?YPBBBBBBB########&&######&&&&&&##&&&####BBBBBBGGP55555PGBG5Y?~!77J5PP?~~~^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^:::::^^^^^^^^^!J5GBBBBBBBBBBBBBBBBB####&&&&&&&&&&&&&&&&&&&&#######BBGGGP555PG5J7^~7?JJ?Y5J!^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^:^^^^^^^^~~!?5GBBBBBBBBBGBGGGGBB###&&&&&&&&&&&&&##&&&&&&&&##BGGGGGGBBB##BGGPP5?!^^!7?JJ??JJ7!~^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^~~!7YPGBBBB#BBBBBGPPGB##&######&&&&&&&&&&&&&&&&&&&&###BGGPPGGBB####BBBGG57~~!!!!!!!!7??7!~~^^^::^^^^^
~~~^^~~~~~^^^^^^~~~~!?5GBBBB##BBBBBGGB###BGGGGGB##&&&##&&&&&&&&&&&&&&&&####BBBGGGGB######BGGGP?!~~~~~~~~~~!7!!~^^^^^^^^^
~~~~~~~~~~~~~~~~~~~!?PGBB#####BB#####BGP555PGGBB#&&#BB###&&&&&&&&&&##&&&BGGGGB#BBBGB##&&###G5GYY!~~~~~~~~~~~~~~^^^^^^^^^
~~~~~~~~~~~~~~~~~!7JPBB######BB##&#BGP55PPPGGGG##BGGB#BB&&&&&&&##&&&##&&&#GPPPGB###BBB##&##BP5J7!~~~~~~~~~~~~~~~^^^^^:::
!!!!~~~~~~~~~~~~!7JGB#######BB#&&##BBGGGGGGPPGGGGGB#BG#&&&&&&&&&###&&#B#&&##BGGGB#&&####&&###B5?~~~~~~~~~~~^^^^^~~~^^^^^
!!!!!!!!!!~~~~!!~?G#####&&#B###&&##BBBBBGPPPGGBBB#BGB&&###&&&&&&#####&#B###&&##BB###&&#&&&&&##BP!^~~~~~~~~^^^^^^^^^^^^^^
!!!!!!!!!!!!!!!!?P######&#####&&###B##BBGGBB###BBGB###BB####&&&&&&#####BB###&&&&###&&&&&&&&&&#BG5~:~!~^^^^^^^^^^^^::::::
!~~!!!!!!!!!!777YB##&#####&&&&&#&&#####BB####BGBB#BBBBBBBBB##&&&&&B###########&&&&&&&&&&&&&&&&#BG5!:^~~^^^^^^::::::::::^
~~!!!!!!!!!!!77JPB#&###&&&&&&##&&&&&####&&##BBBBBBBBBBBBB##B##&&#5YPG#######&&####&&&&&&###&&&##BPY!^^^~^^^^^^^^^^^~~^^^
!!!!~!!!!!!!!777P######&&&&###&&&&&&#&&&&&&#BBBBBBBBBBB##BBB#&#PYJJJY5PPPGGGBB#&&&&&&&#&&#BGBBB##BPY!^^~~~^~~~!~~~!!~^^^
!!!~~~~!!!!7!77?B#B###&&&###&&&&&&###&&&&&&BBBGBBBBB###BB###BG5J????JJYY5555555PB&&&&&&&####BGPPGBBPY7^^~~~!!!77!!77!!^^
7~~!!!!!777JYJYG########BB#&&&&#BGB#&&&&###BBBBBBB###BB#BG5J?JYY?77??JJJYYYY55555PB###&&&&&###BP555PP5?~~!!777?7!777?7!7
!!!7!!~!!!!7JPGBBB####BB#&&&#BP55G#&&&&&###BB#BB#&##BBGY!^^~!7??J?7!!7??JJYYYJJYYY5PGB##&&&&&###BG5JJYYY77???J??J???J??J
~~~!!!!7!!!777?5####BBBBBGP5YY5G#&&&&&&&&##BB###&#BG5J!!7?JYYYJJJ???77!7?JJJJ???JJYYY5PGB&&&&&&&BB#BPJ??J?77????777???JJ
~~!77~!!!!!!77!YB####BBGGP555GB&&&&&#&&&&###G####P5J??JJ?77?YPGGGG55YJJJJ??JJ7!77?JYY5YYB&&&&&&&&5JG##PY?77777~~!JY77777
!77??7!!!??~~7JGGB#######G5PPP5&&&&&&#&#####PB##PJJ???7!~~~~~7J5GBBB&#BGGP5J?77?Y5YY5PB#&BB&&&&###PJYPBBPY?~!??JYJJJ?~~~
JYJJJJ77?J?7!JGPPB#######PJ?JJB&&#&#&####&##PPB#YJ???77!!7??J5PGBBGGGBB##BPPPP5YJGG#&&##G5&&#GB##BBGJ?YBBPP57~!JYJ?!~~~~
?JJ?????????JPGGBBB####&&P?!~JB#&####&#BG#&B#PP&P??????JYPGG55YGPGBBBGGGGGP5YYPP~5G#&###YG&&B~Y5GBGGPYJ?PBPY5J~~7JJ?J777
~!!7777777?JYJ55PGPB####&#J775GG#&##B##&G5##GBGG#Y7!77?JJYJYJ??JJ5GGGGPPPP5?~!JY!YGB#&##?B##G:~JJ5GGYJYYJPG5??57~7Y5YYYJ
~^~~~~~~~~!!!?Y55YYGBGB#&&#5J5GPG##BBBBB&GYPP5GBBP7~~!!7????JY5PPP5YYJ?YYY5J!^7J5PGBB###7G##P^~!7~YPPJ755JYP5^757!7?JJ5Y
????JJJJ?7!?^!JJ??YP55GG##&&PYYPGB##BGBBB#GJ?JJYB#5!^^^~!7?????????7!7?JJJJJJ7!?PYYB####?Y#BJ~J!~~!?5PJ7J!?Y5?.!577J7!77
55555555J!~7!^!!!!7J5555G#&&&GJ??JB#&BPGPG#BYJ?7?5PY~^::^^~!!!!7777777????JJYJ?JYG?5####77#GJ7YY7??JYPGY?YJYP?:~J57J!~~!
5555YYY5Y7!?J~~!!~~~!!75BGB&&&#5??JG&#5Y5JP#BGP5YJJYJ!^^::^^^~~~!!7777???JJYYYJJJYGPG#P!?B#BP!?55YY5YPGGYYBB5?:^?PYJ!!!!
5555YYY55YJYY?77!!!!!!7JY?PB##&&B?JG&BBJJ?YB#PGGGGP5YJ7~^^^^~~~!!777??JJJJJYYYJ??7YGG5J?###GP7!?Y5YYY55PB5YG5J^^?YP5?YY?
55Y55YY5555Y7~777!!!!!!~!!75###&Y~P5P#P7?J5P#PJJ5PP5P5YJ!~~~!!!7777??JYJ7!77???~^7~JY??B&##G5!7?J5PGGPY5PPJ5P?^~YJPP5PP5
55555YY5555?~~77!!~~~~~!77?5GG#P~Y5J?5??GY5G#GY!!7JYJJ?JJ7777777?????J55YY55YYYJJ577!7B&###B5?~??Y55YJ77?7??Y?~~?J5Y5555
5555YYY555Y7!??7!!~~~~~!!7??5B#Y?Y?7Y?JGBYGB#BJ!~!!?JJ?7?7777??????????JYPGGBBGGPY?!^5##P#GBPY~!?JY55PPP5Y5J??~!7?!~~~~~
5555YY55555J???7!!~~~!7?JY5GB#B#BPPGYPGGPG#B#BY7!!!7????77777????77777!!!7JPGGGPYJ?^75PBPGBGG5!^7?J555J?JJJJJ~^!7!!!~^^~
555Y5YY555JJJ?77!!!7?77JPBGBBBBB##GYPGGPB#GP#BY?!!!!7?7??7777???7!!!!!!!~~!JP5Y??J?^7JJYYPP5GG?^?JJYYYYYYYYJ?^!JJJJJJJ??
55555J??YYJJY!~~~~!J??YGG55GBBBBB#GGBGGG#BGGBP5J7!!77777?777????JJJ??JJJY555555JJJ7^^~7777JJ5P5~!JJYYYYYYYYY!~?JJ????777
555555J7!??JY7~^^^^~75GBB##BBB###5JB#PGG#B##GYYY?7777777?777???!7JY555P55PGGGGYJJ?57^^~~~!~J555~~7?YYJJ??JJ?~7????7777!!
PPPPP55Y~~~~?77!^^:~5GGGB#BBB#&##J?GBGPBBBGP5555YJ?????????????7!!!7?JJJJYY5P5YJ?PP?~~~~^^~7JYP~~7!?YJ?7?J?77?7777777777
PPPPPP55?!7~~7!^~!JPBB#BBBGGB#&##Y~5GGPGGPY77Y55P5YJJJJJJJJJ????77??JY55PPPPP5Y?GB55J?77~~77?YJ!!J?7JJJ???7777777!!!!!!~
PPPPPPJ55~!~~!^~JPP5BBBBGGGG##&##G~75GGPBPJ7~!JJJ5PP5YYYYYJJJJ?????????JY5PP5?!Y##BGPYJ?7?JJJ?!!7?J7????????????7777777!
PPPPPP7?J^::^~~?GGPGBBBBGBBB#&####?^!YGGGG5J!!?!~7J5PPP55YYYJJJ?777!!!!7?JJY57!B###BGGPP55YYYJ?!~!77??????????????777777
PPP5YJ~!!~~~!7YBGGBB##BGBBB##&#&B#B7^^7PGP5Y?7!~~~!7J5PGGGPP5YJ?77!!~^~!7?JYJ~5##G5Y5P5YJJJ?7?7!^:^^7????77777!!!!!!~~~~
5Y??7~~!~^~75PB#BB###BBBBBB#&&##BBBG?~:^?PG5JJ?!~~!!7?JYPGGGGGP5YJJJ?JYYY555YP##PYJ??YJYY?!!!!~!~::::~77777!777!!!!!!!!!
77?JY?~~~~~!?P####BBGBBGGBB#&&#BBBBBG5?~:~JPPYY?7!!!777?JY5PGGGGGGGGP5PBPPBB###BP5JY?7?7!!!~~^^^!!^:::^~!7777777!7777!!!
55Y7!!~~!?5PGBBGBBPPBBP5PGB#&&#GBGB#B5PPJ~^7Y55YJ?77777?????J5PGGGGYYPBBY?B#BBGPJJY57!7?~^^^~^^::!?^::::~77~^^!7!7!!!!!!
Y5Y!~^!7!?5BBGGBBGGPBBPYPPGG#&&GGBBB#G?JPPY!~7JY5YJ???????7!77JYPP?~YGG5J7BBBG5??Y??7!!?~^^^!~^^^^?~::^^^~^^.^7?????7777
Y5?^!7!!!YG##BB##BGB##BPPGGGGB#BPGBBB#BJ?JY5Y!:^7?JYYYJ??7!!!77?JJ~?GP5J^?BBPPY7?J777?!!~^~~~!^~!!~~^:!!^^~~.!?JJJJ?????
5J!?Y5P5P&##BB#######&&BB#BB#BGBBGPGB##BY?JYPPJ~:::^!7?JYYJ?7777?7?GBJ!~~YBGP5Y??7??7?7!~~!7!!!?!?!~^^!!^77~:JJJYYYYJJJJ
&##&&@@&&&##B###&&&#&&&###&##&###BBGP5P##P??Y5PYJ!~^:.:^!?55YJ????JP#B:7Y5GGP5YYYYYY????~~!????JJ7?7~!!!7777!7?JYYYYY555
&&&&&&&&&&##B##&&&&##############&#BGPJ?G&BYJYP555?77~~^.P&G5Y?!7J5##&5J55GGP5Y55PPP5Y?J?~!?J?7?JJJ7!!!7????7^~!JYYJJJ?7
######&&&&&#B####&&######BBBBBBBBB###GP?~5&#5?JY5GY??JYJ7B@&G555GGG###&55YGGP5Y5PPGGPP5JY?!777!77J?777!~^~!77~^~~J?7777!
BBGGGG#&&&&##&######B#BBGPGGPGGGGGGGB##GY~G#5?~~JY5YJ?Y5YP@@GPPPPPGG&#@GY5PPP5Y55PGGP555YJ?7!!!77??77??7!^^^^!!!!7YYYYYY
BBGGPPGB#&&###&BBB##GGGGG55PGP5PPPPPGBBB#PP#Y!!^^~!??7?YY5#&GPPPPPPPB&@@57JGPP5555PPPP5JJJ??7!!!7????777?7^^^:^~7^???777
&#BBBGGB##&&&###BGB#BPGPGP5Y555Y55PGGGBBBBBBPJ77!~^::~!7?J&&GP5555PP5G&@@57YPGPP5555P5YJ7~~~!!^^~!777!~^~!!:^^::!:~!~!77
&&&########&&#B&#BGGBGPGGGP55Y55555PGGBB#B#BGPP5?7777!!7!P@&#P55PPPY~?B&@@#PYPGPPPP55YJJJ?!~^~~::^~~~~^^^^!^:^::!:~!!??J
@@&#&&&&&&&&&@&#&#BBBBGGGBBGPPPPPGGGGGGB####G5Y5G5JJY5Y?Y@@@@B55PP5~^YGPB@@@#PPPPPPPPP55J?7~^^!!^^^^^^^^^^~^:^^!7:JY!!7?
&@@&&&&@@&&&&&@&#BGB####B#####BBBGGGB#BB###&#GP7?5GP777^G@@@@&GYYYJ~JG5J?5#&#55PPPPPPP55YJ?7!~^~~~~~~^~~~^^~!!!?7!YJ!!^~
#&@@&&&@@@@&&&&&@&GPGB####&&&&&#####BB###B#&&BG57!?5Y~^^B@@@@@BGGPPPPJ??77Y#5JY55555555YJ??777!~!!!7!!!!!~~^!!7J7?Y?~^::
#&@@@&&&@@@@@&&&@&PPG#######&&&&&&&&#B###GPPB&BG5?!!?555#@@@@&GGGP55Y??777YBY^7JYYYYYYYYJ???7!!7!77??77?77~~:~7!7JYJ?~^:
##&@@&&&&@@@@@&&@&PPG&&&####B#&&&&&&&##&&&B55G#BY5Y7!!?5GB&@@BGGPYYJJJ7!JYJ5B!!?JJJJJ???JJJJJ?7!!!!!77??77~^~^!JJYY5YJ7~
&##&@&&&@@@@@@@&@#PPB#PG&&&&#BG#&&&&&&##&&&BGGBBJ!JYJ!~7YY5B#P5Y?YY77Y??J??JB57?JJJJYJ77?JYYYYYJ??77!!77!~^~Y!~PPGBB5YJ7
&&&&@@&@@@@@@@@@@BYYG&#&@&&&&&#GB###&&&&&#&&#B##G7~7??7?!~!J5G5J?Y5YY5J7777?5#!^!JYY?JJ??JY55555YYJJ?JJY?~~J5?!G&&#P55YY
5&@&&@@@@@@@@@@@@G^!G@@@&&&&&&##BB###&&&&&###B#&#P7~~7!!!~~?5P#BP5Y55P5J7!~!JBG^!!7YYJYYYYY5PPP5P5Y?77JJ7??YP5G###BP555P
?JB@@@@@@@@@@@@@@5:^P@@@&&###&&&###&#####&&#BB#&#G5!:^^!~!?J7!Y&B5YYYPP57~~!!J#J^~!?5YYY55PPPPGPP55J7!!!777YB###BPY555G#
!?5B@@@@@@@@@@&@@J:^B@&&&&&####&&###&#####&&#&&&#BP5!~:^~!7~:^^?##5YJY55Y!!~~~5#7^^~J5YY5PPPPGGGGP5PY??!!7~?GBBBPG5?!YB#
:75P&@@@@@@@@@&@@?:^#&##&&&#######&&&&&&#####&&&&&BPY7^:.^~!~~!!!G&5JJJY5?!~~~!BB~^^~YYJJY55PPPGGGPPP5YY???JPBBBGGG5?JY5
^~JYB@@@@@@&&&&@@?^~#&####&&&#&&###&&&@&&########&&BP57~::~?J?7?7!5&PJJJYY?!~~~J&Y:::?YJ7?JYYY5PPPPY5Y7JYYGGBBBBBBB#GYJY
~:!YG&@@@@&&&&@@&?^~#&#####&&&##&&&#&&&&@&B##&&&##&##BP5?!!7?YJ??7!Y&PJJYYJ7!!!7G&!:^!5Y!7??JJJJY55JJ7~!?PBB#####&&BPYJ?
?~^?P&@@&&&&&&@@&J~~#@&###&&&&&#&&@&&&#&&&&#GB&&&&&####BBGG5J?YY???7J#GJYY5J7777J&Y:~~Y57~7?J?J77???JJ!!7?YG#&&&&#GP5J^.
GPJJP&@@&@@@&@@@&P5?#@&&&&&&&&&&&&@@@&&##&&#B5P##&&####BPPGGBPYYYJ???J#GYY5Y??77?BB^~!J5J^7?P5YJJJ?7!!!~!7??P#&#BBG5?J?:
Y5BGG&@@@@@@@@@@&GBP#@@@&&&&&&@@@&@@@&@&GB&&BPJGGB&#B##BBP5YJ5G5Y5YJ??J#GY55Y????G&!~7?5Y!7?B#BGPPY?77777?JJG&##BGPY:^J?
YYPG#@@@@@@@@@@@&BBBGGB#&@@&&&&&@@@@@@@&GP#&BP?PBPB&###BPGP55JY5JYP5JJJJBG555Y???P@J~??Y577?G&#####BPJ55YJ5YG#BBBPJJ!.^?
5PPG#@@@@@@@@@@@@&##BPJ!7YGB#&@@@@@@@@&#GB##G5JGBGP#&B##GY5555Y5YYJPPY5YYBBPPP5YJY@G~??YYJ??G&#####&&PPPP5PG##PYGP~!J:.:
55PGB#&@@@@@@@@@@&&&&&BY?JY5PPGGB&&@&&&B###BG5YG#BGG&&BB#GJJY555555JPPPP55#BPP5Y55##7??J5Y??G&#######GP55PGB###PJJ:!J~..
''')
        continue

    if user_command == 'load':
        Path(".\\banner_info").mkdir(parents=True, exist_ok=True)
        try:
            pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count = load_info()
            print(Fore.LIGHTGREEN_EX + ' Loaded additional information successfully!' + Style.RESET_ALL)
            info_ok = True
        except:
            print(Fore.RED + ' Something off with info file. Clearing everything...' + Style.RESET_ALL)
            info_ok = False

        if info_ok:
            try:
                cchar, wweap, sstd, cchron = load_history()
                wish_history = {"character": cchar, "weapon": wweap, "standard": sstd, "chronicled": cchron}
                print(Fore.LIGHTGREEN_EX + ' Loaded wish history successfully!' + Style.RESET_ALL)
                history_ok = True
            except:
                print(Fore.RED + ' Something off with wish history file. Clearing everything...' + Style.RESET_ALL)
                history_ok = False

        if info_ok and history_ok:
            try:
                constellations, refinements = load_archive()
                print(Fore.LIGHTGREEN_EX + ' Loaded archive successfully!' + Style.RESET_ALL)
                archive_ok = True
            except:
                print(Fore.RED + ' Something off with archive file. Clearing everything...' + Style.RESET_ALL)
                archive_ok = False

        if not (info_ok and history_ok and archive_ok):
            set_defaults()

        load_distribution()

        try:
            load_banner()
            print(Fore.LIGHTGREEN_EX + ' Loaded banner information successfully!' + Style.RESET_ALL)
        except:
            print(Fore.RED + ' Something off with banner file. Setting to default...' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()

        print()
        continue

    if user_command == 'clear':
        set_defaults()
        pity_info = pities[banner_of_choice[0]]  # pities was reinitialized, need to make the reference again
        # print(' Done')
        print()
        continue

    if user_command == 'pity':
        print_pity(count, pity_info, five_count, four_count)
        print()
        continue

    if user_command == 'system':
        print(f"\n {Fore.CYAN}Choose gacha system:{Style.RESET_ALL}")
        print(f" Current system: {Fore.CYAN}{gacha_system}{Style.RESET_ALL}")
        systems = {"1": 'old', "2": 'new'}
        for i in systems.items():
            print(f" {i[0]} = {i[1]}")
        print('\n (Type 0 to exit)\n')
        while True:
            new_system = input(' Your pick: ').strip().lower()
            if new_system in ('0', 'exit'):
                break
            if new_system in systems or new_system in systems.values():
                break
            else:
                print(f' {Fore.RED}Please input either the number or the name of the system of choice{Style.RESET_ALL}\n')
        if new_system in ('0', 'exit'):
            print(f' {Fore.LIGHTMAGENTA_EX}Ok, not changing gacha system anymore{Style.RESET_ALL}\n')
            continue
        if new_system in systems:
            new_system = systems[new_system]
        print(f' {Fore.YELLOW}{new_system.capitalize()} gacha system selected.{Style.RESET_ALL}\n')
        gacha_system = new_system
        save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                          unique_four_weap_count, gacha_system)
        continue

    if user_command == 'inv':
        print_full_inventory()
        continue

    if user_command == 'inv box':
        print_inventory_box()
        continue

    if user_command.split()[0] == 'dist':
        total1 = sum(character_distribution.values()) - character_distribution[100]
        total2 = sum(weapon_distribution.values()) - weapon_distribution[100]
        if total1 or total2:
            print(' 1 = character\n 2 = weapon\n (they have different distributions, pick one)\n\n Type 0 to exit\n')
            while True:
                t = input(' Your choice: ').strip().lower()
                if t in ('0', 'exit'):
                    break
                if t == '1' or t == 'character':
                    t = 'character'
                    break
                elif t == '2' or t == 'weapon':
                    t = 'weapon'
                    break
                else:
                    print(' Please input either the number or the name of the distribution you want to see\n')

            if t in ('0', 'exit'):
                print(' Ok, exiting distribution selection\n')
                continue

            if t == 'character':
                if total1 > 0:
                    print(f' Total entries = {character_distribution[100]}')
                    print(f' Total 5★ entries = {total1}\n')
                    for i in range(1, 91):
                        print(f' Pity {i}: {character_distribution[i] / total1 * 100:.2f}% - {character_distribution[i]}/{total1}')
                    print(' If you want to visualize your results, type "viz" and then "1" or run visualize_character_distribution.py')
                else:
                    print(' Get a 5-star character first!')
                print()
                continue

            elif t == 'weapon':
                if total2 > 0:
                    print(f' Total entries = {weapon_distribution[100]}')
                    print(f' Total 5★ entries = {total2}\n')
                    for i in range(1, 78):
                        print(f' Pity {i}: {weapon_distribution[i] / total2 * 100:.2f}% - {weapon_distribution[i]}/{total2}')
                    print(' If you want to visualize your results, type "viz" and then "2" or run visualize_weapon_distribution.py')
                else:
                    print(' Get a 5-star from the weapon banner first!')
                print()
                continue
        else:
            print(' Get a 5-star first!\n')
            continue

    if user_command.split()[0] == 'viz':
        print(' 1 = character\n 2 = weapon\n (they have different distributions, pick one)\n\n Type 0 to exit\n')
        while True:
            t = input(' Your choice: ').strip().lower()
            if t in ('0', 'exit'):
                break
            if t == '1' or t == 'character':
                t = 'character'
                break
            elif t == '2' or t == 'weapon':
                t = 'weapon'
                break
            else:
                print(' Please input either the number or the name of the visualization you want to see\n')

        if t in ('0', 'exit'):
            print(' Ok, exiting visualization selection\n')
            continue

        if t == 'character':
            if character_distribution[100] < 10000000:
                print(f' {Fore.YELLOW}To see actual trends I recommend doing at least 10 million wishes{Style.RESET_ALL}\n')
                c = input(f' Type {Fore.CYAN}OK{Style.RESET_ALL} to do the remaining {10000000 - character_distribution[100]} wishes\n'
                          f' Or type {Fore.CYAN}CONFIRM{Style.RESET_ALL} if you want to see the graph regardless\n\n'
                          f' Your choice: ').strip()
                if c not in ("CONFIRM", "OK"):
                    print(' Aborting\n')
                    continue
            else:
                c = "CONFIRM"
            if c == "CONFIRM":
                if 'visualize_character_distribution' not in sys.modules:
                    import visualize_character_distribution
                else:
                    importlib.reload(visualize_character_distribution)
                print()
                continue
            else:
                if user_banner_input[0] != 'weapon':
                    user_command = 10000000 - character_distribution[100]
                    wished_by_viz = True
                else:
                    print(f' {Fore.RED}Change your banner type to {Fore.YELLOW}anything other than weapon {Fore.RED}first, then type the "viz" command again{Style.RESET_ALL}')
                    continue

        elif t == 'weapon':
            if weapon_distribution[100] < 10000000:
                print(f' {Fore.YELLOW}To see actual trends I recommend doing at least 10 million wishes{Style.RESET_ALL}')
                c = input(f' Type {Fore.CYAN}OK{Style.RESET_ALL} to do the remaining {10000000 - weapon_distribution[100]} wishes\n'
                          f' Or type {Fore.CYAN}CONFIRM{Style.RESET_ALL} if you want to see the graph regardless\n\n'
                          f' Your choice: ').strip()
                if c not in ("CONFIRM", "OK"):
                    print(' Aborting\n')
                    continue
            else:
                c = "CONFIRM"
            if c == "CONFIRM":
                if 'visualize_weapon_distribution' not in sys.modules:
                    import visualize_weapon_distribution
                else:
                    importlib.reload(visualize_weapon_distribution)
                print()
                continue
            else:
                if user_banner_input[0] == 'weapon':
                    user_command = 10000000 - weapon_distribution[100]
                    wished_by_viz = True
                else:
                    print(f' {Fore.RED}Change your banner type to {Fore.YELLOW}weapon {Fore.RED}first, then type the "viz" command again{Style.RESET_ALL}')
                    continue

    if user_command == 'h':
        if len(wish_history[banner_of_choice[0]]):
            num_of_pages = (len(wish_history[banner_of_choice[0]]) - 1) // 25 + 1
            print(f'\n========================= {Fore.LIGHTCYAN_EX}WISH HISTORY{Style.RESET_ALL} ===========================\n')
            t = f'Total number of entries for {Fore.CYAN}{user_banner_input[0].capitalize()} Banner{Style.RESET_ALL}: {len(wish_history[user_banner_input[0]]):,}'
            extra = (64 - len(t) + 10)//2  # +10 to account for the color change
            print(" " + ' ' * extra + t + '\n')
            page = 1
            print_history_page()

            while True:
                cmd = input('    History Command: ').strip().lower()
                if not cmd:
                    print(f'    Try {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL}\n')
                    continue

                if cmd[0] == 'n':
                    cmd = cmd.split()
                    if cmd[0] == 'n':
                        if len(cmd) == 1:
                            amount = 1
                        else:
                            if cmd[1].isnumeric():
                                amount = min(int(cmd[1]), num_of_pages - page)
                            else:
                                print(f'    {Fore.RED}"{cmd[1]}" is not a number{Style.RESET_ALL}\n')
                                continue
                        if page < num_of_pages:
                            print()

                            page += amount
                            print_history_page()

                        else:
                            print(f"    {Fore.LIGHTMAGENTA_EX}You're already at the last page{Style.RESET_ALL}\n")

                    elif cmd[0] == 'number':
                        print('    Input an actual number like 10 instead of typing "number"\n')

                    else:
                        print(f'    Try {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL}\n')

                elif cmd[0] == 'p':
                    cmd = cmd.split()
                    if cmd[0] == 'p':
                        if len(cmd) == 1:
                            amount = 1
                        else:
                            if cmd[1].isnumeric():
                                amount = min(int(cmd[1]), page - 1)
                            else:
                                print(f'    {Fore.RED}"{cmd[1]}" is not a number{Style.RESET_ALL}\n')
                                continue
                        if page > 1:
                            print()

                            page -= amount
                            print_history_page()

                        elif page == 1:
                            print(f"    {Fore.LIGHTMAGENTA_EX}You're already at the first page{Style.RESET_ALL}\n")

                        else:
                            print(f"    {Fore.LIGHTMAGENTA_EX}You can't go back even further{Style.RESET_ALL}\n")
                    else:
                        print(f'    Try {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL}\n')

                elif cmd in ('e', '0'):
                    print('    No longer viewing wish history!\n')
                    print('==================================================================\n')
                    break

                elif cmd.isnumeric():
                    page = min(int(cmd), num_of_pages)
                    print()
                    if page == 0:
                        print(" " + Style.RESET_ALL + '   ' + '-' * 58)
                        print(" " + Fore.YELLOW + '                       You found page 0')
                        print(" " + Style.RESET_ALL + '   ' + '-' * 58)
                        print(f"\n    (Page 0/{num_of_pages})\n")
                    else:
                        print_history_page()

                elif cmd in ['help', "'help'", '"help"']:
                    print(f'    {Fore.BLUE}numbers in [] are optional{Style.RESET_ALL}\n'
                          f'    {Fore.LIGHTMAGENTA_EX}n {Fore.BLUE}[number]{Style.RESET_ALL} = go forward a number of pages\n'
                          f'    {Fore.LIGHTMAGENTA_EX}p {Fore.BLUE}[number]{Style.RESET_ALL} = go back a number of pages\n'
                          f'    {Fore.LIGHTMAGENTA_EX}number{Style.RESET_ALL} = go to page\n'
                          f'    {Fore.LIGHTMAGENTA_EX}e{Style.RESET_ALL} = exit\n')

                else:
                    print(f'    Try {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL}\n')
        else:
            print(f' {Fore.MAGENTA}Wish history empty!{Style.RESET_ALL}\n')
        continue

    try:
        user_command = int(user_command)
    except ValueError:
        print(f' Try {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL}\n')
        continue

    if user_command <= 1000000000:
        print()
        verbose_threshold = 7 - (user_command <= 10000000) - (user_command <= 1000000) - (user_command <= 100000) - (user_command <= 10000)
        # pulls <= 10k = show every pull
        # 10k < pulls <= 100k = show 4* and 5*
        # 100k < pulls <= 1M = show only 5*
        # 1M < pulls = show progress (percentage) and stop showing "10 PULLS WITHOUT A 4 STAR" message
        # comparison to 10M is made just in case ill need it in the future

        if user_command > 1000000:  # if number bigger than 1 million
            print(f' Are you sure? Doing {user_command} pulls would take around {round((5+replit*4) * user_command / 1000000)} seconds.')
            # ask user if they're sure
            sure = input(f' Type {Fore.CYAN}CONFIRM{Style.RESET_ALL} if you want to proceed: ')
            if sure != "CONFIRM":  # if they're not sure
                print(' Aborting\n')  # abort this job
                continue  # and ask for next command
            else:
                print()  # otherwise add an extra space cuz pretty
        count += user_command
        pity_info[-1][0] += user_command
        if user_banner_input[0] != 'weapon':
            character_distribution[100] += user_command
        else:
            weapon_distribution[100] += user_command
        for i in range(user_command):
            try:
                res, p, w = make_pull(banner_of_choice, pity_info)
            except MemoryError:
                print(' The program ran out of memory dude what have you DONE')
                save_archive_to_file(constellations, refinements)
                save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                                  unique_four_weap_count, gacha_system)
                save_character_distribution_to_file()
                save_weapon_distribution_to_file()
                try:
                    saving_dict[banner_of_choice[0]]()
                    print(' backed up the history at least')
                except:
                    print(" couldn't even save the wish history")
                break
            if isinstance(res, Character):
                if res in constellations:
                    if constellations[res] < 6:
                        constellations[res] += 1
                else:
                    constellations[res] = 0
                    if res.rarity == 5:
                        unique_five_char_count += 1
            else:
                if res in refinements:
                    refinements[res] += 1
                else:
                    refinements[res] = 1
                    if res.rarity == 5:
                        unique_five_weap_count += 1
                    elif res.rarity == 4:
                        unique_four_weap_count += 1

            if res.rarity == 4:
                four_count += 1
                pity_info[-1][2] += 1
            elif res.rarity == 5:
                five_count += 1
                pity_info[-1][1] += 1

            if res.rarity >= verbose_threshold:
                print(" " + Style.RESET_ALL + f'{win_map[w]}{color_map[res.rarity]}{res.name}{f", {p} pity" if res.rarity >= 4 else ""}')
            if verbose_threshold >= 6 and i % 100000 == 0:
                print_progress_bar(i//100000, user_command//100000)
                # print(f'\r {i//100000}/{user_command//100000} done', end='')
            if user_banner_input[0] != 'standard':
                if verbose_threshold < 6 and pity_info[1] >= (10 - (user_banner_input[0] == 'weapon')):
                    print(" " + Fore.CYAN + f"{pity_info[1]} PULLS WITHOUT A 4-STAR!" + Style.RESET_ALL)
        if verbose_threshold >= 6:
            print(f"\r {Fore.LIGHTGREEN_EX}Wishing complete - 100%{Style.RESET_ALL}" + ' '*50)
        # print(wish_history)
        save_archive_to_file(constellations, refinements)
        save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                          unique_four_weap_count, gacha_system)
        save_character_distribution_to_file()
        save_weapon_distribution_to_file()
        print()
        if user_banner_input[0] == 'character':
            print(Style.RESET_ALL + f' {pity_info[0]} pity, {"guaranteed" if pity_info[2] else "50/50"}')
        elif user_banner_input[0] == 'chronicled':
            print(Style.RESET_ALL + f' {pity_info[0]} pity, {"guaranteed" if pity_info[2] else "50/50"}')
        elif user_banner_input[0] == 'weapon':
            epitomized = f"epitomized points: {pity_info[2]}"
            print(Style.RESET_ALL + f' {pity_info[0]} pity, {epitomized if pity_info[2] >= 2-(gacha_system == 'new') else "37.5% / 37.5% / 25%, "+epitomized if not pity_info[3] else "50/50, "+epitomized}')
        elif user_banner_input[0] == 'standard':
            recent, not_recent = ('character', 'weapon') if pity_info[0] < pity_info[1] else ('weapon', 'character')
            pulls_since_not_recent = f', {max(pity_info[0], pity_info[1])} {not_recent} pity' if pity_info[0] != pity_info[1] else ''
            print(Style.RESET_ALL + f' {min(pity_info[0], pity_info[1])} {recent} pity{pulls_since_not_recent}')
            if pity_info[0] >= 180 or pity_info[1] >= 180:
                print(
                    f' Next {Fore.YELLOW}5★ item{Style.RESET_ALL} is guaranteed to be a {"character" if pity_info[0] >= 180 else "weapon"}')
            if pity_info[2] >= 20 or pity_info[3] >= 20:
                print(
                    f' Next {Fore.MAGENTA}4★ item{Style.RESET_ALL} is guaranteed to be a {"character" if pity_info[2] >= 20 else "weapon"}')

        if not messaged and len(wish_history[banner_of_choice[0]]) > 2500000:
            messaged = True
            print(Fore.LIGHTRED_EX + '\n To save disk space and ensure acceptable simulator performance,\n'
                                     ' the size of the wish history has been limited to 2.5 million entries.\n'
                                     ' This does NOT limit the the distribution data size (e.g. character_distribution.txt)',
                  Style.RESET_ALL)
        wish_history[banner_of_choice[0]] = wish_history[banner_of_choice[0]][-2500000:]
        try:
            saving_dict[banner_of_choice[0]]()
        except:
            print(' Not enough storage to hold this wish history. Wish history not backed up')
    elif user_command < 0:
        print(' what are u doing bro')

    else:
        print(" I'm not letting you do that. Max 1 billion wishes at a time please")

    if wished_by_viz:
        print(f'\n{Fore.RED} Now please run the "viz" command again{Style.RESET_ALL}')

    print()

if __name__ == '__main__':
    print('\n==================================================================')
    print('\n Thank you for using Wish Simulator')
