from random import choice, choices
import time


class Artifact:

    def __init__(self, type, mainstat, threeliner, substats, level, last_upgrade=""):
        self.type = type
        self.mainstat = mainstat
        self.threeliner = threeliner
        self.substats = substats
        self.level = level
        self.last_upgrade = last_upgrade
        if "Crit RATE%" in self.substats:
            if self.substats["Crit RATE%"] == 23.0:
                self.substats["Crit RATE%"] = 22.9

    def __str__(self):
        return f"{self.mainstat} {self.type} (+{self.level})"

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
                f"- {i}: {str(round(self.substats[i], 1)) + '%' if is_percentage else round(self.substats[i])}{' (+)' if i == self.last_upgrade else ''}")
        print()

    def upgrade(self):
        if self.level != 20:
            if self.threeliner:
                self.substats[self.threeliner] = max_rolls[
                                                     self.threeliner] * choice(possible_rolls)
                self.last_upgrade = self.threeliner
                self.threeliner = 0
            else:
                sub = choice(list(self.substats.keys()))
                self.substats[sub] += max_rolls[sub] * choice(possible_rolls)
                self.last_upgrade = sub
            self.level += 4

    def cv(self):
        crit_value = 0
        if "Crit DMG%" in self.substats:
            crit_value += round(self.substats["Crit DMG%"], 1)
        if "Crit RATE%" in self.substats:
            crit_value += round(self.substats["Crit RATE%"], 1) * 2
        return round(crit_value, 1)


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
    ok1 = False
    ok2 = False
    print("\nPlease input conditions.\nLeave blank to use defaults (1 test, 50 CV).\n")

    while not ok1:
        size = input("Number of tests to run: ")
        if size:
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

    print(f"Running {int(size)} simulation{'s' if int(size) != 1 else ''}, looking for at least {float(cv)} CV.")
    return int(size), float(cv)


def create_artifact(source):
    type = choice(artifact_types)
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

    fourliner_weights = (2, 8) if source == 'domain' else (34, 66)
    fourliner = choices((1, 0), weights=fourliner_weights)[0]
    subs = {}

    subs_pool = list(substats)
    subs_weights = list(substats_weights)
    if mainstat in subs_pool:
        subs_weights.remove(subs_weights[subs_pool.index(mainstat)])
        subs_pool.remove(mainstat)

    for _i in range(3 + fourliner):
        sub = choices(subs_pool, weights=subs_weights)[0]
        subs_weights.remove(subs_weights[subs_pool.index(sub)])
        subs_pool.remove(sub)
        subs[sub] = max_rolls[sub] * choice(possible_rolls)

    threeliner = choices(subs_pool,
                         weights=subs_weights)[0] if not fourliner else 0

    return Artifact(type, mainstat, threeliner, subs, 0)


def create_and_roll_artifact(arti_source, highest_cv=0):
    artifact = create_artifact(arti_source)
    if not highest_cv:
        artifact.print_stats()
    for j in range(5):
        artifact.upgrade()
        if not highest_cv:
            artifact.print_stats()
    if highest_cv:
        if artifact.cv() > highest_cv:
            highest_cv = artifact.cv()
            print(f'Day {day}: {artifact.cv()} CV ({artifact}) - {artifact.subs()}')
    return artifact, highest_cv


def compare_to_highest_cv(artifact, fastest, slowest, days_list, day_number, cv_want):
    flag_break = False
    if artifact.cv() >= min(54.5, cv_want):
        days_list.append(day_number)
        if fastest[0] == 0 or day_number < fastest[0]:
            fastest = (day_number, artifact)
        if day_number > slowest[0]:
            slowest = (day_number, artifact)
        print(artifact.subs())
        flag_break = True
    return fastest, slowest, days_list, flag_break


def print_controls():
    print('\n' +
          '=' * 19 + ' CONTROLS ' + '=' * 19 + '\n'
                                               '\nhelp = send this message\n'
                                               '\n'
                                               '+ = upgrade to next tier\n'
                                               '++ = upgrade to +20\n'
                                               'r = re-roll\n'
                                               'r++ = re-roll and upgrade to +20\n'
                                               's = save to inventory\n'
                                               'inv = show inventory\n'
                                               '\n'
                                               'domain = change artifact source to domain (default)\n'
                                               'strongbox = change artifact source to strongbox\n\n'
                                               'artifact = show current artifact\n'
                                               'exit = go back to menu\n'
                                               '\n'
                                               '================================================\n'
          )


