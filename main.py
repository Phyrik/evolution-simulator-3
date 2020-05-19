import pygame, pygame.key
import random
import time
import sys
import math
import threading
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
import os

os.remove("population-graph.png")

WIDTH = 1000
HEIGHT = 500
SIMULATIONDRAWOFFSETX = 100
SIMULATIONDRAWOFFSETY = 50
REPRODUCTIONENERGY = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("evolution-simulator-3")

def distanceBetween(a, b):
    xa = a[0]
    xb = b[0]
    ya = a[1]
    yb = b[1]

    return math.sqrt(((xa - xb)**2) + ((ya - yb)**2))

# main evolution classes


class Population:
    def __init__(self, startingNumberOfIndividuals, baseMutationChancePercent, baseEatingDistance, baseVisionDistance, simulationAreaSize, pygameScreen, foodToSpawnEachTurn, simulationPlayer):
        self.startingNumberOfIndividuals = startingNumberOfIndividuals
        self.baseMutationChancePercent = baseMutationChancePercent
        self.baseEatingDistance = baseEatingDistance
        self.baseVisionDistance = baseVisionDistance
        self.simulationAreaSize = simulationAreaSize
        self.pygameScreen = pygameScreen
        self.simulationPlayer = simulationPlayer

        self.amountOfAliveIndividuals = startingNumberOfIndividuals
        self.amountOfDeadIndividuals = 0
        self.listOfPopulationEachDay = []

        self.individualsList = []
        for i in range(1, startingNumberOfIndividuals + 1):
            individual = Individual(self.baseEatingDistance, self.baseVisionDistance, self.baseMutationChancePercent, None, 1, [random.randint(0, self.simulationAreaSize["width"]), random.randint(0, self.simulationAreaSize["height"])], self)
            self.individualsList.append(individual)

        self.highestPopulation = len(self.individualsList)

        self.foodSpawner = FoodSpawner(foodToSpawnEachTurn, self.simulationAreaSize, self.pygameScreen)
        self.foodSpawner.spawnAndDrawFood()

        self.redrawIndividuals()

    def nextDay(self):
        # handle the next day (remember pause points!)

        if len(self.individualsList) > self.highestPopulation:
            self.highestPopulation = len(self.individualsList)

        self.foodSpawner.spawnAndDrawFood()
        self.simulationPlayer.setStatusText("Food spawned.")
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY, 800, 400), 2)
        simulationPlayer.redrawSimulation()
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (0, SIMULATIONDRAWOFFSETY + 400, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (SIMULATIONDRAWOFFSETX + 800 + 1, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        simulationPlayer.redrawGUI()
        pygame.display.flip()

        for individual in self.individualsList:
            if individual.energy <= 0:
                individual.die()

        self.simulationPlayer.setStatusText("Killed 0 energy Individuals.")
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY, 800, 400), 2)
        simulationPlayer.redrawSimulation()
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (0, SIMULATIONDRAWOFFSETY + 400, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (SIMULATIONDRAWOFFSETX + 800 + 1, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        simulationPlayer.redrawGUI()
        pygame.display.flip()

        for individual in self.individualsList:
            individual.eatFood()

        self.simulationPlayer.setStatusText("Individuals have eaten their food.")
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY, 800, 400), 2)
        simulationPlayer.redrawSimulation()
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (0, SIMULATIONDRAWOFFSETY + 400, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (SIMULATIONDRAWOFFSETX + 800 + 1, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        simulationPlayer.redrawGUI()
        pygame.display.flip()

        for individual in self.individualsList:
            if individual.energy >= REPRODUCTIONENERGY:
                individual.reproduce()

        self.simulationPlayer.setStatusText("Individuals have reproduced.")
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY, 800, 400), 2)
        simulationPlayer.redrawSimulation()
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (0, SIMULATIONDRAWOFFSETY + 400, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (SIMULATIONDRAWOFFSETX + 800 + 1, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        simulationPlayer.redrawGUI()
        pygame.display.flip()

        for individual in self.individualsList:
            individual.move()
        for food in self.foodSpawner.foodList:
            food.individualMovingToSelf = False

        self.simulationPlayer.setStatusText("Individuals have moved to their next best position.")
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY, 800, 400), 2)
        simulationPlayer.redrawSimulation()
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (0, SIMULATIONDRAWOFFSETY + 400, WIDTH, SIMULATIONDRAWOFFSETY))
        pygame.draw.rect(screen, (255, 255, 255), (SIMULATIONDRAWOFFSETX + 800 + 1, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
        simulationPlayer.redrawGUI()
        pygame.display.flip()

        for individual in self.individualsList:
            individual.energy -= 1

        self.simulationPlayer.currentDay += 1
        self.listOfPopulationEachDay.append(len(self.individualsList))

        plt.clf()
        plt.plot(self.listOfPopulationEachDay, label="Population")
        xint = range(min(self.listOfPopulationEachDay), math.ceil(max(self.listOfPopulationEachDay)) + 1)
        plt.legend()
        plt.savefig("population-graph.png")

    def redrawIndividuals(self):
        for individual in self.individualsList:
            if not individual.selected:
                pygame.draw.circle(self.pygameScreen, (0, 0, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), 8)
            if individual.selected:
                pygame.draw.circle(self.pygameScreen, (0, 255, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), 8)
            pygame.draw.circle(self.pygameScreen, (255, 0, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), individual.eatingDistance, 2)
            pygame.draw.circle(self.pygameScreen, (0, 0, 255), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), individual.visionDistance, 2)
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(str(individual.energy), 1, (0, 0, 0))
            self.pygameScreen.blit(text, (individual.location[0] - (text.get_width() / 2) + SIMULATIONDRAWOFFSETX, individual.location[1] - 40 + SIMULATIONDRAWOFFSETY, 0, 0))


class Individual:
    def __init__(self, eatingDistance, visionDistance, mutationChancePercent, parent, generation, location, population):
        self.eatingDistance = eatingDistance
        self.visionDistance = visionDistance
        self.mutationChancePercent = mutationChancePercent
        self.familyTree = FamilyTree(parent, generation)
        self.location = location
        self.population = population
        self.energy = 2
        self.state = "alive"
        self.selected = False

    def eatFood(self):
        for food in self.population.foodSpawner.foodList:
            distance = distanceBetween(food.location, self.location)
            if distance <= self.eatingDistance:
                self.energy += food.nutrition
                self.population.foodSpawner.destroy(food)

    def reproduce(self):
        eatingMutationRoll = random.randint(1, 100)
        visionMutationRoll = random.randint(1, 100)
        mutationMutationRoll = random.randint(1, 100)

        if eatingMutationRoll <= self.mutationChancePercent:
            eatingMutationSignRoll = random.randint(1, 2)
            if eatingMutationSignRoll == 1:
                childEatingDistance = self.eatingDistance + random.randint(1, 5)
            if eatingMutationSignRoll == 2:
                childEatingDistance = self.eatingDistance - random.randint(1, 5)
        else:
            childEatingDistance = self.eatingDistance

        if visionMutationRoll <= self.mutationChancePercent:
            visionMutationSignRoll = random.randint(1, 2)
            if visionMutationSignRoll == 1:
                childVisionDistance = self.visionDistance + random.randint(1, 5)
            if visionMutationSignRoll == 2:
                childVisionDistance = self.visionDistance - random.randint(1, 5)
        else:
            childVisionDistance = self.visionDistance

        if mutationMutationRoll <= self.mutationChancePercent:
            mutationMutationSignRoll = random.randint(1, 2)
            if mutationMutationSignRoll == 1:
                childMutationChancePercent = self.mutationChancePercent + random.randint(1, 5)
            if mutationMutationSignRoll == 2:
                childMutationChancePercent = self.mutationChancePercent - random.randint(1, 5)
        else:
            childMutationChancePercent = self.mutationChancePercent

        child = Individual(childEatingDistance, childVisionDistance, childMutationChancePercent, self, self.familyTree.generation + 1, self.location, self.population)
        self.population.individualsList.append(child)
        self.energy -= REPRODUCTIONENERGY

    def die(self):
        self.state = "dead"
        self.population.individualsList.remove(self)

    def move(self):
        closestDistance = 9999
        closestLocation = self.location
        closestFood = None

        for food in self.population.foodSpawner.foodList:
            if not food.individualMovingToSelf:
                distance = distanceBetween(food.location, self.location)
                if distance <= self.visionDistance:
                    if distance < closestDistance:
                        closestDistance = distance
                        closestLocation = food.location
                        closestFood = food

        self.location = closestLocation
        try:
            closestFood.individualMovingToSelf = True
        except:
            pass
        

class FamilyTree:
    def __init__(self, parent, generation):
        self.parent = parent
        self.children = []
        self.generation = generation


class SimulationPlayer:
    def __init__(self, simulationAreaSize, startingNumberOfIndividuals, baseMutationChancePercent, baseEatingDistance, baseVisionDistance, pygameScreen, foodToSpawnEachTurn):
        self.population = Population(startingNumberOfIndividuals, baseMutationChancePercent, baseEatingDistance, baseVisionDistance, simulationAreaSize, pygameScreen, foodToSpawnEachTurn, self)
        self.simulationAreaSize = simulationAreaSize
        self.pygameScreen = pygameScreen
        self.currentStatusText = " "
        self.runAuto = False
        self.currentIndividualForDetails = None
        self.currentDay = 0

    def redrawGUI(self):
        pygame.draw.rect(self.pygameScreen, (200, 200, 200), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY + 400, SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY), 0)
        pygame.draw.rect(self.pygameScreen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY + 400, SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY), 1)
        pygame.draw.rect(self.pygameScreen, (200, 200, 200), (SIMULATIONDRAWOFFSETX + SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY + 400, SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY), 0)
        pygame.draw.rect(self.pygameScreen, (0, 0, 0), (SIMULATIONDRAWOFFSETX + SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY + 400, SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY), 1)
        font = pygame.font.SysFont('comicsans', 30)
        if not self.runAuto:
            text = font.render("Next", 1, (0, 0, 0))
            self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + (SIMULATIONDRAWOFFSETY / 2 - text.get_width() / 2), SIMULATIONDRAWOFFSETY + 400 + (SIMULATIONDRAWOFFSETY / 2 - text.get_height() / 2)))
        if self.runAuto:
            text = font.render("Next", 1, (100, 100, 100))
            self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + (SIMULATIONDRAWOFFSETY / 2 - text.get_width() / 2), SIMULATIONDRAWOFFSETY + 400 + (SIMULATIONDRAWOFFSETY / 2 - text.get_height() / 2)))
        if not self.runAuto:
            text = font.render("Run", 1, (0, 0, 0))
            self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + (SIMULATIONDRAWOFFSETY / 2 - text.get_width() / 2) + SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY + 400 + (SIMULATIONDRAWOFFSETY / 2 - text.get_height() / 2)))
        if self.runAuto:
            text = font.render("Stop", 1, (0, 0, 0))
            self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + (SIMULATIONDRAWOFFSETY / 2 - text.get_width() / 2) + SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY + 400 + (SIMULATIONDRAWOFFSETY / 2 - text.get_height() / 2)))

        text = font.render("Individuals alive: " + str(len(self.population.individualsList)), 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY - text.get_height(), 0, 0))

        text = font.render("Day", 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + 800 + SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY, 0, 0))
        text = font.render(str(self.currentDay), 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + 800 + SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY + 20, 0, 0))

        text = font.render("Peak population: " + str(self.population.highestPopulation), 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + 800 - text.get_width(), SIMULATIONDRAWOFFSETY - text.get_height(), 0, 0))

        text = font.render(self.currentStatusText, 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + 800 - text.get_width(), HEIGHT - text.get_height()))

        try:
            populationGraph = pygame.image.load("population-graph.png")
            populationGraph = pygame.transform.scale(populationGraph, (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETX))
            screen.blit(populationGraph, (SIMULATIONDRAWOFFSETX + 800, SIMULATIONDRAWOFFSETY + 400 - populationGraph.get_height(), 0, 0))
        except:
            pass

        self.redrawDetails()

    def checkForButtonPresses(self):
        if pygame.mouse.get_pos()[1] > SIMULATIONDRAWOFFSETY + 400 and pygame.mouse.get_pos()[1] < SIMULATIONDRAWOFFSETY + 400 + SIMULATIONDRAWOFFSETY:
            if pygame.mouse.get_pos()[0] > SIMULATIONDRAWOFFSETX and pygame.mouse.get_pos()[0] < SIMULATIONDRAWOFFSETX + SIMULATIONDRAWOFFSETY:
                return "next"
            if pygame.mouse.get_pos()[0] > SIMULATIONDRAWOFFSETX + SIMULATIONDRAWOFFSETY and pygame.mouse.get_pos()[0] < SIMULATIONDRAWOFFSETX + SIMULATIONDRAWOFFSETY + SIMULATIONDRAWOFFSETY:
                if not self.runAuto:
                    return "run"
                if self.runAuto:
                    return "stop"
        if pygame.mouse.get_pos()[1] > SIMULATIONDRAWOFFSETY + 400 - SIMULATIONDRAWOFFSETX and pygame.mouse.get_pos()[1] < SIMULATIONDRAWOFFSETY + 400:
            if pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[0] < SIMULATIONDRAWOFFSETX:
                return "popGraph"
        return None

    def redrawSimulation(self):
        self.population.foodSpawner.redrawFood()
        self.population.redrawIndividuals()

    def setStatusText(self, text):
        self.currentStatusText = text

        font = pygame.font.SysFont('comicsans', 20)
        text = font.render(text, 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + 800 - text.get_width(), HEIGHT - text.get_height()))

    def showDetailsOfIndividual(self, individual):
        if self.currentIndividualForDetails != None:
            self.currentIndividualForDetails.selected = False
        self.currentIndividualForDetails = individual
        individual.selected = True

        self.redrawDetails()

    def redrawDetails(self):
        if self.currentIndividualForDetails != None:
            if self.currentIndividualForDetails.state == "alive":
                smallFont = pygame.font.SysFont('comicsans', 25)
                bigFont = pygame.font.SysFont('comicsans', 40)

                text = smallFont.render("Generation", 1, (0, 0, 0))
                self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY, 0, 0))
                text = bigFont.render(str(self.currentIndividualForDetails.familyTree.generation), 1, (0, 0, 0))
                self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY + 15, 0, 0))

                text = smallFont.render("Eating Dist.", 1, (0, 0, 0))
                self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY + 60, 0, 0))
                text = bigFont.render(str(self.currentIndividualForDetails.eatingDistance), 1, (0, 0, 0))
                self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY + 60 + 15, 0, 0))

                text = smallFont.render("Vision Dist.", 1, (0, 0, 0))
                self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY + 60 * 2, 0, 0))
                text = bigFont.render(str(self.currentIndividualForDetails.visionDistance), 1, (0, 0, 0))
                self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY + 60 * 2 + 15, 0, 0))

            if self.currentIndividualForDetails.state == "dead":
                font = pygame.font.SysFont('comicsans', 25)
                text = font.render("Dead", 1, (0, 0, 0))
                self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX / 2 - text.get_width() / 2, SIMULATIONDRAWOFFSETY, 0, 0))


