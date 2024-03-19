from random import choice, choices
import time, json
import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

dict_of_days_total = {0.0: 0.0}
dict_of_days_average = {0.0: 0.0}


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
    print(
        "\nPlease input conditions. Type 'exit' to exit the program.\nLeave blank to use defaults (100 tests, 50 CV).\n")

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
            size = 100

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

    print(f"Running {int(size)} simulation{'s' if int(size) != 1 else ''}, looking for at least {float(cv)} CV.\n")
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


def create_and_roll_artifact(arti_source, highest_cv, cv_want, day):
    artifact = create_artifact(arti_source)
    for j in range(5):
        artifact.upgrade()
    a_cv = artifact.cv()
    if artifact.cv() > highest_cv:
        if highest_cv == 0:
            dict_of_days_total[0] += 1
        for q in range(int(highest_cv * 10) + 1, int(min(a_cv * 10, cv_want * 10)) + 1):
            if q / 10 in dict_of_days_total:
                dict_of_days_total[q / 10] += day
            else:
                dict_of_days_total[q / 10] = day
        highest_cv = artifact.cv()
        # print(f'Day {day}: {artifact.cv()} CV ({artifact}) - {artifact.subs()}')
    return artifact, highest_cv


def upgrade_to_next_tier(artifact):
    if artifact.level == 20:
        print("Artifact already at +20\n")
    else:
        print('Upgrading...\n')
        artifact.upgrade()
        artifact.print_stats()


def upgrade_to_max_tier(artifact, do_we_print=True):
    if artifact.level == 20:
        print("Artifact already at +20\n")
    else:
        print('Upgrading to +20...\n')
        while artifact.level < 20:
            artifact.upgrade()
            if do_we_print:
                artifact.print_stats()
        if not do_we_print:
            artifact.print_stats()


def compare_to_highest_cv(artifact, fastest, slowest, days_list, day_number, cv_want):
    flag_break = False
    if artifact.cv() >= min(54.5, cv_want):
        days_list.append(day_number)
        if fastest[0] == 0 or day_number < fastest[0]:
            fastest = (day_number, artifact)
        if day_number > slowest[0]:
            slowest = (day_number, artifact)
        # print(artifact.subs())
        flag_break = True
    return fastest, slowest, days_list, flag_break


def print_inventory(list_of_artifacts):
    print("Inventory:\n")
    t1 = list_of_artifacts[0].type
    print('-' * 43, f'{t1}{"s" if t1 != "Sands" else ""}', '-' * 43)
    for i in range(len(list_of_artifacts)):
        print(f'{i + 1}) {list_of_artifacts[i]} - {list_of_artifacts[i].subs()}')
        if i + 1 < len(list_of_artifacts):
            t2 = list_of_artifacts[i + 1].type
            if t2 != list_of_artifacts[i].type:
                print('\n' + '-' * 43, f'{t2}{"s" if t2 != "Sands" else ""}', '-' * 43)


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


def plot_this(cv_plot, days_plot, cv_range, sample_size):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    if len(cv_plot) == 1:
        ax[0].scatter(cv_plot, days_plot, color='red', label='Single Point')
        ax[1].scatter(cv_plot, days_plot, color='red', label='Single Point')
    else:
        ax[0].plot(cv_plot, days_plot, label='Data')
        ax[1].plot(cv_plot, days_plot, label='Data')

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

    # if len(ax.get_xticks()) > 12:
    # plt.xticks(rotation=60)

    # plt.plot(cv_plot, days_plot)
    # plt.xticks(np.arange(min(cv_plot), max(cv_plot) + 1, 2.5), rotation=60)
    # plt.yticks(np.arange(0, 100, 250))

    # plt.xlabel("Crit Value")
    # plt.ylabel("Days to reach CV")
    fig.suptitle(f"Average time to reach Crit Value (sample size = {sample_size})")
    plt.tight_layout()
    # plt.grid()
    Path(".\\plots").mkdir(parents=True, exist_ok=True)
    Path(f".\\plots\\sample size = {sample_size}").mkdir(parents=True, exist_ok=True)

    if int(cv_range[0]) == cv_range[0]:
        from_cv = max(int(cv_range[0]), 0)
    else:
        from_cv = max(cv_range[0], 0)

    is_int = int(cv_desired) if int(cv_desired) == cv_desired else cv_desired
    if int(cv_range[1]) == cv_range[1]:
        to_cv = min(int(cv_range[1]), is_int)
    else:
        to_cv = min(cv_range[1], is_int)

    plt.savefig(
        f'.\\plots\\sample size = {sample_size}\\Plot of {from_cv}CV to {to_cv}CV (size = {sample_size}).png',
        dpi=900)
    plt.show()


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

