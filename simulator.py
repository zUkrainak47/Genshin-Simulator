# This program is an artifact simulator!

# You can
# 1 - Roll artifacts one-by-one as if you have unlimited resin, upgrade them, save them to your inventory etc.
# 2 - Set a Crit Value requirement and roll artifacts automatically until an artifact with enough CV is found
#     to find out how long that takes - in days and years (assuming all of your resin goes into artifact farming)
#     You can also run multiple tests and find out the average amount of time that took!


import json
import time
from operator import itemgetter
from random import choice, choices
from colorama import init, Fore, Style
from pathlib import Path

init()
Path(".\\banner_info").mkdir(parents=True, exist_ok=True)

class Artifact:
    def __init__(self, artifact_type, mainstat, mainstat_value, threeliner, sub_stats, level, last_upgrade="",
                 roll_value=0):
        self.type = artifact_type
        self.mainstat = mainstat
        self.mainstat_value = mainstat_value
        self.threeliner = threeliner
        self.substats = sub_stats
        self.level = level
        self.last_upgrade = last_upgrade
        self.roll_value = roll_value

        if "Crit RATE%" in self.substats:
            if self.substats["Crit RATE%"] == 23.0:
                self.substats["Crit RATE%"] = 22.9

    def __str__(self):
        val = (self.mainstat_value[0])[self.mainstat_value[1]]
        return f"{val} {self.mainstat} {self.type} (+{self.level})"

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

        print(self)

        for sub in self.substats:
            is_percentage = '%' in sub
            print(
                f"- {sub}: {str(round(self.substats[sub], 1)) if is_percentage else round(self.substats[sub])}{' (+)' if sub == self.last_upgrade else ''}")

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
        if "Crit DMG%" in self.substats:
            # for eyeball:
            crit_value += round(self.substats["Crit DMG%"], 1)
            # for cv like in akasha:
            # crit_value += self.substats["Crit DMG%"]
        if "Crit RATE%" in self.substats:
            # for eyeball:
            crit_value += round(self.substats["Crit RATE%"], 1) * 2
            # for cv like in akasha:
            # crit_value += self.substats["Crit RATE%"] * 2
        return round(crit_value, 1)

    def rv(self):
        return int(self.roll_value)


class ArtifactEncoder(json.JSONEncoder):
    def default(self, artifact):
        return [artifact.type, artifact.mainstat, artifact.mainstat_value, artifact.threeliner, artifact.substats,
                artifact.level, artifact.last_upgrade, artifact.roll_value]


artifact_types = ('Flower', 'Feather', 'Sands', 'Goblet', 'Circlet')
sands_main_stats = ('HP%', 'ATK%', 'DEF%', 'ER%', 'EM')
goblet_main_stats = ('Pyro DMG% Bonus', 'Hydro DMG% Bonus', 'Cryo DMG% Bonus',
                     'Electro DMG% Bonus', 'Anemo DMG% Bonus',
                     'Geo DMG% Bonus', 'Physical DMG% Bonus',
                     'Dendro DMG% Bonus', 'HP%', 'ATK%', 'DEF%', 'EM')
circlet_main_stats = ('HP%', 'ATK%', 'DEF%', 'EM', 'Crit DMG%', 'Crit RATE%',
                      'Healing Bonus')
substats = ('HP', 'ATK', 'DEF', 'HP%', 'ATK%', 'DEF%', 'ER%', 'EM',
            'Crit RATE%', 'Crit DMG%')
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
    'Crit RATE%': 3.889999,
    'Crit DMG%': 7.769999
}
possible_rolls = (0.7, 0.8, 0.9, 1.0)

sands_main_stats_weights = (26.68, 26.66, 26.66, 10.0, 10.0)
goblet_main_stats_weights = (5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 19.25,
                             19.25, 19.0, 2.5)
circlet_main_stats_weights = (22.0, 22.0, 22.0, 4.0, 10.0, 10.0, 10.0)
substats_weights = (6, 6, 6, 4, 4, 4, 4, 4, 3, 3)


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

    print(
        f"Running {int(size)} simulation{'s' if int(size) != 1 else ''}, looking for at least {min(54.5, float(cv))} CV.")
    return size, cv


def load_inventory():
    try:
        with open('.\\inventory.txt') as file:
            data = file.read()
        inv = json.loads(data)
        inv = [Artifact(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]) for a in inv]
        inv = sort_inventory(inv)
        return inv

    except FileNotFoundError:
        with open('.\\inventory.txt', 'w') as file:
            file.write('[]')
        return []


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
        return {int(k): v for k, v in x.items()}
    return x


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

    if mainstat == 'HP':
        mainstat_value = [flower_stats, 0]
    elif mainstat == 'ATK':
        mainstat_value = [feather_stats, 0]
    elif mainstat in ('Pyro DMG% Bonus', 'Hydro DMG% Bonus', 'Cryo DMG% Bonus',
                      'Electro DMG% Bonus', 'Anemo DMG% Bonus',
                      'Geo DMG% Bonus', 'Physical DMG% Bonus',
                      'Dendro DMG% Bonus', 'HP%', 'ATK%'):
        mainstat_value = [hp_atk_dmg_stats, 0]
    elif mainstat == 'DEF%':
        mainstat_value = [def_stats, 0]
    elif mainstat == 'ER%':
        mainstat_value = [er_stats, 0]
    elif mainstat == 'EM':
        mainstat_value = [em_stats, 0]
    elif mainstat == 'Healing Bonus%':
        mainstat_value = [healing_bonus_stats, 0]
    elif mainstat == 'CRIT Rate%':
        mainstat_value = [crit_rate_stats, 0]
    else:
        mainstat_value = [crit_dmg_stats, 0]

    fourliner_weights = (1, 4) if from_where == 'domain' else (1, 2)  # 20% or 33.33% chance for artifact to be 4-liner
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
            print(f'Day {day}: {artifact.cv()} CV ({artifact}) - {artifact.subs()}')

    if silent:
        artifact.last_upgrade = ""

    return artifact, highest_cv


def upgrade_to_next_tier(artifact, do_we_print=True, extra_space=False):
    if artifact.level == 20:
        if do_we_print:
            print("Artifact already at +20\n")

    else:
        if do_we_print:
            print('Upgrading...')
            if extra_space:
                print()

        artifact.upgrade()

        if do_we_print:
            artifact.print_stats()
        else:
            artifact.last_upgrade = ''