class FoodSpawner:
    def __init__(self, foodToSpawnEachTurn, simulationAreaSize, pygameScreen):
        self.foodToSpawnEachTurn = foodToSpawnEachTurn
        self.simulationAreaSize = simulationAreaSize
        self.foodList = []
        self.pygameScreen = pygameScreen

    def spawnAndDrawFood(self):
        for i in range(1, self.foodToSpawnEachTurn):
            food = Food(2, [random.randint(0, self.simulationAreaSize["width"]), random.randint(0, self.simulationAreaSize["height"])])
            self.foodList.append(food)
            pygame.draw.circle(self.pygameScreen, (0, 0, 0), (food.location[0] + SIMULATIONDRAWOFFSETX, food.location[1] + SIMULATIONDRAWOFFSETY), 2)

    def redrawFood(self):
        for food in self.foodList:
            pygame.draw.circle(self.pygameScreen, (0, 0, 0), (food.location[0] + SIMULATIONDRAWOFFSETX, food.location[1] + SIMULATIONDRAWOFFSETY), 2)

    def destroy(self, food):
        self.foodList.remove(food)


class Food:
    def __init__(self, nutrition, location):
        self.nutrition = nutrition
        self.location = location
        self.individualMovingToSelf = False


# a = amount, m = mutation, e = eating, v = vision, f = food       a↓  m↓  e↓  v↓          f↓
simulationPlayer = SimulationPlayer({"width": 800, "height": 400}, 10, 10, 20, 50, screen, 100)

