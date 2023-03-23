help_instr = '**!pp help** - displays all commands and usages \n\
**!pp help <command>** - dispalys usage of a particular command'

calc_instr = '**!pp calc <mods (optional)> <beatmap link> <acc> <combo>** - gives a pp estimate for given mods, beatmap link, accuracy (0-100), and max combo \n\
!**pp calc <mods (optional)> <beatmap link>** - gives an SS pp estimate for a given map\n\
Note: mods must be inputted as a combination of hd hr dt fl (ex. hdhr)'

best_instr = '**!pp best <username | id>** - displays the best play for a given user'

help_info = 'displays all commands and usages or usage for a single command'
calc_info = 'gives a pp estimate for given mods, beatmap link, accuracy, and max combo'

colors = {'pink': 0xff66aa, 'red': 0xff0033}

param_nums = {'help': {0,1}, 'calc': {1,2,3,4}, 'best': {1}}

commands = ['help', 'calc', 'best']
instructions = [help_instr, calc_instr, best_instr]

instruction_dict = dict()

for i in range(len(commands)):
    instruction_dict[commands[i]] = instructions[i]

instruction_str = ''
for command, instruction in instruction_dict.items():
    instruction_str += "**" + command + "**" + '\n'
    instruction_str += instruction + '\n\n'


help = f'''
Welcome to ppcalc!
Here are the commands that are currently available!

{instruction_str}
'''

