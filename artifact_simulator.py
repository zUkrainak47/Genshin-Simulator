# This program is an artifact simulator!

# You can
# 1 - Roll artifacts one-by-one as if you have unlimited resin, upgrade them, save them to your inventory etc.
# 2 - Set a Crit Value requirement and roll artifacts automatically until an artifact with enough CV is found
#     to find out how long that takes - in days and years (assuming all of your resin goes into artifact farming)
#     You can also run multiple tests and find out the average amount of time that took!


import json
import time
from colorama import init, Fore, Style
from operator import itemgetter
from random import choice, choices

init()

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

        if "CRIT Rate%" in self.substats:
            if self.substats["CRIT Rate%"] == 23.0:
                self.substats["CRIT Rate%"] = 22.9

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
        print(" ", end='')
        print(self)

        for sub in self.substats:
            is_percentage = '%' in sub
            print(
                f" - {sub}: {str(round(self.substats[sub], 1)) if is_percentage else round(self.substats[sub])}{f' {Fore.GREEN}(+){Style.RESET_ALL}' if sub == self.last_upgrade else ''}")

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


def load_inventory():
    try:
        with open('inventory.txt') as file:
            data = file.read()
        inv = json.loads(data)
        inv = [Artifact(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]) for a in inv]
        inv = sort_inventory(inv)
        return inv

    except FileNotFoundError:
        with open('inventory.txt', 'w') as file:
            file.write('[]')
        return []


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
            print(f' Day {day}: {artifact.cv()} CV ({artifact}) - {artifact.subs()}')

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
    with open('inventory.txt', 'w') as f:
        f.write(json.dumps(artifacts, cls=ArtifactEncoder, separators=(',', ':')))


def sort_inventory(artifacts):
    return sorted(artifacts, key=lambda x: (sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))


def print_inventory(list_of_artifacts, indexes_to_print=None):
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
    print('-' * 44, f'{Fore.LIGHTCYAN_EX}{t1}{"s" if t1 != "Sands" else ""}{Style.RESET_ALL}', '-' * 44)

    for this_index in range(len(needed_indexes)):
        current_index = int(needed_indexes[this_index])

        if this_index != 0:
            t_last = list_of_artifacts[needed_indexes[this_index - 1]].type
            t_now = list_of_artifacts[needed_indexes[this_index]].type

            if t_now != t_last:
                print('\n' + '-' * 44, f'{Fore.LIGHTCYAN_EX}{t_now}{"s" if t_now != "Sands" else ""}{Style.RESET_ALL}', '-' * 44)

        print(f' {current_index + 1}) {list_of_artifacts[current_index]} - {list_of_artifacts[current_index].subs()}')


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


def print_controls():
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
        f' {Fore.BLUE}s{Style.RESET_ALL} = save to inventory\n'        # save
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
        f' {Fore.CYAN}inv {Fore.MAGENTA}[indexes]{Style.RESET_ALL} = view artifacts from inventory (use indexes from \'inv\' view)\n'
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
        '\n'
        f' {Fore.LIGHTCYAN_EX}source{Style.RESET_ALL} = view current source\n'
        f' {Fore.CYAN}domain{Style.RESET_ALL} = change artifact source to domain (default)\n'
        f' {Fore.CYAN}strongbox{Style.RESET_ALL} = change artifact source to strongbox\n'
        f' {Fore.CYAN}abyss{Style.RESET_ALL} = change artifact source to abyss (same rate as strongbox)\n'
        '\n'
        f' {Fore.LIGHTCYAN_EX}0{Style.RESET_ALL} = exit Artifact Simulator\n'  # 0, menu
        '\n'
        '==================================================================================================\n'
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
    print('\n' + '=' * 30 + " MENU " + '=' * 30 + '\n')
    print(" 0 = exit Artifact Simulator\n"
          " 1 = roll one artifact at a time\n"
          " 2 = roll artifacts until a certain CV is reached\n")


