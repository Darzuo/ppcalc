
colors = {'pink': 0xff66aa, 'red': 0xff0033}

help_info = 'displays all commands and usages'
calc_info = 'gives a pp estimate for a given, beatmap, mods, accuracy, and max combo'
best_info = 'displays the best play for a given username or user id'
rec_info = 'gives a map recommendation for a user using the users average accuracy'
user_info = 'displays stats about a given user'

help_instr = f'**/pp, /pphelp** - {help_info}'
calc_instr = f'**/ppcalc [beatmap link] [mods\*] [acc\*] [combo\*]** - {calc_info} \n\
mods must be inputted as a combination of hd hr dt fl (ex. hdhr) \n\
if no accuracy or combo are provided, the max will be used (100% and FC)'
best_instr = f'**/ppbest [user]** - {best_info}'
rec_instr = f'**/pprec [user] [mods\*] [max_length\*]** - {rec_info} \n\
a max song duration (in seconds) may be inputted to limit results'
user_instr = f'**/ppuser [user]** - {user_info}'

commands = ['help', 'calc', 'best', 'rec', 'user']
instructions = [help_instr, calc_instr, best_instr, rec_instr, user_instr]
instruction_dict = dict()
for i in range(len(commands)):
    instruction_dict[commands[i]] = instructions[i]

instruction_str = ''
for command, instruction in instruction_dict.items():
    instruction_str += "**" + command + "**" + '\n'
    instruction_str += instruction + '\n\n'


help = f'''
Welcome to ppcalc!
Here are the commands that are currently available! (*optional)

{instruction_str}
'''
