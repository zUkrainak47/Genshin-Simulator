from random import choice, choices
import time, json
import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import datetime
from simulator import Artifact, take_input, create_artifact, compare_to_highest_cv

dict_of_days_total = {0.0: 0.0}
dict_of_days_average = {0.0: 0.0}


def create_and_roll_artifact(arti_source, highest_cv, cv_want, d):
    artifact = create_artifact(arti_source)

    for j in range(5):
        artifact.upgrade()

    a_cv = artifact.cv()

    if a_cv > highest_cv:
        if highest_cv == 0:
            dict_of_days_total[0] += 1

        for q in range(int(highest_cv * 10) + 1, int(min(a_cv * 10, cv_want * 10)) + 1):
            if q / 10 in dict_of_days_total:
                dict_of_days_total[q / 10] += d
            else:
                dict_of_days_total[q / 10] = d

        highest_cv = a_cv

    return artifact, highest_cv


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


def plot_this(plot_cv, plot_days, range_cv, amount_of_tests):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    if len(plot_cv) == 1:
        ax[0].scatter(plot_cv, plot_days, color='red', label='Single Point')
        ax[1].scatter(plot_cv, plot_days, color='red', label='Single Point')
    else:
        ax[0].plot(plot_cv, plot_days, label='Data')
        ax[1].plot(plot_cv, plot_days, label='Data')

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

    fig.suptitle(f"Average time to reach Crit Value (sample size = {amount_of_tests})")
    plt.tight_layout()
    # plt.grid()

    if int(range_cv[0]) == range_cv[0]:
        from_cv = max(int(range_cv[0]), 0)
    else:
        from_cv = max(range_cv[0], 0)

    is_int = int(cv_desired) if int(cv_desired) == cv_desired else cv_desired
    if int(range_cv[1]) == range_cv[1]:
        to_cv = min(int(range_cv[1]), is_int)
    else:
        to_cv = min(range_cv[1], is_int)

    plt.savefig(
        f'.\\plots\\sample size = {amount_of_tests}\\Plot of {from_cv}CV to {to_cv}CV (size = {amount_of_tests}).png',
        dpi=900)
    print("Here you go. This was also saved as a .png file.\n"
          "(To continue, close the graph if this is the last line you see)")
    plt.show()
    print("\nYou can plot another graph now if you want.\n")


sample_size, cv_desired = take_input((100, 50))
if sample_size == 'exit' or cv_desired == 'exit':
    print("Exiting program")
    sys.exit()
sample_size, cv_desired = int(sample_size), float(cv_desired)
days_it_took_to_reach_desired_cv = []
artifacts_generated = []
low = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))
high = (0, Artifact('this', 'needs', 'to', 'be', 'done', 0))
start = time.perf_counter()
sample_size_is_one = sample_size == 1
for i in range(sample_size):
    c = 0
    day = 0
    highest = 0
    total_generated = 0
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
    print(f'Now running simulation {i + 1}...', end=' ')
    while not flag:
        day += 1
        # print(f'new day {day}')
        if day % 10000 == 0:
            print(f'Day {day} - still going')
        if day % 15 == 1:  # 4 artifacts from abyss every 15 days
            for k in range(4):
                inventory += 1
                total_generated += 1
                art, highest = create_and_roll_artifact("abyss", highest, cv_desired, day)
                low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                    compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv, artifacts_generated,
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
            amount = choices((1, 2), weights=(93, 7))
            # if amount[0] == 2:
            #     print('lucky!')
            total_generated += amount[0]
            inventory += amount[0]
            for k in range(amount[0]):
                art, highest = create_and_roll_artifact("domain", highest, cv_desired, day)
                low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                    compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv, artifacts_generated,
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
                art, highest = create_and_roll_artifact("strongbox", highest, cv_desired, day)
                low, high, days_it_took_to_reach_desired_cv, artifacts_generated, flag = (
                    compare_to_highest_cv(art, low, high, days_it_took_to_reach_desired_cv, artifacts_generated,
                                          day, total_generated, cv_desired, sample_size_is_one))
                if flag:
                    break
            # print(f'{inventory} left in inventory')

end = time.perf_counter()
days = round(sum(days_it_took_to_reach_desired_cv) / sample_size, 2)
if sample_size > 1:
    print(
        f'\nOut of {sample_size} simulations, it took an average of {days} days ({round(days / 365.25, 2)} years) to reach {cv_desired} CV.')
    print(f'Fastest - {low[0]} days: {low[1].subs()}')
    print(f'Slowest - {high[0]} days ({round(high[0] / 365.25, 2)} years): {high[1].subs()}')
else:
    print(f'It took {low[0]} days (or {round(high[0] / 365.25, 2)} years)!')
print(f'Total artifacts generated: {sum(artifacts_generated)}')
run_time = end - start
to_hours = time.strftime("%T", time.gmtime(run_time))
decimals = f'{(run_time % 1):.3f}'
print()
print(f'The simulation{"s" if sample_size > 1 else ""} took {to_hours}:{str(decimals)[2:]} ({run_time:.3f} seconds)')
print(f'Performance: {round(sum(artifacts_generated) / run_time / 1000, 2)} artifacts per ms')
print(run_time)

for i in dict_of_days_total:
    dict_of_days_average[i] = round(dict_of_days_total[i] / sample_size, 2)

days_for_plotting = list(dict_of_days_average.values())
cv_for_plotting = np.arange(cv_desired * 10 + 1) / 10

print('Dict:', dict_of_days_average)
print('List:', days_for_plotting)
print()

Path(".\\plots").mkdir(parents=True, exist_ok=True)
Path(f".\\plots\\sample size = {sample_size}").mkdir(parents=True, exist_ok=True)

with open(f'.\\plots\\sample size = {sample_size}\\{cv_desired}CV - {sample_size} at {str(datetime.datetime.now())[:-7].replace(":", "-")}.txt', 'w') as file:
    file.write(json.dumps(days_for_plotting))

plot_this(cv_for_plotting, days_for_plotting, [0.0, cv_desired], sample_size)

first_time = True
while True:
    print('What CV range would you like to see the plot for?')
    if first_time:
        print('Leave blank to use the entire range. Type "exit" to quit.')
        print('Example: 20.5:45')
        first_time = False
    user_cmd = input('Range: ')
    if user_cmd:
        if user_cmd in ('exit', "'exit'", '"exit"', '0'):
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

print('\nThank you for using Artifact Simulator (plotting edition)')
