# Artifact Simulator
## About
Ever wanted to know how long it *actually* takes to get a 50CV artifact? \
Are you out of resin but crave that lovely RNG?

This artifact simulator can help you with that.
# Using `simulator.py`
## Mode 1: 
- The program will continuously generate artifacts until your desired Crit Value is reached.
- It will tell you how many days (or years) of resin that took.
- You can choose to run multiple tests, the program will show the average time.
- It will use 1 Transient Resin per week, assumes unlimited fodder and throws all artifacts in the Strongbox.

## Mode 2:
- Allows you to level and re-roll artifacts one by one. Basically like running domains, but you have unlimited resin.
- If there's an artifact that you like, you can add it to your inventory. It also carries over sessions.
- Commands include:
  - leveling artifact (to next tier or to +20)
  - re-rolling artifact
  - viewing inventory
  - etc

# Plotting with `simulator_for_plotting.py`
This program will run Mode 1 of `simulator.py`, but will create a graph to visualize the results. \
Right now only CV is supported as a stat, but I might add more in the future.