def upgrade_to_max_tier(artifact, do_we_print=2, extra_space=False):  # 2 - print everything
    if artifact.level == 20 and do_we_print >= 1:  # 1 - print only status and last upgrade
        print("Artifact already at +20\n")  # 0 - dont print

    else:
        if do_we_print >= 1:
            print('Upgrading to +20...')
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
    with open(r'.\inventory.txt', 'w') as f:
        f.write(json.dumps(artifacts, cls=ArtifactEncoder, separators=(',', ':')))


def save_history_to_file(data):
    with open(r'.\banner_info\wish.txt', 'w') as f:
        f.write(json.dumps(data, separators=(',', ':')))


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


def sort_inventory(artifacts):
    return sorted(artifacts, key=lambda x: (sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))


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


def print_inventory(list_of_artifacts, indexes_to_print=None):
    if indexes_to_print is None:
        needed_indexes = range(len(list_of_artifacts))

    else:
        for current_index in indexes_to_print:
            if current_index == -1 or current_index >= len(artifact_list):
                print(f'No artifact with index "{current_index + 1}" in your inventory. ', end='')
                print(f'Indexes go from 1 to {len(artifact_list)}\n') if len(artifact_list) > 1 else print_empty_inv()
                raise StopIteration

        needed_indexes = indexes_to_print

    print("Inventory:\n")
    t1 = list_of_artifacts[needed_indexes[0]].type
    print('-' * 43, f'{t1}{"s" if t1 != "Sands" else ""}', '-' * 43)

    for this_index in range(len(needed_indexes)):
        current_index = int(needed_indexes[this_index])

        if this_index != 0:
            t_last = list_of_artifacts[needed_indexes[this_index - 1]].type
            t_now = list_of_artifacts[needed_indexes[this_index]].type

            if t_now != t_last:
                print('\n' + '-' * 43, f'{t_now}{"s" if t_now != "Sands" else ""}', '-' * 43)

        print(f'{current_index + 1}) {list_of_artifacts[current_index]} - {list_of_artifacts[current_index].subs()}')


def get_indexes(user_input):
    if ',' in user_input:  # if , in input
        idxs = user_input.split(',')  # split by commas
        # print(idxs)
        case = 'comma'

        for idx in range(len(idxs)):  # for every part separated by ,
            this_index = idxs[idx]

            if this_index == '':
                print('Try removing the space between the indexes (if applicable)\n')
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
                            print(f"\"{this_index}\" doesn't seem like a correct range\n")
                            raise StopIteration

                    else:
                        print(
                            f"Index \"{this_index[0] if not this_index[0].isnumeric() else this_index[1]}\" is non-numeric\n")
                        raise StopIteration

                else:
                    print(
                        f"Index \"{this_index}\" is incorrect, the range must consist of two numbers separated by \"-\"\n")
                    raise StopIteration

            elif not this_index.isnumeric():
                print(f"Index \"{this_index}\" is non-numeric", end='')

                if '[' in this_index:
                    print(f'. Remove the parentheses\n')
                else:
                    print('\n')

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
                    print(f'"{this_index}" doesn\'t seem like a correct range\n')
                    raise StopIteration

            else:
                print(f'Index "{this_index[0] if not this_index[0].isnumeric() else this_index[1]}" is non-numeric',
                      end='')

                if '[' in this_index[0]:
                    print(f'. Remove the parentheses\n')
                else:
                    print('\n')

                raise StopIteration

        else:
            print(f'Index "{user_input}" is incorrect, the range must consist of two numbers separated by "-"\n')
            raise StopIteration
        # print('flatten?', idxs)
        # idxs = flatten_list(idxs)

        case = 'range'

    else:
        if user_input.isnumeric():
            idxs = [user_input]

        else:
            print(f'Index "{user_input}" is non-numeric\n')
            raise StopIteration

        case = 'index'

    # print(list(map(int, idxs)))
    return list(map(int, idxs)), case


def print_empty_inv():
    print('Inventory is empty - try "r 5" to save 5 random artifacts\n')


def print_controls():
    print(
        '\n' + '=' * 43 + ' CONTROLS ' + '=' * 43 + '\n\n'  # aliases included next to each command
        '-------------------------------- ACTIONS WITH GENERATED ARTIFACT -------------------------------\n'
        '\n'
        'a = show generated artifact\n'  # artifact
        '\n'
        'a rv = show its roll value\n'   # rv
        'a cv = show crit value\n'       # cv
        '+ = upgrade to next tier\n'     # a+, a +
        '++ = upgrade to +20\n'          # a++, a ++
        'r = re-roll\n'
        'r++ = re-roll and upgrade to +20\n'  # r ++
        '\n'
        's = save to inventory\n'        # save
        'del = remove/delete from inventory\n'  # d, delete, rm, remove
        '\n'
        'r [number] = re-roll and save a given number of artifacts to the inventory\n'
        'r++ [number] = re-roll, +20, and save a given number of artifacts to the inventory\n'
        '\n'
        '------------------------------------ ACTIONS WITH INVENTORY ------------------------------------\n'
        '\n'
        'inv = show inventory\n'  # inventory
        # this is true for every other inventory command too
        '\n'
        'inv [indexes] = view artifacts from inventory (use indexes from \'inv\' view)\n'
        'inv [indexes] +/++/cv/rv/del = perform action with artifacts from the inventory (pick one)\n'
        '\n'
        'VALID INDEXING: inv 3 | inv 1,4 | inv 1-5 | inv 9,2-6 | inv 5-35\n'
        'INVALID INDEXING: inv [8,9] | inv 7.9 | inv 3, 2 | inv 3 - 8 | inv 4,6-2\n'
        'NOTE: Indexes may change after deletion or upgrading of artifacts due to inventory sorting\n'
        '\n'
        'inv size = view amount of artifacts in inventory\n'  # inv len/inv length
        'inv cv = show artifact with highest crit value\n'
        'inv rv = show artifact with highest roll value\n'
        'inv load = load updates made to inventory.txt\n'
        'inv c = clear inventory\n'  # aliases for 'c': clear, clr
        '\n'
        '---------------------------------------- OTHER COMMANDS ---------------------------------------\n'
        '\n'
        'domain = change artifact source to domain (default)\n'
        'strongbox = change artifact source to strongbox\n'
        'abyss = change artifact source to abyss (same rate as strongbox)\n'
        'source = view current source\n'
        '\n'
        'exit = go back to menu\n'  # 0, menu
        '\n'
        '================================================================================================\n'
        )


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
    print('\n' + '=' * 29 + " MENU " + '=' * 29 + '\n')
    print("0 = exit the simulator\n"
          "1 = roll one artifact at a time\n"
          "2 = roll artifacts until a certain CV is reached\n")


