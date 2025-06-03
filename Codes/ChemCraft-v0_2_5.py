"""
the main python script of the game `ChemCraft`
this is a game where you mix compounds, explore planets from real life observable universe, and explore biochemistry!
However, this is only an early version (alpha) so there are not many compounds, planets, or features yet.
"""
import pygame, random, math

pygame.init()
width, height = 1350, 800
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.RESIZABLE)
pygame.display.set_caption("ChemCraft v0.2.5")
font = pygame.font.SysFont("monospace", 32)

heater = pygame.Rect(width-200, 0, 200, 200)
cooler = pygame.Rect(width-200, 200, 200, 200)
anode = pygame.Rect(width//4-50, height-200, 50, 200)
cathode = pygame.Rect(width//2+50, height-200, 50, 200)
thermometer = pygame.Rect(width//2-200, 0, 300, 80)
disector = pygame.Rect(width-200, height//1.5, 200, 200)

temp = False
elec = False
therm = False
dis = False

scene1 = True
gaming = True
started = False

campos = [0, 0]

thermometer_temp = 25

toremove = []

def removestr(toremove, string):
    ss = string.split(toremove)
    return ss[0]

# Recourse map HV = "H+"ydrotherm "v"ent, RT = "r"ocky "t"errain, ST = "s"oily "t"errain, IT = "i"cy "t"errain, CA = "c"loudy "a"rea
map = "HV-1"

rmap = {
    "HV-1": {
        "compounds": [
            "CH4",
            "CO2",
            "H2O",
            "H2S",
            "CH3SCH3"
        ],
        "rarities": [
            0.2,
            0.3,
            0.7,
            0.2,
            0.1
        ],
        "states": [
            3,
            3,
            2,
            3,
            3
        ],
        "temperature": 300,
        "position": [1000, 1600, pygame.Rect(640, 1600, 32, 40)]
    },
    "HV-2": {
        "compounds": [
            "CH4",
            "CO2",
            "H2O",
            "Cl2",
            "H2",
            "Na"
        ],
        "rarities": [
            0.2,
            0.3,
            0.7,
            0.2,
            0.2,
            0.2
        ],
        "states": [
            3,
            3,
            2,
            3,
            3,
            1
        ],
        "temperature": 230,
        "position": [220, 1630, pygame.Rect(220, 1630, 32, 40)]
    },
    "ST-1": {
        "compounds": [
            "NaCl",
            "H2O",
            "SiO2",
            "CaCO3"
        ],
        "rarities": [
            0.5,
            0.3,
            0.5,
            0.5,
        ],
        "states": [
            3,
            3,
            2,
            3,
        ],
        "temperature": 30,
        "position": [450, 400, pygame.Rect(450, 900, 32, 40)]
    },
    "ST-2": {
        "compounds": [
            "NH3",
            "O2",
            "CaO",
            "CaCO3"
        ],
        "rarities": [
            0.2,
            0.3,
            0.5,
            0.5,
        ],
        "states": [
            2,
            3,
            1,
            1,
        ],
        "temperature": 34,
        "position": [900, 500, pygame.Rect(650, 700, 32, 40)]
    },
    "ST-3": {
        "compounds": [
            "NO2",
            "O2",
            "SiO2",
            "MgCO3"
        ],
        "rarities": [
            0.2,
            0.3,
            0.5,
            0.5,
        ],
        "states": [
            2,
            3,
            1,
            1,
        ],
        "temperature": 34,
        "position": [1000, 550, pygame.Rect(650, 700, 32, 40)]
    },
    "CA-1": {
        "compounds": [
            "H2O",
            "CO2",
            "H2CO3",
            "H2"
        ],
        "rarities": [
            0.5,
            0.5,
            0.5,
            0.5,
        ],
        "states": [
            2,
            2,
            2,
            3,
        ],
        "temperature": 20,
        "position": [950, 800, pygame.Rect(950, 300, 32, 40)]
    },
    "CA-2": {
        "compounds": [
            "CH4",
            "CO2",
            "N2",
            "H2",
            "O2",
            "H2S"
        ],
        "rarities": [
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5
        ],
        "states": [
            3,
            3,
            3,
            3,
            3,
            3
        ],
        "temperature": 30,
        "position": [300, 60, pygame.Rect(600, 60, 32, 40)]
    },
    "CA-3": {
        "compounds": [
            "H2O",
            "CO2",
            "Cl2",
            "H2",
            "O2",
            "NH3"
        ],
        "rarities": [
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.3
        ],
        "states": [
            3,
            3,
            3,
            3,
            3,
            3
        ],
        "temperature": 20,
        "position": [600, 350, pygame.Rect(600, 350, 32, 40)]
    },
}

compounds = []

class Compound:
    def __init__(self, x, y, structure, temp=25, state=2, ammount=1):
        self.x, self.y = x, y
        self.structure = structure
        self.temp = int(temp)
        self.ammount = ammount
        self.state = state
        self.rect = font.render(f"{str(self.ammount) + ' ' if self.ammount > 1 else ''}{self.structure}", True, (200, 200, 200)).get_rect()

    def update(self):
        self.rect = font.render(f"{str(self.ammount) + ' ' if self.ammount > 1 else ''}{self.structure}", True, (200, 200, 200)).get_rect(x=self.x, y=self.y)

        compoundins = []

        self.structure = removestr("['", removestr("']", str(self.structure)))

        if self.ammount <= 0:
            toremove.append(self)
            return

        for compound in compounds:
            compoundins.append(compound.structure)

        if self.temp <= 25 and self.temp > 10 and self.structure == "H2O" and self.ammount >= 2:
            compounds.append(Compound(self.x, self.y, "OH", self.temp, 3))
            compounds.append(Compound(self.x + 10, self.y + 40, "H+", self.temp, 3))
            self.ammount -= 1
        if self.temp <= 75 and self.temp > 10 and self.structure == "H+" and self.ammount >= 2:
            self.ammount -= 2
            compounds.append(Compound(self.x-10, self.y-40, "H2", self.temp, 3))

        if self.temp <= 75 and self.temp > 10:
            for compound in compounds:
                if compound != self and self.rect.colliderect(compound.rect):
                    if compound.structure == "OH" and self.structure == "H3O":
                        compound.ammount -= 1
                        self.ammount -= 1
                        compounds.append(Compound(self.x-10, self.y-40, "H2O", self.temp, 2))
                        compounds.append(Compound(self.x-10, self.y, "H2O", self.temp, 2))
                    if compound.structure == "H2O" and self.structure == "H+":
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x-10, self.y-40, "H3O", self.temp, 3))
                    if compound.structure == "OH" and self.structure == "H+":
                        compound.ammount -= 1
                        self.ammount -= 1
                        compounds.append(Compound(self.x-10, self.y, "H2O", self.temp, 2))
                    if compound.structure == "CO2" and self.structure == "H2O":
                        compound.ammount -= 1
                        self.ammount -= 1
                        compounds.append(Compound(self.x-10, self.y-40, "H2CO3", self.temp, 2))

        if self.temp <= -75:
            if self.structure == "SO2":
                self.state = 2
        if self.temp <= 0:
            if self.structure == "H2O":
                self.state = 1
        if self.temp >= 100:
            if self.structure == "H2O":
                self.state = 3
            for compound in compounds:
                if self != compound and self.rect.colliderect(compound.rect):
                    if self.structure == "H2" and compound.structure == "O2" and self.ammount >= 2 and self.temp >= 500:
                        compound.ammount -= 1
                        self.ammount -= 2
                        compounds.append(Compound(self.x-10, self.y-40, "H2O", self.temp, 3))
                        compounds.append(Compound(self.x-10, self.y, "H2O", self.temp, 3))
                    if self.structure == "CH4" and compound.structure == "O2" and self.temp >= 300 and self.temp <= 600:
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y+40, "CH2O", self.temp+10, 3))
                        compounds.append(Compound(self.x, self.y-40, "H2O", self.temp+10, 3))
                    if self.structure == "H2O" and compound.structure == "Mg" and self.ammount >= 2:
                        self.ammount -= 2
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y-40, "H2", self.temp, 3))
                        compounds.append(Compound(self.x, self.y, "Mg(OH)2", self.temp, 1))
                    if self.structure == "CH2O" and compound.structure == "O2" and self.temp >= 300 and self.temp <= 600:
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y+40, "CO2", self.temp+10, 3))
                        compounds.append(Compound(self.x, self.y-40, "H2O", self.temp+10, 3))
                    if self.structure == "SiO2" and compound.structure == "NaOH" and  self.temp <= 200 and compound.ammount >= 2:
                        self.ammount -= 1
                        compound.ammount -= 2
                        compounds.append(Compound(self.x, self.y+40, "Na2SiO3", self.temp, 3))
                        compounds.append(Compound(self.x, self.y-40, "H2O", self.temp, 3))

        if self.temp >= 50 and self.temp <= 150:
            if self.structure == "CH2O" and self.ammount >= 2 and ("Mg(OH)2" in compoundins or "Ca(OH)2" in compoundins or "NaOH" in compoundins):
                self.ammount -= 2
                compounds.append(Compound(self.x, self.y-40, "CH2OHCHO", self.temp, 3))
            for compound in compounds:
                if self != compound and compound.rect.colliderect(self.rect):
                    if self.structure == "CH3SCH3" and compound.structure == "NaOH":
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y+40, "Na", self.temp+10, 1))
                        compounds.append(Compound(self.x, self.y-40, "CH3SCH2", self.temp+10, 3))
                        compounds.append(Compound(self.x, self.y+40, "H2O", self.temp-1, 3))
                    if self.structure == "CH3SCH3" and compound.structure == "KOH":
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y+40, "K", self.temp+10, 1))
                        compounds.append(Compound(self.x, self.y-40, "CH3SCH2", self.temp+10, 3))
                        compounds.append(Compound(self.x, self.y+40, "H2O", self.temp-1, 3))

        if self.temp >= 360:
            if self.structure == "Mg(OH)2" and self.temp <= 550:
                self.ammount -= 1
                compounds.append(Compound(self.x, self.y+40, "MgO", self.temp+10, 3))
                compounds.append(Compound(self.x, self.y-40, "H2O", self.temp+10, 3))
            if self.structure == "H2S" and self.temp >= 700 and self.temp <= 1000 and self.ammount >= 2:
                self.ammount -= 2
                compounds.append(Compound(self.x, self.y+40, "H2", self.temp, 3, 2))
                compounds.append(Compound(self.x, self.y-40, "S2", self.temp, 3))
            if self.structure == "CaCO3" and self.temp <= 900:
                self.ammount -= 1
                compounds.append(Compound(self.x, self.y+40, "CaO", self.temp, self.state))
                compounds.append(Compound(self.x, self.y-40, "CO2", self.temp, 3))
            for compound in compounds:
                if self != compound and compound.rect.colliderect(self.rect):
                    if self.structure == "NH3" and compound.structure == "O2" and self.ammount >= 4 and compound.ammount >= 3 and self.temp >= 600 and self.temp <= 700:
                        self.ammount -= 4
                        compound.ammount -= 3
                        compounds.append(Compound(self.x, self.y+40, "N2", self.temp, 3, 2))
                        compounds.append(Compound(self.x, self.y-40, "H2O", self.temp, 3, 6))

        if self.structure == "H2CO3" and self.temp > 15 and random.random() < 0.1:
            self.ammount-= 1
            compounds.append(Compound(self.x, self.y+40, "CO2", self.temp, 3))
            compounds.append(Compound(self.x, self.y-40, "H2O", self.temp, 2))

        if self.structure == "H+":
            for compound in compounds:
                if compound.structure == "e" and self.rect.colliderect(compound.rect):
                    self.ammount -= 1
                    compound.ammount -= 1
                    compounds.append(Compound(self.x, self.y-40, "H", self.temp, 3))

        if self.structure == "H":
            for compound in compounds:
                if compound.structure == "e" and self.rect.colliderect(compound.rect):
                    self.ammount -= 1
                    compound.ammount -= 1
                    compounds.append(Compound(self.x, self.y-40, "H-", self.temp, 3))

        if self.structure == "H-":
            for compound in compounds:
                if compound.structure == "H+" and self.rect.colliderect(compound.rect):
                    self.ammount -= 1
                    compound.ammount -= 1
                    compounds.append(Compound(self.x, self.y-40, "H2", self.temp, 3))

        for compound in compounds:
            if compound != self and self.rect.colliderect(compound.rect):
                if compound.structure == self.structure:
                    self.ammount += compound.ammount
                    compound.ammount = 0
                else:
                    self.temp, compound.temp = (self.temp + (compound.temp//2)) - self.temp//2, (compound.temp + (self.temp//2)) - self.temp//2

        if self.rect.colliderect(thermometer) and therm:
            global thermometer_temp
            thermometer_temp = int(self.temp) if self.temp != float("inf") else 99999999999
        if self.rect.colliderect(heater) and temp:
            self.temp += 0.2
        if self.rect.colliderect(cooler) and temp:
            self.temp -= 0.2 if self.temp > -273.15 else 0
        if self.rect.colliderect(anode) and elec:
            if self.structure == "H2O" and self.ammount >= 2:
                self.ammount -= 2
                compounds.append(Compound(self.x, self.y-40, "H+", self.temp, 3))
                compounds.append(Compound(self.x, self.y-80, "H+", self.temp, 3))
                compounds.append(Compound(self.x, self.y-120, "H+", self.temp, 3))
                compounds.append(Compound(self.x, self.y-160, "H+", self.temp, 3))
                compounds.append(Compound(self.x, self.y+80, "e", self.temp, 3))
                compounds.append(Compound(self.x, self.y+120, "e", self.temp, 3))
                compounds.append(Compound(self.x, self.y+160, "e", self.temp, 3))
                compounds.append(Compound(self.x, self.y-200, "e", self.temp, 3))
                compounds.append(Compound(self.x, self.y+40, "O2", self.temp, 3))
            if self.structure == "e":
                toremove.append(self)
        if self.rect.colliderect(disector) and dis:
            for _ in range(self.ammount-1):
                compounds.append(Compound(self.x, self.y-40, self.structure, self.temp, self.state))
                self.ammount -= 1

    def draw(self):
        screen.blit(font.render(f"{str(self.ammount) + ' ' if self.ammount > 1 else ''}{self.structure}", True, (max(0, min(255, self.temp)), 50*self.state, max(0, min(255, -self.temp)))), (self.x, self.y))
        self.update()

grabbed = False
grabbing = None

def start():
    global compounds
    for _ in range(20):
        k = random.randint(0, len(rmap[map]["compounds"])-1)
        temp = rmap[map]["temperature"]
        structure = rmap[map]["compounds"][k]
        state = rmap[map]["states"][k]
        compounds.append(Compound(random.randint(50, width-50), random.randint(32, height-32), structure, temp, state))

def draw_terrain():
    for i, (key, data) in enumerate(rmap.items()):
        x, y, rect = data["position"]
        if key.startswith("HV"):
            pygame.draw.circle(screen, (50, 50, 255), (x+campos[0], y+campos[1]), 300)
        elif key.startswith("ST"):
            pygame.draw.circle(screen, (139, 29, 10), (x+campos[0], y+campos[1]), 300)
        elif key.startswith("RT"):
            pygame.draw.circle(screen, (50, 50, 50), (x+campos[0], y+campos[1]), 300)
        elif key.startswith("IT"):
            pygame.draw.circle(screen, (200, 200, 255), (x+campos[0], y+campos[1]), 300)
    
    for i, (key, data) in enumerate(rmap.items()):
        x, y, rect = data["position"]
        if key.startswith("HV"):
            pygame.draw.circle(screen, (50, 50, 200), (x+campos[0], y+campos[1]), 250)
        elif key.startswith("ST"):
            pygame.draw.circle(screen, (149, 39, 19), (x+campos[0], y+campos[1]), 200)
        elif key.startswith("RT"):
            nx = x + math.cos(i * 2 * math.pi / len(rmap)) * 300
            ny = y + math.sin(i * 2 * math.pi / len(rmap)) * 300
            pygame.draw.circle(screen, (50, 50, 50), (nx+campos[0], ny+campos[1]), 250)
        elif key.startswith("IT"):
            pygame.draw.circle(screen, (180, 180, 240), (x+campos[0], y+campos[1]), 250)
    
    for i, (key, data) in enumerate(rmap.items()):
        x, y, rect = data["position"]
        if key.startswith("HV"):
            pygame.draw.circle(screen, (50, 50, 150), (x+campos[0], y+campos[1]), 200)
        elif key.startswith("ST"):
            pygame.draw.circle(screen, (159, 49, 29), (x+campos[0], y+campos[1]), 100)
        elif key.startswith("RT"):
            pygame.draw.circle(screen, (100, 100, 100), (x+campos[0], y+campos[1]), 200)
        elif key.startswith("IT"):
            pygame.draw.circle(screen, (160, 160, 220), (x+campos[0], y+campos[1]), 200)
    
    for i, (key, data) in enumerate(rmap.items()):
        x, y, rect = data["position"]
        if key.startswith("HV"):
            pygame.draw.circle(screen, (30, 30, 100), (x+campos[0], y+campos[1]), 150)
        elif key.startswith("RT"):
            pygame.draw.circle(screen, (150, 150, 150), (x+campos[0], y+campos[1]), 100)
        elif key.startswith("IT"):
            pygame.draw.circle(screen, (140, 140, 200), (x+campos[0], y+campos[1]), 150)

    for i, (key, data) in enumerate(rmap.items()):
        x, y, rect = data["position"]
        if key.startswith("CA"):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 255, 255, 100), (x+campos[0], y+campos[1]), 300)
            nx = x + math.cos(i * 2 * math.pi / len(rmap)) * 300
            ny = y + math.sin(i * 2 * math.pi / len(rmap)) * 300
            pygame.draw.circle(surface, (255, 255, 255, 100), (nx+campos[0], ny+campos[1]), 250)
            screen.blit(surface, (0, 0))

