from random import choice, choices
import time, json
from operator import itemgetter


class Artifact:
    def __init__(self, type, mainstat, mainstat_value, threeliner, substats, level, last_upgrade="", roll_value=0):
        self.type = type
        self.mainstat = mainstat
        self.mainstat_value = mainstat_value
        self.threeliner = threeliner
        self.substats = substats
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
        sub_stats = {
            sub: round(self.substats[sub], 1)
            if "%" in sub else round(self.substats[sub])
            for sub in self.substats
        }
        return sub_stats

    def print_stats(self):
        print(self)
        for i in self.substats:
            is_percentage = '%' in i
            print(
                f"- {i}: {str(round(self.substats[i], 1)) if is_percentage else round(self.substats[i])}{' (+)' if i == self.last_upgrade else ''}")
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
            crit_value += round(self.substats["Crit DMG%"], 1)
        if "Crit RATE%" in self.substats:
            crit_value += round(self.substats["Crit RATE%"], 1) * 2
        return round(crit_value, 1)

    def rv(self):
        return int(self.roll_value)


class ArtifactEncoder(json.JSONEncoder):
    def default(self, art):
        return [art.type, art.mainstat, art.mainstat_value, art.threeliner, art.substats, art.level, art.last_upgrade,
                art.roll_value]


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
    'ATK': 19.4500007629394,
    'DEF': 23.1499996185302,
    'HP%': 5.8335,
    'ATK%': 5.8335,
    'DEF%': 7.28999972343444,
    'EM': 23.3099994659423,
    'ER%': 6.48000016808509,
    'Crit RATE%': 3.88999991118907,
    'Crit DMG%': 7.76999965310096
}
possible_rolls = (0.7, 0.8, 0.9, 1.0)

sands_main_stats_weights = (26.68, 26.66, 26.66, 10.0, 10.0)
goblet_main_stats_weights = (5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 19.25,
                             19.25, 19.0, 2.5)
circlet_main_stats_weights = (22.0, 22.0, 22.0, 4.0, 10.0, 10.0, 10.0)
substats_weights = (6, 6, 6, 4, 4, 4, 4, 4, 3, 3)


def take_input():
    valid_exit = ('exit', "'exit'", '"exit"')
    ok1 = False
    ok2 = False
    print("\nPlease input conditions. Type 'exit' to go back to menu.\nLeave blank to use defaults (1 test, 50 CV).\n")

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
            size = 1

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
            cv = 50

    print(f"Running {int(size)} simulation{'s' if int(size) != 1 else ''}, looking for at least {min(54.5, float(cv))} CV.")
    return size, cv


def load_data():
    try:
        with open('.\\inventory.txt') as file:
            data = file.read()
        d = json.loads(data)
        d = [Artifact(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]) for i in d]
        return d
    except FileNotFoundError:
        with open('.\\inventory.txt', 'w') as file:
            file.write('[]')
        return []


def create_artifact(source):
    type = choice(artifact_types)
    rv = 0
    if type == 'Flower':
        mainstat = 'HP'
    elif type == 'Feather':
        mainstat = 'ATK'
    elif type == 'Sands':
        mainstat = choices(sands_main_stats,
                           weights=sands_main_stats_weights)[0]
    elif type == 'Goblet':
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
    fourliner_weights = (2, 8) if source == 'domain' else (34, 66)
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

    threeliner = choices(subs_pool,
                         weights=subs_weights)[0] if not fourliner else 0

    return Artifact(type, mainstat, mainstat_value, threeliner, subs, 0, "", rv)


def create_and_roll_artifact(arti_source, highest_cv=0, silent=False):
    artifact = create_artifact(arti_source)
    if not highest_cv:
        if not silent:
            artifact.print_stats()
    for j in range(5):
        artifact.upgrade()
        if not highest_cv and not silent:
            artifact.print_stats()
    if highest_cv:
        if artifact.cv() > highest_cv:
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
        if extra_space and do_we_print:
            print()
        artifact.upgrade()
        if do_we_print:
            artifact.print_stats()
        else:
            artifact.last_upgrade = ''


def upgrade_to_max_tier(artifact, do_we_print=2, extra_space=False):    # 2 - print everything
    if artifact.level == 20 and do_we_print >= 1:                       # 1 - print only status and last upgrade
        print("Artifact already at +20\n")                              # 0 - dont print
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


