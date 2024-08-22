# Genshin Impact Simulator
Welcome to the ultimate (command-line interface) Genshin Impact simulator. \
With this project, I did my best to replicate Genshin Impact's two major gacha systems: the Wish System and the Artifact System.

If you find any bugs, report them to me :)

# DISCLAIMER
Genshin Impact changed the chance of getting a rate-up 5-star character when not guaranteed from 50/50 to 55/45 in version 5.0. I need more information in order to implement this change. They also reduced the maximum number of fate points in the weapon banner from 2 to 1 which i will introduce alongside the 55/45 change. Right now this project will be on hiatus until i figure that out, hopefully there will be more information available on this change, right now it's basically a guessing game and I want this simulator to copy the game mechanics without guessing how they work.

### How do I start simulating Genshin Impact?

First you need to download or clone the repository on your device (i know) \
Next, locate `simulator.py`. You can access both simulators from there! \
Alternatively, you can run `wish_simulator.py` or `artifact_simulator.py` to access the respective simulator directly.

Or  click this button and Fork & Run on replit

[![Run on Replit](https://user-images.githubusercontent.com/50180265/221977287-4622854b-8c89-4f75-81af-eee6058a20fa.png)](https://replit.com/@zUkrainak47/Genshin-Simulator?v=1)

---

# Wish Simulator
## About
You're out of primogems? You watched a friend whale? You just lost your 50/50? Or do you just want to try your luck without risking thousands of dollars? \
I've got you covered! Hop on and spend any amount of pulls on any banner that's ever existed (yes, even the Keqing banner)
## Using `Wish Simulator`

- Allows you to do virtually any amount of pulls on any banner
- Check your wish history
- Check your inventory containing every character's constellations and weapon refinements
- Make a "5-stars VS Pity" graph based on your results

All of your results are backed up in separate files, so you don't have to worry about your data getting lost!

---

# Artifact Simulator
## About
Ever wanted to know how long it *actually* takes to get a 50CV artifact? \
Are you out of resin but crave that lovely RNG?

This Artifact Simulator can help you with that.
## Using `Artifact Simulator`

- Allows you to generate and upgrade artifacts one by one. Basically like running domains or using the strongbox, but you have unlimited resin.
- If there's an artifact that you like, you can add it to your inventory. It also carries over sessions!
- Commands include:
  - Leveling artifact (to next tier or to +20)
  - Re-rolling artifact
  - Viewing inventory
  - etc.

### Automation Mode (accessed by typing "auto" or "automate"):
- Will continuously generate artifacts until your desired Crit Value is reached.
- Will tell you how many days (or years) of continuous farming that took.
- You can choose to run multiple tests, the program will show the average time.
- It will use 1 Transient Resin per week, assumes unlimited fodder and throws all artifacts in the Strongbox.
- It also assumes a 33.3% (1/3) chance to get a 4-liner from strongbox and 20% from domains, as well as a 6.66% (2/30) chance to get double artifact drops from a domain run. 

## Plotting with `simulator_for_plotting.py`

This program will run Automation Mode of `Artifact Simulator`, and will also create a graph to visualize the results. \
Right now only CV is supported as a stat, but I might add more in the future.