def game():
    global temp, elec, therm, dis, scene1, gaming, started, grabbing, grabbed

    if not started:
        #start()
        started = True
    mbd = False
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                running = False
                gaming = False
            if eve.type == pygame.MOUSEBUTTONDOWN:
                if eve.button == 1:
                    mbd = True
                    for compound in compounds:
                        if compound.rect.collidepoint(mouse):
                            grabbed = True
                            grabbing = compound
                            break
                    if pygame.Rect(0, 0, 100, 100).collidepoint(mouse):
                        ltemp = rmap[map]["temperature"]
                        structure = random.choices(rmap[map]["compounds"], rmap[map]["rarities"])[0]
                        state = random.choices(rmap[map]["states"], rmap[map]["rarities"])[0]
                        compounds.append(Compound(random.randint(50, width-50), random.randint(32, height-32), structure, ltemp, state))
                    elif pygame.Rect(0, 110, 100, 100).collidepoint(mouse):
                        temp = not temp
                    elif pygame.Rect(0, 220, 100, 100).collidepoint(mouse):
                        elec = not elec
                    elif pygame.Rect(0, 330, 100, 100).collidepoint(mouse):
                        therm = not therm
                    elif pygame.Rect(0, 440, 100, 100).collidepoint(mouse):
                        dis = not dis
                    elif pygame.Rect(0, 550, 100, 100).collidepoint(mouse):
                        scene1 = True
                        running = False
                    elif cathode.collidepoint(mouse) and elec:
                        compounds.append(Compound(cathode.x+20, cathode.y-40, "e", 25, 3))
            if eve.type == pygame.MOUSEBUTTONUP:
                mbd = False
                grabbed = False

        screen.fill((0, 0, 0))

        if temp:
            pygame.draw.rect(screen, (120, 100, 100), heater)
            pygame.draw.rect(screen, (100, 100, 120), cooler)
        if elec:
            pygame.draw.rect(screen, (120, 120, 120), anode)
            pygame.draw.rect(screen, (100, 100, 100), cathode)
            screen.blit(font.render("A", True, (250, 200, 200)), anode)
            screen.blit(font.render("C", True, (200, 200, 250)), cathode)
        if therm:
            pygame.draw.rect(screen, (120, 120, 120), thermometer)
            surf = pygame.Surface((thermometer.width, thermometer.height), pygame.SRCALPHA)
            surf.blit(font.render(f"{thermometer_temp}*C", True, (150, 150, 150)), (0, thermometer.height//2-32))
            screen.blit(surf, thermometer)
        if dis:
            pygame.draw.rect(screen, (140, 140, 140), disector)

        for compound in compounds:
            if compound.rect.colliderect(screen.get_rect(x=0, y=0)):
                compound.draw()
            if grabbed:
                if grabbing == compound:
                    grabbing.x, grabbing.y = mouse[0] - grabbing.rect.width//2, mouse[1] - grabbing.rect.height//2
                    compound = grabbing
            else:
                grabbing = None

        for compound in toremove:
            if compound in compounds:
                compounds.remove(compound)

        pygame.draw.rect(screen, (50, 255, 50), (0, 0, 100, 100))
        pygame.draw.rect(screen, (50, 50, 255), (0, 110, 100, 100))
        pygame.draw.rect(screen, (255, 50, 50), (0, 220, 100, 100))
        pygame.draw.rect(screen, (255, 255, 50), (0, 330, 100, 100))
        pygame.draw.rect(screen, (50, 255, 255), (0, 440, 100, 100))
        pygame.draw.rect(screen, (255, 50, 255), (0, 550, 100, 100))

        pygame.display.flip()

# Variables to track dragging
dragging = False
last_mouse_pos = (0, 0)

def mapscene():
    global dragging, last_mouse_pos, campos, map, gaming, scene1

    land = pygame.Surface((width*1.5, height//1.5), pygame.SRCALPHA)
    land.fill((129, 19, 0))

    sea = pygame.Surface((width*1.5, height//1.5), pygame.SRCALPHA)
    sea.fill((50, 50, 200))

    # Create a combined surface
    surf = pygame.Surface((width*1.5, land.get_height() + sea.get_height()), pygame.SRCALPHA)
    surf.blit(land, (0, 0))
    surf.blit(sea, (0, land.get_height()))

    for x in range(0, surf.get_width(), 100):
        for _ in range(random.randint(1, 3)):
            y = random.randint(-40, 40)
            pygame.draw.circle(surf, (200, 200, 50), (x, land.get_height() + y), random.randint(50, 100))

    surf = pygame.transform.scale(surf, (land.get_width()+1500, land.get_height()+1500))

    running = True
    while running:
        screen.fill((0, 0, 0))

        mouse = pygame.mouse.get_pos()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gaming = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Start dragging
                if event.button == 1:  # Left mouse button
                    dragging = True
                    last_mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:  # Stop dragging
                if event.button == 1:
                    dragging = False
                    last_mouse_pos = event.pos

                    for key, data in rmap.items():
                        rect = data["position"][2]  # Use the rect from rmap
                        data["position"][2].x = data["position"][0]
                        data["position"][2].y = data["position"][1]
                        rect_offset = rect.move(campos[0], campos[1])  # Offset by camera position
                        text = font.render(key, True, (100, 100, 100))
                        rect_offs = screen.blit(text, (rect_offset.x, rect_offset.y))  # Display key name
                        if rect_offs.collidepoint(mouse):
                            running = False
                            scene1 = False  # Exit map scene
                            map = key  # Set the map to the selected terrain
            elif event.type == pygame.MOUSEMOTION and dragging:
                speed = 0.99  # Lower = slower camera, adjust as needed
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                campos[0] += int(dx * speed)
                campos[1] += int(dy * speed)
                last_mouse_pos = event.pos  # Update for next motion

        # Clamp camera so it doesn't go outside the map
        max_x = 0
        min_x = width - surf.get_width()
        max_y = 0
        min_y = height - surf.get_height()
        campos[0] = min(max(campos[0], min_x), max_x)
        campos[1] = min(max(campos[1], min_y), max_y)

        # Blit surfaces with horizontal wrapping
        screen.blit(surf, (campos[0], campos[1]))

        draw_terrain()

        # Draw the map keys with offsets
        for key, data in rmap.items():
            rect = data["position"][2]  # Use the rect from rmap
            data["position"][2].x = data["position"][0]
            data["position"][2].y = data["position"][1]
            rect_offset = rect.move(campos[0], campos[1])  # Offset by camera position
            text = font.render(key, True, (100, 100, 100))
            rect_offs = screen.blit(text, (rect_offset.x, rect_offset.y))  # Display key name
            if rect_offs.collidepoint(mouse):
                text = font.render(key, True, (100, 100, 100))
            else:
                text = font.render(key, True, (200, 200, 200))
            screen.blit(text, (rect_offset.x, rect_offset.y))

        pygame.display.flip()  # Update the display

def main():
    while gaming:
        if scene1:
            mapscene()
        else:
            game()

if __name__ == "__main__":
    main()
    pygame.quit()
    exit()
