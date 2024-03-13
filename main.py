from random import choice, choices
import time


class Artifact:

    def __init__(self, type, mainstat, threeliner, substats, level):
        self.type = type
        self.mainstat = mainstat
        self.threeliner = threeliner
        self.substats = substats
        self.level = level

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


def create_artifact():
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

    threeliner = choice((1, 0))
    subs = {}

    subs_pool = list(substats)
    subs_weights = list(substats_weights)
    if mainstat in subs_pool:
        subs_weights.remove(subs_weights[subs_pool.index(mainstat)])
        subs_pool.remove(mainstat)

    for _i in range(3 + threeliner):
        sub = choices(subs_pool, weights=subs_weights)[0]
        subs_weights.remove(subs_weights[subs_pool.index(sub)])
        subs_pool.remove(sub)
        subs[sub] = max_rolls[sub] * choice(possible_rolls)

    threeliner = choices(subs_pool,
                         weights=subs_weights)[0] if not threeliner else 0

    return Artifact(type, mainstat, threeliner, subs, 0)


sample_size = 100
cv_desired = 50

days_it_took_to_reach_50_cv = []
low = (0, Artifact('this', 'needs', 'to', 'be', 'done'))
high = (0, Artifact('this', 'needs', 'to', 'be', 'done'))
for i in range(sample_size):
    c = 0
    highest = 0
    flag = False
    print(f'\nSimulation {i + 1}:')
    while True:
        if flag:
            break
        c += 1
        day = c//9
        if c % 90000 == 0:
            print(f'Day {day} - still going')
        day_float = c/9
        art = create_artifact()

        for _j in range(5):
            art.upgrade()
            if art.cv() > highest:
                highest = art.cv()
                print(f'Day {day}: {art.cv()}CV ({art})')
                if art.cv() >= min(54.4, cv_desired):
                    days_it_took_to_reach_50_cv.append(day_float)
                    if low[0] == 0 or day_float < low[0]:
                        low = (round(day_float, 2), art)
                    if day_float > high[0]:
                        high = (round(day_float, 2), art)
                    print(art.subs())
                    flag = True
                    break

print()
print(f'Out of {sample_size} simulations, it took {round(sum(days_it_took_to_reach_50_cv)/sample_size, 2)} days to reach {cv_desired} CV on average.')
print(f'Fastest - {low[0]} days: {low[1].subs()}')
print(f'Slowest - {high[0]} days ({round(high[0]/365.25, 2)} years): {high[1].subs()}')
