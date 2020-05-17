import pygame
import random
import time
import sys
import math

WIDTH = 1000
HEIGHT = 500
SIMULATIONDRAWOFFSETX = 100
SIMULATIONDRAWOFFSETY = 50
REPRODUCTIONENERGY = 4

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

        self.individualsList = []
        for i in range(1, startingNumberOfIndividuals):
            individual = Individual(self.baseEatingDistance, self.baseVisionDistance, self.baseMutationChancePercent, None, 1, [random.randint(0, self.simulationAreaSize["width"]), random.randint(0, self.simulationAreaSize["height"])], self)
            self.individualsList.append(individual)

        self.foodSpawner = FoodSpawner(foodToSpawnEachTurn, self.simulationAreaSize, self.pygameScreen)
        self.foodSpawner.spawnAndDrawFood()
        for individual in self.individualsList:
                pygame.draw.circle(self.pygameScreen, (0, 0, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), 8)
                pygame.draw.circle(self.pygameScreen, (255, 0, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), individual.eatingDistance, 2)
                pygame.draw.circle(self.pygameScreen, (0, 0, 255), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), individual.visionDistance, 2)

    def nextDay(self):
        # handle the next day (remember pause points!)

        self.foodSpawner.spawnAndDrawFood()
        self.simulationPlayer.setStatusText("Food spawned.")
        self.simulationPlayer.pausePoint()

        for individual in self.individualsList:
            if individual.energy <= 0:
                individual.die()

        self.simulationPlayer.setStatusText("Killed 0 energy Individuals.")
        self.simulationPlayer.pausePoint()

        for individual in self.individualsList:
            individual.eatFood()

        self.simulationPlayer.setStatusText("Individuals have eaten their food.")
        self.simulationPlayer.pausePoint()

        for individual in self.individualsList:
            if individual.energy >= REPRODUCTIONENERGY:
                individual.reproduce()

        self.simulationPlayer.setStatusText("Individuals have reproduced.")
        self.simulationPlayer.pausePoint()

        for individual in self.individualsList:
            individual.energy -= 1

    def redrawIndividuals(self):
        for individual in self.individualsList:
            pygame.draw.circle(self.pygameScreen, (0, 0, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), 8)
            pygame.draw.circle(self.pygameScreen, (255, 0, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), individual.eatingDistance, 2)
            pygame.draw.circle(self.pygameScreen, (0, 0, 255), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), individual.visionDistance, 2)


class Individual:
    def __init__(self, eatingDistance, visionDistance, mutationChancePercent, parent, generation, location, population):
        self.eatingDistance = eatingDistance
        self.visionDistance = visionDistance
        self.mutationChancePercent = mutationChancePercent
        self.familyTree = FamilyTree(parent, generation)
        self.location = location
        self.population = population
        self.energy = 2

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
        self.population.individualsList.remove(self)
        

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
        
    def pausePoint(self):
        # handle a point that the "next pause point" button will bring you to

        goToNextPoint = False

        while not goToNextPoint:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttonPressed = simulationPlayer.checkForButtonPresses()
                    if buttonPressed == "next":
                        goToNextPoint = True

            self.pygameScreen.fill((255, 255, 255))
            pygame.draw.rect(self.pygameScreen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY, 800, 400), 2)
            self.redrawSimulation()
            pygame.draw.rect(self.pygameScreen, (255, 255, 255), (0, 0, WIDTH, SIMULATIONDRAWOFFSETY))
            pygame.draw.rect(self.pygameScreen, (255, 255, 255), (0, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
            pygame.draw.rect(self.pygameScreen, (255, 255, 255), (0, SIMULATIONDRAWOFFSETY + 400 + 2, WIDTH, SIMULATIONDRAWOFFSETY))
            pygame.draw.rect(self.pygameScreen, (255, 255, 255), (SIMULATIONDRAWOFFSETX + 800 + 1, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
            self.redrawGUI()

            buttonPressed = None

            pygame.display.flip()

    def redrawGUI(self):
        pygame.draw.rect(self.pygameScreen, (200, 200, 200), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY + 400, SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY), 0)
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render("Next", 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + (SIMULATIONDRAWOFFSETY / 2 - text.get_width() / 2), SIMULATIONDRAWOFFSETY + 400 + (SIMULATIONDRAWOFFSETY / 2 - text.get_height() / 2)))

        text = font.render("Individuals alive: " + str(len(self.population.individualsList)), 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY / 4, 0, 0))

        text = font.render(self.currentStatusText, 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + 800 - text.get_width(), HEIGHT - text.get_height()))

    def checkForButtonPresses(self):
        if pygame.mouse.get_pos()[1] > SIMULATIONDRAWOFFSETY + 400 and pygame.mouse.get_pos()[1] < SIMULATIONDRAWOFFSETY + 400 + SIMULATIONDRAWOFFSETY:
            if pygame.mouse.get_pos()[0] > SIMULATIONDRAWOFFSETX and pygame.mouse.get_pos()[0] < SIMULATIONDRAWOFFSETX + SIMULATIONDRAWOFFSETY:
                return "next"
        return None

    def redrawSimulation(self):
        self.population.foodSpawner.redrawFood()
        self.population.redrawIndividuals()

    def setStatusText(self, text):
        self.currentStatusText = text

        font = pygame.font.SysFont('comicsans', 20)
        text = font.render(text, 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + 800 - text.get_width(), HEIGHT - text.get_height()))  


class FoodSpawner:
    def __init__(self, foodToSpawnEachTurn, simulationAreaSize, pygameScreen):
        self.foodToSpawnEachTurn = foodToSpawnEachTurn
        self.simulationAreaSize = simulationAreaSize
        self.foodList = []
        self.pygameScreen = pygameScreen

    def spawnAndDrawFood(self):
        for i in range(1, self.foodToSpawnEachTurn):
            food = Food(1, [random.randint(0, self.simulationAreaSize["width"]), random.randint(0, self.simulationAreaSize["height"])])
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


# a = amount, m = mutation, e = eating, v = vision, f = food       a↓  m↓ e↓  v↓          f↓
simulationPlayer = SimulationPlayer({"width": 800, "height": 400}, 10, 5, 20, 50, screen, 200)

running = True
while running:
    # main loop
    simulationPlayer.setStatusText("New day.")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttonPressed = simulationPlayer.checkForButtonPresses()
            if buttonPressed == "next":
                simulationPlayer.population.nextDay()

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY, 800, 400), 2)
    simulationPlayer.redrawSimulation()
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, SIMULATIONDRAWOFFSETY))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (0, SIMULATIONDRAWOFFSETY + 400 + 2, WIDTH, SIMULATIONDRAWOFFSETY))
    pygame.draw.rect(screen, (255, 255, 255), (SIMULATIONDRAWOFFSETX + 800 + 1, 0, SIMULATIONDRAWOFFSETX, HEIGHT))
    simulationPlayer.redrawGUI()
        
    buttonPressed = None

    #time.sleep(0.01)

    pygame.display.flip()

pygame.display.quit()
pygame.quit()
sys.exit()
