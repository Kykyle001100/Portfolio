import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('Monospace', 32, True)

clock = pygame.time.Clock()
daylight = 0

plants = []

def metabolize(self, tiles, tile, rate):
    if self.energy > 0.2:
        strings = self.metabolism.split(' ')
        last = ""
        lastlast = ""
        for s in strings:
            if last == "citrate" and s == "synthesis":
                self.energy += 0.1 * rate
                self.nutrients -= 0.1 * rate
                tiles.modify(*tile, tiles.get(*tile) + 0.001 * rate)
            if last == "citrate" and s == "oxidation":
                self.energy += 0.2 * rate * tiles.O2
                self.nutrients -= 1 * rate * tiles.O2
                tiles.CO2 = max(0, min(1, tiles.CO2 + 0.0000001))
                tiles.O2 = max(0, min(1, tiles.O2 - 0.0000001))
            if last == "glucose" and s == "synthesis":
                self.energy -= 0.1 * rate
                self.nutrients += 0.2 * rate
            if last == "glucose" and s == "oxidation":
                self.energy += 0.2 * rate * tiles.O2
                self.nutrients -= 0.1 * rate * tiles.O2
                tiles.CO2 = max(0, min(1, tiles.CO2 + 0.0000001))
                tiles.O2 = max(0, min(1, tiles.O2 - 0.0000001))
            if lastlast == "water" and last == "photo" and s == "lysis":
                self.energy += (0.1 * ((math.sin(daylight)+1)/2) * rate) / (tiles.O2 + 1)
                self.nutrients -= 0.03 * ((math.sin(daylight)+1)/2) * rate / (tiles.O2 + 1)
                tiles.O2 = max(0, min(1, tiles.O2 + 0.0000001))
            if last == "ribulose" and s == "carboxylation":
                self.energy -= 0.07 * rate * tiles.CO2
                self.nutrients += 0.12 * rate * tiles.CO2
                tiles.CO2 = max(0, min(1, tiles.CO2 - 0.0000001))
            if last == "ribulose" and s == "oxidation":
                self.energy += 0.1 * rate
                self.nutrients -= 0.1 * rate
            if last == "nitrogen" and s == "reduction":
                self.energy -= 0.3 * rate
                self.nutrients += 0.5 * rate
                tiles.N2 = max(0, min(1, tiles.N2 - 0.0000001))
                tiles.modify(*tile, tiles.get(*tile) + 0.01 * rate)
            if last == "hydrogen" and s == "lysis":
                self.energy += 0.2 * rate * tiles.H2
                tiles.H2 = max(0, min(1, tiles.H2 - 0.0000001))
            if last == "glucose" and s == "fermentation":
                self.energy += 0.2 * rate * tiles.H2
                self.nutrients -= 0.1 * rate * tiles.H2
                tiles.H2 = max(0, min(1, tiles.H2 - 0.0000001))

            lastlast = last
            last = s

def mutate_bacterial_genome(genome):
    keywords = [
        "citrate", "glucose", "water", "ribulose",
        "nitrogen", "hydrogen",

        "photo",

        "synthesis", "oxidation", "lysis",
        "carboxylation", "reduction", "fermentation"
    ]

    new_genome = ""

    keyword = random.choice(keywords)
    choice = random.choice([True, False, None, 0, 1])
    if choice == None:
        new_genome = genome + " " + keyword
    elif choice == False:
        new_genome = keyword + " " + genome
    elif choice == 0:
        words = genome.split(' ')
        new_genome = " ".join(words[:-1])
    elif choice == 1:
        words = genome.split(' ')
        new_genome = " ".join(words[1:])
    else:
        words = genome.split(' ')
        n = random.randint(0, len(words)-1)
        words[n] = keyword
        new_genome = " ".join(words)

    return new_genome

def generate_bacterial_genome():
    metabolism1 = random.choice([
        "citrate synthesis", "citrate oxidation",
        "glucose synthesis", "glucose oxidation",
        "water photo lysis", "ribulose carboxylation",
        "ribulose oxidation", "nitrogen reduction",
        "hydrogen lysis", "glucose fermentation"
    ])
    metabolism2 = random.choice([
        "citrate synthesis", "citrate oxidation",
        "glucose synthesis", "glucose oxidation",
        "water photo lysis", "ribulose carboxylation",
        "ribulose oxidation", "nitrogen reduction",
        "hydrogen lysis", "glucose fermentation"
    ])
    return metabolism1 + " " + metabolism2

