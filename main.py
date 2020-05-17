import pygame
import random
import time
import sys
import math

WIDTH = 1000
HEIGHT = 500
SIMULATIONDRAWOFFSETX = 100
SIMULATIONDRAWOFFSETY = 50

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
        for individual in self.individualsList:
            # handle the next day (remember pause points!)
            self.foodSpawner.spawnAndDrawFood()
            self.simulationPlayer.pausePoint()
            for individual in self.individualsList:
                individual.eatFood()

    def redrawIndividuals(self):
        for individual in self.individualsList:
            pygame.draw.circle(self.pygameScreen, (0, 0, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), 8)
            pygame.draw.circle(self.pygameScreen, (255, 0, 0), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), individual.eatingDistance, 2)
            pygame.draw.circle(self.pygameScreen, (0, 0, 255), (individual.location[0] + SIMULATIONDRAWOFFSETX, individual.location[1] + SIMULATIONDRAWOFFSETY), individual.visionDistance, 2)


class Individual:
    def __init__(self, eatingDistance, visionDistance, mutationChancePercent, parents, generation, location, population):
        self.eatingDistance = eatingDistance
        self.visionDistance = visionDistance
        self.mutationChancePercent = mutationChancePercent
        self.familyTree = FamilyTree(parents, generation)
        self.location = location
        self.population = population
        self.energy = 2

    def eatFood(self):
        for food in self.population.foodSpawner.foodList:
            distance = distanceBetween(food.location, self.location)
            if distance <= self.eatingDistance:
                self.energy += food.nutrition
                self.population.foodSpawner.destroy(food)
        

class FamilyTree:
    def __init__(self, parents, generation):
        self.parents = parents
        self.children = []
        self.generation = generation


class SimulationPlayer:
    def __init__(self, simulationAreaSize, startingNumberOfIndividuals, baseMutationChancePercent, baseEatingDistance, baseVisionDistance, pygameScreen, foodToSpawnEachTurn):
        self.population = Population(startingNumberOfIndividuals, baseMutationChancePercent, baseEatingDistance, baseVisionDistance, simulationAreaSize, pygameScreen, foodToSpawnEachTurn, self)
        self.simulationAreaSize = simulationAreaSize
        self.pygameScreen = pygameScreen
        
    def pausePoint(self):
        # handle a point that the "next pause point" button will bring you to
        pass

    def redrawGUI(self):
        pygame.draw.rect(self.pygameScreen, (200, 200, 200), (SIMULATIONDRAWOFFSETX, SIMULATIONDRAWOFFSETY + 400, SIMULATIONDRAWOFFSETY, SIMULATIONDRAWOFFSETY), 0)
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render("Next", 1, (0, 0, 0))
        self.pygameScreen.blit(text, (SIMULATIONDRAWOFFSETX + (SIMULATIONDRAWOFFSETY / 2 - text.get_width() / 2), SIMULATIONDRAWOFFSETY + 400 + (SIMULATIONDRAWOFFSETY / 2 - text.get_height() / 2)))

    def checkForButtonPresses(self):
        if pygame.mouse.get_pos()[1] > SIMULATIONDRAWOFFSETY + 400 and pygame.mouse.get_pos()[1] < SIMULATIONDRAWOFFSETY + 400 + SIMULATIONDRAWOFFSETY:
            if pygame.mouse.get_pos()[0] > SIMULATIONDRAWOFFSETX and pygame.mouse.get_pos()[0] < SIMULATIONDRAWOFFSETX + SIMULATIONDRAWOFFSETY:
                return "next"
        return None

    def redrawSimulation(self):
        self.population.foodSpawner.redrawFood()
        self.population.redrawIndividuals()


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


# a = amount, m = mutation, e = eating, v = vision                 a   m  e   v
simulationPlayer = SimulationPlayer({"width": 800, "height": 400}, 10, 5, 20, 50, screen, 100)

running = True
while running:
    # main loop
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
