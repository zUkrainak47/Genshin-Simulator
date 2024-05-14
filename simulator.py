import importlib
import os
import sys
from colorama import init, Fore, Style
init()


try:
    os.environ['replit']
    replit = True
    if replit:
        print('\n Running in replit!')
    if not os.environ['replit']:
        print(' To get rid of "Missing required secrets", set the replit variable to anything')
except KeyError:
    replit = False
    # print('\n Not running in replit!')


def print_rules():
    print(' Pick an action!\n'
          '\n '
          '0 = exit Genshin Simulator\n'
          ' 1 = enter Artifact Simulator\n'
          ' 2 = enter Wish Simulator\n',
          end='')


last_mode = 2

if __name__ == '__main__':
    print()
    print('=' * 28 + f' {Fore.LIGHTCYAN_EX}LAUNCHER{Style.RESET_ALL} ' + '=' * 28)
    print('\n Welcome to Genshin Simulator!', end='')
    while True:
        if last_mode:
            if last_mode == 1:
                print()
                print('='*28 + f' {Fore.LIGHTCYAN_EX}LAUNCHER{Style.RESET_ALL} ' + '='*28 + '\n')
            print_rules()

        print()
        mode = input(' Command: ')

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
            print(' Exiting Genshin Simulator...\n'
                  '\n'
                  '==================================================================')
            break

        else:
            last_mode = 0
            print(' 1 for Artifact Simulator, 2 for Wish Simulator, 0 to exit')

    print('\n Thank you for using Genshin Simulator')
