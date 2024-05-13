import json
from random import choice, choices
from colorama import init, Fore, Style
from pathlib import Path
import sys
import importlib

print('\n============================ LOADING ===========================\n')
init()
Path(".\\banner_info").mkdir(parents=True, exist_ok=True)


def save_history_to_file(data):
    with open(r'.\banner_info\wish.txt', 'w') as f:
        f.write(json.dumps(data, separators=(',', ':')))


def save_character_distribution_to_file():
    with open(r'.\banner_info\character_distribution.txt', 'w') as f:
        f.write(json.dumps(character_distribution, separators=(',', ':')))


def save_weapon_distribution_to_file():
    with open(r'.\banner_info\weapon_distribution.txt', 'w') as f:
        f.write(json.dumps(weapon_distribution, separators=(',', ':')))


def save_info_to_file(pity, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count):
    with open(r'.\banner_info\info.txt', 'w') as f:
        f.write(json.dumps([pity, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count], separators=(',', ':')))


def save_banner_to_file():
    with open(r'.\banner_info\banner.txt', 'w') as f:
        f.write(json.dumps(user_banner_input, separators=(',', ':')))


def save_archive_to_file(cons, refs):

    numeric_indexes_c = [character.num for character in cons]
    numeric_indexes_w = [weapon.num for weapon in refs]
    new_dict_c = dict(zip(numeric_indexes_c, list(cons.values())))
    new_dict_w = dict(zip(numeric_indexes_w, list(refs.values())))
    with open(r'.\banner_info\archive.txt', 'w') as f:
        data = (new_dict_c, new_dict_w)
        f.write(json.dumps(data, separators=(',', ':')))

banner_types = ["character", "weapon", "standard", "chronicled"]


def load_history():
    try:
        with open('.\\banner_info\\wish.txt') as file:
            data = file.read()
        history = json.loads(data)
        for i in banner_types:
            for num in history[i]:
                if num not in number_to_item_dict:
                    raise ValueError

        return history

    except FileNotFoundError:
        with open('.\\banner_info\\wish.txt', 'w') as file:
            file.write('{"character":[],"weapon":[],"standard":[],"chronicled":[]}')
        return {"character": [], "weapon": [], "standard": [], "chronicled": []}


def load_info():
    try:
        with open('.\\banner_info\\info.txt') as file:
            data = file.read()
        pity_and_other_info = json.loads(data)
        return pity_and_other_info

    except FileNotFoundError:
        pities = {'character': [0, 0, False, False, [0, 0, 0]],
                  'weapon': [0, 0, 0, False, False, [0, 0, 0]],
                  'standard': [0, 0, 0, 0, [0, 0, 0]],
                  'chronicled': [0, 0, False, [0, 0, 0]]}
        with open('.\\banner_info\\info.txt', 'w') as file:
            info = [pities, 0, 0, 0, 0, 0, 0]
            file.write(json.dumps(info, separators=(',', ':')))
        return info


def load_banner():  # always returns a valid banner
    global user_banner_input
    try:  # if can read, read.
        with open('.\\banner_info\\banner.txt') as file:
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
        with open('.\\banner_info\\character_distribution.txt') as file:
            data = file.read()
        character_distribution = json.loads(data, object_hook=jsonKeys2int)

    except:
        character_distribution = {i: 0 for i in range(1, 91)}
        character_distribution[100] = 0
        save_character_distribution_to_file()

    try:
        with open('.\\banner_info\\weapon_distribution.txt') as file:
            data = file.read()
        weapon_distribution = json.loads(data, object_hook=jsonKeys2int)

    except:
        weapon_distribution = {i: 0 for i in range(1, 78)}
        weapon_distribution[100] = 0
        save_weapon_distribution_to_file()

    print(Fore.GREEN + 'Loaded distribution successfully!' + Style.RESET_ALL)


def load_archive():
    try:
        with open('.\\banner_info\\archive.txt') as file:
            data = file.read()
        archive = json.loads(data, object_hook=jsonKeys2int)

        indexes_c = [number_to_item_dict[i] for i in archive[0]]
        indexes_w = [number_to_item_dict[i] for i in archive[1]]
        new_dict_c = dict(zip(indexes_c, list(archive[0].values())))
        new_dict_w = dict(zip(indexes_w, list(archive[1].values())))

        return new_dict_c, new_dict_w

    except FileNotFoundError:
        with open('.\\banner_info\\archive.txt', 'w') as file:
            file.write("[{}, {}]")
        return {}, {}


