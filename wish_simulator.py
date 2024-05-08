import json
from random import choice, choices
from colorama import init, Fore, Style
from pathlib import Path
import sys
import importlib

print("\nTHIS IS A WIP PROJECT. SOME FEATURES ARE BROKEN, I'M WORKING ON THEM.")
print('\n============================ LOADING ===========================\n')
init()
Path(".\\banner_info").mkdir(parents=True, exist_ok=True)


def save_history_to_file(data):
    with open(r'.\banner_info\wish.txt', 'w') as f:
        f.write(json.dumps(data, separators=(',', ':')))


def save_distribution_to_file():
    with open(r'.\banner_info\character_distribution.txt', 'w') as f:
        f.write(json.dumps(distribution, separators=(',', ':')))


def save_pity_to_file(pity, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count):
    with open(r'.\banner_info\pity.txt', 'w') as f:
        f.write(json.dumps([pity, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count], separators=(',', ':')))


def save_archive_to_file(cons, refs):

    numeric_indexes_c = [character.num for character in cons]
    numeric_indexes_w = [weapon.num for weapon in refs]
    new_dict_c = dict(zip(numeric_indexes_c, list(cons.values())))
    new_dict_w = dict(zip(numeric_indexes_w, list(refs.values())))
    with open(r'.\banner_info\archive.txt', 'w') as f:
        data = (new_dict_c, new_dict_w)
        f.write(json.dumps(data, separators=(',', ':')))


def load_history():
    try:
        with open('.\\banner_info\\wish.txt') as file:
            data = file.read()
        history = json.loads(data)
        return history

    except FileNotFoundError:
        with open('.\\banner_info\\wish.txt', 'w') as file:
            file.write('{"character": [], "weapon": [], "standard": [], "chronicled": []}')
        return {"character": [], "weapon": [], "standard": [], "chronicled": []}


def load_pity():
    try:
        with open('.\\banner_info\\pity.txt') as file:
            data = file.read()
        pity_and_other_info = json.loads(data)
        return pity_and_other_info

    except FileNotFoundError:
        pities = {'character': [0, 0, False, False],
                  'weapon': [0, 0, 0, False, False],
                  'standard': [0, 0, 0, 0],
                  'chronicled': [0, 0, True, False]}
        with open('.\\banner_info\\pity.txt', 'w') as file:
            file.write(f'[{pities},0,0,0,0,0,0]')
        return [pities, 0, 0, 0, 0, 0, 0]


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(kk): vv for kk, vv in x.items()}
    return x


def load_distribution():
    global distribution
    try:
        with open('.\\banner_info\\character_distribution.txt') as file:
            data = file.read()
        distribution = json.loads(data, object_hook=jsonKeys2int)

    except:
        distribution = {i: 0 for i in range(1, 91)}
        distribution[100] = 0
        save_distribution_to_file()

    print('Loaded distribution successfully!')


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

