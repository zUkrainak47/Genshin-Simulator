import json
import numpy as np
import matplotlib.pyplot as plt


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(kk): vv for kk, vv in x.items()}
    return x


try:
    with open('.\\banner_info\\weapon_distribution.txt') as file:
        data = file.read()
    weapon_distribution = json.loads(data, object_hook=jsonKeys2int)
    num = weapon_distribution.pop(100)
    s = sum(weapon_distribution.values())
    for i in weapon_distribution:
        weapon_distribution[i] = weapon_distribution[i] / s * 100

    plt.plot(weapon_distribution.keys(), weapon_distribution.values())
    plt.xticks([1] + list(range(4, 80, 4)), rotation=45)
    plt.yticks(np.arange(0, 12.1, 0.6))
    plt.ylabel('Percentage')
    plt.xlabel('Pity')
    plt.title(f'Distribution of 5★ weapons per pity (size = {num:,} pulls)')
    plt.grid()
    plt.tight_layout()
    plt.savefig(f'.\\banner_info\\weapon distribution (size = {num}).png', dpi=500)
    plt.show()
    print(' Done')

except FileNotFoundError:
    print(' No distribution file')

except ZeroDivisionError:
    print(' Get a 5-star first!')

except:
    print(' Something went wrong')