def set_defaults():
    global wish_history, constellations, refinements, pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count

    wish_history = {"character": [], "weapon": [], "standard": [], "chronicled": []}
    save_history_to_file(wish_history)

    constellations, refinements = {}, {}
    save_archive_to_file(constellations, refinements)

    pities = {'character': [0, 0, False, False, [0, 0, 0]],
              # 5-star pity / 4-star pity / 5-star guarantee / 4-star guarantee
              'weapon': [0, 0, 0, False, False, [0, 0, 0]],
              # 5-star pity / 4-star pity / epitomized path / last 5 star was standard? / 4-star guarantee
              'standard': [0, 0, 0, 0, [0, 0, 0]],
              # wishes since last [5-star char / 5-star weapon / 4-star char / 4-star weapon]
              'chronicled': [0, 0, False, [0, 0, 0]]
              # 5-star pity / 4-star pity / 5-star guarantee
              }
              # last item is [total pull count, 5-star count, 4-star count]
    count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count = 0, 0, 0, 0, 0, 0
    save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                      unique_four_weap_count)
    print(Fore.GREEN + "Everything cleared!" + Style.RESET_ALL)


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
        print(Fore.RED + 'Banner mismatch detected, setting to default' + Style.RESET_ALL)
        user_banner_input = ['character', 'tao-3']
        save_new_banner_of_choice()
        return

    # left only ['character', 'weapon', 'chronicled']

    banner_id = user_banner_input[1]
    if banner_type == 'character':
        # ["character", "tao-4"]

        if banner_id not in character_banner_list:
            print(Fore.RED + 'Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return

    elif banner_type == 'weapon':
        # ["weapon", ["Staff of Homa - Aqua Simulacra", "Staff of Homa"]]

        if banner_id[0] not in weapon_banner_list:
            # ["weapon", ["something", "Staff of Homa"]]
            print(Fore.RED + 'Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return
        if banner_id[1] not in [s.name for s in weapon_banner_list[banner_id[0]][0][:2]]:
            # ["weapon", ["Staff of Homa - Aqua Simulacra", "Mistsplitter Reforged"]]
            print(Fore.RED + 'Banner mismatch detected, setting to default' + Style.RESET_ALL)
            print(banner_id[1])
            print(weapon_banner_list[banner_id[0]][0][:2])
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return

    else:  # ['chronicled', ['mondstadt-1', 'Jean']]
        if banner_id[0] not in chronicled_banner_list:
            # ['chronicled', ['mondstadt-8', 'Jean']]
            print(Fore.RED + 'Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return

        chron_banner = chronicled_banner_list[banner_id[0]]
        valids = ([i.name for i in chron_banner['characters']['5-stars']] +
                  [i.name for i in chron_banner['weapons']['5-stars']])
        if banner_id[1] not in valids:
            # ['chronicled', ['mondstadt-1', 'Furina']]
            print(Fore.RED + 'Banner mismatch detected, setting to default' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()
            return

    save_new_banner_of_choice()
    return


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


characters_dict = {
    "Amber": Character("Amber", "Mondstadt", "Pyro", "Bow", 1.0, 4, 1+12),
    "Barbara": Character("Barbara", "Mondstadt", "Hydro", "Catalyst", 1.0, 4, 2+12),
    "Beidou": Character("Beidou", "Liyue", "Electro", "Claymore", 1.0, 4, 3+12),
    "Bennett": Character("Bennett", "Mondstadt", "Pyro", "Sword", 1.0, 4, 4+12),
    "Chongyun": Character("Chongyun", "Liyue", "Cryo", "Claymore", 1.0, 4, 5+12),
    "Diluc": Character("Diluc", "Mondstadt", "Pyro", "Claymore", 1.0, 5, 6+12),
    "Fischl": Character("Fischl", "Mondstadt", "Electro", "Bow", 1.0, 4, 7+12),
    "Jean": Character("Jean", "Mondstadt", "Anemo", "Sword", 1.0, 5, 8+12),
    "Kaeya": Character("Kaeya", "Mondstadt", "Cryo", "Sword", 1.0, 4, 9+12),
    "Keqing": Character("Keqing", "Liyue", "Electro", "Sword", 1.0, 5, 10+12),
    "Klee": Character("Klee", "Mondstadt", "Pyro", "Catalyst", 1.0, 5, 11+12),
    "Lisa": Character("Lisa", "Mondstadt", "Electro", "Catalyst", 1.0, 4, 12+12),
    "Mona": Character("Mona", "Mondstadt", "Hydro", "Catalyst", 1.0, 5, 13+12),
    "Ningguang": Character("Ningguang", "Liyue", "Geo", "Catalyst", 1.0, 4, 14+12),
    "Noelle": Character("Noelle", "Mondstadt", "Geo", "Claymore", 1.0, 4, 15+12),
    "Qiqi": Character("Qiqi", "Liyue", "Cryo", "Sword", 1.0, 5, 16+12),
    "Razor": Character("Razor", "Mondstadt", "Electro", "Claymore", 1.0, 4, 17+12),
    "Sucrose": Character("Sucrose", "Mondstadt", "Anemo", "Catalyst", 1.0, 4, 18+12),
    "Venti": Character("Venti", "Mondstadt", "Anemo", "Bow", 1.0, 5, 19+12),
    "Xiangling": Character("Xiangling", "Liyue", "Pyro", "Polearm", 1.0, 4, 20+12),
    "Xingqiu": Character("Xingqiu", "Liyue", "Hydro", "Sword", 1.0, 4, 21+12),
    "Diona": Character("Diona", "Mondstadt", "Cryo", "Bow", 1.1, 4, 22+12),
    "Tartaglia": Character("Tartaglia", "Snezhnaya", "Hydro", "Bow", 1.1, 5, 23+12),
    "Xinyan": Character("Xinyan", "Liyue", "Pyro", "Claymore", 1.1, 4, 24+12),
    "Zhongli": Character("Zhongli", "Liyue", "Geo", "Polearm", 1.1, 5, 25+12),
    "Albedo": Character("Albedo", "Mondstadt", "Geo", "Sword", 1.2, 5, 26+12),
    "Ganyu": Character("Ganyu", "Liyue", "Cryo", "Bow", 1.2, 5, 27+12),
    "Hu Tao": Character("Hu Tao", "Liyue", "Pyro", "Polearm", 1.3, 5, 28+12),
    "Xiao": Character("Xiao", "Liyue", "Anemo", "Polearm", 1.3, 5, 29+12),
    "Rosaria": Character("Rosaria", "Mondstadt", "Cryo", "Polearm", 1.4, 4, 30+12),
    "Eula": Character("Eula", "Mondstadt", "Cryo", "Claymore", 1.5, 5, 31+12),
    "Yanfei": Character("Yanfei", "Liyue", "Pyro", "Catalyst", 1.5, 4, 32+12),
    "Kaedehara Kazuha": Character("Kazuha", "Inazuma", "Anemo", "Sword", 1.6, 5, 33+12),
    "Kamisato Ayaka": Character("Ayaka", "Inazuma", "Cryo", "Sword", 2.0, 5, 34+12),
    "Sayu": Character("Sayu", "Inazuma", "Anemo", "Claymore", 2.0, 4, 35+12),
    "Yoimiya": Character("Yoimiya", "Inazuma", "Pyro", "Bow", 2.0, 5, 36+12),
    # "Aloy": Character("Aloy", "None", "Cryo", "Bow", 2.1, 5, 37+12),
    "Kujou Sara": Character("Kujou Sara", "Inazuma", "Electro", "Bow", 2.1, 4, 38+12),
    "Raiden Shogun": Character("Raiden Shogun", "Inazuma", "Electro", "Polearm", 2.1, 5, 39+12),
    "Sangonomiya Kokomi": Character("Kokomi", "Inazuma", "Hydro", "Catalyst", 2.1, 5, 40+12),
    "Thoma": Character("Thoma", "Inazuma", "Pyro", "Polearm", 2.2, 4, 41+12),
    "Arataki Itto": Character("Itto", "Inazuma", "Geo", "Claymore", 2.3, 5, 42+12),
    "Gorou": Character("Gorou", "Inazuma", "Geo", "Bow", 2.3, 4, 43+12),
    "Shenhe": Character("Shenhe", "Liyue", "Cryo", "Polearm", 2.4, 5, 44+12),
    "Yun Jin": Character("Yun Jin", "Liyue", "Geo", "Polearm", 2.4, 4, 45+12),
    "Yae Miko": Character("Yae Miko", "Inazuma", "Electro", "Catalyst", 2.5, 5, 46+12),
    "Kamisato Ayato": Character("Ayato", "Inazuma", "Hydro", "Sword", 2.6, 5, 47+12),
    "Kuki Shinobu": Character("Kuki Shinobu", "Inazuma", "Electro", "Sword", 2.7, 4, 48+12),
    "Yelan": Character("Yelan", "Liyue", "Hydro", "Bow", 2.7, 5, 49+12),
    "Shikanoin Heizou": Character("Heizou", "Inazuma", "Anemo", "Catalyst", 2.8, 4, 50+12),
    "Collei": Character("Collei", "Sumeru", "Dendro", "Bow", 3.0, 4, 51+12),
    "Dori": Character("Dori", "Sumeru", "Electro", "Claymore", 3.0, 4, 52+12),
    "Tighnari": Character("Tighnari", "Sumeru", "Dendro", "Bow", 3.0, 5, 53+12),
    "Candace": Character("Candace", "Sumeru", "Hydro", "Polearm", 3.1, 4, 54+12),
    "Cyno": Character("Cyno", "Sumeru", "Electro", "Polearm", 3.1, 5, 55+12),
    "Nilou": Character("Nilou", "Sumeru", "Hydro", "Sword", 3.1, 5, 56+12),
    "Layla": Character("Layla", "Sumeru", "Cryo", "Sword", 3.2, 4, 57+12),
    "Nahida": Character("Nahida", "Sumeru", "Dendro", "Catalyst", 3.2, 5, 58+12),
    "Faruzan": Character("Faruzan", "Sumeru", "Anemo", "Bow", 3.3, 4, 59+12),
    "Wanderer": Character("Wanderer", "Sumeru", "Anemo", "Catalyst", 3.3, 5, 60+12),
    "Alhaitham": Character("Alhaitham", "Sumeru", "Dendro", "Sword", 3.4, 5, 61+12),
    "Yaoyao": Character("Yaoyao", "Liyue", "Dendro", "Polearm", 3.4, 4, 62+12),
    "Dehya": Character("Dehya", "Sumeru", "Pyro", "Claymore", 3.5, 5, 63+12),
    "Mika": Character("Mika", "Mondstadt", "Cryo", "Polearm", 3.5, 4, 64+12),
    "Baizhu": Character("Baizhu", "Liyue", "Dendro", "Catalyst", 3.6, 5, 65+12),
    "Kaveh": Character("Kaveh", "Sumeru", "Dendro", "Claymore", 3.6, 4, 66+12),
    "Kirara": Character("Kirara", "Inazuma", "Dendro", "Sword", 3.7, 4, 67+12),
    "Freminet": Character("Freminet", "Fontaine", "Cryo", "Claymore", 4.0, 4, 68+12),
    "Lynette": Character("Lynette", "Fontaine", "Anemo", "Sword", 4.0, 4, 69+12),
    "Lyney": Character("Lyney", "Fontaine", "Pyro", "Bow", 4.0, 5, 70+12),
    "Neuvillette": Character("Neuvillette", "Fontaine", "Hydro", "Catalyst", 4.1, 5, 71+12),
    "Wriothesley": Character("Wriothesley", "Fontaine", "Cryo", "Catalyst", 4.1, 5, 72+12),
    "Charlotte": Character("Charlotte", "Fontaine", "Cryo", "Catalyst", 4.2, 4, 73+12),
    "Furina": Character("Furina", "Fontaine", "Hydro", "Sword", 4.2, 5, 74+12),
    "Chevreuse": Character("Chevreuse", "Fontaine", "Pyro", "Polearm", 4.3, 4, 75+12),
    "Navia": Character("Navia", "Fontaine", "Geo", "Claymore", 4.3, 5, 76+12),
    "Gaming": Character("Gaming", "Liyue", "Pyro", "Claymore", 4.4, 4, 77+12),
    "Xianyun": Character("Xianyun", "Liyue", "Anemo", "Catalyst", 4.4, 5, 78+12),
    "Chiori": Character("Chiori", "Inazuma", "Geo", "Sword", 4.5, 5, 79+12),
    "Arlecchino": Character("Arlecchino", "Snezhnaya", "Pyro", "Polearm", 4.6, 5, 80+12),
    # "Sigewinne": Character("Sigewinne", "Fontaine", "Hydro", "Bow", 4.7, 5, 81+12),
    # "Clorinde": Character("Clorinde", "Fontaine", "Electro", "Sword", 4.7, 5, 82+12),
    # "Sethos": Character("Sethos", "idk", "idk", "idk", 4.7, 4, 83+12)
}

weapons_dict = {
    "A Thousand Floating Dreams": Weapon("A Thousand Floating Dreams", "Catalyst", 5, 300),
    "Akuoumaru": Weapon("Akuoumaru", "Claymore", 4, 301),
    "Alley Hunter": Weapon("Alley Hunter", "Bow", 4, 302),
    "Amos' Bow": Weapon("Amos' Bow", "Bow", 5, 303),
    "Aqua Simulacra": Weapon("Aqua Simulacra", "Bow", 5, 304),
    "Aquila Favonia": Weapon("Aquila Favonia", "Sword", 5, 305),

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

    "Rainslasher": Weapon("Rainslasher", "Claymore", 4, 810),
    "Range Gauge": Weapon("Range Gauge", "Bow", 3, 811),
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


amount_of_five_stars = sum([i.rarity == 5 for i in characters_dict.values()])
amount_of_four_stars = len(characters_dict) - amount_of_five_stars


# thank you chatgpt for helping me convert paimon moe to this
standard_5_star_characters = ["Jean", "Qiqi", "Mona", "Diluc", "Keqing", "Tighnari", "Dehya"]
standard_5_star_weapons = ["Primordial Jade Winged-Spear", "Skyward Blade", "Skyward Spine",
                           "Skyward Harp", "Skyward Pride", "Skyward Atlas", "Aquila Favonia",
                           "Wolf's Gravestone", "Amos' Bow", "Lost Prayer to the Sacred Winds"]
standard_4_star_characters = [
    "Charlotte", "Sayu", "Barbara", "Chongyun", "Collei", "Gaming", "Kuki Shinobu", "Freminet",
    "Razor", "Rosaria", "Diona", "Candace", "Shikanoin Heizou", "Kirara", "Chevreuse", "Xiangling",
    "Yaoyao", "Yanfei", "Gorou", "Xingqiu", "Kujou Sara", "Lynette", "Layla", "Bennett", "Beidou",
    "Dori", "Yun Jin", "Ningguang", "Sucrose", "Xinyan", "Noelle", "Thoma", "Fischl", "Kaveh", "Faruzan",
    "Mika"
]
standard_4_star_weapons = [
    "The Widsith", "Sacrificial Fragments", "Rust", "Sacrificial Sword", "Favonius Greatsword",
    "Rainslasher", "Dragon's Bane", "The Flute", "Favonius Codex", "Sacrificial Greatsword",
    "Favonius Warbow", "Favonius Lance", "Favonius Sword", "Lion's Roar", "Sacrificial Bow",
    "Eye of Perception", "The Stringless", "The Bell"
]
three_star_weapons = [
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


character_banner_list = {  # thank you @shilva on discord for typing this out BY HAND WHAT THE HELL DID U DO BRO
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
    "lyney-2": (["Lyney", "Freminet", "Lynette", "Xiangling"], 4.6)
}

weapon_banner_list = {
    "Aquila Favonia - Amos' Bow": (["Aquila Favonia", "Amos' Bow", "The Flute", "The Bell", "The Widsith", "The Stringless", "Favonius Lance"], 1.0),
    "Lost Prayer to the Sacred Winds - Wolf's Gravestone": (["Lost Prayer to the Sacred Winds", "Wolf's Gravestone", "Sacrificial Sword", "Sacrificial Bow", "Sacrificial Fragments", "Sacrificial Fragments", "Dragon's Bane"], 1.0),
    "Memory of Dust - Skyward Harp": (["Memory of Dust", "Skyward Harp",  "The Flute", "Rainslasher", "Eye of Perception", "Rust", "Favonius Lance"], 1.1),
    "Vortex Vanquisher - The Unforged": (["Vortex Vanquisher", "The Unforged",  "Lion's Roar", "The Bell", "Favonius Codex", "Favonius Warbow", "Dragon's Bane"], 1.1),
    "Summit Shaper - Skyward Atlas": (["Summit Shaper", "Skyward Atlas",  "Favonius Sword", "Favonius Greatsword", "Favonius Lance", "Sacrificial Fragments", "The Stringless"], 1.2),
    "Skyward Pride - Amos' Bow": (["Skyward Pride", "Amos' Bow",  "Sacrificial Sword", "The Bell", "Dragon's Bane", "Eye of Perception", "Favonius Warbow"], 1.2),
    "Primordial Jade Cutter - Primordial Jade Winged-Spear": (["Primordial Jade Cutter", "Primordial Jade Winged-Spear",  "The Flute", "Sacrificial Greatsword", "Rust", "Eye of Perception", "Favonius Lance"], 1.3),
    "Staff of Homa - Wolf's Gravestone": (["Staff of Homa", "Wolf's Gravestone",  "Lithic Blade", "Lithic Spear", "Lion's Roar", "Sacrificial Bow", "The Widsith"], 1.3),
    "Elegy for the End - Skyward Blade": (["Elegy for the End", "Skyward Blade",  "The Alley Flash", "Wine and Song", "Favonius Greatsword", "Favonius Warbow", "Dragon's Bane"], 1.4),
    "Skyward Harp - Lost Prayer to the Sacred Winds": (["Skyward Harp", "Lost Prayer to the Sacred Winds",  "Alley Hunter", "Favonius Sword", "Sacrificial Greatsword", "Favonius Codex", "Favonius Lance"], 1.4),
    "Summit Shaper - Memory of Dust": (["Summit Shaper", "Memory of Dust",  "Lithic Blade", "Lithic Spear", "The Flute", "Eye of Perception", "Sacrificial Bow"], 1.5),
    "Song of Broken Pines - Aquila Favonia": (["Song of Broken Pines", "Aquila Favonia",  "Sacrificial Sword", "Rainslasher", "Dragon's Bane", "Sacrificial Fragments", "Rust"], 1.5),
    "Skyward Pride - Lost Prayer to the Sacred Winds": (["Skyward Pride", "Lost Prayer to the Sacred Winds",  "Mitternachts Waltz", "Lion's Roar", "The Bell", "Favonius Lance", "The Widsith"], 1.6),
    "Freedom-Sworn - Skyward Atlas": (["Freedom-Sworn", "Skyward Atlas",  "The Alley Flash", "Wine and Song", "Alley Hunter", "Dragon's Bane", "Favonius Greatsword"], 1.6),
    "Mistsplitter Reforged - Skyward Spine": (["Mistsplitter Reforged", "Skyward Spine",  "Sacrificial Greatsword", "Favonius Lance", "Favonius Codex", "Favonius Sword", "The Stringless"], 2.0),
    "Thundering Pulse - Skyward Blade": (["Thundering Pulse", "Skyward Blade",  "Sacrificial Sword", "Rainslasher", "Dragon's Bane", "Sacrificial Fragments", "Favonius Warbow"], 2.0),
    "Engulfing Lightning - The Unforged": (["Engulfing Lightning", "The Unforged",  "Lion's Roar", "The Bell", "Favonius Lance", "The Widsith", "Sacrificial Bow"], 2.1),
    "Everlasting Moonglow - Primordial Jade Cutter": (["Everlasting Moonglow", "Primordial Jade Cutter",  "The Flute", "Favonius Greatsword", "Dragon's Bane", "Favonius Codex", "The Stringless"], 2.1),
    "Polar Star - Memory of Dust": (["Polar Star", "Memory of Dust",  "Akuoumaru", "Favonius Sword", "Favonius Lance", "Eye of Perception", "Rust"], 2.2),
    "Staff of Homa - Elegy for the End": (["Staff of Homa", "Elegy for the End",  "Wavebreaker's Fin", "Mouun's Moon", "Sacrificial Sword", "Rainslasher", "The Widsith"], 2.2),
    "Freedom-Sworn - Song of Broken Pines": (["Freedom-Sworn", "Song of Broken Pines",  "Wine and Song", "Alley Hunter", "Lion's Roar", "Sacrificial Greatsword", "Dragon's Bane"], 2.3),
    "Redhorn Stonethresher - Skyward Harp": (["Redhorn Stonethresher", "Skyward Harp",  "The Alley Flash", "Mitternachts Waltz", "The Bell", "Favonius Lance", "Sacrificial Fragments"], 2.3),
    "Calamity Queller - Primordial Jade Winged-Spear": (["Calamity Queller", "Primordial Jade Winged-Spear",  "Lithic Spear", "The Flute", "Favonius Greatsword", "The Widsith", "Favonius Warbow"], 2.4),
    "Vortex Vanquisher - Amos' Bow": (["Vortex Vanquisher", "Amos' Bow",  "Lithic Blade", "Favonius Sword", "Dragon's Bane", "Favonius Codex", "Sacrificial Bow"], 2.4),
    "Kagura's Verity - Primordial Jade Cutter": (["Kagura's Verity", "Primordial Jade Cutter",  "Wavebreaker's Fin", "Sacrificial Sword", "Rainslasher", "Eye of Perception", "The Stringless"], 2.5),
    "Engulfing Lightning - Everlasting Moonglow": (["Engulfing Lightning", "Everlasting Moonglow",  "Akuoumaru", "Mouun's Moon", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments"], 2.5),
    "Haran Geppaku Futsu - Elegy for the End": (["Haran Geppaku Futsu", "Elegy for the End",  "The Flute", "Sacrificial Greatsword", "Dragon's Bane", "The Widsith", "Rust"], 2.6),
    "Mistsplitter Reforged - The Unforged": (["Mistsplitter Reforged", "The Unforged",  "Favonius Sword", "The Bell", "Favonius Lance", "Favonius Codex", "Favonius Warbow"], 2.6),
    "Aqua Simulacra - Primordial Jade Winged-Spear": (["Aqua Simulacra", "Primordial Jade Winged-Spear",  "Lithic Spear", "Eye of Perception", "Favonius Greatsword", "Sacrificial Bow", "Sacrificial Sword"], 2.7),
    "Redhorn Stonethresher - Memory of Dust": (["Redhorn Stonethresher", "Memory of Dust",  "Lithic Blade", "Lion's Roar", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"], 2.7),
    "Freedom-Sworn - Lost Prayer to the Sacred Winds": (["Freedom-Sworn", "Lost Prayer to the Sacred Winds",  "The Alley Flash", "Mitternachts Waltz", "Rainslasher", "Favonius Lance", "The Widsith"], 2.8),
    "Thundering Pulse - Summit Shaper": (["Thundering Pulse", "Summit Shaper",  "Wine and Song", "Alley Hunter", "The Flute", "Sacrificial Greatsword", "Dragon's Bane"], 2.8),
    "Hunter's Path - Vortex Vanquisher": (["Hunter's Path", "Vortex Vanquisher",  "Favonius Sword", "The Bell", "Favonius Lance", "Favonius Codex", "The Stringless"], 3.0),
    "Everlasting Moonglow - Amos' Bow": (["Everlasting Moonglow", "Amos' Bow",  "Sacrificial Sword", "Favonius Greatsword", "Dragon's Bane", "Eye of Perception", "Rust"], 3.0),
    "Staff of the Scarlet Sands - Elegy for the End": (["Staff of the Scarlet Sands", "Elegy for the End",  "Makhaira Aquamarine", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments", "Favonius Warbow"], 3.1),
    "Key of Khaj-Nisut - Primordial Jade Cutter": (["Key of Khaj-Nisut", "Primordial Jade Cutter",  "Xiphos' Moonlight", "Wandering Evenstar", "Rainslasher", "Dragon's Bane", "Sacrificial Bow"], 3.1),
    "A Thousand Floating Dreams - Thundering Pulse": (["A Thousand Floating Dreams", "Thundering Pulse",  "The Flute", "Sacrificial Greatsword", "Favonius Lance", "The Widsith", "Rust"], 3.2),
    "Kagura's Verity - Polar Star": (["Kagura's Verity", "Polar Star",  "Favonius Sword", "The Bell", "Dragon's Bane", "Favonius Codex", "The Stringless"], 3.2),
    "Tulaytullah's Remembrance - Redhorn Stonethresher": (["Tulaytullah's Remembrance", "Redhorn Stonethresher",  "Wavebreaker's Fin", "Sacrificial Sword", "Favonius Greatsword", "Eye of Perception", "Favonius Warbow"], 3.3),
    "Engulfing Lightning - Haran Geppaku Futsu": (["Engulfing Lightning", "Haran Geppaku Futsu",  "Akuoumaru", "Mouun's Moon", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments"], 3.3),
    "Light of Foliar Incision - Primordial Jade Winged-Spear": (["Light of Foliar Incision", "Primordial Jade Winged-Spear",  "Lithic Spear", "The Flute", "Rainslasher", "The Widsith", "Sacrificial Bow"], 3.4),
    "Staff of Homa - Aqua Simulacra": (["Staff of Homa", "Aqua Simulacra",  "Lithic Blade", "Favonius Sword", "Dragon's Bane", "Favonius Codex", "Rust"], 3.4),
    "Beacon of the Reed Sea - Staff of the Scarlet Sands": (["Beacon of the Reed Sea", "Staff of the Scarlet Sands",  "The Alley Flash", "Alley Hunter", "Sacrificial Greatsword", "Dragon's Bane", "Eye of Perception"], 3.5),
    "Calamity Queller - Mistsplitter Reforged": (["Calamity Queller", "Mistsplitter Reforged",  "Wine and Song", "Sacrificial Sword", "The Bell", "Favonius Lance", "Favonius Warbow"], 3.5),
    "A Thousand Floating Dreams - Key of Khaj-Nisut": (["A Thousand Floating Dreams", "Key of Khaj-Nisut",  "Xiphos' Moonlight", "Favonius Greatsword", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"], 3.6),
    "Jadefall's Splendor - Amos' Bow": (["Jadefall's Splendor", "Amos' Bow",  "Makhaira Aquamarine", "Wandering Evenstar", "Lion's Roar", "Favonius Lance", "Sacrificial Bow"], 3.6),
    "Thundering Pulse - Kagura's Verity": (["Thundering Pulse", "Kagura's Verity",  "Akuoumaru", "The Flute", "Dragon's Bane", "The Widsith", "Rust"], 3.7),
    "Light of Foliar Incision - Freedom-Sworn": (["Light of Foliar Incision", "Freedom-Sworn",  "Favonius Codex", "Favonius Sword", "Mouun's Moon", "Sacrificial Greatsword", "Wavebreaker's Fin"], 3.7),
    "Song of Broken Pines - Lost Prayer to the Sacred Winds": (["Song of Broken Pines", "Lost Prayer to the Sacred Winds",  "The Alley Flash", "Alley Hunter", "Rainslasher", "Favonius Lance", "Eye of Perception"], 3.8),
    "Everlasting Moonglow - Tulaytullah's Remembrance": (["Everlasting Moonglow", "Tulaytullah's Remembrance",  "Wine and Song", "Lion's Roar", "The Bell", "Dragon's Bane", "Favonius Warbow"], 3.8),
    "The First Great Magic - Aqua Simulacra": (["The First Great Magic", "Aqua Simulacra",  "Sacrificial Sword", "Favonius Greatsword", "Favonius Lance", "Sacrificial Fragments", "Sacrificial Bow"], 4.0),
    "Vortex Vanquisher - Polar Star": (["Vortex Vanquisher", "Polar Star",  "The Flute", "Sacrificial Greatsword", "Dragon's Bane", "The Widsith", "Rust"], 4.0),
    "Tome of the Eternal Flow - Staff of Homa": (["Tome of the Eternal Flow", "Staff of Homa",  "The Dockhand's Assistant", "Portable Power Saw", "Mitternachts Waltz", "Favonius Lance", "Favonius Codex"], 4.1),
    "Cashflow Supervision - Elegy for the End": (["Cashflow Supervision", "Elegy for the End",  "Prospector's Drill", "Range Gauge", "Favonius Sword", "Rainslasher", "Eye of Perception"], 4.1),
    "Splendor of Tranquil Waters - Jadefall's Splendor": (["Splendor of Tranquil Waters", "Jadefall's Splendor",  "Sacrificial Sword", "The Bell", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"], 4.2),
    "Staff of the Scarlet Sands - Haran Geppaku Futsu": (["Staff of the Scarlet Sands", "Haran Geppaku Futsu",  "Lion's Roar", "Favonius Greatsword", "Favonius Lance", "The Widsith", "Favonius Warbow"], 4.2),
    "Verdict - Mistsplitter Reforged": (["Verdict", "Mistsplitter Reforged",  "Akuoumaru", "Mouun's Moon", "The Flute", "Dragon's Bane", "Favonius Codex"], 4.3),
    "Engulfing Lightning - Thundering Pulse": (["Engulfing Lightning", "Thundering Pulse",  "Wavebreaker's Fin", "Favonius Sword", "Rainslasher", "Eye of Perception", "Rust"], 4.3),
    "Crane's Echoing Call - A Thousand Floating Dreams": (["Crane's Echoing Call", "A Thousand Floating Dreams",  "Lithic Spear", "Sacrificial Sword", "Sacrificial Greatsword", "Sacrificial Fragments", "Sacrificial Bow"], 4.4),
    "Kagura's Verity - Primordial Jade Winged-Spear": (["Kagura's Verity", "Primordial Jade Winged-Spear",  "Lithic Blade", "Lion's Roar", "Favonius Lance", "The Widsith", "The Stringless"], 4.4),
    "Uraku Misugiri - Redhorn Stonethresher": (["Uraku Misugiri", "Redhorn Stonethresher",  "The Alley Flash", "Alley Hunter", "The Bell", "Dragon's Bane", "Favonius Codex"], 4.5),
    "Tome of the Eternal Flow - Freedom-Sworn": (["Tome of the Eternal Flow", "Freedom-Sworn",  "Wine and Song", "Mitternachts Waltz", "The Flute", "Favonius Greatsword", "Favonius Lance"], 4.5),
    "Crimson Moon's Semblance - The First Great Magic": (["Crimson Moon's Semblance", "The First Great Magic",  "The Dockhand's Assistant", "Portable Power Saw", "Dragon's Bane", "Eye of Perception", "Favonius Warbow"], 4.6)
}


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
                                                  "Favonius Codex", "Favonius Greatsword",  "Favonius Lance",
                                                  "Favonius Sword", "Favonius Warbow", "Lion's Roar",
                                                  "Mitternachts Waltz", "Rainslasher", "Rust", "Sacrificial Bow",
                                                  "Sacrificial Fragments", "Sacrificial Greatsword",
                                                  "Sacrificial Sword",  "The Alley Flash", "The Bell", "The Flute",
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


# replace strings with objects in lists of standard characters
for chars in (standard_5_star_characters, standard_4_star_characters):
    for i in range(len(chars)):
        chars[i] = characters_dict[chars[i]]

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

    elif user_banner_input[0] == 'chronicled':  # ['chronicled', ['mondstadt-1', 'Jean']]
        t = 'characters' if user_banner_input[1][1] in characters_dict else 'weapons'

        banner_of_choice = (
            user_banner_input[0],
            chronicled_banner_list[user_banner_input[1][0]],
            characters_dict[user_banner_input[1][1]] if t == 'characters' else weapons_dict[user_banner_input[1][1]])

        legal_standard_four_stars = (banner_of_choice[1]['characters']['4-stars'],   # 4-star characters
                                     banner_of_choice[1]['weapons']['4-stars'])      # 4-star weapons

        legal_standard_five_stars = [i for i in banner_of_choice[1][t]['5-stars']    # every item that's a 5-star of the same type as the chosen 5-star
                                     if i.name != user_banner_input[1][1]]           # that isn't the chosen item

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


def print_pity(counter, p, c5, c4):
    print("\n" + "="*23 + " PITY INFORMATION " + "="*23)
    print(f'{counter} pull{"s" if counter != 1 else ""} done on all banners combined')
    print(f'Out of them {Fore.YELLOW}{c5} five-star{"s" if c5 != 1 else ""}{Style.RESET_ALL} and {Fore.MAGENTA}{c4} four-star{"s" if c4 != 1 else ""}{Style.RESET_ALL}'
           '\n')
    print(f'{p[-1][0]} pull{"s" if p[-1][0] != 1 else ""} done on the {user_banner_input[0]} banner')
    print(f'Out of them {Fore.YELLOW}{p[-1][1]} five-star{"s" if c5 != 1 else ""}{Style.RESET_ALL} and {Fore.MAGENTA}{p[-1][2]} four-star{"s" if c4 != 1 else ""}{Style.RESET_ALL}')
    if p[0] < 10 and p[1] < 10:
        insert1, insert2 = '', ''
    else:
        insert1 = ' ' * (p[0] < 10)
        insert2 = ' ' * (p[1] < 10)
    if user_banner_input[0] == 'character':
        fifty = "you're on a 50/50"  # python 3.10 breaks if I just put this into the f-string
        print(f'{Fore.YELLOW}5★{Style.RESET_ALL} pity = {p[0]},{insert1} {fifty if not p[2] else "next is guaranteed to be featured"}')
        print(f'{Fore.MAGENTA}4★{Style.RESET_ALL} pity = {p[1]},{insert2} {fifty if not p[3] else "next is guaranteed to be featured"}')
    elif user_banner_input[0] == 'chronicled':
        fifty = "you're on a 50/50"  # python 3.10 breaks if I just put this into the f-string
        print(f'{Fore.YELLOW}5★{Style.RESET_ALL} pity = {p[0]}, {fifty if not p[2] else "next is guaranteed to be featured"}')
    elif user_banner_input[0] == 'weapon':
        was_standard = 'was standard' if p[3] else 'was not standard'
        epitomized = f"epitomized points: {p[2]}, last {was_standard}"
        seventyfive = "you're on a 75/25"
        print(f'{Fore.YELLOW}5★{Style.RESET_ALL} pity = {p[0]},{insert1} {epitomized if p[2] < 2 else "next is guaranteed to be featured"}')
        print(f'{Fore.MAGENTA}4★{Style.RESET_ALL} pity = {p[1]},{insert2} {seventyfive if not p[4] else "next is guaranteed to be featured"}')
    elif user_banner_input[0] == 'standard':
        print(f'{Fore.YELLOW}5★ character{Style.RESET_ALL} pity = {p[0]}\n'
              f'{Fore.YELLOW}5★ weapon{Style.RESET_ALL}    pity = {p[1]}')
        print(f'{Fore.MAGENTA}4★ character{Style.RESET_ALL} pity = {p[2]}\n'
              f'{Fore.MAGENTA}4★ weapon{Style.RESET_ALL}    pity = {p[3]}')
        if p[0] >= 180 or p[1] >= 180:
            print(f'Next {Fore.YELLOW}5★ item{Style.RESET_ALL} is guaranteed to be a {"character" if p[0] >= 180 else "weapon"}')
        if p[2] >= 20 or p[3] >= 20:
            print(f'Next {Fore.YELLOW}4★ item{Style.RESET_ALL} is guaranteed to be a {"character" if p[2] >= 20 else "weapon"}')

    # print('\n================================================================')

def print_character_archive():
    global sorted_constellations, a
    sorted_constellations = sorted(list(constellations.items()),
                                   key=lambda x: (-x[0].rarity, x[0] not in banner_of_choice[1], -x[1]))
    if sorted_constellations:
        last_rarity = 0
        print("\n" + "="*23 + " CHARACTER ARCHIVE " + "="*22)
        print(f"{len(constellations)}/{len(characters_dict)} characters ({unique_five_char_count}/{amount_of_five_stars} {Fore.YELLOW}5★{Style.RESET_ALL}, {len(constellations) - unique_five_char_count}/{amount_of_four_stars} {Fore.MAGENTA}4★{Style.RESET_ALL})")
        # print()
        for a in sorted_constellations:
            if a[0].rarity != last_rarity:
                # print(Style.RESET_ALL + "-" * 28 + f' {a[0].rarity} STARS ' + "-" * 27 + color_map[a[0].rarity])
                print(color_map[a[0].rarity], end='')
                last_rarity = a[0].rarity
            print(f'c{a[1]} {a[0].name}')
        print(Style.RESET_ALL)
        return True
    return False


def print_weapon_archive():
    global sorted_refinements, a
    sorted_refinements = sorted(list(refinements.items()),
                                key=lambda x: (-x[0].rarity, x[0] not in banner_of_choice[1], -x[1]))
    if sorted_refinements:
        last_rarity = 0
        print("\n" + "="*24 + " WEAPON ARCHIVE " + "="*24)
        print(f"{len(refinements)}/{len(weapons_dict)} gacha weapons ({unique_five_weap_count}/{amount_of_five_star_weapons} {Fore.YELLOW}5★{Style.RESET_ALL}, {unique_four_weap_count}/{amount_of_four_star_weapons} {Fore.MAGENTA}4★{Style.RESET_ALL}, {len(refinements) - unique_five_weap_count - unique_four_weap_count}/{amount_of_three_star_weapons} {Fore.BLUE}3★{Style.RESET_ALL})")
        # print()
        for a in sorted_refinements:
            if a[0].rarity != last_rarity:
                # print(Style.RESET_ALL + "-" * 28 + f' {a[0].rarity} STARS ' + "-" * 27 + color_map[a[0].rarity])
                print(color_map[a[0].rarity], end='')
                last_rarity = a[0].rarity
            print(f'r{a[1]} {a[0].name}')
        print(Style.RESET_ALL)
        return True
    return False


def show_full_inventory():
    print()
    if not print_character_archive():
        if not print_weapon_archive():
            print('Character/weapon archive empty!')
    else:
        print_weapon_archive()
    print()


def print_history_page():  # no idea how this works anymore
    global print_from, print_to, cc, number, color_map
    print_from = -((page - 1) * 25) - 1
    print_to = -(min(page * 25, len(wish_history[banner_of_choice[0]]))) - 1
    cc = -print_from - 1
    print(Style.RESET_ALL + '   ' + '-' * 58)
    for number in wish_history[banner_of_choice[0]][print_from:print_to:-1]:
        cc += 1
        print(color_map[number_to_item_dict[number].rarity] + f'   {cc}.{" " if len(str(cc)) < len(str(-print_to - 1)) else ""}',
              number_to_item_dict[number].name)
    print(Style.RESET_ALL + '   ' + '-' * 58)
    print(f'\n   (Page {page}/{num_of_pages})\n')



try:
    pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count = load_info()
    print(Fore.GREEN + 'Loaded additional information successfully!' + Style.RESET_ALL)
    info_ok = True
except:
    print(Fore.RED + 'Something off with info file. Clearing everything...' + Style.RESET_ALL)
    info_ok = False


if info_ok:
    try:  # if i extract this into a method pycharm stops seeing all the variables assigned
        wish_history = load_history()
        print(Fore.GREEN + 'Loaded wish history successfully!' + Style.RESET_ALL)
        history_ok = True
    except:
        print(Fore.RED + 'Something off with wish history file. Clearing everything...' + Style.RESET_ALL)
        history_ok = False


if info_ok and history_ok:
    try:
        constellations, refinements = load_archive()
        print(Fore.GREEN + 'Loaded archive successfully!' + Style.RESET_ALL)
        archive_ok = True
    except:
        print(Fore.RED + 'Something off with archive file. Clearing everything...' + Style.RESET_ALL)
        archive_ok = False


if not (info_ok and history_ok and archive_ok):
    set_defaults()


# try:
load_banner()
print(Fore.GREEN + 'Loaded banner information successfully!' + Style.RESET_ALL)
# except:
#     print(Fore.RED + 'Something off with banner file. Setting to default...' + Style.RESET_ALL)
#     user_banner_input = ['character', 'tao-3']
#     save_new_banner_of_choice()


load_distribution()


# print([c in standard_characters for c in character_banner_list["venti-1"]])


def make_pull(banner_info, pity):
    five_star_chance, four_star_chance = get_chances(banner_info[0], pity)
    rarity = 5 if choices((True, False), (five_star_chance, 100 - five_star_chance))[0] \
        else 4 if choices((True, False), (four_star_chance, 100 - four_star_chance))[0] else 3

    if banner_info[0] == 'character':  # banner_info = ['character', banner dictionary, banner version]
        featured_five_star = banner_info[1][0]
        featured_four_stars = banner_info[1][1:]
        if rarity == 5:
            character_distribution[pity[0] + 1] += 1
            # print(f'{Style.RESET_ALL}{five_star_chance}')
            if pity[2]:  # if guaranteed
                result = [featured_five_star, pity[0] + 1]  # give featured 5-star character
                pity[2] = False  # change guaranteed to false
                result.append(2)  # log that guarantee took place
            else:  # if not guaranteed
                # choose if win 50/50
                result = [choice((featured_five_star, choice(legal_standard_five_stars))), pity[0] + 1]
                if result[0] != featured_five_star:  # if didnt win 50/50
                    pity[2] = True  # set guarantee to true
                result.append(int(result[0] == featured_five_star))  # log if you won or not
            pity[0] = 0
            pity[1] += 1

        elif rarity == 4:
            # print(f'{Style.RESET_ALL}{four_star_chance}')
            if pity[3]:  # if guaranteed
                result = [choice(featured_four_stars), pity[1] + 1]  # give a featured 4-star character
                pity[3] = False  # change guaranteed to false
                result.append(2)  # log that guarantee took place
            else:  # if not guaranteed
                # choose what to give from different pools
                result = [choice(choices((featured_four_stars, legal_standard_four_stars, standard_4_star_weapons), [50, 25, 25])[0]), pity[1] + 1]
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
            # print(f'{Style.RESET_ALL}{five_star_chance}')
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
            if pity[2] < 2:  # 'weapon': [0, 0, 0, False, False] - 5-star pity, 4-star pity, epitomized path, last 5-star was standard, last 4-star was standard
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
            if pity[0] >= 180:
                result = [choice(standard_5_star_characters), f'{pity[1] + 1} ({pity[0] + 1})', 2]
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
                result = [choice(choice((standard_5_star_characters, standard_5_star_weapons)))]
                got = int(result[0] in standard_5_star_weapons)  # 0 if character, 1 if weapon
                result.extend([pity[got] + 1, 7])
                pity[got] = 0
                pity[1 - got] += 1
                pity[2] += 1
                pity[3] += 1

        elif rarity == 4:
            if pity[2] >= 20:
                result = [choice(standard_4_star_characters), f'{pity[3] + 1} ({pity[2] + 1})', 2]
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
                result = [choice(choice((standard_4_star_characters, standard_4_star_weapons)))]
                got = int(result[0] in standard_4_star_weapons) + 2  # 2 if character, 3 if weapon
                result.extend([pity[got] + 1, 7])
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
color_map = {3: Fore.BLUE, 4: Fore.MAGENTA, 5: Fore.YELLOW}
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

print('\n================================================================\n')
print('Type "help" for the list of commands\n')


def print_banner(t):
    if t == 'Chosen':
        t2 = 'B'
    elif t == 'Current':
        t2 = 'Current b'
    elif t == 'New':
        t2 = 'New b'
    else:
        t2 = '???'
    print(f'\n{t} banner type: {Fore.CYAN}{user_banner_input[0]}{Style.RESET_ALL}')
    if banner_of_choice[0] == 'character':
        print(f'{t2}anner ID: {user_banner_input[1]}')
        for i in banner_of_choice[1]:
            print(f'{color_map[i.rarity]}{i.rarity}★ {i.name}{Style.RESET_ALL}')
    elif banner_of_choice[0] == 'weapon':
        print(f'{t2}anner ID: {user_banner_input[1][0]}\nEpitomized Path: {color_map[5]}{user_banner_input[1][1]}{Style.RESET_ALL}\n')
        for i in banner_of_choice[1]:
            print(f'{color_map[i.rarity]}{i.rarity}★ {i.name}{Style.RESET_ALL}')
    elif banner_of_choice[0] == 'chronicled':
        print(f'{t2}anner ID: {user_banner_input[1][0]}\nChronicled Path: {color_map[5]}{user_banner_input[1][1]}{Style.RESET_ALL}')

while True:
    user_command = input('Command: ').lower().strip()
    if not user_command:
        print('Try "help"\n')
        continue

    if user_command in ('0', 'exit'):
        print('Exiting Wish Simulator...')
        print('\n================================================================')
        break

    if user_command in ['help', "'help'", '"help"']:
        print('\n' +
              '=' * 27 + " CONTROLS " + '=' * 27 + '\n'
              '\n'
              f'{Fore.BLUE}numbers in [] are optional{Style.RESET_ALL}\n\n'
              f'{Fore.LIGHTCYAN_EX}number{Style.RESET_ALL} = do a number of pulls\n'
              f'{Fore.LIGHTCYAN_EX}banner{Style.RESET_ALL} = view current banner\n'
              f'{Fore.LIGHTCYAN_EX}change{Style.RESET_ALL} = choose a different banner\n\n'
              f'{Fore.LIGHTCYAN_EX}pity{Style.RESET_ALL} = view pity related information\n'
              f'{Fore.LIGHTCYAN_EX}inv{Style.RESET_ALL} = view character/weapon archive\n'
              f'{Fore.LIGHTCYAN_EX}h{Style.RESET_ALL} = view wish history, commands to interact with it:\n'
              f'\t{Fore.LIGHTMAGENTA_EX}n [number]{Style.RESET_ALL} = go forward a number of pages,\n'
              f'\t{Fore.LIGHTMAGENTA_EX}p [number]{Style.RESET_ALL} = go back a number of pages,\n'
              f'\t{Fore.LIGHTMAGENTA_EX}number{Style.RESET_ALL} = go to page,\n'
              f'\t{Fore.LIGHTMAGENTA_EX}e{Style.RESET_ALL} = exit\n\n'
              f'{Fore.LIGHTCYAN_EX}dist{Style.RESET_ALL} = view disribution of 5-star items per pity\n'
              f'{Fore.LIGHTCYAN_EX}viz{Style.RESET_ALL} = plot a "Distribution of 5★ items per pity" graph\n\n'
              f'{Fore.LIGHTCYAN_EX}clear{Style.RESET_ALL} = clear wish history, pity, archive\n'
              f'{Fore.LIGHTCYAN_EX}load{Style.RESET_ALL} = load updates made to files located in ./banner_info.\n'
              f'{Fore.RED}It is not encouraged to introduce changes to the files yourself\n'
                        f'as they work together in tandem and by changing a file, chaos is\n'
                        f'introduced which may or may not cause unpredictable behavior!{Style.RESET_ALL}\n'
              f'\n'
              f'{Fore.LIGHTCYAN_EX}0{Style.RESET_ALL} = exit Wish Simulator\n'
              f'\n' +
              '=' * 64 +
              '\n')
        continue

    if user_command == 'number':
        print('real funny, input an actual number tho\n')
        continue

    if user_command == 'banner':
        print_banner('Chosen')
        print()
        continue
    
    if user_command == 'change':
        if user_banner_input[0] == 'weapon' and pity_info[2]:
            print(f'\n{Fore.RED}NOTE: YOUR EPITOMIZED PATH WILL RESET IF YOU CHANGE THE BANNER\n'
                  f'(You own {pity_info[2]} Epitomized Point{"s" if pity_info[2] != 1 else ""}){Style.RESET_ALL}')
        elif user_banner_input[0] == 'chronicled' and pity_info[2]:
            print(f'\n{Fore.RED}NOTE: YOUR CHRONICLED PATH WILL RESET IF YOU CHANGE THE BANNER\n'
                  f'(You own 1 Chronicled Point){Style.RESET_ALL}')
        print_banner('Current')
        print()
        m = {"1": "character", "2": "weapon", "3": "chronicled", "4": "standard"}
        print("Choose the banner type:")
        print("0 = exit")
        for i in m.items():
            print(f"{i[0]} = {i[1]}")
        print("(note: standard banner is not supported yet)\n")
        while True:
            new1 = input('Your pick: ').strip().lower()
            if new1 in ('0', 'exit'):
                break
            if new1 in m or new1 in m.values():
                break
            else:
                print('Please input either the number or the name of the banner type of choice\n')
        if new1 in ('0', 'exit'):
            print('Ok, not changing banner anymore.\n')
            continue
        if new1 in m:
            new1 = m[new1]
        print(f'{new1.capitalize()} banner selected.')


        if new1 == 'standard':
            user_banner_input = [new1]

        else:
            print('Choose the banner now!\n'
                  'List of available banners:\n')

            if new1 == 'character':
                print(', '.join(i for i in character_banner_list))
                print('\n(Type 0 to exit)\n')

                while True:
                    new2 = input('Choose one: ').strip().lower()
                    if new2 in ('0', 'exit'):
                        break
                    if new2 not in character_banner_list.keys():
                        print("That's not a banner that's available! Try again\n")
                    else:
                        print(f"Ok, {new2} selected")
                        break

                if new2 in ('0', 'exit'):
                    print('Ok, not changing banner anymore.\n')
                    continue
                user_banner_input = [new1, new2]

            elif new1 == 'chronicled':
                print(', '.join(i for i in chronicled_banner_list))
                print('\n(Type 0 to exit)\n')

                while True:
                    new2 = input('Choose one: ').strip().lower()
                    if new2 in ('0', 'exit'):
                        break
                    if new2 not in chronicled_banner_list.keys():
                        print("That's not a banner that's available! Try again\n")
                    else:
                        print(f"Ok, {new2} selected")
                        break

                if new2 in ('0', 'exit'):
                    print('Ok, not changing banner anymore.\n')
                    continue
                print(f'Choose your Chronicled Path now!\n'
                      f'List of available options:\n')
                options = ([i.name for i in chronicled_banner_list[new2]['characters']['5-stars']] +
                           [i.name for i in chronicled_banner_list[new2]['weapons']['5-stars']])
                print(', '.join(i for i in options))
                print('\n(Type 0 to exit)\n')

                while True:
                    new3 = input('Choose one: ').strip()
                    if new3 in ('0', 'exit'):
                        break
                    if new3 not in options:
                        print("That's not a valid pick! Try again\n"
                              "Please make sure the capitalization matches\n")
                    else:
                        print(f"Ok, {new3} selected")
                        break

                if new3 in ('0', 'exit'):
                    print('Ok, not choosing Chronicled Path anymore.\n')
                    continue
                user_banner_input = [new1, [new2, new3]]

            elif new1 == 'weapon':
                print('\n'.join(i for i in weapon_banner_list))
                print('\n(Type 0 to exit)\n')

                while True:
                    new2 = input('Choose one: ').strip()
                    if new2 in ('0', 'exit'):
                        break
                    if new2 not in weapon_banner_list.keys():
                        print("That's not a banner that's available! Try again\n")
                    else:
                        print(f"Ok, {new2} selected")
                        break

                if new2 in ('0', 'exit'):
                    print('Ok, not changing banner anymore.\n')
                    continue
                print(f'Choose your Epitomized Path now!\n'
                      f'List of available options:\n')
                print(weapon_banner_list[new2][0][0].name + '\n' + weapon_banner_list[new2][0][1].name)
                print('\n(Type 0 to exit)\n')

                while True:
                    new3 = input('Choose one: ').strip()
                    if new3 in ('0', 'exit'):
                        break
                    if new3 not in [weapon_banner_list[new2][0][0].name, weapon_banner_list[new2][0][1].name]:
                        print("That's not a valid pick! Try again\n"
                              "Please make sure the capitalization matches\n")
                    else:
                        print(f"Ok, {new3} selected")
                        break

                if new3 in ('0', 'exit'):
                    print('Ok, not choosing Eptomized Path anymore.\n')
                    continue
                user_banner_input = [new1, [new2, new3]]

        pities['weapon'][2] = 0
        pities['chronicled'][2] = False
        save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                          unique_four_weap_count)
        save_new_banner_of_choice()
        print_banner('New')
        print()
        continue

    if user_command == 'load':
        try:
            pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count = load_info()
            print(Fore.GREEN + 'Loaded additional information successfully!' + Style.RESET_ALL)
            info_ok = True
        except:
            print(Fore.RED + 'Something off with info file. Clearing everything...' + Style.RESET_ALL)
            info_ok = False


        if info_ok:
            try:
                wish_history = load_history()
                print(Fore.GREEN + 'Loaded wish history successfully!' + Style.RESET_ALL)
                history_ok = True
            except:
                print(Fore.RED + 'Something off with wish history file. Clearing everything...' + Style.RESET_ALL)
                history_ok = False


        if info_ok and history_ok:
            try:
                constellations, refinements = load_archive()
                print(Fore.GREEN + 'Loaded archive successfully!' + Style.RESET_ALL)
                archive_ok = True
            except:
                print(Fore.RED + 'Something off with archive file. Clearing everything...' + Style.RESET_ALL)
                archive_ok = False

        if not (info_ok and history_ok and archive_ok):
            set_defaults()

        load_distribution()

        try:
            load_banner()
            print(Fore.GREEN + 'Loaded banner information successfully!' + Style.RESET_ALL)
        except:
            print(Fore.RED + 'Something off with banner file. Setting to default...' + Style.RESET_ALL)
            user_banner_input = ['character', 'tao-3']
            save_new_banner_of_choice()

        print()
        continue

    if user_command == 'clear':
        set_defaults()
        pity_info = pities[banner_of_choice[0]]  # pities was reinitialized, need to make the reference again
        print('Done\n')
        continue

    if user_command == 'pity':
        print_pity(count, pity_info, five_count, four_count)
        print()
        continue

    if user_command == 'inv':
        show_full_inventory()
        continue

    if user_command.split()[0] == 'dist':
        total1 = sum(character_distribution.values()) - character_distribution[100]
        total2 = sum(weapon_distribution.values()) - weapon_distribution[100]
        if total1 or total2:
            print('1 = character\n2 = weapon\n(they have different distributions, pick one)\n\nType 0 to exit\n')
            while True:
                t = input('Your choice: ').strip().lower()
                if t in ('0', 'exit'):
                    break
                if t == '1' or t == 'character':
                    t = 'character'
                    break
                elif t == '2' or t == 'weapon':
                    t = 'weapon'
                    break
                else:
                    print('Please input either the number or the name of the distribution you want to see\n')

            if t in ('0', 'exit'):
                print('Ok, exiting distribution selection\n')
                continue

            if t == 'character':
                if total1 > 0:
                    print(f'Total entries = {character_distribution[100]}')
                    print(f'Total 5★ entries = {total1}\n')
                    for i in range(1, 91):
                        print(f'Pity {i}: {character_distribution[i] / total1 * 100:.2f}% - {character_distribution[i]}/{total1}')
                    print('If you want to visualize your results, type "viz" and then "1" or run visualize_character_distribution.py')
                else:
                    print('Get a 5-star character first!')
                print()
                continue

            elif t == 'weapon':
                if total2 > 0:
                    print(f'Total entries = {weapon_distribution[100]}')
                    print(f'Total 5★ entries = {total2}\n')
                    for i in range(1, 78):
                        print(f'Pity {i}: {weapon_distribution[i] / total2 * 100:.2f}% - {weapon_distribution[i]}/{total2}')
                    print('If you want to visualize your results, type "viz" and then "2" or run visualize_weapon_distribution.py')
                else:
                    print('Get a 5-star from the weapon banner first!')
                print()
                continue
        else:
            print('Get a 5-star first!\n')
            continue

    if user_command.split()[0] == 'viz':
        print('1 = character\n2 = weapon\n(they have different distributions, pick one)\n\nType 0 to exit\n')
        while True:
            t = input('Your choice: ').strip().lower()
            if t in ('0', 'exit'):
                break
            if t == '1' or t == 'character':
                t = 'character'
                break
            elif t == '2' or t == 'weapon':
                t = 'weapon'
                break
            else:
                print('Please input either the number or the name of the visualization you want to see\n')

        if t in ('0', 'exit'):
            print('Ok, exiting visualization selection\n')
            continue

        if t == 'character':
            if 'visualize_character_distribution' not in sys.modules:
                import visualize_character_distribution
            else:
                importlib.reload(visualize_character_distribution)
            print()
            continue

        elif t == 'weapon':
            if 'visualize_weapon_distribution' not in sys.modules:
                import visualize_weapon_distribution
            else:
                importlib.reload(visualize_weapon_distribution)
            print()
            continue

    if user_command == 'h':
        if len(wish_history[banner_of_choice[0]]):
            num_of_pages = (len(wish_history[banner_of_choice[0]]) - 1) // 25 + 1
            print('\n======================== WISH HISTORY ==========================\n')
            t = f'Total number of entries for {user_banner_input[0]} banner: {len(wish_history[user_banner_input[0]])}'
            extra = (64 - len(t))//2
            print(' ' * extra + t + '\n')
            page = 1
            print_history_page()

            while True:
                cmd = input('   History Command: ').strip().lower()
                if not cmd:
                    print('   Try "help"\n')
                    continue

                if cmd[0] == 'n':
                    cmd = cmd.split()
                    if len(cmd) == 1:
                        amount = 1
                    else:
                        if cmd[1].isnumeric():
                            amount = min(int(cmd[1]), num_of_pages - page)
                        else:
                            print(f'   "{cmd[1]}" is not a number\n')
                            continue
                    if page < num_of_pages:
                        print()

                        page += amount
                        print_history_page()

                    else:
                        print("   You're already at the last page\n")

                elif cmd[0] == 'p':
                    cmd = cmd.split()
                    if len(cmd) == 1:
                        amount = 1
                    else:
                        if cmd[1].isnumeric():
                            amount = min(int(cmd[1]), page - 1)
                        else:
                            print(f'   "{cmd[1]}" is not a number\n')
                            continue
                    if page > 1:
                        print()

                        page -= amount
                        print_history_page()

                    elif page == 1:
                        print("   You're already at the first page\n")

                    else:
                        print("   You can't go back even further\n")

                elif cmd.isnumeric():
                    page = min(int(cmd), num_of_pages)
                    print()
                    if page == 0:
                        print(Style.RESET_ALL + '   ' + '-' * 58)
                        print(Fore.YELLOW + '                       You found page 0')
                        print(Style.RESET_ALL + '   ' + '-' * 58)
                        print(f"\n   (Page 0/{num_of_pages})\n")
                    else:
                        print_history_page()

                elif cmd == 'e':
                    print('   No longer viewing wish history!\n')
                    print('================================================================\n')
                    break

                elif cmd in ['help', "'help'", '"help"']:
                    print(f'   {Fore.BLUE}numbers in [] are optional{Style.RESET_ALL}\n'
                          f'   {Fore.LIGHTMAGENTA_EX}n [number]{Style.RESET_ALL} = go forward a number of pages\n'
                          f'   {Fore.LIGHTMAGENTA_EX}p [number]{Style.RESET_ALL} = go back a number of pages\n'
                          f'   {Fore.LIGHTMAGENTA_EX}number{Style.RESET_ALL} = go to page\n'
                          f'   {Fore.LIGHTMAGENTA_EX}e{Style.RESET_ALL} = exit\n')

                else:
                    print('   Try "help"\n')
        else:
            print('Wish history empty!\n')
        continue

    try:
        user_command = int(user_command)
    except ValueError:
        print('Try "help"\n')
        continue

    if user_command <= 1000000000:
        print()
        verbose_threshold = 7 - (user_command <= 10000000) - (user_command <= 1000000) - (user_command <= 100000) - (user_command <= 10000)
        # pulls <= 10k = show every pull
        # 10k < pulls <= 100k = show 4* and 5*
        # 100k < pulls <= 1M = show only 5*
        # 1M < pulls = show progress (10k step) and stop showing "10 PULLS WITHOUT A 4 STAR" message
        # comparison to 10M is made just in case ill need it in the future

        if user_command > 1000000:  # if number bigger than 1 million
            print(f'Are you sure? Doing {user_command} pulls would take around {round(50 * user_command / 10000000)} seconds.')
            sure = input('Type "CONFIRM" if you want to proceed: ')  # ask user if they're sure
            if sure != "CONFIRM":  # if they're not sure
                print('Aborting\n')  # abort this job
                continue  # and ask for next command
            else:
                print()  # otherwise add an extra space cuz pretty
        count += user_command  # if the program came this far, go on with the job
        pity_info[-1][0] += user_command
        if user_banner_input[0] != 'weapon':
            character_distribution[100] += user_command
        else:
            weapon_distribution[100] += user_command
        for i in range(user_command):
            try:
                res, p, w = make_pull(banner_of_choice, pity_info)
            except MemoryError:
                print('The program ran out of memory dude what have you DONE')
                save_archive_to_file(constellations, refinements)
                save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                                  unique_four_weap_count)
                save_character_distribution_to_file()
                save_weapon_distribution_to_file()
                try:
                    save_history_to_file(wish_history)
                    print('backed up the history at least')
                except:
                    print('couldnt even save the wish history')
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
                print(Style.RESET_ALL + f'{win_map[w]}{color_map[res.rarity]}{res.name}{f", {p} pity" if res.rarity >= 4 else ""}')
            if verbose_threshold >= 6 and i % 100000 == 0:
                print(f'{i}/{user_command} wishes done')
            if user_banner_input[0] != 'standard':
                if verbose_threshold < 6 and pity_info[1] >= (10 - (user_banner_input[0] == 'weapon')):
                    print(Fore.CYAN + f"{pity_info[1]} PULLS WITHOUT A 4-STAR!" + Style.RESET_ALL)
        # print(wish_history)
        save_archive_to_file(constellations, refinements)
        save_info_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                          unique_four_weap_count)
        save_character_distribution_to_file()
        save_weapon_distribution_to_file()
        print()
        if user_banner_input[0] == 'character':
            print(Style.RESET_ALL + f'{pity_info[0]} pity, {"guaranteed" if pity_info[2] else "50/50"}')
        elif user_banner_input[0] == 'chronicled':
            print(Style.RESET_ALL + f'{pity_info[0]} pity, {"guaranteed" if pity_info[2] else "50/50"}')
        elif user_banner_input[0] == 'weapon':
            epitomized = f"epitomized points: {pity_info[2]}"
            print(Style.RESET_ALL + f'{pity_info[0]} pity, {"guaranteed" if pity_info[2] == 2 else "37.5% / 37.5% / 25%, "+epitomized if not pity_info[3] else "50/50, "+epitomized}')
        elif user_banner_input[0] == 'standard':
            recent, not_recent = ('character', 'weapon') if pity_info[0] < pity_info[1] else ('weapon', 'character')
            pulls_since_not_recent = f', {max(pity_info[0], pity_info[1])} {not_recent} pity' if pity_info[0] != pity_info[1] else ''
            print(Style.RESET_ALL + f'{min(pity_info[0], pity_info[1])} {recent} pity{pulls_since_not_recent}')

        if not messaged and len(wish_history[banner_of_choice[0]]) > 2500000:
            messaged = True
            print(Fore.LIGHTRED_EX + '\nTo save disk space and ensure acceptable simulator performance,\n'
                                     'the size of the wish history has been limited to 2.5 million entries.\n'
                                     'This does NOT limit the the distribution data size (e.g. character_distribution.txt)',
                  Style.RESET_ALL)
        wish_history[banner_of_choice[0]] = wish_history[banner_of_choice[0]][-2500000:]
        try:
            save_history_to_file(wish_history)
        except:
            print('Not enough storage to hold this wish history. Wish history not backed up')
    elif user_command < 0:
        print('what are u doing bro')

    else:
        print("I'm not letting you do that. Max 1 billion wishes at a time please")
    print()

if __name__ == '__main__':
    print('\nThank you for using Wish Simulator')