def show_index_changes(old_list, new_list):
    # ty chatgpt this is actually a cool approach
    index_differences = []
    artifact_map = {artifact: i for i, artifact in enumerate(old_list)}

    for i, artifact in enumerate(new_list):
        if artifact != old_list[i]:
            index_differences.append((artifact_map.get(artifact, -1), i))

    if index_differences:
        counter = 0
        print(f' {Fore.LIGHTMAGENTA_EX}SOME INVENTORY INDEXES CHANGED:{Style.RESET_ALL}')
        for old, new in index_differences:
            counter += 1
            print(f' {old + 1} -> {new + 1}', end='')
            if counter >= 25:
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

source = 'domain'
print(f'\n Type {Fore.LIGHTCYAN_EX}help{Style.RESET_ALL} for the list of commands\n')
art = create_artifact(source)
artifact_log = [art]
art.print_stats()


def print_log():
    for this_index in range(1, len(artifact_log) + 1):
        if art == artifact_log[-this_index]:
            color = Fore.GREEN
        else:
            color = ''
        print(
            f' {color}{this_index}) {artifact_log[-this_index]} - {artifact_log[-this_index].subs()}{Style.RESET_ALL}')
    print()

day = 0
def run_simulation(i):
    global day
    day = 0
    highest = 0.1
    total_generated = 0
    inventory = 0
    print(f'\n {Fore.LIGHTMAGENTA_EX}Simulation {i + 1}:{Style.RESET_ALL}' if sample_size > 1 else '')

    def gen_artifact(source):
        nonlocal total_generated, highest
        total_generated += 1
        art, highest = create_and_roll_artifact(source, highest)
        return art
 
    while True:
        day += 1

        if day % 10000 == 0:
            print(f' {Fore.MAGENTA}Day {day} - still going{Style.RESET_ALL}')

        if day % 15 == 1:  # 4 artifacts from abyss every 15 days
            for _ in range(4):
                inventory += 1
                art = gen_artifact('abyss')
                if art.cv() >= cv_desired:
                    return total_generated, day, art

        resin = 180

        if day % 7 == 1:  # 1 transient resin from tubby every monday
            resin += 60

        while resin:
            # print('domain run')
            resin -= 20
            amount = choices((1, 2), weights=(28, 2))[0]  # 6.66% chance for 2 artifacts
            # if amount == 2:
            #     print('lucky!')
            inventory += amount
            for _ in range(amount):
                art = gen_artifact('domain')
                if art.cv() >= cv_desired:
                    return total_generated, day, art

        while inventory >= 3:
            # print(f'strongbox {inventory}')
            inventory -= 2
            art = gen_artifact('strongbox')
            if art.cv() >= cv_desired:
                return total_generated, day, art
            # print(f'{inventory} left in inventory')
    raise Exception('should not reach here')


