import pygame
import random
import time
import sys

WIDTH = 1000
HEIGHT = 500
SIMULATIONDRAWOFFSETX = 100
SIMULATIONDRAWOFFSETY = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("evolution-simulator-3")

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
    
    def nextDay(self):
        for individual in self.individualsList:
            # handle the next day (remember pause points!)
            self.foodSpawner.spawnAndDrawFood()
            self.simulationPlayer.pausePoint()
            individual.eatFood()


class Individual:
    def __init__(self, eatingDistance, visionDistance, mutationChancePercent, parents, generation, location, population):
        self.eatingDistance = eatingDistance
        self.visionDistance = visionDistance
        self.mutationChancePercent = mutationChancePercent
        self.familyTree = FamilyTree(parents, generation)
        self.location = location
        self.population = population

    def eatFood(self):
        pass
        

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


class Food:
    def __init__(self, nutrition, location):
        self.nutrition = nutrition
        self.location = location


simulationPlayer = SimulationPlayer({"width": 800, "height": 400}, 10, 5, 10, 20, screen, 100)

running = True
while running:
    # main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    simulationPlayer.redrawGUI()
    simulationPlayer.redrawSimulation()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttonPressed = simulationPlayer.checkForButtonPresses()
            if buttonPressed == "next":
                print("sb1")
                simulationPlayer.population.nextDay()
    buttonPressed = None

    time.sleep(0.01)

    pygame.display.flip()

pygame.display.quit()
pygame.quit()
sys.exit()