running = True
while running:
    # main loop
    simulationPlayer.setStatusText("New day.")

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY, 800, 400), 2)
    simulationPlayer.redrawSimulation()
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, SIMULATIONDRAWOFFSETY))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (0, SIMULATIONDRAWOFFSETY + 400, WIDTH, SIMULATIONDRAWOFFSETY))
    pygame.draw.rect(screen, (255, 255, 255), (SIMULATIONDRAWOFFSETX + 800 + 1, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
    simulationPlayer.redrawGUI()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttonPressed = simulationPlayer.checkForButtonPresses()
            if buttonPressed == "next" and simulationPlayer.runAuto == False:
                simulationPlayer.population.nextDay()
            if buttonPressed == "run":
                simulationPlayer.runAuto = True
            if buttonPressed == "stop":
                simulationPlayer.runAuto = False
            if buttonPressed == "popGraph":
                simulationPlayer.openPopGraph()
            for individual in simulationPlayer.population.individualsList:
                if distanceBetween((pygame.mouse.get_pos()[0] - SIMULATIONDRAWOFFSETX, pygame.mouse.get_pos()[1] - SIMULATIONDRAWOFFSETY), individual.location) <= 8:
                    simulationPlayer.showDetailsOfIndividual(individual)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                simulationPlayer.currentIndividualForDetails.selected = False
                simulationPlayer.currentIndividualForDetails = None

    if simulationPlayer.runAuto:
        simulationPlayer.population.nextDay()
        
    buttonPressed = None

    #time.sleep(0.01)

    pygame.display.flip()

pygame.display.quit()
pygame.quit()
sys.exit()
