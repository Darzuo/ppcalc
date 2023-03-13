help_instr = 'help - displays all commands and usages \n\
help <command> - dispalys usage of a particular command'

calc_instr = 'calc <mods (optional)> <beatmap link> <acc> <combo> - gives a pp estimate for given mods, beatmap link, accuracy (0-100), and max combo \n\
calc <mods (optional)> <beatmap link> - gives an SS pp estimate for a given map\n\
mods must be inputted as a combination of hd hr dt fl (ex. hdhr)'

best_instr = 'best <username / id> - displays the best play for a given user'

colors = {'osu_pink': 0xff66aa, 'error_red': 0xff0033}


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
ppcalc is a Discord Bot made for calculating pp scores in the game Osu!
Here are some commands that are currently available!

{instruction_str}
'''