help = ['help', "'help'", '"help"']
artifact_list = []
while True:
    print('\n' + '=' * 21 + " MENU " + '=' * 21 + '\n')
    print("0 = exit the simulator\n"
          "1 = roll artifacts until a certain CV is reached\n"
          "2 = roll one artifact at a time\n")
    automate = input('Your pick: ')
    print('For the list of commands, type "help"\n' if automate == '2' else '')
    print('=' * 48)
    if automate == "1":
        sample_size, cv_desired = take_input()
        days_it_took_to_reach_50_cv = []
        low = (0, Artifact('this', 'needs', 'to', 'be', 'done'))
        high = (0, Artifact('this', 'needs', 'to', 'be', 'done'))
        start = time.perf_counter()
        for i in range(sample_size):
            c = 0
            day = 0
            highest = 0.1
            inventory = 0
            flag = False
            print(f'\nSimulation {i + 1}:')
            while not flag:
                day += 1
                # print(f'new day {day}')
                if day % 10000 == 0:
                    print(f'Day {day} - still going')
                resin = 180
                if day % 7 == 1:
                    resin += 60
                while resin:
                    # print('domain run')
                    resin -= 20
                    amount = choices((1, 2), weights=(93, 7))
                    # if amount[0] == 2:
                    #     print('lucky!')
                    inventory += amount[0]
                    for k in range(amount[0]):
                        art, highest = create_and_roll_artifact("domain", highest)
                        low, high, days_it_took_to_reach_50_cv, flag = compare_to_highest_cv(art, low, high,
                                                                                             days_it_took_to_reach_50_cv,
                                                                                             day, cv_desired)
                        if flag:
                            break
                    if flag:
                        break
                else:
                    while inventory >= 3:
                        # print(f'strongbox {inventory}')
                        inventory -= 2
                        art, highest = create_and_roll_artifact("strongbox", highest)
                        low, high, days_it_took_to_reach_50_cv, flag = compare_to_highest_cv(art, low, high,
                                                                                             days_it_took_to_reach_50_cv,
                                                                                             day, cv_desired)
                        if flag:
                            break
                    # print(f'{inventory} left in inventory')

        print()
        days = round(sum(days_it_took_to_reach_50_cv) / sample_size, 2)
        if sample_size > 1:
            print(
                f'Out of {sample_size} simulations, it took an average of {days} days ({round(days / 365.25, 2)} years) to reach {cv_desired} CV.')
            print(f'Fastest - {low[0]} days: {low[1].subs()}')
            print(f'Slowest - {high[0]} days ({round(high[0] / 365.25, 2)} years): {high[1].subs()}')
        else:
            print(f'It took {low[0]} days!')
        end = time.perf_counter()
        run_time = end - start
        to_hours = time.strftime("%T", time.gmtime(run_time))
        decimals = f'{(run_time % 1):.3f}'
        print()
        print(f'The simulation took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
    elif automate == "2":
        source = "domain"
        print()
        art = create_artifact(source)
        art.print_stats()
        while True:
            user_command = input('Command: ')
            if user_command == '+':
                if art.level == 20:
                    print("Artifact already at +20\n")
                else:
                    print('Upgrading...\n')
                    art.upgrade()
                    art.print_stats()
            elif user_command == '++':
                if art.level == 20:
                    print("Artifact already at +20\n")
                else:
                    print('Upgrading to +20...\n')
                    while art.level < 20:
                        art.upgrade()
                        art.print_stats()
            elif user_command.lower() == 'r':
                print('Re-rolling...\n')
                art = create_artifact(source)
                art.print_stats()
            elif user_command.lower() == 'r++':
                print('Re-rolling and upgrading...\n')
                art, _ = create_and_roll_artifact(source)
            elif user_command.lower() == 's':
                if art not in artifact_list:
                    artifact_list.append(art)
                    print(f'{len(artifact_list)} artifacts in inventory\n')
                else:
                    print('Already saved this artifact\n')
            elif user_command.lower() == 'inv':
                for i in artifact_list:
                    print(f'{i} - {i.subs()}')
                print()
            elif user_command.lower() == 'domain':
                source = 'domain'
                print('Source set to domain\n')
            elif user_command.lower() == 'strongbox':
                source = 'strongbox'
                print('Source set to strongbox\n')
            elif user_command.lower() == 'artifact':
                print()
                art.print_stats()
            elif user_command.lower() in ('exit', 'menu', '0'):
                print('Exiting...')
                break
            elif user_command.lower() in help:
                print_controls()
            else:
                print("Try 'help'\n")
    elif automate == '0' or automate.lower() == 'exit':
        break
    else:
        print('\nNot a valid choice, go again')
print('\nThank you for using Artifact Simulator')
