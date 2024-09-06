import json
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(kk): vv for kk, vv in x.items()}
    return x


try:
    with open(Path('wish_simulator_resources', 'character_distribution.txt')) as file:
        data = file.read()
    character_distribution = json.loads(data, object_hook=jsonKeys2int)
    num = character_distribution.pop(100)
    s = sum(character_distribution.values())
    for i in character_distribution:
        character_distribution[i] = character_distribution[i] / s * 100

    plt.plot(character_distribution.keys(), character_distribution.values())
    plt.xticks([1] + list(range(4, 82, 4)) + [83, 87, 90], rotation=45)
    plt.yticks(np.arange(0, 11, 0.6))
    plt.ylabel('Percentage')
    plt.xlabel('Pity')
    plt.title(f'Distribution of 5★ characters per pity (size = {num:,} pulls)')
    plt.grid()
    plt.tight_layout()
    Path('wish_simulator_resources', 'visualizations').mkdir(parents=True, exist_ok=True)
    plt.savefig(Path('wish_simulator_resources', 'visualizations', f'character distribution (size = {num}).png'), dpi=500)
    plt.show()
    print(' Done')

except FileNotFoundError:
    print(' No distribution file')

except ZeroDivisionError:
    print(' Get a 5-star first!')

except:
    print(' Something went wrong')