def compare_to_highest_cv(artifact, fastest, slowest, days_list, artifact_list, day_number, artifact_number, cv_want, only_one):
    flag_break = False  # I'm incredibly sorry, this is absolutely unreadable
    if artifact.cv() >= min(54.5, cv_want):
        days_list.append(day_number)
        artifact_list.append(artifact_number)
        if fastest[0] == 0 or day_number < fastest[0]:
            fastest = (day_number, artifact)
        if day_number > slowest[0]:
            slowest = (day_number, artifact)
        # print(artifact.subs())
        if not only_one:
            print(f'Artifacts generated: {artifact_number}')
        flag_break = True
    return fastest, slowest, days_list, artifact_list, flag_break


def print_inventory(list_of_artifacts, which='all'):
    if which == 'all':
        needed_indexes = range(len(list_of_artifacts))
    else:
        for i in which:
            if i == -1 or i >= len(artifact_list):
                print(f'No artifact with index "{i + 1}" in your inventory. ', end='')
                if len(artifact_list) > 0:
                    print(f'Indexes go from 1 to {len(artifact_list)}\n')
                else:
                    print_empty_inv()
                raise StopIteration
        needed_indexes = which
    print("Inventory:\n")
    t1 = list_of_artifacts[0].type
    print('-' * 43, f'{t1}{"s" if t1 != "Sands" else ""}', '-' * 43)
    for this_index in range(len(needed_indexes)):
        i = int(needed_indexes[this_index])
        if this_index != 0:
            t_last = list_of_artifacts[needed_indexes[this_index - 1]].type
            t_now = list_of_artifacts[i].type
            if t_now != t_last:
                print('\n' + '-' * 43, f'{t_now}{"s" if t_now != "Sands" else ""}', '-' * 43)
        print(f'{i + 1}) {list_of_artifacts[i]} - {list_of_artifacts[i].subs()}')


def get_indexes(user_input):
    if ',' in user_input:  # if , in input
        idxs = user_input.split(',')  # split by commas
        # print(idxs)
        case = 'comma'
        for i in range(len(idxs)):  # for every part separated by ,
            this_index = idxs[i]
            if this_index == '':
                print('Try removing the space between the indexes (if applicable)\n')
                raise StopIteration
            if '-' in this_index:  # if it has -
                if len(this_index.split('-')) == 2:  # and there's only one -
                    this_index = this_index.split('-')  # split by -
                    if this_index[0].isnumeric() and this_index[1].isnumeric() and int(this_index[0]) <= int(
                            this_index[1]):  # if the range is correct
                        this_index[0] = int(this_index[0])
                        this_index[1] = int(this_index[1])
                        idxs[i] = [ind for ind in range(this_index[0], this_index[
                            1] + 1)]  # replace the part with the range instead
                    else:
                        print(f"\"{this_index}\" doesn't seem like a correct range\n")
                        raise StopIteration
                else:
                    print(f"Index \"{this_index}\" is incorrect, try again\n")
                    raise StopIteration
            elif not this_index.isnumeric():
                print(f"Index \"{this_index}\" is incorrect", end='')
                if '[' in this_index:
                    print(f'. Remove the parentheses\n')
                else:
                    print('\n')
                raise StopIteration
        idxs = flatten_list(idxs)

    elif '-' in user_input:
        if len(user_input.split('-')) == 2:
            this_index = user_input.split('-')
            if this_index[0].isnumeric() and this_index[1].isnumeric() and int(this_index[0]) <= int(
                    this_index[1]):  # if the range is correct
                this_index[0] = int(this_index[0])
                this_index[1] = int(this_index[1])
                idxs = [ind for ind in range(this_index[0], this_index[
                    1] + 1)]  # replace the part with the range instead
            else:
                print(f"\"{this_index}\" doesn't seem like a correct range\n")
                raise StopIteration
        else:
            print(f"\"{user_input}\" is incorrect, try again\n")
            raise StopIteration
        # print('flatten?', idxs)
        # idxs = flatten_list(idxs)

        case = 'range'

    else:
        if user_input.isnumeric():
            idxs = [user_input]
        else:
            print(f'{user_input} is not numeric\n')
            raise StopIteration
        case = 'index'
    # print(list(map(int, idxs)))
    return list(map(int, idxs)), case