while True:
    user_command = input(' Command: ').lower().strip()
    if user_command in valid_help:
        print_controls()

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
            cv_desired = min(54.5, cv_desired)

        days_it_took_to_reach_desired_cv = []
        artifacts_generated = []
        low = (1000000, Artifact('this', 'needs', 'to', 'be', 'done', 0))
        high = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))
        start = time.perf_counter()

        for i in range(sample_size):
            total_generated, day, art = run_simulation(i)
            
            artifacts_generated.append(total_generated)
            days_it_took_to_reach_desired_cv.append(day)
            low = min(low, (day, art))
            high = max(high, (day, art))
            if not sample_size == 1:
                print(f' Artifacts generated: {Fore.MAGENTA}{total_generated}{Style.RESET_ALL}')

        end = time.perf_counter()
        run_time = end - start
        to_hours = time.strftime("%T", time.gmtime(run_time))
        decimals = f'{(run_time % 1):.3f}'

        print()
        days = round(sum(days_it_took_to_reach_desired_cv) / sample_size, 2)

        if sample_size > 1:
            print(
                f' Out of {sample_size} simulations, it took an average of {Fore.LIGHTCYAN_EX}{days}{Style.RESET_ALL} days ({round(days / 365.25, 2)} years) to reach at least {cv_desired} CV.')
            print(f' Fastest - {low[0]} day{"s" if low[0] > 1 else ""}: {low[1].subs()}')
            print(
                f' Slowest - {high[0]} day{"s" if high[0] > 1 else ""} ({round(high[0] / 365.25, 2)} years): {high[1].subs()}')

        else:
            print(f' It took {Fore.LIGHTCYAN_EX}{low[0]} days{Style.RESET_ALL} (or {round(high[0] / 365.25, 2)} years)!')

        print(f' Total artifacts generated: {Fore.MAGENTA}{sum(artifacts_generated)}{Style.RESET_ALL}\n')
        print(
            f' The simulation{"s" if sample_size > 1 else ""} took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
        print(f' Performance: {round(sum(artifacts_generated) / run_time / 1000, 2)} artifacts per ms')
        print()
        print('=' * 27 + f' {Fore.LIGHTCYAN_EX}NORMAL MODE{Style.RESET_ALL} ' + '=' * 26)
        print()

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

    elif user_command == 'r':
        print(f' {Fore.LIGHTMAGENTA_EX}Re-rolling...{Style.RESET_ALL}\n')
        art = create_artifact(source)
        artifact_log.append(art)
        if len(artifact_log) > 10:
            artifact_log = artifact_log[1:]
        art.print_stats()

    elif user_command in ('r++', 'r ++'):
        print(f' {Fore.LIGHTMAGENTA_EX}Re-rolling and upgrading...{Style.RESET_ALL}\n')
        art, _ = create_and_roll_artifact(source)
        artifact_log.append(art)
        if len(artifact_log) > 10:
            artifact_log = artifact_log[1:]

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

                print(f' {Fore.LIGHTGREEN_EX}{cmd} new +20 artifact{"s" if cmd > 1 else ""} added to inventory{Style.RESET_ALL}\n')
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

                print(f' {Fore.LIGHTGREEN_EX}{cmd} new +0 artifact{"s" if cmd > 1 else ""} added to inventory{Style.RESET_ALL}\n')
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

                print(f' {Fore.LIGHTGREEN_EX}Saved - {len_artifact_list} artifact{"s" if len_artifact_list > 1 else ""} in inventory{Style.RESET_ALL}\n')
            else:
                print(f' {Fore.RED}Inventory full (100k artifacts).\n'
                      f' {Fore.LIGHTMAGENTA_EX}Delete some artifacts first to continue saving.\n'
                      f' You may still generate artifacts without saving them.{Style.RESET_ALL}\n')
        else:
            print(f' {Fore.LIGHTMAGENTA_EX}Already saved this artifact{Style.RESET_ALL}\n')

    elif user_command in ('d', 'del', 'delete', 'rm', 'remove'):
        if art in artifact_list:
            artifact_list.remove(art)
            len_artifact_list = len(artifact_list)

            save_inventory_to_file(artifact_list)
            print(
                f' {Fore.LIGHTGREEN_EX}Removed - {len_artifact_list} artifact{"s" if len_artifact_list != 1 else ""} in inventory{Style.RESET_ALL}\n')

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
                            print(f' {index + 1})', end='')
                        upgrade_to_next_tier(arti_list[iterative_index], do_print)

                    elif cmd == '++':
                        if do_print:
                            print(f' {index + 1})', end='')
                        upgrade_to_max_tier(arti_list[iterative_index], do_print)

                    elif cmd == 'rv':
                        print(f' {index + 1}) RV: {arti_list[iterative_index].rv()}%')

                    elif cmd == 'cv':
                        print(f' {index + 1}) CV: {arti_list[iterative_index].cv()}')

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
                        print(f" {Fore.LIGHTGREEN_EX}Done! Artifacts upgraded{Style.RESET_ALL}\n")
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
                print(f' {artifact_list.index(big_cv) + 1}) {big_cv} - {big_cv.subs()}')
                print(f' CV: {big_cv.cv()}')
                print()

            elif cmd == 'rv':
                big_rv = max(artifact_list, key=lambda x: x.rv())
                print(f' {artifact_list.index(big_rv) + 1}) {big_rv} - {big_rv.subs()}')
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

    elif user_command in ('domain', 'strongbox', 'abyss'):
        source = user_command
        print(f' Source set to {Fore.LIGHTGREEN_EX}{source}{Style.RESET_ALL}\n')

    elif user_command == 'source':
        print(f' Current source: {Fore.LIGHTGREEN_EX}{source}{Style.RESET_ALL}\n')

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
