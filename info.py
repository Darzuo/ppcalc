calc_instr = 'calc <beatmap link> <acc> <combo> - gives a pp estimate for a given map, accuracy (0-100), and max combo \n\
calc <beatmap link> - gives an FC perfect accuracy estimate for a given map'

help_instr = 'help - displays all commands and usages \n\
help <command> - dispalys usage of a particular command'


commands = ['help', 'calc']
instructions = [help_instr, calc_instr]

instruction_dict = dict()

for i in range(len(commands)):
    instruction_dict[commands[i]] = instructions[i]

instruction_str = ''
for instruction in instructions:
    instruction_str = instruction_str + instruction + '\n'


help = f'''
ppcalc is a Discord Bot made for calculating pp scores in the game Osu!
Here are some commands that are currently available!

{instruction_str}
'''

