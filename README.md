# ppcalc

### A Machine Learning based PP calculator for the game 'Osu!'
* Uses data from past years to estimate pp gain from any play given accuracy, combo and mods
* Includes Discord integration with other Osu-related functionality
* Currently only supports integration for:
  * Classic Osu! game mode
  * Any combination of: No mods, Hidden, Hard Rock, Double Time, Flashlight

### Discord Bot
* Add the bot to your server with the following link:
  * https://discord.com/api/oauth2/authorize?client_id=1083614941476560966&permissions=277025466368&scope=applications.commands%20bot
* Here's the list of currently available commands (* means optional):
  * **/pp, /pphelp** - displays all commands and usages 
  * **/ppcalc [beatmap link] [mods\*] [accuracy\*] [combo\*]** - gives a pp estimate for a given beatmap, mods, accuracy and max combo
    * mods must be inputted as a combination of hd, hr, dt, fl (ex. hdhr)
    * the default values are a max combo, no mod, 100 accuracy play
  * **/ppbest [user]** - displays the best play for a given username or user id
  * **/pprec [user] [mods\*] [max_length\*]** - gives a mac recommendation for a user using the user's average accuracy
    * a max song duration (in seconds) may be inputted to limit results
  * **/ppuser** - displays stats about a specific user
    * accuracy, play time, global and country ranks, total pp