# try:
#     artifact_list = load_data()
#     print('Loading successful')
#     # print_inventory(artifact_list)
#     # print()
# except json.decoder.JSONDecodeError:
#     print('Something off with inventory file. Clearing inventory.txt')
#     artifact_list = []
#     with open(r'.\inventory.txt', 'w') as file:
#         file.write(str(json.dumps(artifact_list, cls=ArtifactEncoder)))
#     print('Inventory cleared')
sample_size, cv_desired = take_input()
if sample_size == 'exit' or cv_desired == 'exit':
    print("Exiting program")
    sys.exit()
sample_size, cv_desired = int(sample_size), float(cv_desired)
days_it_took_to_reach_desired_cv = []
low = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))
high = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))
start = time.perf_counter()
for i in range(sample_size):
    c = 0
    day = 0
    highest = 0
    inventory = 0
    flag = False
    if (i + 1) % 25 == 0:
        print("\nResults so far:")
        for dd in dict_of_days_total:
            dict_of_days_average[dd] = round(dict_of_days_total[dd] / i, 2)
            # print(f'{dd}: {dict_of_days_total[dd]/i}')
        print('Dict:', dict_of_days_average)
        print('List:', list(dict_of_days_average.values()))
        print()
    print(f'Now running simulation {i + 1}...')
    while not flag:
        day += 1
        # print(f'new day {day}')
        if day % 10000 == 0:
            print(f'Day {day} - still going')
        if day % 15 == 1:  # 4 artifacts from abyss every 15 days
            inventory += 4
            for k in range(4):
                art, highest = create_and_roll_artifact("abyss", highest, cv_desired, day)
                low, high, days_it_took_to_reach_desired_cv, flag = compare_to_highest_cv(art, low, high,
                                                                                          days_it_took_to_reach_desired_cv,
                                                                                          day, cv_desired)
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
            inventory += amount[0]
            for k in range(amount[0]):
                art, highest = create_and_roll_artifact("domain", highest, cv_desired, day)
                low, high, days_it_took_to_reach_desired_cv, flag = compare_to_highest_cv(art, low, high,
                                                                                          days_it_took_to_reach_desired_cv,
                                                                                          day, cv_desired)
                if flag:
                    break
            if flag:
                break
        else:
            while inventory >= 3:
                # print(f'strongbox {inventory}')
                inventory -= 2
                art, highest = create_and_roll_artifact("strongbox", highest, cv_desired, day)
                low, high, days_it_took_to_reach_desired_cv, flag = compare_to_highest_cv(art, low, high,
                                                                                          days_it_took_to_reach_desired_cv,
                                                                                          day, cv_desired)
                if flag:
                    break
            # print(f'{inventory} left in inventory')

print()

days = round(sum(days_it_took_to_reach_desired_cv) / sample_size, 2)
if sample_size > 1:
    print(
        f'Out of {sample_size} simulations, it took an average of {days} days ({round(days / 365.25, 2)} years) to reach {cv_desired} CV.')
    print(f'Fastest - {low[0]} days: {low[1].subs()}')
    print(f'Slowest - {high[0]} days ({round(high[0] / 365.25, 2)} years): {high[1].subs()}')
else:
    print(f'It took {low[0]} days (or {round(high[0] / 365.25, 2)} years)!')
end = time.perf_counter()
run_time = end - start
to_hours = time.strftime("%T", time.gmtime(run_time))
decimals = f'{(run_time % 1):.3f}'
print(f'The simulation took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
print()

for i in dict_of_days_total:
    dict_of_days_average[i] = round(dict_of_days_total[i] / sample_size, 2)

days_for_plotting = list(dict_of_days_average.values())
cv_for_plotting = np.arange(cv_desired * 10 + 1) / 10

print('Dict:', dict_of_days_average)
print('List:', days_for_plotting)
print()

plot_this(cv_for_plotting, days_for_plotting, [0.0, cv_desired], sample_size)

print("Here you go. This was also saved as a .png file.\n"
      "You can plot another graph now if you want.\n")

first_time = True
while True:
    print('What CV range would you like to see the plot for?')
    if first_time:
        print('Leave blank to use the entire range. Type "exit" to quit.')
        print('Example: 20.5:45')
        first_time = False
    user_cmd = input('Range: ')
    if user_cmd:
        if user_cmd in ('exit', "'exit'", '"exit"'):
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
    plot_this(cv_plot, days_plot, cv_range, sample_size)


    print("Ok, here you go. This was also saved as a .png file.\n"
          "You can plot another graph now if you want.\n")

print('\nThank you for using Artifact Simulator (plotting edition)')
