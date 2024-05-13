import importlib
import os
import sys


def print_rules():
    print('Pick an action!\n'
          '\n'
          '0 = exit Genshin Simulator\n'
          '1 = enter Artifact Simulator\n'
          '2 = enter Wish Simulator (WIP)\n',
          end='')


last_mode = 2

if __name__ == '__main__':
    print()
    print('=' * 27 + ' LAUNCHER ' + '=' * 27)
    print('\nWelcome to Genshin Simulator!', end=' ')
    while True:
        if last_mode:
            if last_mode == 1:
                print()
                print('='*27 + ' LAUNCHER ' + '='*27 + '\n')
            print_rules()

        print()
        mode = input('Command: ')

        if mode == '1':
            last_mode = 1
            if 'artifact_simulator' not in sys.modules:
                import artifact_simulator
            else:
                importlib.reload(artifact_simulator)

        elif mode == '2':
            last_mode = 1
            if 'wish_simulator' not in sys.modules:
                import wish_simulator
            else:
                importlib.reload(wish_simulator)

        elif mode in ('0', 'exit'):
            print('Exiting Genshin Simulator...\n'
                  '\n'
                  '================================================================')
            break

        else:
            last_mode = 0
            print('1 for Artifact Simulator, 2 for Wish Simulator, 0 to exit')

    print('\nThank you for using Genshin Simulator')
