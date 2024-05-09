# this file shows some statistical information about getting 5-star characters based on pity

# d stands for the percentage of all pulls that will end up being a 5-star character on a specific pity
# cum stands for the probability that you will have gotten a 5-star character by that pity
# r stands for the probability that you will NOT have gotten a 5-star character by that pity
# raw stands for the probability of getting a 5-star character at any given pity (that is, if you got to it)

remaining = 100
cumulative = 0
count = 0

for pity in range(1, 91):
    raw = min(max(pity - 73, 0) * 0.06 + 0.006, 1)  # count raw probability for x pity
    delta = raw * remaining      # count how many wishes will be successful exactly on x pity
    cumulative += delta          # count how many wishes were successful on x pity or before
    count += delta / 100 * pity  # update counter for average pity
    remaining *= (1 - raw)       # count what percentage of pulls still weren't successful
    print(f'p={pity} - d = {delta:.12f}%, cum = {cumulative:.12f}%, '
          f'r = {remaining:.12f}%, raw = {raw * 100:.1f}%')
    # print(100/delta)  # one in how many attempts will stop at this pity

print(f'\nAverage pity = {count}')
print(f'{1 / count * 100:.4f}% of all pulls are 5-stars on average')