def clear_everything():
    global wish_history, constellations, refinements, pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count
    wish_history = {"character": [], "weapon": [], "standard": [], "chronicled": []}
    save_history_to_file(wish_history)

    constellations, refinements = {}, {}
    save_archive_to_file(constellations, refinements)

    pities = {'character': [0, 0, False, False],
              # 5-star pity / 4-star pity / 5-star guarantee / 4-star guarantee
              'weapon': [0, 0, 0, False, False],
              # 5-star pity / 4-star pity / epitomized path / last 5 star was standard? / 4-star guarantee
              'standard': [0, 0, 0, 0],
              # wishes since last [5-star char / 4-star char / 5-star weapon / 4-star weapon]
              'chronicled': [0, 0, True, False]
              # 5-star pity / 4-star pity / 5-star guarantee / 4-star guarantee
              }
    count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count = 0, 0, 0, 0, 0, 0
    save_pity_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                      unique_four_weap_count)
    print("Everything cleared!")


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
    "Aquila Favonia - Amos' Bow": ["Aquila Favonia", "Amos' Bow", "The Flute", "The Bell", "The Widsith", "The Stringless", "Favonius Lance"],
    "Lost Prayer to the Sacred Winds - Wolf's Gravestone": ["Lost Prayer to the Sacred Winds", "Wolf's Gravestone", "Sacrificial Sword", "Sacrificial Bow", "Sacrificial Fragments", "Sacrificial Fragments", "Dragon's Bane"],
    "Memory of Dust - Skyward Harp": ["Memory of Dust", "Skyward Harp",  "The Flute", "Rainslasher", "Eye of Perception", "Rust", "Favonius Lance"],
    "Vortex Vanquisher - The Unforged": ["Vortex Vanquisher", "The Unforged",  "Lion's Roar", "The Bell", "Favonius Codex", "Favonius Warbow", "Dragon's Bane"],
    "Summit Shaper - Skyward Atlas": ["Summit Shaper", "Skyward Atlas",  "Favonius Sword", "Favonius Greatsword", "Favonius Lance", "Sacrificial Fragments", "The Stringless"],
    "Skyward Pride - Amos' Bow": ["Skyward Pride", "Amos' Bow",  "Sacrificial Sword", "The Bell", "Dragon's Bane", "Eye of Perception", "Favonius Warbow"],
    "Primordial Jade Cutter - Primordial Jade Winged-Spear": ["Primordial Jade Cutter", "Primordial Jade Winged-Spear",  "The Flute", "Sacrificial Greatsword", "Rust", "Eye of Perception", "Favonius Lance"],
    "Staff of Homa - Wolf's Gravestone": ["Staff of Homa", "Wolf's Gravestone",  "Lithic Blade", "Lithic Spear", "Lion's Roar", "Sacrificial Bow", "The Widsith"],
    "Elegy for the End - Skyward Blade": ["Elegy for the End", "Skyward Blade",  "The Alley Flash", "Wine and Song", "Favonius Greatsword", "Favonius Warbow", "Dragon's Bane"],
    "Skyward Harp - Lost Prayer to the Sacred Winds": ["Skyward Harp", "Lost Prayer to the Sacred Winds",  "Alley Hunter", "Favonius Sword", "Sacrificial Greatsword", "Favonius Codex", "Favonius Lance"],
    "Summit Shaper - Memory of Dust": ["Summit Shaper", "Memory of Dust",  "Lithic Blade", "Lithic Spear", "The Flute", "Eye of Perception", "Sacrificial Bow"],
    "Song of Broken Pines - Aquila Favonia": ["Song of Broken Pines", "Aquila Favonia",  "Sacrificial Sword", "Rainslasher", "Dragon's Bane", "Sacrificial Fragments", "Rust"],
    "Skyward Pride - Lost Prayer to the Sacred Winds": ["Skyward Pride", "Lost Prayer to the Sacred Winds",  "Mitternachts Waltz", "Lion's Roar", "The Bell", "Favonius Lance", "The Widsith"],
    "Freedom-Sworn - Skyward Atlas": ["Freedom-Sworn", "Skyward Atlas",  "The Alley Flash", "Wine and Song", "Alley Hunter", "Dragon's Bane", "Favonius Greatsword"],
    "Mistsplitter Reforged - Skyward Spine": ["Mistsplitter Reforged", "Skyward Spine",  "Sacrificial Greatsword", "Favonius Lance", "Favonius Codex", "Favonius Sword", "The Stringless"],
    "Thundering Pulse - Skyward Blade": ["Thundering Pulse", "Skyward Blade",  "Sacrificial Sword", "Rainslasher", "Dragon's Bane", "Sacrificial Fragments", "Favonius Warbow"],
    "Engulfing Lightning - The Unforged": ["Engulfing Lightning", "The Unforged",  "Lion's Roar", "The Bell", "Favonius Lance", "The Widsith", "Sacrificial Bow"],
    "Everlasting Moonglow - Primordial Jade Cutter": ["Everlasting Moonglow", "Primordial Jade Cutter",  "The Flute", "Favonius Greatsword", "Dragon's Bane", "Favonius Codex", "The Stringless"],
    "Polar Star - Memory of Dust": ["Polar Star", "Memory of Dust",  "Akuoumaru", "Favonius Sword", "Favonius Lance", "Eye of Perception", "Rust"],
    "Staff of Homa - Elegy for the End": ["Staff of Homa", "Elegy for the End",  "Wavebreaker's Fin", "Mouun's Moon", "Sacrificial Sword", "Rainslasher", "The Widsith"],
    "Freedom-Sworn - Song of Broken Pines": ["Freedom-Sworn", "Song of Broken Pines",  "Wine and Song", "Alley Hunter", "Lion's Roar", "Sacrificial Greatsword", "Dragon's Bane"],
    "Redhorn Stonethresher - Skyward Harp": ["Redhorn Stonethresher", "Skyward Harp",  "The Alley Flash", "Mitternachts Waltz", "The Bell", "Favonius Lance", "Sacrificial Fragments"],
    "Calamity Queller - Primordial Jade Winged-Spear": ["Calamity Queller", "Primordial Jade Winged-Spear",  "Lithic Spear", "The Flute", "Favonius Greatsword", "The Widsith", "Favonius Warbow"],
    "Vortex Vanquisher - Amos' Bow": ["Vortex Vanquisher", "Amos' Bow",  "Lithic Blade", "Favonius Sword", "Dragon's Bane", "Favonius Codex", "Sacrificial Bow"],
    "Kagura's Verity - Primordial Jade Cutter": ["Kagura's Verity", "Primordial Jade Cutter",  "Wavebreaker's Fin", "Sacrificial Sword", "Rainslasher", "Eye of Perception", "The Stringless"],
    "Engulfing Lightning - Everlasting Moonglow": ["Engulfing Lightning", "Everlasting Moonglow",  "Akuoumaru", "Mouun's Moon", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments"],
    "Haran Geppaku Futsu - Elegy for the End": ["Haran Geppaku Futsu", "Elegy for the End",  "The Flute", "Sacrificial Greatsword", "Dragon's Bane", "The Widsith", "Rust"],
    "Mistsplitter Reforged - The Unforged": ["Mistsplitter Reforged", "The Unforged",  "Favonius Sword", "The Bell", "Favonius Lance", "Favonius Codex", "Favonius Warbow"],
    "Aqua Simulacra - Primordial Jade Winged-Spear": ["Aqua Simulacra", "Primordial Jade Winged-Spear",  "Lithic Spear", "Eye of Perception", "Favonius Greatsword", "Sacrificial Bow", "Sacrificial Sword"],
    "Redhorn Stonethresher - Memory of Dust": ["Redhorn Stonethresher", "Memory of Dust",  "Lithic Blade", "Lion's Roar", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"],
    "Freedom-Sworn - Lost Prayer to the Sacred Winds": ["Freedom-Sworn", "Lost Prayer to the Sacred Winds",  "The Alley Flash", "Mitternachts Waltz", "Rainslasher", "Favonius Lance", "The Widsith"],
    "Thundering Pulse - Summit Shaper": ["Thundering Pulse", "Summit Shaper",  "Wine and Song", "Alley Hunter", "The Flute", "Sacrificial Greatsword", "Dragon's Bane"],
    "Hunter's Path - Vortex Vanquisher": ["Hunter's Path", "Vortex Vanquisher",  "Favonius Sword", "The Bell", "Favonius Lance", "Favonius Codex", "The Stringless"],
    "Everlasting Moonglow - Amos' Bow": ["Everlasting Moonglow", "Amos' Bow",  "Sacrificial Sword", "Favonius Greatsword", "Dragon's Bane", "Eye of Perception", "Rust"],
    "Staff of the Scarlet Sands - Elegy for the End": ["Staff of the Scarlet Sands", "Elegy for the End",  "Makhaira Aquamarine", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments", "Favonius Warbow"],
    "Key of Khaj-Nisut - Primordial Jade Cutter": ["Key of Khaj-Nisut", "Primordial Jade Cutter",  "Xiphos' Moonlight", "Wandering Evenstar", "Rainslasher", "Dragon's Bane", "Sacrificial Bow"],
    "A Thousand Floating Dreams - Thundering Pulse": ["A Thousand Floating Dreams", "Thundering Pulse",  "The Flute", "Sacrificial Greatsword", "Favonius Lance", "The Widsith", "Rust"],
    "Kagura's Verity - Polar Star": ["Kagura's Verity", "Polar Star",  "Favonius Sword", "The Bell", "Dragon's Bane", "Favonius Codex", "The Stringless"],
    "Tulaytullah's Remembrance - Redhorn Stonethresher": ["Tulaytullah's Remembrance", "Redhorn Stonethresher",  "Wavebreaker's Fin", "Sacrificial Sword", "Favonius Greatsword", "Eye of Perception", "Favonius Warbow"],
    "Engulfing Lightning - Haran Geppaku Futsu": ["Engulfing Lightning", "Haran Geppaku Futsu",  "Akuoumaru", "Mouun's Moon", "Lion's Roar", "Favonius Lance", "Sacrificial Fragments"],
    "Light of Foliar Incision - Primordial Jade Winged-Spear": ["Light of Foliar Incision", "Primordial Jade Winged-Spear",  "Lithic Spear", "The Flute", "Rainslasher", "The Widsith", "Sacrificial Bow"],
    "Staff of Homa - Aqua Simulacra": ["Staff of Homa", "Aqua Simulacra",  "Lithic Blade", "Favonius Sword", "Dragon's Bane", "Favonius Codex", "Rust"],
    "Beacon of the Reed Sea - Staff of the Scarlet Sands": ["Beacon of the Reed Sea", "Staff of the Scarlet Sands",  "The Alley Flash", "Alley Hunter", "Sacrificial Greatsword", "Dragon's Bane", "Eye of Perception"],
    "Calamity Queller - Mistsplitter Reforged": ["Calamity Queller", "Mistsplitter Reforged",  "Wine and Song", "Sacrificial Sword", "The Bell", "Favonius Lance", "Favonius Warbow"],
    "A Thousand Floating Dreams - Key of Khaj-Nisut": ["A Thousand Floating Dreams", "Key of Khaj-Nisut",  "Xiphos' Moonlight", "Favonius Greatsword", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"],
    "Jadefall's Splendor - Amos' Bow": ["Jadefall's Splendor", "Amos' Bow",  "Makhaira Aquamarine", "Wandering Evenstar", "Lion's Roar", "Favonius Lance", "Sacrificial Bow"],
    "Thundering Pulse - Kagura's Verity": ["Thundering Pulse", "Kagura's Verity",  "Akuoumaru", "The Flute", "Dragon's Bane", "The Widsith", "Rust"],
    "Light of Foliar Incision - Freedom-Sworn": ["Light of Foliar Incision", "Freedom-Sworn",  "Favonius Codex", "Favonius Sword", "Mouun's Moon", "Sacrificial Greatsword", "Wavebreaker's Fin"],
    "Song of Broken Pines - Lost Prayer to the Sacred Winds": ["Song of Broken Pines", "Lost Prayer to the Sacred Winds",  "The Alley Flash", "Alley Hunter", "Rainslasher", "Favonius Lance", "Eye of Perception"],
    "Everlasting Moonglow - Tulaytullah's Remembrance": ["Everlasting Moonglow", "Tulaytullah's Remembrance",  "Wine and Song", "Lion's Roar", "The Bell", "Dragon's Bane", "Favonius Warbow"],
    "The First Great Magic - Aqua Simulacra": ["The First Great Magic", "Aqua Simulacra",  "Sacrificial Sword", "Favonius Greatsword", "Favonius Lance", "Sacrificial Fragments", "Sacrificial Bow"],
    "Vortex Vanquisher - Polar Star": ["Vortex Vanquisher", "Polar Star",  "The Flute", "Sacrificial Greatsword", "Dragon's Bane", "The Widsith", "Rust"],
    "Tome of the Eternal Flow - Staff of Homa": ["Tome of the Eternal Flow", "Staff of Homa",  "The Dockhand's Assistant", "Portable Power Saw", "Mitternachts Waltz", "Favonius Lance", "Favonius Codex"],
    "Cashflow Supervision - Elegy for the End": ["Cashflow Supervision", "Elegy for the End",  "Prospector's Drill", "Range Gauge", "Favonius Sword", "Rainslasher", "Eye of Perception"],
    "Splendor of Tranquil Waters - Jadefall's Splendor": ["Splendor of Tranquil Waters", "Jadefall's Splendor",  "Sacrificial Sword", "The Bell", "Dragon's Bane", "Sacrificial Fragments", "The Stringless"],
    "Staff of the Scarlet Sands - Haran Geppaku Futsu": ["Staff of the Scarlet Sands", "Haran Geppaku Futsu",  "Lion's Roar", "Favonius Greatsword", "Favonius Lance", "The Widsith", "Favonius Warbow"],
    "Verdict - Mistsplitter Reforged": ["Verdict", "Mistsplitter Reforged",  "Akuoumaru", "Mouun's Moon", "The Flute", "Dragon's Bane", "Favonius Codex"],
    "Engulfing Lightning - Thundering Pulse": ["Engulfing Lightning", "Thundering Pulse",  "Wavebreaker's Fin", "Favonius Sword", "Rainslasher", "Eye of Perception", "Rust"],
    "Crane's Echoing Call - A Thousand Floating Dreams": ["Crane's Echoing Call", "A Thousand Floating Dreams",  "Lithic Spear", "Sacrificial Sword", "Sacrificial Greatsword", "Sacrificial Fragments", "Sacrificial Bow"],
    "Kagura's Verity - Primordial Jade Winged-Spear": ["Kagura's Verity", "Primordial Jade Winged-Spear",  "Lithic Blade", "Lion's Roar", "Favonius Lance", "The Widsith", "The Stringless"],
    "Uraku Misugiri - Redhorn Stonethresher": ["Uraku Misugiri", "Redhorn Stonethresher",  "The Alley Flash", "Alley Hunter", "The Bell", "Dragon's Bane", "Favonius Codex"],
    "Tome of the Eternal Flow - Freedom-Sworn": ["Tome of the Eternal Flow", "Freedom-Sworn",  "Wine and Song", "Mitternachts Waltz", "The Flute", "Favonius Greatsword", "Favonius Lance"],
    "Crimson Moon's Semblance - The First Great Magic": ["Crimson Moon's Semblance", "The First Great Magic",  "The Dockhand's Assistant", "Portable Power Saw", "Dragon's Bane", "Eye of Perception", "Favonius Warbow"]
}

# replace strings with objects in lists of banners
for banner in character_banner_list:
    for i in range(len(character_banner_list[banner][0])):
        character_banner_list[banner][0][i] = characters_dict[character_banner_list[banner][0][i]]

for banner in weapon_banner_list:
    for i in range(len(weapon_banner_list[banner])):
        weapon_banner_list[banner][i] = weapons_dict[weapon_banner_list[banner][i]]


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

def print_pity(counter, p, c5, c4):
    print("\n" + "="*23 + " PITY INFORMATION " + "="*23 + '\n')
    print(f'{counter} wish{"es" if counter != 1 else ""} done so far')
    print(f'Out of them {Fore.LIGHTYELLOW_EX}{c5} five-star{"s" if c5 != 1 else ""}{Style.RESET_ALL} and {Fore.MAGENTA}{c4} four-star{"s" if c4 != 1 else ""}{Style.RESET_ALL}')
    if p[0] < 10 and p[1] < 10:
        insert1, insert2 = '', ''
    else:
        insert1 = ' ' * (p[0] < 10)
        insert2 = ' ' * (p[1] < 10)
    print(f'{Fore.LIGHTYELLOW_EX}5★{Style.RESET_ALL} pity = {p[0]},{insert1} {"you're on a 50/50" if not p[-2] else "next is guaranteed to be featured"}')
    print(f'{Fore.MAGENTA}4★{Style.RESET_ALL} pity = {p[1]},{insert2} {"you're on a 50/50" if not p[-1] else "next is guaranteed to be featured"}')
    # print('\n================================================================')

def print_character_archive():
    global sorted_constellations, a
    sorted_constellations = sorted(list(constellations.items()),
                                   key=lambda x: (-x[0].rarity, x[0] not in banner_of_choice[1], -x[1]))
    if sorted_constellations:
        last_rarity = 0
        print("\n" + "="*23 + " CHARACTER ARCHIVE " + "="*22)
        print(f"{len(constellations)}/{len(characters_dict)} characters ({unique_five_char_count}/{amount_of_five_stars} {Fore.LIGHTYELLOW_EX}5★{Style.RESET_ALL}, {len(constellations) - unique_five_char_count}/{amount_of_four_stars} {Fore.MAGENTA}4★{Style.RESET_ALL})")
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
        print(f"{len(refinements)}/{len(weapons_dict)} gacha weapons ({unique_five_weap_count}/{amount_of_five_star_weapons} {Fore.LIGHTYELLOW_EX}5★{Style.RESET_ALL}, {unique_four_weap_count}/{amount_of_four_star_weapons} {Fore.MAGENTA}4★{Style.RESET_ALL}, {len(refinements) - unique_five_weap_count - unique_four_weap_count}/{amount_of_three_star_weapons} {Fore.BLUE}3*{Style.RESET_ALL})")
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
    print(Style.RESET_ALL + '-' * 51)
    for number in wish_history[banner_of_choice[0]][print_from:print_to:-1]:
        cc += 1
        print(color_map[number_to_item_dict[number].rarity] + f'{cc}.{" " if len(str(cc)) < len(str(-print_to - 1)) else ""}',
              number_to_item_dict[number].name)
    print(Style.RESET_ALL + '-' * 51)
    print(f'\n(Page {page}/{num_of_pages})\n')


try:  # if i extract this into a method pycharm stops seeing all the variables assigned
    wish_history = load_history()
    print('Loaded wish history successfully!')
    history_ok = True
except:
    print('Something off with wish history file. Clearing everything...')
    history_ok = False

if history_ok:
    try:
        constellations, refinements = load_archive()
        print('Loaded archive successfully!')
        archive_ok = True
    except:
        print('Something off with archive file. Clearing everything...')
        archive_ok = False

if history_ok and archive_ok:  # history_ok == True -> archive_ok exists, otherwise check fails at history_ok
    try:
        pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count = load_pity()
        print('Loaded additional information successfully!')
        pity_ok = True
    except:
        print('Something off with pity file. Clearing everything...')
        pity_ok = False

if not (history_ok and archive_ok and pity_ok):
    clear_everything()

load_distribution()

banner_types = ["character", "weapon", "standard", "chronicled"]


# print([c in standard_characters for c in character_banner_list["venti-1"]])


def make_pull(banner_info, pity):
    global legal_standard_four_stars, legal_standard_five_stars
    five_star_chance, four_star_chance = get_chances(banner_info[0], pity)
    rarity = 5 if choices((True, False), (five_star_chance, 100 - five_star_chance))[0] \
        else 4 if choices((True, False), (four_star_chance, 100 - four_star_chance))[0] else 3
    if banner_info[0] == 'character':
        featured_five_star = banner_info[1][0]
        featured_four_stars = banner_info[1][1:]
        if rarity == 5:
            distribution[pity[0] + 1] += 1
            # print(f'{Style.RESET_ALL}{five_star_chance}')
            if pity[-2]:  # if guaranteed
                result = [featured_five_star, pity[0] + 1]  # give featured 5-star character
                pity[-2] = False  # change guaranteed to false
                result.append(2)  # log that guarantee took place
            else:  # if not guaranteed
                # choose if win 50/50
                result = [choice((featured_five_star, choice(legal_standard_five_stars))), pity[0] + 1]
                if result[0] != featured_five_star:  # if didnt win 50/50
                    pity[-2] = True  # set guarantee to true
                result.append(int(result[0] == featured_five_star))  # log if you won or not
            pity[0] = 0
            pity[1] += 1

        elif rarity == 4:
            # print(f'{Style.RESET_ALL}{four_star_chance}')
            if pity[-1]:  # if guaranteed
                result = [choice(featured_four_stars), pity[1] + 1]  # give a featured 4-star character
                pity[-1] = False  # change guaranteed to false
                result.append(2)  # log that guarantee took place
            else:  # if not guaranteed
                # choose what to give from different pools
                result = [choice(
                    choices((featured_four_stars, legal_standard_four_stars, standard_4_star_weapons), [50, 25, 25])[
                        0]), pity[1] + 1]
                if result[0] not in featured_four_stars:  # if 50/50 lost
                    pity[-1] = True  # set guarantee to true
                result.append(int(result[0] in featured_four_stars))  # log if you won or not
            pity[0] += 1
            pity[1] = 0

        elif rarity == 3:
            result = [choice(three_star_weapons), 0, False]
            pity[0] += 1
            pity[1] += 1

    # elif banner_info[0] == 'weapon':
    #     result = [0, 0]
    wish_history[banner_info[0]].append(result[0].num)
    pities[banner_info[0]] = pity
    return result


def get_chances(banner_type, pity):  # returns (% to get 5 star, % to get 4 star)
    if banner_type != 'weapon':  # + 1 here to check the number of the next pull you're making
        five_star_chance = max(0, pity[0] + 1 - 73) * 6 + 0.6  # every pull above 73 adds 6%
        four_star_chance = 100 if pity[1] + 1 >= 10 else (56.1 if pity[1] + 1 == 9 else 5.1)
        # 10+ pity = 4 star in case of no 5 star, 9 pity = 56.1% chance, <9 = 5.6%

    else:
        five_star_chance = max(0, pity[0] + 1 - 62) * 7 + 0.7
        four_star_chance = 100 if pity[1] + 1 >= 10 else (66 if pity[1] + 1 == 9 else 6)

    return five_star_chance, four_star_chance


user_banner_input = 'character', "ganyu-4"
banner_of_choice = (
user_banner_input[0], character_banner_list[user_banner_input[1]][0], character_banner_list[user_banner_input[1]][1])
legal_standard_four_stars = [s for s in standard_4_star_characters if
                             (s not in banner_of_choice[1] and s.version < banner_of_choice[-1])]
legal_standard_five_stars = [s for s in standard_5_star_characters if
                             (s not in banner_of_choice[1] and s.version < banner_of_choice[-1])]
pity_info = pities[banner_of_choice[0]]

three_stars = '(   ★ ★ ★   )'
four_stars = '(  ★ ★ ★ ★  )'
five_stars = '( ★ ★ ★ ★ ★ )'
color_map = {3: Fore.BLUE, 4: Fore.MAGENTA, 5: Fore.LIGHTYELLOW_EX}
win_map = {0: f'{Fore.RED}L{Style.RESET_ALL}', 1: f'{Fore.LIGHTCYAN_EX}W{Style.RESET_ALL}',
           2: f'{Fore.LIGHTGREEN_EX}G{Style.RESET_ALL}'}
verbose_threshold = 3

print('\n================================================================\n')
print('Type "help" for the list of commands\n')
while True:
    user_command = input('Command: ').lower().strip()

    if user_command == 'help':
        print('\n'
              'i will update "help" later\n'
              'but if you\'re using this rn, here\'s some commands you can get silly with:\n'
              '\n'
              '<number> = do <number> pulls\n'
              'banner = view current banner\n'
              'load = load updates made to wish.txt, archive.txt, pity.txt, character_distribution.txt\n'
              'clear = clear wishing history, pity, inventory. basically like starting a new account\n'
              'pity = view pity related information\n'
              'inv = view character/weapon archive\n'
              'dist = view disribution of 5-star character per pity (from 71 to 90)\n'
              'full dist = same as dist except from 1 to 90\n'
              'viz = plot a "Distribution of 5★ characters per pity" graph, visualizing full dist\n'
              'h = view wish history, commands to interact with it:\n'
              '\t\tn [<number>] = go forward <number> pages\n'
              '\t\tp [<number>] = go back <number> pages,\n'
              '\t\t<number> = go to page <number>,\n'
              '\t\te = exit\n'
              '0 = exit the simulator\n')
        continue

    if user_command == 'banner':
        print(f'\nChosen banner type: {user_banner_input[0]}\nBanner ID: {user_banner_input[1]}')
        if banner_of_choice[0] != 'standard':
            for i in banner_of_choice[1]:
                print(f'{color_map[i.rarity]}{i.rarity}★ {i.name}{Style.RESET_ALL}')
        print()
        continue

    if user_command == 'load':
        try:
            wish_history = load_history()
            print('Loaded wish history successfully!')
            history_ok = True
        except:
            print('Something off with wish history file. Clearing everything...')
            history_ok = False

        if history_ok:
            try:
                constellations, refinements = load_archive()
                print('Loaded archive successfully!')
                archive_ok = True
            except:
                print('Something off with archive file. Clearing everything...')
                archive_ok = False

        if history_ok and archive_ok:  # history_ok == True -> archive_ok exists, otherwise check fails at history_ok
            try:
                pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count = load_pity()
                print('Loaded additional information successfully!')
                pity_ok = True
            except:
                print('Something off with pity file. Clearing everything...')
                pity_ok = False

        if not (history_ok and archive_ok and pity_ok):
            clear_everything()

        load_distribution()

        print()
        continue

    if user_command == 'clear':
        clear_everything()
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

    if user_command == 'dist':
        total = sum(distribution.values()) - distribution[100]
        if total > 0:
            print(f'Total entries = {distribution[100]}')
            print(f'Total 5★ entries = {total}\n')
            for i in range(71, 91):
                print(f'Pity {i}: {distribution[i] / total * 100:.2f}% - {distribution[i]}/{total}')
        else:
            print('Get a 5-star first')
        print()
        continue

    if user_command == 'full dist':
        total = sum(distribution.values()) - distribution[100]
        if total > 0:
            print(f'Total entries = {distribution[100]}')
            print(f'Total 5★ entries = {total}\n')
            for i in range(1, 91):
                print(f'Pity {i}: {distribution[i] / total * 100:.2f}% - {distribution[i]}/{total}')
            print('If you want to visualize your results, type "viz" or run visualize_distribution.py')
        else:
            print('Get a 5-star first')
        print()
        continue

    if user_command == 'viz':
        if 'visualize_distribution' not in sys.modules:
            import visualize_distribution
        else:
            importlib.reload(visualize_distribution)
        print('Done\n')
        continue

    if user_command == 'h':
        if len(wish_history[banner_of_choice[0]]):
            num_of_pages = (len(wish_history[banner_of_choice[0]]) - 1) // 25 + 1
            print('\n================== WISH HISTORY ===================\n')

            page = 1
            print_history_page()

            while True:
                cmd = input('History Command: ')
                if 'n' in cmd:
                    cmd = cmd.split()
                    if len(cmd) == 1:
                        amount = 1
                    else:
                        amount = min(int(cmd[1]), num_of_pages - page)

                    if page < num_of_pages:
                        print()

                        page += amount
                        print_history_page()

                    else:
                        print("You're already at the last page\n")

                elif 'p' in cmd:
                    cmd = cmd.split()
                    if len(cmd) == 1:
                        amount = 1
                    else:
                        amount = min(int(cmd[1]), page - 1)

                    if page > 1:
                        print()

                        page -= amount
                        print_history_page()

                    elif page == 1:
                        print("You're already at the first page\n")

                    else:
                        print("You can't go back even further\n")

                elif cmd.isnumeric():

                    if int(cmd) > num_of_pages:
                        print(f'Pages go up to {num_of_pages}, you provided {cmd}\n')
                    else:
                        page = int(cmd)
                        print()
                        if page == 0:
                            print(Style.RESET_ALL + '-' * 51)
                            print(Fore.LIGHTYELLOW_EX + '                 You found page 0')
                            print(Style.RESET_ALL + '-' * 51)
                            print(f"\n(Page 0/{num_of_pages})\n")
                        else:
                            print_history_page()

                elif cmd == 'e':
                    print('No longer viewing wish history!\n')
                    break

        else:
            print('Wish history empty!\n')
        continue

    try:
        user_command = int(user_command)
    except ValueError:
        print('Try "help"\n')
        continue

    if 0 <= user_command <= 1000000000:
        if user_command == 0:
            # print_pity(count, pity_info, five_count, four_count)
            # show_full_inventory()
            print('Exiting...')
            print('\n================================================================')
            break
        print()
        verbose_threshold = 7 - (user_command <= 10000000) - (user_command <= 1000000) - (user_command <= 100000) - (user_command <= 10000)
        # pulls <= 10k = show every pull
        # 10k < pulls <= 100k = show 4* and 5*
        # 100k < pulls <= 1M = show only 5*
        # 1M < pulls = show progress (10k step) and stop showing "10 PULLS WITHOUT 4 STAR" message
        # comparison to 10M is made just in case ill need it in the future

        if user_command > 1000000:  # if number bigger than 1 million
            print(f'Are you sure? Doing {user_command} pulls would take around {round(50 * user_command / 10000000)} seconds.\n')
            sure = input('Type "CONFIRM" if you want to proceed: ')  # ask user if they're sure
            if sure != "CONFIRM":  # if they're not sure
                print()
                continue  # abort this job and ask for next command
        count += user_command  # if the program came this far, go on with the job
        distribution[100] += user_command
        for i in range(user_command):
            try:
                res, p, w = make_pull(banner_of_choice, pity_info)
            except MemoryError:
                print('The program ran out of memory dude what have you DONE')
                save_archive_to_file(constellations, refinements)
                save_pity_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                                  unique_four_weap_count)
                save_distribution_to_file()
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
            elif res.rarity == 5:
                five_count += 1

            if res.rarity >= verbose_threshold:
                print(
                    Style.RESET_ALL + f'{f"[{win_map[w]}] " if res.rarity >= 4 else ""}{color_map[res.rarity]}{res.name}{f", {p} pity" if res.rarity >= 4 else ""}')
            if verbose_threshold >= 6 and i % 10000 == 0:
                print(f'{i}/{user_command} wishes done')
            if verbose_threshold < 6 and pity_info[1] >= 10:
                print(Fore.CYAN + f"{pity_info[1]} PULLS WITHOUT A 4-STAR!" + Style.RESET_ALL)
        # print(wish_history)
        save_archive_to_file(constellations, refinements)
        save_pity_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count,
                          unique_four_weap_count)
        save_distribution_to_file()
        print()
        print(Style.RESET_ALL + f'{pity_info[0]} pity, {"guaranteed" if pity_info[-2] else "50/50"}')
        try:
            save_history_to_file(wish_history)
        except:
            print('not enough storage to hold this wish history')
    elif user_command < 0:
        print('what are u doing bro')

    else:
        print("I'm not letting you do that. Max 1 billion wishes at a time please")
    print()

if __name__ == '__main__':
    print('\nThank you for using Wish Simulator')