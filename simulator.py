from random import choice, choices
import time

class Artifact:

    def __init__(self, type, mainstat, threeliner, substats, level):
        self.type = type
        self.mainstat = mainstat
        self.threeliner = threeliner
        self.substats = substats
        self.level = level
        if "Crit RATE%" in self.substats:
            if self.substats["Crit RATE%"] == 23.0:
                self.substats["Crit RATE%"] = 22.9

    def __str__(self):
        return f"+{self.level} {self.mainstat} {self.type}"

    def subs(self):
        sub_stats = {
            sub: round(self.substats[sub], 1)
            if "%" in sub else round(self.substats[sub])
            for sub in self.substats
        }
        return sub_stats

    def upgrade(self):
        if self.level != 20:
            if self.threeliner:
                self.substats[self.threeliner] = max_rolls[
                    self.threeliner] * choice(possible_rolls)
                self.threeliner = 0
            else:
                sub = choice(list(self.substats.keys()))
                self.substats[sub] += max_rolls[sub] * choice(possible_rolls)
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
    print("\nPlease input the conditions. Leave blank to use defaults (25 simulations, 50 CV).\n")

    while not ok1:
        size = input("Amount of tests to run: ")
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
            size = 25

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

    print(f'Running {int(size)} simulations, looking for at least {float(cv)} CV.')
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


def create_and_roll_artifact(source, highest_cv):
    artifact = create_artifact(source)
    for j in range(5):
        artifact.upgrade()
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


sample_size, cv_desired = take_input()
days_it_took_to_reach_50_cv = []
low = (0, Artifact('this', 'needs', 'to', 'be', 'done'))
high = (0, Artifact('this', 'needs', 'to', 'be', 'done'))
for i in range(sample_size):
    c = 0
    day = 0
    highest = 0
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
                low, high, days_it_took_to_reach_50_cv, flag = compare_to_highest_cv(art, low, high, days_it_took_to_reach_50_cv, day, cv_desired)
                if flag:
                    break
            if flag:
                break
        else:
            while inventory >= 3:
                # print(f'strongbox {inventory}')
                inventory -= 2
                art, highest = create_and_roll_artifact("strongbox", highest)
                low, high, days_it_took_to_reach_50_cv, flag = compare_to_highest_cv(art, low, high, days_it_took_to_reach_50_cv, day, cv_desired)
                if flag:
                    break
            # print(f'{inventory} left in inventory')


print()
days = round(sum(days_it_took_to_reach_50_cv)/sample_size, 2)
print(f'Out of {sample_size} simulations, it took an average of {days} days ({round(days/365.25, 2)} years) to reach {cv_desired} CV.')
print(f'Fastest - {low[0]} days: {low[1].subs()}')
print(f'Slowest - {high[0]} days ({round(high[0]/365.25, 2)} years): {high[1].subs()}')
