# evolution-simulator-3
## My third attempt at an evolution simulator

Sequel to [evolution-simulator-2](https://github.com/Phyrik/evolution-simulator-2).

Based of the principles described in Primer's YouTube series on evolution.

## Installation and running

To install and run evolution-simulator-3 simply download the source code, ensure you have Python 3, Pygame, and matplotlib installed, and run

```python3 main.py```

in the terminal or command prompt.

### Command Line Arguments

optional arguments:
  -h, --help           show this help message and exit
  -i , --individuals   The amount of Individuals to spawn at the start of the
                       simulation
  -f , --food          Amount of food to spawn each day
  -v , --vision        Default vision distance for Individuals
  -e , --eating        Default eating distance for Individuals
  -m , --mutation      Default mutation chance of Individuals (in percent)

## User Manual

This Python simulation aims to explain and show evolution.

![](https://imgur.com/aMUEZr7.png)

1: The Simulation Area - this is the area that the [simulation](#simulation) is run and displayed.

2: Next Button - this button runs one day in the simulation. NOTE: this button cannot be pressed whilst the simulation is running.

3: Run Button - this button automatically runs the simulation until you press it again.

4: Status Text - this tells you what the simulation is doing.

5: Day Counter - this shows you how many days have passed since the start of the simulation.

6: Peak Population Counter - this displays the highest ever number of [Individuals](#individuals) alive during this simulation.

7: Number of Individuals Alive Counter - this simply displays the current amount of Individuals that are alive.

8: [Chart and Graph Area](#chart-and-graph-area) - any graphs and charts about the simulation are displayed here.

### Simulation

The simulation is the main aspect of evolution-simulator-3.

It handles the [Individuals](#individuals), [food](#food), and anything else in the simulation area.

### Individuals

![An individual](https://imgur.com/g0YlFpn.png)

Individuals are the only creatures in evolution-simulator-3.

They consist of a black filled circle which is their body, two coloured rings representing their vision distance (blue) and eating distance (red), and some text above their body that signifies their energy.

An individual's vision distance determines how far it can move each day.

An individual's eating distance determines how close food has to be to the Individual for it to be eaten.

Individuals can reproduce each day, which takes 10 energy.

Each day an Individual must use 1 energy to survive to the next day.

If an Individual has 0 or less energy, it dies.

When an Individual is born, it starts with 2 energy.

## Food

Food is the sole source of energy for Individuals.

Food has a nutrition value, which defaults to 2.

Food can be eaten when it is within an Individual's eating distance.

## Chart and Graph Area

The Chart and Graph Area displays any charts and graphs to do with the simulation.

The default graphs are population over time, average vision distance over time, and average eating distance over time.