class Tiles:
    def __init__(self):
        self.tiles = {}
        self.bacteria = {}

        self.CO2 = random.uniform(0, 1)
        self.O2 = random.uniform(0, 1)
        self.N2 = random.uniform(0, 1)
        self.H2 = random.uniform(0, 1)

    def init(self):
        for x in range(0, WIDTH, 100):
            for y in range(0, HEIGHT, 100):
                self.tiles[(x, y)] = random.uniform(0, 1)
                self.bacteria[(x, y)] = Bacteria(generate_bacterial_genome(), random.uniform(0.3, 1))

    def get(self, x, y):
        cell = (x // 100 * 100, y // 100 * 100)
        return self.tiles.get(cell, 0)

    def modify(self, x, y, value):
        cell = (x // 100 * 100, y // 100 * 100)
        self.tiles[cell] = value + self.tiles.get(cell, 0)
        self.tiles[cell] = max(0, min(1, self.tiles[cell]))

    def draw(self):
        for (x, y), value in self.tiles.items():
            color = (int(value * 139), int(value * 59), int(value * 19))
            pygame.draw.rect(screen, color, (x, y, 100, 100))

        for (x, y), bacteria in self.bacteria.items():
            if bacteria:
                bacteria.update(self,
                                ((random.choice([-100, 0, 100])+x)%WIDTH, (random.choice([-100, 0, 100])+y)%HEIGHT),
                                (x, y)
                )

                surface = pygame.Surface((100, 100), pygame.SRCALPHA)
                color = (50, 255, 50, int(bacteria.rate * 128))
                pygame.draw.rect(surface, color, (0, 0, 100, 100))
                screen.blit(surface, (x, y))

class Grid:
    def __init__(self):
        self.contents = {}

    def add(self, obj):
        cell = (obj.x // 100, obj.y // 100)
        if cell not in self.contents:
            self.contents[cell] = []
        self.contents[cell].append(obj)

    def query(self, obj):
        cell = (obj.x // 100, obj.y // 100)
        return self.contents.get(cell, [])

    def clear(self):
        self.contents.clear()

class Bacteria:
    def __init__(self, metabolism, rate):
        self.metabolism = metabolism
        self.rate = rate
        self.energy = 5
        self.nutrients = 5

    def same_species(self, other):
        return self.rate == other.rate and self.metabolism == other.metabolism 

    def update(self, tiles, neighbor, tile):
        rate = self.rate or self.metabolic_rate

        metabolize(self, tiles, tile, rate)

        if self.nutrients < 10:
            tile_value = tiles.get(*tile)

            self.nutrients += tile_value * 0.001 * (1 / 60) * rate
            tiles.modify(*tile, tile_value * 0.001 * (1 / 60) * rate)

        if neighbor != tile and self.energy > 10 and self.nutrients > 10:
            if neighbor in tiles.bacteria:
                other_bacteria = tiles.bacteria[neighbor]
                if other_bacteria:
                    if self.energy > other_bacteria.energy + 2 and self.rate > other_bacteria.rate and not self.same_species(other_bacteria):
                        offspring = Bacteria(self.metabolism, self.rate)
                        if random.random() < 0.1:
                            offspring.rate += random.uniform(-0.1, 0.1)
                        if random.random() < 0.1:
                            offspring.metabolism = mutate_bacterial_genome(offspring.metabolism)
                        tiles.bacteria[neighbor] = offspring
                        self.nutrients -= 5
                        self.energy -= 5
                    else:
                        tiles.bacteria[neighbor].nutrients += self.nutrients / 2
                        self.nutrients /= 2

        if self.energy <= 0:
            tiles.bacteria[tile] = None

class Fruit:
    def __init__(self, x, y, nutrients, genome):
        self.x, self.y = x, y
        self.nutrients = nutrients
        self.genome = genome
        self.time = 2

    def update(self):
        self.time = max(0, self.time - (1 / FPS))

        if self.time <= 0:
            max_size = self.genome['max_size']
            fruit_properties = self.genome['fruit']
            metabolism_properties = self.genome['metabolism']
            plant = Plant(self.x, self.y, fruit_properties, metabolism_properties, max_size)
            plant.nutrients = self.nutrients
            return plant

    def draw(self, surface):
        pygame.draw.circle(surface, (200, 200, 50), (int(self.x), int(self.y)), int(self.nutrients))

class Plant:
    def __init__(self, x, y, fruit_properties, metabolism_properties, max_size):
        self.x, self.y = x, y
        self.nutrients = 2
        self.does_fruit = fruit_properties['does']
        self.fruit_amount = fruit_properties['amount']
        self.fruits = []
        self.metabolism = metabolism_properties['metabolism']
        self.metabolic_rate = metabolism_properties['rate']
        self.energy = 100
        self.max_size = max_size
        self.size = 2

    def update(self, tiles, plantss):

        before_energy = self.energy

        metabolize(self, tiles, (self.x // 100 * 100, self.y // 100 * 100), self.metabolic_rate)
        
        if self.energy <= before_energy:
            self.energy -= self.metabolic_rate * (1 / FPS)
            if self.energy <= 0:
                self.size = max(1, self.size - 1)
                self.energy = 0
        else:
            self.size = max(1, self.size - 1 * (1/FPS))

        if self.nutrients < self.max_size*1.9:
            tile = tiles.get(self.x, self.y)

            if tile > 0:
                self.nutrients += tile * (1 / 60)
                tiles.modify(self.x, self.y, -tile * (1 / 60))

        if self.nutrients > self.max_size and self.energy >= 90:
            if self.does_fruit:
                angle = random.uniform(0, 2 * math.pi)
                x = self.x + math.cos(angle) * (20 + self.max_size)
                y = self.y + math.sin(angle) * (20 + self.max_size)
                genome = {
                    'max_size': self.max_size,
                    'fruit': {
                        'does': True,
                        'amount': self.fruit_amount
                    },
                    'metabolism': {
                        'metabolism': self.metabolism,
                        'rate': self.metabolic_rate
                    }
                }
                for plant in plantss:
                    dist = math.sqrt((plant.x - x) ** 2 + (plant.y - y) ** 2)
                    if dist > plant.max_size + self.max_size:
                        self.fruits.append(Fruit(x, y, self.nutrients//2, genome))
                        self.nutrients //= 2
                        self.energy //=2
                        break
            else:
                if self.size > self.max_size * 0.5:
                    angle = random.uniform(0, 2 * math.pi)
                    x = self.x + math.cos(angle) * (self.max_size*2)
                    y = self.y + math.sin(angle) * (self.max_size*2)
                    for plant in plantss:
                        dist = math.sqrt((plant.x - x) ** 2 + (plant.y - y) ** 2)
                        if dist > plant.max_size + self.max_size:
                            plants.append(Plant(x, y, {'does': self.does_fruit, 'amount': self.fruit_amount}, {'metabolism': self.metabolism, 'rate': self.metabolic_rate}, self.max_size))
                            self.nutrients //= 2
                            self.energy //= 2
                            break

        self.fruits = self.fruits[:self.fruit_amount]

        if self.size > self.max_size:
            self.size = self.max_size

        for fruit in self.fruits:
            new_plant = fruit.update()
            if new_plant:
                plants.append(new_plant)
                self.fruits.remove(fruit)
                
        if self.nutrients > 0 and self.size < self.max_size:
            self.size += self.nutrients * (1 / 60) * self.metabolic_rate
            self.nutrients -= self.nutrients * 0.01 * (1 / 60) * self.metabolic_rate

        self.nutrients = max(0, self.nutrients)

    def draw(self):
        color = (0, 255, 0)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))
        for fruit in self.fruits:
            fruit.draw(screen)

plant_grid = Grid()
tiles = Tiles()
tiles.init()

plants = [Plant(random.randint(0, WIDTH), random.randint(0, HEIGHT), {'does': random.choice([True, False]), 'amount': random.randint(1, 4)}, {'metabolism': random.choice(["water photo lysis water photo lysis", "ribulose carboxylation glucose oxidation", "water photo lysis water photo lysis ribulose carboxylation", "glucose oxidation water photo lysis water photo lysis"]), 'rate': 0.1}, random.randint(3, 10)) for _ in range(20)]

while True:
    mouse = pygame.mouse.get_pos()
    daylight += 0.001

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                plants.append(Plant(mouse[0], mouse[1], {'does': random.choice([True, False]), 'amount': random.randint(1, 4)}, {'metabolism': random.choice(["water photo lysis water photo lysis", "ribulose carboxylation glucose oxidation", "water photo lysis water photo lysis ribulose carboxylation", "glucose oxidation water photo lysis water photo lysis"]), 'rate': 0.1}, random.randint(3, 10)))

    light = int(((math.sin(daylight) + 1) / 2) * 128)
    screen.fill((light, light, light))

    plant_grid.clear()

    for plant in plants:
        plant_grid.add(plant)

    tiles.draw()

    for plant in plants[:]:
        neighbors = plant_grid.query(plant)
        plant.update(tiles, neighbors)
        plant.draw()

        if plant.energy <= 0:
            plants.remove(plant)
            continue

    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (20, 20, 100, 128 - light), (0, 0, WIDTH, HEIGHT))

    txt = font.render(f"CO2: {tiles.CO2:.4f}", True, (255, 55, 55))
    surface.blit(txt, (10, 10))

    txt = font.render(f"O2: {tiles.O2:.4f}", True, (255, 55, 55))
    surface.blit(txt, (10, 42))

    txt = font.render(f"N2: {tiles.N2:.4f}", True, (255, 55, 55))
    surface.blit(txt, (10, 74))

    txt = font.render(f"H2: {tiles.H2:.4f}", True, (255, 55, 55))
    surface.blit(txt, (10, 106))

    screen.blit(surface, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)