def print_empty_inv():
    print('Inventory is empty\n'
          'Try "r 5" to save 5 random artifacts\n')


def print_controls():
    print('\n' +
          '=' * 43 + ' CONTROLS ' + '=' * 43 + '\n\n'  # aliases included next to each command
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
                                    'r [number] = re-roll and save a given number of artifacts to inventory\n'
                                    'r++ [number] = re-roll, +20, and save a given number of artifacts to inv\n'
                                    '\n'
                                    '------------------------------------ ACTIONS WITH INVENTORY ------------------------------------\n'
                                    '\n'
                                    'inv = show inventory\n'  # any string with 'inv' in it
                                    # this is true for every other command too.
                                    # the program will treat any string containing 'inv' as inv.
                                    '\n'
                                    'inv [index(es)] = view artifact(s) from inventory (use indexes from \'inv\' view)\n'
                                    'inv [index1,index2,...] +/++/cv/rv/del = perform action with artifacts in inv\n'
                                    'inv [index1-index2] +/++/cv/rv/del = perform action on a range of artifacts\n'
                                    '\n'
                                    'EXAMPLES: "inv 3", "inv 1-4", "inv 1,5 +", "inv 9,2-6 cv", "inv 5-35 del"\n'
                                    'NOTE: Indexes may change after deletion or upgrading of artifacts due to inventory sorting\n'
                                    '\n'
                                    'inv size = view amount of artifacts in inventory\n'
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
          "1 = roll artifacts until a certain CV is reached\n"
          "2 = roll one artifact at a time\n")


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

try:
    artifact_list = load_data()
    print('Loading successful')
    # print_inventory(artifact_list)
    # print()
except json.decoder.JSONDecodeError:
    print('Something off with inventory file. Clearing inventory.txt')
    artifact_list = []
    with open(r'.\inventory.txt', 'w') as file:
        file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
    print('Inventory cleared')

