print("""
here's some statistical information about getting 5-star characters based on pity

d   - percentage of all pulls that will end up being a 5-star on a specific pity
cum - probability that you will have gotten a 5-star by that pity
r   - probability that you will NOT have gotten a 5-star by that pity
raw - probability of getting a 5-star at any given pity (that is, if you got to it)
""")


def show_chances(t):
    remaining = 100
    cumulative = 0
    count = 0

    if t == 'character':
        hard, soft, base = 90, 74, 0.006
    else:
        hard, soft, base = 77, 63, 0.007

    print(f'\n{t.upper()} BANNER\n')
    for pity in range(1, hard+1):
        raw = min(max(pity - (soft-1), 0) * base*10 + base, 1)  # count raw probability for x pity
        delta = raw * remaining      # count how many wishes will be successful exactly on x pity
        cumulative += delta          # count how many wishes were successful on x pity or before
        count += delta / 100 * pity  # update counter for average pity
        remaining *= (1 - raw)       # count what percentage of pulls still weren't successful
        print(f'p={pity} - d = {delta:.12f}%, cum = {cumulative:.12f}%, '
              f'r = {remaining:.12f}%, raw = {raw * 100:.1f}%')
        # print(100/delta)  # one in how many attempts will stop at this pity

    print(f'\nAverage pity = {count}')
    print(f'{1 / count * 100:.4f}% of all pulls are 5-star {t}s on average')


show_chances('character')
print()
show_chances('weapon')
