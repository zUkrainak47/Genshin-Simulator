import json
import numpy as np
import matplotlib.pyplot as plt

def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(kk): vv for kk, vv in x.items()}
    return x

try:
    with open('.\\banner_info\\datamine.txt') as file:
        data = file.read()
    pity_datamine = json.loads(data, object_hook=jsonKeys2int)
    s = sum(pity_datamine.values())
    for i in pity_datamine:
        pity_datamine[i] = pity_datamine[i]/s * 100

    plt.plot(pity_datamine.keys(), pity_datamine.values())
    plt.xticks([1] + list(range(4, 82, 4)) + [83, 87, 90], rotation=45)
    plt.yticks(np.arange(0, 11, 0.6))
    plt.ylabel('Percentage')
    plt.xlabel('Pity')
    plt.title(f'Percentage of pulls at pity (size = {s} 5-stars)')
    plt.grid()
    plt.tight_layout()
    plt.savefig('.\\banner_info\\datamine.png', dpi=500)
    plt.show()

except FileNotFoundError:
    print('No datamine file')