def show_index_changes(old_list, new_list):
    # ty chatgpt this is actually a cool approach
    index_differences = []
    artifact_map = {artifact: i for i, artifact in enumerate(old_list)}

    for i, artifact in enumerate(new_list):
        if artifact != old_list[i]:
            index_differences.append((artifact_map.get(artifact, -1), i))

    if index_differences:
        counter = 0
        print('SOME INVENTORY INDEXES CHANGED:')
        for old, new in index_differences:
            counter += 1
            print(f'{old + 1} -> {new + 1}', end='')
            if counter >= 25:
                print('...')
                print(f'Check your inventory to see all {len(index_differences)} changes')
                break
            print()
        print()


sort_order_type = {'Flower': 0, 'Feather': 1, 'Sands': 2, 'Goblet': 3, 'Circlet': 4}
sort_order_mainstat = {'ATK': 0,
                       'HP': 1,
                       'Crit DMG%': 2, 'Crit RATE%': 3,
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
    "Amber": Character("Amber", "Mondstadt", "Pyro", "Bow", 1.0, 4, 1),
    "Barbara": Character("Barbara", "Mondstadt", "Hydro", "Catalyst", 1.0, 4, 2),
    "Beidou": Character("Beidou", "Liyue", "Electro", "Claymore", 1.0, 4, 3),
    "Bennett": Character("Bennett", "Mondstadt", "Pyro", "Sword", 1.0, 4, 4),
    "Chongyun": Character("Chongyun", "Liyue", "Cryo", "Claymore", 1.0, 4, 5),
    "Diluc": Character("Diluc", "Mondstadt", "Pyro", "Claymore", 1.0, 5, 6),
    "Fischl": Character("Fischl", "Mondstadt", "Electro", "Bow", 1.0, 4, 7),
    "Jean": Character("Jean", "Mondstadt", "Anemo", "Sword", 1.0, 5, 8),
    "Kaeya": Character("Kaeya", "Mondstadt", "Cryo", "Sword", 1.0, 4, 9),
    "Keqing": Character("Keqing", "Liyue", "Electro", "Sword", 1.0, 5, 10),
    "Klee": Character("Klee", "Mondstadt", "Pyro", "Catalyst", 1.0, 5, 11),
    "Lisa": Character("Lisa", "Mondstadt", "Electro", "Catalyst", 1.0, 4, 12),
    "Mona": Character("Mona", "Mondstadt", "Hydro", "Catalyst", 1.0, 5, 13),
    "Ningguang": Character("Ningguang", "Liyue", "Geo", "Catalyst", 1.0, 4, 14),
    "Noelle": Character("Noelle", "Mondstadt", "Geo", "Claymore", 1.0, 4, 15),
    "Qiqi": Character("Qiqi", "Liyue", "Cryo", "Sword", 1.0, 5, 16),
    "Razor": Character("Razor", "Mondstadt", "Electro", "Claymore", 1.0, 4, 17),
    "Sucrose": Character("Sucrose", "Mondstadt", "Anemo", "Catalyst", 1.0, 4, 18),
    "Venti": Character("Venti", "Mondstadt", "Anemo", "Bow", 1.0, 5, 19),
    "Xiangling": Character("Xiangling", "Liyue", "Pyro", "Polearm", 1.0, 4, 20),
    "Xingqiu": Character("Xingqiu", "Liyue", "Hydro", "Sword", 1.0, 4, 21),
    "Diona": Character("Diona", "Mondstadt", "Cryo", "Bow", 1.1, 4, 22),
    "Tartaglia": Character("Tartaglia", "Snezhnaya", "Hydro", "Bow", 1.1, 5, 23),
    "Xinyan": Character("Xinyan", "Liyue", "Pyro", "Claymore", 1.1, 4, 24),
    "Zhongli": Character("Zhongli", "Liyue", "Geo", "Polearm", 1.1, 5, 25),
    "Albedo": Character("Albedo", "Mondstadt", "Geo", "Sword", 1.2, 5, 26),
    "Ganyu": Character("Ganyu", "Liyue", "Cryo", "Bow", 1.2, 5, 27),
    "Hu Tao": Character("Hu Tao", "Liyue", "Pyro", "Polearm", 1.3, 5, 28),
    "Xiao": Character("Xiao", "Liyue", "Anemo", "Polearm", 1.3, 5, 29),
    "Rosaria": Character("Rosaria", "Mondstadt", "Cryo", "Polearm", 1.4, 4, 30),
    "Eula": Character("Eula", "Mondstadt", "Cryo", "Claymore", 1.5, 5, 31),
    "Yanfei": Character("Yanfei", "Liyue", "Pyro", "Catalyst", 1.5, 4, 32),
    "Kaedehara Kazuha": Character("Kazuha", "Inazuma", "Anemo", "Sword", 1.6, 5, 33),
    "Kamisato Ayaka": Character("Ayaka", "Inazuma", "Cryo", "Sword", 2.0, 5, 34),
    "Sayu": Character("Sayu", "Inazuma", "Anemo", "Claymore", 2.0, 4, 35),
    "Yoimiya": Character("Yoimiya", "Inazuma", "Pyro", "Bow", 2.0, 5, 36),
    # "Aloy": Character("Aloy", "None", "Cryo", "Bow", 2.1, 5, 37),
    "Kujou Sara": Character("Kujou Sara", "Inazuma", "Electro", "Bow", 2.1, 4, 38),
    "Raiden Shogun": Character("Raiden Shogun", "Inazuma", "Electro", "Polearm", 2.1, 5, 39),
    "Sangonomiya Kokomi": Character("Kokomi", "Inazuma", "Hydro", "Catalyst", 2.1, 5, 40),
    "Thoma": Character("Thoma", "Inazuma", "Pyro", "Polearm", 2.2, 4, 41),
    "Arataki Itto": Character("Itto", "Inazuma", "Geo", "Claymore", 2.3, 5, 42),
    "Gorou": Character("Gorou", "Inazuma", "Geo", "Bow", 2.3, 4, 43),
    "Shenhe": Character("Shenhe", "Liyue", "Cryo", "Polearm", 2.4, 5, 44),
    "Yun Jin": Character("Yun Jin", "Liyue", "Geo", "Polearm", 2.4, 4, 45),
    "Yae Miko": Character("Yae Miko", "Inazuma", "Electro", "Catalyst", 2.5, 5, 46),
    "Kamisato Ayato": Character("Ayato", "Inazuma", "Hydro", "Sword", 2.6, 5, 47),
    "Kuki Shinobu": Character("Kuki Shinobu", "Inazuma", "Electro", "Sword", 2.7, 4, 48),
    "Yelan": Character("Yelan", "Liyue", "Hydro", "Bow", 2.7, 5, 49),
    "Shikanoin Heizou": Character("Heizou", "Inazuma", "Anemo", "Catalyst", 2.8, 4, 50),
    "Collei": Character("Collei", "Sumeru", "Dendro", "Bow", 3.0, 4, 51),
    "Dori": Character("Dori", "Sumeru", "Electro", "Claymore", 3.0, 4, 52),
    "Tighnari": Character("Tighnari", "Sumeru", "Dendro", "Bow", 3.0, 5, 53),
    "Candace": Character("Candace", "Sumeru", "Hydro", "Polearm", 3.1, 4, 54),
    "Cyno": Character("Cyno", "Sumeru", "Electro", "Polearm", 3.1, 5, 55),
    "Nilou": Character("Nilou", "Sumeru", "Hydro", "Sword", 3.1, 5, 56),
    "Layla": Character("Layla", "Sumeru", "Cryo", "Sword", 3.2, 4, 57),
    "Nahida": Character("Nahida", "Sumeru", "Dendro", "Catalyst", 3.2, 5, 58),
    "Faruzan": Character("Faruzan", "Sumeru", "Anemo", "Bow", 3.3, 4, 59),
    "Wanderer": Character("Wanderer", "Sumeru", "Anemo", "Catalyst", 3.3, 5, 60),
    "Alhaitham": Character("Alhaitham", "Sumeru", "Dendro", "Sword", 3.4, 5, 61),
    "Yaoyao": Character("Yaoyao", "Liyue", "Dendro", "Polearm", 3.4, 4, 62),
    "Dehya": Character("Dehya", "Sumeru", "Pyro", "Claymore", 3.5, 5, 63),
    "Mika": Character("Mika", "Mondstadt", "Cryo", "Polearm", 3.5, 4, 64),
    "Baizhu": Character("Baizhu", "Liyue", "Dendro", "Catalyst", 3.6, 5, 65),
    "Kaveh": Character("Kaveh", "Sumeru", "Dendro", "Claymore", 3.6, 4, 66),
    "Kirara": Character("Kirara", "Inazuma", "Dendro", "Sword", 3.7, 4, 67),
    "Freminet": Character("Freminet", "Fontaine", "Cryo", "Claymore", 4.0, 4, 68),
    "Lynette": Character("Lynette", "Fontaine", "Anemo", "Sword", 4.0, 4, 69),
    "Lyney": Character("Lyney", "Fontaine", "Pyro", "Bow", 4.0, 5, 70),
    "Neuvillette": Character("Neuvillette", "Fontaine", "Hydro", "Catalyst", 4.1, 5, 71),
    "Wriothesley": Character("Wriothesley", "Fontaine", "Cryo", "Catalyst", 4.1, 5, 72),
    "Charlotte": Character("Charlotte", "Fontaine", "Cryo", "Catalyst", 4.2, 4, 73),
    "Furina": Character("Furina", "Fontaine", "Hydro", "Sword", 4.2, 5, 74),
    "Chevreuse": Character("Chevreuse", "Fontaine", "Pyro", "Polearm", 4.3, 4, 75),
    "Navia": Character("Navia", "Fontaine", "Geo", "Claymore", 4.3, 5, 76),
    "Gaming": Character("Gaming", "Liyue", "Pyro", "Claymore", 4.4, 4, 77),
    "Xianyun": Character("Xianyun", "Liyue", "Anemo", "Catalyst", 4.4, 5, 78),
    "Chiori": Character("Chiori", "Inazuma", "Geo", "Sword", 4.5, 5, 79),
    "Arlecchino": Character("Arlecchino", "Snezhnaya", "Pyro", "Polearm", 4.6, 5, 80),
    # "Sigewinne": Character("Sigewinne", "Fontaine", "Hydro", "Bow", 4.7, 5, 81),
    # "Clorinde": Character("Clorinde", "Fontaine", "Electro", "Sword", 4.7, 5, 82),
    # "Sethos": Character("Sethos", "idk", "idk", "idk", 4.7, 4, 83)
}