while True:
    print_menu()
    while True:
        automate = input('Your pick: ')
        if automate.lower() in valid_picks:
            break
        else:
            print('Commands are 0, 1 or 2\n')
    print("For the list of commands, type 'help'\n" if automate == '2' else "")
    print('=' * 64)
    if automate == "1":
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
                # print(f'new day {day}')
                if day % 10000 == 0:
                    print(f'Day {day} - still going')
                if day % 15 == 1:  # 4 artifacts from abyss every 15 days
                    for k in range(4):
                        inventory += 1
                        total_generated += 1
                        absolute_generated += 1
                        art, highest = create_and_roll_artifact("abyss", highest)
                        low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = compare_to_highest_cv(art, low, high,
                                                                                                                       days_it_took_to_reach_desired_cv, artifacts_generated,
                                                                                                                       day, total_generated, cv_desired, sample_size_is_one)
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
                    amount = choices((1, 2), weights=(93, 7))
                    # if amount[0] == 2:
                    #     print('lucky!')
                    total_generated += amount[0]
                    absolute_generated += amount[0]
                    inventory += amount[0]
                    for k in range(amount[0]):
                        art, highest = create_and_roll_artifact("domain", highest)
                        low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = compare_to_highest_cv(art, low, high,
                                                                                                                       days_it_took_to_reach_desired_cv, artifacts_generated,
                                                                                                                       day, total_generated, cv_desired, sample_size_is_one)
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
                        low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = compare_to_highest_cv(art, low, high,
                                                                                                                       days_it_took_to_reach_desired_cv, artifacts_generated,
                                                                                                                       day, total_generated, cv_desired, sample_size_is_one)
                        if flag:
                            break
                    # print(f'{inventory} left in inventory')
        end = time.perf_counter()
        print()
        days = round(sum(days_it_took_to_reach_desired_cv) / sample_size, 2)
        if sample_size > 1:
            print(
                f'Out of {sample_size} simulations, it took an average of {days} days ({round(days / 365.25, 2)} years) to reach at least {cv_desired} CV.')
            print(f'Fastest - {low[0]} day{"s" if low[0] > 1 else ""}: {low[1].subs()}')
            print(f'Slowest - {high[0]} day{"s" if high[0] > 1 else ""} ({round(high[0] / 365.25, 2)} years): {high[1].subs()}')
        else:
            print(f'It took {low[0]} days (or {round(high[0] / 365.25, 2)} years)!')
        print(f'Total artifacts generated: {sum(artifacts_generated)}')
        run_time = end - start
        to_hours = time.strftime("%T", time.gmtime(run_time))
        decimals = f'{(run_time % 1):.3f}'
        print()
        print(f'The simulation{"s" if sample_size > 1 else ""} took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
        print(f'Performance: {round(sum(artifacts_generated)/run_time/1000, 2)} artifacts per ms')
    elif automate == "2":
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
                    artifact_list.sort(
                        key=lambda x: (sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))
                    with open(r'.\inventory.txt', 'w') as file:
                        file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
            elif user_command in ('++', 'a++', 'a ++'):
                upgrade_to_max_tier(art, 2, True)
                if art in artifact_list:
                    artifact_list.sort(
                        key=lambda x: (sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))
                    with open(r'.\inventory.txt', 'w') as file:
                        file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))

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
                    else:
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
                        artifact_list.sort(
                            key=lambda x: (sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))
                        with open(r'.\inventory.txt', 'w') as file:
                            file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
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
                    artifact_list.sort(
                        key=lambda x: (sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))
                    with open(r'.\inventory.txt', 'w') as file:
                        file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
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
                    artifact_list.sort(
                        key=lambda x: (sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))
                    with open(r'.\inventory.txt', 'w') as file:
                        file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
                    print(
                        f'Saved - {len_artifact_list} artifact{"s" if len_artifact_list > 1 else ""} in inventory\n')
                else:
                    print('Already saved this artifact\n')

            elif user_command in ('d', 'del', 'delete', 'rm', 'remove'):
                if art in artifact_list:
                    artifact_list.remove(art)
                    len_artifact_list = len(artifact_list)
                    with open(r'.\inventory.txt', 'w') as file:
                        file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
                    print(
                        f'Removed - {len_artifact_list} artifact{"s" if len_artifact_list != 1 else ""} in inventory\n')
                else:
                    print('This artifact is not in your inventory\n')

            elif 'inv' in user_command:
                # if user_command in ('inv', 'inventory'):
                user_command = user_command.split()
                if len(user_command) == 1:
                    if len(artifact_list) == 0:
                        print_empty_inv()

                    else:
                        print_inventory(artifact_list)
                        print()

                elif len(user_command) == 3:  # e.g. "inv 1 +" or "inv 1,2,4 +" or "inv 2-5 d"
                    _, chosen_numbers, cmd = user_command
                    try:
                        indexes, operation = get_indexes(chosen_numbers)
                    except StopIteration:
                        continue
                    flag = True
                    for i in indexes:
                        # print(i, type(i))
                        # if isinstance(i, str):
                        #     if not i.isnumeric():
                        #         flag = False
                        #         print(f'Index "{i}" is not numeric\n')
                        #         break
                        if int(i) > len(artifact_list) or int(i) == 0:
                            flag = False
                            print(f'No artifact with index "{i}" in your inventory. ', end='')
                            if len(artifact_list) > 0:
                                print(f'Indexes go from 1 to {len(artifact_list)}\n')
                            else:
                                print_empty_inv()
                            break

                    if flag:  # if all given indexes are valid
                        # if operation == 'range' and indexes[0] > indexes[1]:
                        #     print('You know what you did.\n')
                        #     continue
                        indexes = list(map(lambda x: x - 1, map(int, indexes)))  # transform them
                        if len(indexes) == 1:
                            do_print = 2
                        elif len(indexes) <= 25:
                            do_print = 1
                        else:
                            do_print = 0
                        if 1 < len(indexes):  # if there's more than 1 index
                            if len(indexes) <= 25:
                                if cmd in ('+', '++'):
                                    print()
                                    print()
                                if cmd in ('cv', 'rv'):
                                    print()
                            # if operation == 'comma':  # so as I said, if there's more than 1 index
                            arti_list = itemgetter(*indexes)(
                                artifact_list)  # make a new list containing all the artifacts in question
                            # elif operation == 'range':
                            #     arti_list = artifact_list[indexes[0]:indexes[1]+1]
                            #     indexes = list(range(indexes[0], indexes[1]+1))
                        else:  # otherwise, make a list containing 1 artifact
                            if cmd in ('+', '++') and len(indexes) > 25:
                                pass
                            elif cmd in ('+', '++', 'd', 'del', 'rm', 'remove'):
                                print()
                            arti_list = [artifact_list[indexes[0]]]  # because we need a list object to iterate
                        for index, new_index in zip(indexes, range(len(arti_list))):  # then iterate this list and execute command
                            if cmd == '+':
                                if do_print:
                                    print(f'{index + 1}) ', end='')
                                upgrade_to_next_tier(arti_list[new_index], do_print)
                                # artifact_list.sort(key=lambda x: (
                                # sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))
                                # with open(r'.\inventory.txt', 'w') as file:
                                #     file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
                            elif cmd == '++':
                                if do_print:
                                    print(f'{index + 1}) ', end='')
                                upgrade_to_max_tier(arti_list[new_index], do_print)
                                # artifact_list.sort(key=lambda x: (
                                # sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))
                                # with open(r'.\inventory.txt', 'w') as file:
                                #     file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
                            elif cmd == 'rv':
                                print(f'{index + 1}) RV: {arti_list[new_index].rv()}%')

                            elif cmd == 'cv':
                                print(f'{index + 1}) CV: {arti_list[new_index].cv()}')

                            elif cmd in ('d', 'del', 'delete', 'rm', 'remove'):
                                if arti_list[new_index] in artifact_list:
                                    artifact_list.remove(arti_list[new_index])
                            else:
                                print(f'"{cmd}" is not a valid command\n')

                        if cmd in ('d', 'del', 'delete', 'rm', 'remove'):
                            with open(r'.\inventory.txt', 'w') as file:
                                file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
                            print(f'Artifact{"s" if len(indexes) > 1 else ""} removed\n')
                        # if cmd in ('d', 'del', 'delete', 'rm', 'remove', '+', '++'):
                        #     if len(artifact_list) == 0:
                        #         print('Inventory is empty')
                        #     if len(artifact_list) > 30:
                        #         pass
                        #     else:
                        #         print_inventory(artifact_list)
                        if cmd in ('+', '++'):
                            if not do_print:
                                print("Done! Artifacts upgraded\n")
                            elif len(indexes) > 1:
                                print()
                            artifact_list.sort(key=lambda x: (
                                sort_order_type[x.type], sort_order_mainstat[x.mainstat], -x.level))
                            with open(r'.\inventory.txt', 'w') as file:
                                file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
                        if cmd in ('cv', 'rv'):
                            print()

                elif len(user_command) == 2:  # e.g. "inv 2" or "inv 1-5,7"
                    _, cmd = user_command
                    if ',' in cmd or '-' in cmd:
                        try:
                            indexes, operation = get_indexes(cmd)
                        except StopIteration:
                            continue
                        indexes = list(map(lambda x: x - 1, map(int, indexes)))  # transform them
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
                        artifact_list = []
                        with open(r'.\inventory.txt', 'w') as file:
                            file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
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
                    elif cmd == 'size':
                        print(f'Currently {len(artifact_list)} artifacts in inventory', end='')
                        if len(artifact_list) > 0:
                            print(':')
                            print(f'{sum(i.type == 'Flower' for i in artifact_list)} Flowers\n'
                                  f'{sum(i.type == 'Feather' for i in artifact_list)} Feathers\n'
                                  f'{sum(i.type == 'Sands' for i in artifact_list)} Sands\n'
                                  f'{sum(i.type == 'Goblet' for i in artifact_list)} Goblets\n'
                                  f'{sum(i.type == 'Circlet' for i in artifact_list)} Circlets\n')
                        else:
                            print('\n')
                    elif cmd == 'load':
                        try:
                            artifact_list = load_data()
                            print('Loading successful')
                            if len(artifact_list) == 0:
                                print('Inventory is empty')
                            else:
                                print()
                                print_inventory(artifact_list)
                            print()
                        except json.decoder.JSONDecodeError:
                            print('Something off with inventory file. Clearing inventory.txt')
                            artifact_list = []
                            with open(r'.\inventory.txt', 'w') as file:
                                file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
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
print('\nThank you for using Artifact Simulator')
