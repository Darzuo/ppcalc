
colors = {'pink': 0xff66aa, 'red': 0xff0033}

help_info = 'displays all commands and usages'
calc_info = 'gives a pp estimate for a given, beatmap, mods, accuracy, and max combo'
best_info = 'displays the best play for a given username or user id'

help_instr = f'**/pphelp** - {help_info}'
calc_instr = f'**/ppcalc <beatmap link> <mods (optional)> <acc (optional)> <combo (optional)>** - {calc_info} \n\
Mods must be inputted as a combination of hd hr dt fl (ex. hdhr) \n\
If no accuracy or combo are provided, the max will be used (100%, and FC)'
best_instr = f'**/ppbest <username | id>** - {best_info}'

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