weapons_dict = {
    "A Thousand Floating Dreams": Weapon("A Thousand Floating Dreams", "Catalyst", 5, 300),
    "Akuoumaru": Weapon("Akuoumaru", "Claymore", 4, 301),
    "Alley Hunter": Weapon("Alley Hunter", "Bow", 4, 302),
    "Amos' Bow": Weapon("Amos' Bow", "Bow", 5, 303),
    "Aqua Simulacra": Weapon("Aqua Simulacra", "Bow", 5, 304),
    "Aquila Favonia": Weapon("Aquila Favonia", "Sword", 5, 305),

    "Beacon of the Reed Sea": Weapon("Beacon of the Reed Sea", "Claymore", 5, 330),
    "Black Tassel": Weapon("Black Tassel", "Polearm", 3, 331),
    "Bloodtainted Greatsword": Weapon("Bloodtainted Greatsword", "Claymore", 3, 332),

    "Calamity Queller": Weapon("Calamity Queller", "Polearm", 5, 360),
    "Cashflow Supervision": Weapon("Cashflow Supervision", "Catalyst", 5, 361),
    "Cool Steel": Weapon("Cool Steel", "Sword", 3, 362),
    "Crane's Echoing Call": Weapon("Crane's Echoing Call", "Catalyst", 5, 363),
    "Crimson Moon's Semblance": Weapon("Crimson Moon's Semblance", "Polearm", 5, 364),

    "Debate Club": Weapon("Debate Club", "Claymore", 3, 390),
    "Dragon's Bane": Weapon("Dragon's Bane", "Polearm", 4, 391),

    "Elegy for the End": Weapon("Elegy for the End", "Bow", 5, 420),
    "Emerald Orb": Weapon("Emerald Orb", "Catalyst", 3, 421),
    "Engulfing Lightning": Weapon("Engulfing Lightning", "Polearm", 5, 422),
    "Everlasting Moonglow": Weapon("Everlasting Moonglow", "Catalyst", 5, 423),
    "Eye of Perception": Weapon("Eye of Perception", "Catalyst", 4, 424),

    "Favonius Codex": Weapon("Favonius Codex", "Catalyst", 4, 450),
    "Favonius Greatsword": Weapon("Favonius Greatsword", "Claymore", 4, 451),
    "Favonius Lance": Weapon("Favonius Lance", "Polearm", 4, 452),
    "Favonius Sword": Weapon("Favonius Sword", "Sword", 4, 453),
    "Favonius Warbow": Weapon("Favonius Warbow", "Bow", 4, 454),
    "Ferrous Shadow": Weapon("Ferrous Shadow", "Claymore", 3, 455),
    "Freedom-Sworn": Weapon("Freedom-Sworn", "Sword", 5, 456),

    "Haran Geppaku Futsu": Weapon("Haran Geppaku Futsu", "Sword", 5, 510),
    "Harbinger of Dawn": Weapon("Harbinger of Dawn", "Sword", 3, 511),
    "Hunter's Path": Weapon("Hunter's Path", "Bow", 4, 512),

    "Jadefall's Splendor": Weapon("Jadefall's Splendor", "Catalyst", 5, 570),

    "Kagura's Verity": Weapon("Kagura's Verity", "Catalyst", 5, 600),
    "Key of Khaj-Nisut": Weapon("Key of Khaj-Nisut", "Sword", 5, 601),

    "Light of Foliar Incision": Weapon("Light of Foliar Incision", "Sword", 5, 630),
    "Lion's Roar": Weapon("Lion's Roar", "Sword", 4, 631),
    "Lithic Blade": Weapon("Lithic Blade", "Claymore", 4, 632),
    "Lithic Spear": Weapon("Lithic Spear", "Polearm", 4, 633),
    "Lost Prayer to the Sacred Winds": Weapon("Lost Prayer to the Sacred Winds", "Catalyst", 5, 634),

    "Magic Guide": Weapon("Magic Guide", "Catalyst", 3, 660),
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
    "Raven Bow": Weapon("Raven Bow", "Bow", 3, 812),
    "Redhorn Stonethresher": Weapon("Redhorn Stonethresher", "Claymore", 5, 813),
    "Rust": Weapon("Rust", "Bow", 4, 814),

    "Sacrificial Bow": Weapon("Sacrificial Bow", "Bow", 4, 840),
    "Sacrificial Fragments": Weapon("Sacrificial Fragments", "Catalyst", 4, 841),
    "Sacrificial Greatsword": Weapon("Sacrificial Greatsword", "Claymore", 4, 842),
    "Sacrificial Sword": Weapon("Sacrificial Sword", "Sword", 4, 843),
    "Sharpshooter's Oath": Weapon("Sharpshooter's Oath", "Bow", 3, 844),
    "Skyrider Sword": Weapon("Skyrider Sword", "Sword", 3, 845),
    "Skyward Atlas": Weapon("Skyward Atlas", "Catalyst", 5, 846),
    "Skyward Blade": Weapon("Skyward Blade", "Sword", 5, 847),
    "Skyward Harp": Weapon("Skyward Harp", "Bow", 5, 848),
    "Skyward Pride": Weapon("Skyward Pride", "Claymore", 5, 849),
    "Skyward Spine": Weapon("Skyward Spine", "Polearm", 5, 850),
    "Slingshot": Weapon("Slingshot", "Bow", 3, 851),
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
    "Thrilling Tales of Dragon Slayers": Weapon("Thrilling Tales of Dragon Slayers", "Catalyst", 3, 878),
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
    print("\n" + "="*19 + " PITY INFORMATION " + "="*18)
    print(f'{counter} wish{"es" if counter != 1 else ""} done so far')
    print(f'Out of them {Fore.YELLOW}{c5} five-star{"s" if c5 != 1 else ""}{Style.RESET_ALL} and {Fore.MAGENTA}{c4} four-star{"s" if c4 != 1 else ""}{Style.RESET_ALL}')
    if p[0] < 10 and p[1] < 10:
        insert1, insert2 = '', ''
    else:
        insert1 = ' ' * (p[0] < 10)
        insert2 = ' ' * (p[1] < 10)
    print(f'{Fore.YELLOW}5*{Style.RESET_ALL} pity = {p[0]},{insert1} {"you're on a 50/50" if not p[-2] else "next is guaranteed to be featured"}')
    print(f'{Fore.MAGENTA}4*{Style.RESET_ALL} pity = {p[1]},{insert2} {"you're on a 50/50" if not p[-1] else "next is guaranteed to be featured"}')


def print_character_archive():
    global sorted_constellations, a
    sorted_constellations = sorted(list(constellations.items()),
                                   key=lambda x: (-x[0].rarity, x[0] not in banner_of_choice[1], -x[1]))
    if sorted_constellations:
        last_rarity = 0
        print("\n" + "="*18 + " CHARACTER ARCHIVE " + "="*18)
        print(f"You own {len(constellations)}/{len(characters_dict)} characters\n"
              f"({unique_five_char_count}/{amount_of_five_stars} {Fore.YELLOW}5*{Style.RESET_ALL}, {len(constellations) - unique_five_char_count}/{amount_of_four_stars} {Fore.MAGENTA}4*{Style.RESET_ALL})")
        for a in sorted_constellations:
            if a[0].rarity != last_rarity:
                print(Style.RESET_ALL + "-"*23 + f' {a[0].rarity} STARS ' + "-"*23 + print_map[a[0].rarity])
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
        print("\n" + "="*20 + " WEAPON ARCHIVE " + "="*19)
        print(f"You own {len(refinements)}/{len(weapons_dict)} different gacha weapons\n"
              f"({unique_five_weap_count}/{amount_of_five_star_weapons} {Fore.YELLOW}5*{Style.RESET_ALL}, {unique_four_weap_count}/{amount_of_four_star_weapons} {Fore.MAGENTA}4*{Style.RESET_ALL}, {len(refinements) - unique_five_weap_count - unique_four_weap_count}/{amount_of_three_star_weapons} {Fore.BLUE}3*{Style.RESET_ALL})")
        for a in sorted_refinements:
            if a[0].rarity != last_rarity:
                print(Style.RESET_ALL + "-"*23 + f' {a[0].rarity} STARS ' + "-"*23 + print_map[a[0].rarity])
                last_rarity = a[0].rarity
            print(f'r{a[1]} {a[0].name}')
        print(Style.RESET_ALL)
        return True
    return False


def show_full_inventory():
    print()
    if not print_character_archive():
        if not print_weapon_archive():
            print('Do a wish first to see your character/weapon archive!')
    else:
        print_weapon_archive()
    print()


def print_history_page():  # no idea how this works anymore
    global print_from, print_to, cc, number, print_map
    print_from = -((page - 1) * 25) - 1
    print_to = -(min(page * 25, len(wish_history[banner_of_choice[0]]))) - 1
    cc = -print_from - 1
    print(Style.RESET_ALL + '-' * 51)
    for number in wish_history[banner_of_choice[0]][print_from:print_to:-1]:
        cc += 1
        print(print_map[number_to_item_dict[number].rarity] + f'{cc}.{" " if len(str(cc)) < len(str(print_to)) else ""}',
              number_to_item_dict[number].name)
    print(Style.RESET_ALL + '-' * 51)
    print(f'\n(Page {page}/{num_of_pages})\n')


if __name__ == '__main__':
    mode = 'artifact'
    if mode == 'artifact':
        try:
            artifact_list = load_inventory()
            print('Loading successful')
            # print_inventory(artifact_list)
            # print()
        except json.decoder.JSONDecodeError:
            print('Something off with inventory file. Clearing inventory.txt')
            artifact_list = []
            save_inventory_to_file(artifact_list)
            print('Inventory cleared')

        while True:
            print_menu()

            while True:
                automate = input('Your pick: ').strip()
                if automate.lower() in valid_picks:
                    break
                else:
                    print('Commands are 0, 1 or 2\n')

            print("For the list of commands, type 'help'\n" if automate == '1' else "")
            print('=' * 64)

            if automate == "2":
                sample_size, cv_desired = take_input()

                if sample_size == 'exit' or cv_desired == 'exit':
                    print("Going back to menu")
                    continue
                else:
                    sample_size, cv_desired = int(sample_size), float(cv_desired)

                days_it_took_to_reach_desired_cv = []
                artifacts_generated = []
                absolute_generated = 0
                low = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))
                high = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))
                start = time.perf_counter()
                sample_size_is_one = sample_size == 1

                for i in range(sample_size):
                    c = 0
                    day = 0
                    highest = 0.1
                    total_generated = 0
                    inventory = 0
                    flag = False
                    print(f'\nSimulation {i + 1}:' if sample_size > 1 else '')

                    while not flag:
                        day += 1

                        if day % 10000 == 0:
                            print(f'Day {day} - still going')

                        if day % 15 == 1:  # 4 artifacts from abyss every 15 days
                            for k in range(4):
                                inventory += 1
                                total_generated += 1
                                absolute_generated += 1
                                art, highest = create_and_roll_artifact("abyss", highest)
                                low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                                    compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv,
                                                          artifacts_generated,
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
                            absolute_generated += amount[0]
                            inventory += amount[0]
                            for k in range(amount[0]):
                                art, highest = create_and_roll_artifact("domain", highest)
                                low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                                    compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv,
                                                          artifacts_generated,
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
                                absolute_generated += 1
                                art, highest = create_and_roll_artifact("strongbox", highest)
                                low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                                    compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv,
                                                          artifacts_generated,
                                                          day, total_generated, cv_desired, sample_size_is_one))
                                if flag:
                                    break
                            # print(f'{inventory} left in inventory')

                end = time.perf_counter()
                run_time = end - start
                to_hours = time.strftime("%T", time.gmtime(run_time))
                decimals = f'{(run_time % 1):.3f}'

                print()
                days = round(sum(days_it_took_to_reach_desired_cv) / sample_size, 2)

                if sample_size > 1:
                    print(
                        f'Out of {sample_size} simulations, it took an average of {days} days ({round(days / 365.25, 2)} years) to reach at least {cv_desired} CV.')
                    print(f'Fastest - {low[0]} day{"s" if low[0] > 1 else ""}: {low[1].subs()}')
                    print(
                        f'Slowest - {high[0]} day{"s" if high[0] > 1 else ""} ({round(high[0] / 365.25, 2)} years): {high[1].subs()}')

                else:
                    print(f'It took {low[0]} days (or {round(high[0] / 365.25, 2)} years)!')

                print(f'Total artifacts generated: {sum(artifacts_generated)}\n')
                print(
                    f'The simulation{"s" if sample_size > 1 else ""} took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
                print(f'Performance: {round(sum(artifacts_generated) / run_time / 1000, 2)} artifacts per ms')

            elif automate == "1":
                source = "domain"
                print()
                art = create_artifact(source)
                art.print_stats()

                while True:
                    user_command = input('Command: ').lower().strip()
                    if user_command in valid_help:
                        print_controls()

                    elif '"' in user_command or "'" in user_command:
                        print('Remove the quotation marks\n')
                        continue

                    elif user_command in ('+', 'a+', 'a +'):
                        upgrade_to_next_tier(art, True, True)
                        if art in artifact_list:
                            artifact_list = sort_inventory(artifact_list)
                            save_inventory_to_file(artifact_list)

                    elif user_command in ('++', 'a++', 'a ++'):
                        upgrade_to_max_tier(art, 2, True)
                        if art in artifact_list:
                            artifact_list = sort_inventory(artifact_list)
                            save_inventory_to_file(artifact_list)

                    elif user_command[:3] == 'r++' or user_command[:4] == 'r ++':
                        if user_command in ('r++', 'r ++'):
                            print('Re-rolling and upgrading...\n')
                            art, _ = create_and_roll_artifact(source)
                            continue

                        else:
                            if 'r++' in user_command:
                                if len(user_command.split()) == 2:
                                    _, cmd = user_command.split()
                                else:
                                    print('Nuh uh. Only put one number after r++\n')
                                    continue

                            else:  # if it's "r ++ [indexes]" (I want to support both)
                                if len(user_command.split()) == 3:
                                    _, _, cmd = user_command.split()
                                else:
                                    print('Nuh uh. Only put one number after r ++\n')
                                    continue

                            if cmd.isnumeric():
                                cmd = int(cmd)

                                for i in range(cmd):
                                    art, _ = create_and_roll_artifact(source, 0, True)
                                    artifact_list.append(art)

                                artifact_list = sort_inventory(artifact_list)
                                save_inventory_to_file(artifact_list)

                                print(f'{cmd} new +20 artifact{"s" if cmd > 1 else ""} added to inventory\n')
                                continue
                                # print_inventory(artifact_list)
                                # print()

                            else:
                                print(f'{cmd} is not a valid number\n')
                                continue

                    elif user_command == 'r':
                        print('Re-rolling...\n')
                        art = create_artifact(source)
                        art.print_stats()

                    elif user_command[:2] == 'r ':
                        if len(user_command.split()) == 2:
                            _, cmd = user_command.split()
                        else:
                            print('Nuh uh. Only put one number after r\n')
                            continue

                        if cmd.isnumeric():
                            cmd = int(cmd)

                            for i in range(cmd):
                                art = create_artifact(source)
                                artifact_list.append(art)

                            artifact_list = sort_inventory(artifact_list)
                            save_inventory_to_file(artifact_list)

                            print(f'{cmd} new +0 artifact{"s" if cmd > 1 else ""} added to inventory\n')
                            continue
                            # print_inventory(artifact_list)
                            # print()

                        else:
                            print(f'{cmd} is not a valid number\n')
                            continue

                    elif user_command in ('s', 'save'):
                        if art not in artifact_list:
                            artifact_list.append(art)
                            len_artifact_list = len(artifact_list)

                            artifact_list = sort_inventory(artifact_list)
                            save_inventory_to_file(artifact_list)

                            print(
                                f'Saved - {len_artifact_list} artifact{"s" if len_artifact_list > 1 else ""} in inventory\n')

                        else:
                            print('Already saved this artifact\n')

                    elif user_command in ('d', 'del', 'delete', 'rm', 'remove'):
                        if art in artifact_list:
                            artifact_list.remove(art)
                            len_artifact_list = len(artifact_list)

                            save_inventory_to_file(artifact_list)
                            print(
                                f'Removed - {len_artifact_list} artifact{"s" if len_artifact_list != 1 else ""} in inventory\n')

                        else:
                            print('This artifact is not in your inventory\n')

                    elif 'inv' in user_command:
                        user_command = user_command.split()
                        if user_command[0] in ('inv', 'inventory'):
                            pass
                        else:
                            print('Inventory commands must start with "inv".\n'
                                  'If you want to pass any arguments, you must put a space after "inv".\n')
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
                                    print(f'No artifact with index "{i}" in your inventory. ', end='')
                                    print(f'Indexes go from 1 to {len(artifact_list)}\n') if len(
                                        artifact_list) > 0 else print_empty_inv()
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
                                            print(f'{index + 1}) ', end='')
                                        upgrade_to_next_tier(arti_list[iterative_index], do_print)

                                    elif cmd == '++':
                                        if do_print:
                                            print(f'{index + 1}) ', end='')
                                        upgrade_to_max_tier(arti_list[iterative_index], do_print)

                                    elif cmd == 'rv':
                                        print(f'{index + 1}) RV: {arti_list[iterative_index].rv()}%')

                                    elif cmd == 'cv':
                                        print(f'{index + 1}) CV: {arti_list[iterative_index].cv()}')

                                    elif cmd in ('d', 'del', 'delete', 'rm', 'remove'):
                                        if arti_list[iterative_index] in artifact_list:
                                            artifact_list.remove(arti_list[iterative_index])

                                    else:
                                        print(f'"{cmd}" is not a valid command\n')

                                if cmd in ('d', 'del', 'delete', 'rm', 'remove'):
                                    save_inventory_to_file(artifact_list)
                                    print(f'Artifact{"s" if len(indexes) > 1 else ""} removed\n')
                                    show_index_changes(artifact_list_old, artifact_list)

                                if cmd in ('+', '++'):
                                    if not do_print:
                                        print("Done! Artifacts upgraded\n")
                                    elif len(indexes) > 1:
                                        print()

                                    artifact_list_new = sort_inventory(artifact_list)
                                    show_index_changes(artifact_list, artifact_list_new)

                                    artifact_list = artifact_list_new
                                    save_inventory_to_file(artifact_list)

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
                                    artifact_list[int(cmd) - 1].print_stats()

                                else:
                                    print(f'No artifact with index "{cmd}" in your inventory. ', end='')

                                    if len(artifact_list) > 0:
                                        print(f'Indexes go from 1 to {len(artifact_list)}\n')
                                    else:
                                        print_empty_inv()

                            elif cmd in ('clear', 'clr', 'c'):
                                artifact_list.clear()
                                save_inventory_to_file(artifact_list)
                                print('Inventory cleared\n')

                            elif cmd == 'cv':
                                big_cv = max(artifact_list, key=lambda x: x.cv())
                                print(f'{artifact_list.index(big_cv) + 1}) {big_cv} - {big_cv.subs()}')
                                print(f'CV: {big_cv.cv()}')
                                print()

                            elif cmd == 'rv':
                                big_rv = max(artifact_list, key=lambda x: x.rv())
                                print(f'{artifact_list.index(big_rv) + 1}) {big_rv} - {big_rv.subs()}')
                                print(f'RV: {big_rv.rv()}%')
                                print()

                            elif cmd in ('size', 'len', 'length'):
                                print(
                                    f'{len(artifact_list)} artifact{"s" if len(artifact_list) != 1 else ""} in inventory',
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
                                    print(f'{flower_count} Flower{"s" if flower_count != 1 else ""}\n'
                                          f'{feather_count} Feather{"s" if feather_count != 1 else ""}\n'
                                          f'{sands_count} Sands\n'
                                          f'{goblet_count} Goblet{"s" if goblet_count != 1 else ""}\n'
                                          f'{circlet_count} Circlet{"s" if circlet_count != 1 else ""}\n')
                                else:
                                    print('\n')

                            elif cmd == 'load':
                                try:
                                    artifact_list = load_inventory()
                                    print('Loading successful')
                                    if len(artifact_list) == 0:
                                        print('Inventory is empty')
                                    else:
                                        if len(artifact_list) <= 25:
                                            print()
                                            print_inventory(artifact_list)
                                    print()

                                except json.decoder.JSONDecodeError:
                                    print('Something off with inventory file. Clearing inventory.txt')
                                    artifact_list = []
                                    save_inventory_to_file(artifact_list)
                                    print('Inventory cleared\n')

                            else:
                                print(f'"{cmd}" is not a valid inventory command or index\n')
                        else:
                            print(
                                'U did something wrong.\nIf you tried inputting multiple indexes, remove spaces between them\n')

                    elif user_command == 'domain':
                        source = 'domain'
                        print('Source set to domain\n')

                    elif user_command in ('strongbox', 'abyss'):
                        source = user_command
                        print(f'Source set to {source}\n')

                    elif user_command == 'source':
                        print(f'Current source: {source}\n')

                    elif user_command in ('a rv', 'rv'):
                        print(f'RV: {art.rv()}%\n')

                    elif user_command in ('a cv', 'cv'):
                        print(f'CV: {art.cv()}\n')

                    elif user_command in ('artifact', 'a'):
                        print()
                        art.print_stats()

                    elif user_command in ('exit', 'menu', '0'):
                        print('Exiting...')
                        break

                    else:
                        print("Try 'help'\n")

            else:
                break

    elif mode == 'banner':
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
            save_pity_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count)
            print("Everything cleared!")

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

        banner_types = ["character", "weapon", "standard", "chronicled"]

        # print([c in standard_characters for c in character_banner_list["venti-1"]])


        def make_pull(banner_info, pity):
            global legal_standard_four_stars, legal_standard_five_stars
            five_star_chance, four_star_chance = get_chances(banner_info[0], pity)
            rarity = 5 if choices((True, False), (five_star_chance, 100-five_star_chance))[0] \
                else 4 if choices((True, False), (four_star_chance, 100-four_star_chance))[0] else 3
            if banner_info[0] == 'character':
                featured_five_star = banner_info[1][0]
                featured_four_stars = banner_info[1][1:]

                if rarity == 5:
                    # print(f'{Style.RESET_ALL}{five_star_chance}')
                    if pity[-2]:
                        result = [featured_five_star, pity[0] + 1]
                        pity[-2] = False
                    else:
                        result = [choice((featured_five_star, choice(legal_standard_five_stars))), pity[0] + 1]
                        if result[0] != featured_five_star:
                            pity[-2] = True
                    pity[0] = 0
                    pity[1] += 1

                elif rarity == 4:
                    # print(f'{Style.RESET_ALL}{four_star_chance}')
                    if pity[-1]:
                        result = [choice(featured_four_stars), pity[1] + 1]
                        pity[-1] = False
                    else:
                        result = [choice(choices((featured_four_stars, legal_standard_four_stars, standard_4_star_weapons), [50, 25, 25])[0]), pity[1] + 1]
                        if result[0] not in featured_four_stars:
                            pity[-1] = True
                    pity[0] += 1
                    pity[1] = 0

                elif rarity == 3:
                    result = [choice(three_star_weapons), 0]
                    pity[0] += 1
                    pity[1] += 1

            # elif banner_info[0] == 'weapon':
            #     result = [0, 0]
            wish_history[banner_info[0]].append(result[0].num)
            pities[banner_info[0]] = pity
            return result

        def get_chances(banner_type, pity):  # returns (% to get 5 star, % to get 4 star)
            if banner_type != 'weapon':         # + 1 here to check the number of the next pull you're making
                five_star_chance = max(0, pity[0] + 1 - 73) * 6 + 0.6  # every pull above 73 adds 6%
                four_star_chance = 100 if pity[1] + 1 >= 10 else (56.1 if pity[1] + 1 == 9 else 5.1)
                # 10+ pity = 4 star in case of no 5 star, 9 pity = 56.1% chance, <9 = 5.6%

            else:
                five_star_chance = max(0, pity[0] + 1 - 62) * 7 + 0.7
                four_star_chance = 100 if pity[1] + 1 >= 10 else (66 if pity[1] + 1 == 9 else 6)

            return five_star_chance, four_star_chance


        user_banner_input = 'character', "ganyu-4"
        banner_of_choice = (user_banner_input[0], character_banner_list[user_banner_input[1]][0], character_banner_list[user_banner_input[1]][1])
        legal_standard_four_stars = [s for s in standard_4_star_characters if (s not in banner_of_choice[1] and s.version < banner_of_choice[-1])]
        legal_standard_five_stars = [s for s in standard_5_star_characters if (s not in banner_of_choice[1] and s.version < banner_of_choice[-1])]
        pity_info = pities[banner_of_choice[0]]

        three_stars = '(   * * *   )'
        four_stars = '(  * * * *  )'
        five_stars = '( * * * * * )'
        print_map = {3: Fore.BLUE, 4: Fore.MAGENTA, 5: Fore.YELLOW}
        verbose_threshold = 3

        print()
        while True:
            a = input('Command: ').lower().strip()
            if a == 'pity':
                print_pity(count, pity_info, five_count, four_count)
                print()
                continue

            if a == 'info':
                print_pity(count, pity_info, five_count, four_count)

            if a in ('inv', 'info'):
                show_full_inventory()
                continue

            if a == 'h':
                if len(wish_history[banner_of_choice[0]]):
                    num_of_pages = (len(wish_history[banner_of_choice[0]]) - 1)//25 + 1
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
                                amount = min(int(cmd[1]), num_of_pages-page)

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
                                amount = min(int(cmd[1]), page-1)

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
                                    print(Fore.YELLOW + '                 You found page 0')
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

            if a == 'clear':
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
                pity_info = pities[banner_of_choice[0]]
                count = 0
                five_count = 0
                four_count = 0
                unique_five_char_count = 0
                unique_five_weap_count, unique_four_weap_count = 0, 0
                save_pity_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count)

                wish_history = {"character": [], "weapon": [], "standard": [], "chronicled": []}
                save_history_to_file(wish_history)

                print('Done\n')
                continue

            try:
                a = int(a)
            except ValueError:
                print('Try "help"\n')
                continue

            if 0 <= a <= 1000000000:
                print()
                if a == 0:
                    print_pity(count, pity_info, five_count, four_count)
                    show_full_inventory()
                    break
                verbose_threshold = 6 - (a <= 1000000) - (a <= 100000) - (a <= 10000)
                if a > 1000000:  # if number bigger than 1 million
                    print(f'Are you sure? Doing {a} pulls would take around {round(43 * a/10000000)} seconds.\n')
                    sure = input('Type "CONFIRM" if you want to proceed: ')  # ask user if they're sure
                    if sure != "CONFIRM":  # if they're not sure
                        print()
                        continue  # abort this job and ask for next command
                count += a  # if the program came this far, go on with the job
                for i in range(a):
                    res, p = make_pull(banner_of_choice, pity_info)
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
                        print(print_map[res.rarity] + f'{res.name}{f", {p} pity" if res.rarity >= 4 else ""}')
                    if verbose_threshold == 6 and i % 10000 == 0:
                        print(f'{i}/{a} wishes done')
                    if pity_info[1] >= 10:
                        print(Fore.CYAN + f"{pity_info[1]} PULLS WITHOUT A 4-STAR!" + Style.RESET_ALL)
                # print(wish_history)
                save_archive_to_file(constellations, refinements)
                save_pity_to_file(pities, count, five_count, four_count, unique_five_char_count, unique_five_weap_count, unique_four_weap_count)
                print()
                print(Style.RESET_ALL + f'{pity_info[0]} pity, {"guaranteed" if pity_info[-2] else "50/50"}')
                save_history_to_file(wish_history)
            elif a < 0:
                print('what are u doing bro')

            else:
                print("I'm not letting you do that. Max 1 billion wishes at a time please")
            print()

    print('\nThank you for using Artifact Simulator')
