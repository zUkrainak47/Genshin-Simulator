import importlib
import os
import sys

if __name__ == '__main__':

    print('''
0 = exit Genshin Simulator
1 = enter Artifact Simulator
2 = enter Wish Simulator (WIP)
    ''', end='')

    while True:
        print()
        mode = input('Input mode: ')

        if mode == '1':
            if 'artifact_simulator' not in sys.modules:
                import artifact_simulator
            else:
                importlib.reload(artifact_simulator)

        elif mode == '2':
            if 'wish_simulator' not in sys.modules:
                import wish_simulator
            else:
                importlib.reload(wish_simulator)

        elif mode == '0':
            break

        else:
            print('1 for Artifact Simulator, 2 for Wish Simulator, 0 to exit')

    print('\nThank you for using Genshin Simulator')
