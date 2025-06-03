"""
the main python script of the game `interplanetary chemistry exploration`
this is a game where you mix compounds, explore planets from real life observable universe, and explore biochemistry!

"""
import pygame, random, math

pygame.init()
width, height = 800, 1350
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interplanetary Chemistry Exploration")
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

def removestr(toremove, string):
    ss = string.split(toremove)
    return ss[0]

# Recourse map HV = "h"ydrotherm "v"ent, RT = "r"ocky "t"errain, ST = "s"oily "t"errain, IT = "i"cy "t"errain, CA = "c"loudy "a"rea
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
        "position": [240, 1400, pygame.Rect(240, 1400, 32, 40)]
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
        "position": [220, 1430, pygame.Rect(220, 1430, 32, 40)]
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
        "position": [450, 900, pygame.Rect(450, 900, 32, 40)]
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
        "position": [650, 700, pygame.Rect(650, 750, 32, 40)]
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
        "position": [950, 300, pygame.Rect(950, 300, 32, 40)]
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
        "temperature": 260,
        "position": [600, 60, pygame.Rect(600, 60, 32, 40)]
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
        if self.ammount <= 0:
            compounds.remove(self)

        self.rect = font.render(f"{str(self.ammount) + ' ' if self.ammount > 1 else ''}{self.structure}", True, (200, 200, 200)).get_rect(x=self.x, y=self.y)

        compoundins = []

        self.structure = removestr("['", removestr("']", str(self.structure)))

        if self.ammount <= 0:
            compounds.remove(self)

        for compound in compounds:
            compoundins.append(compound.structure)

        if self.temp <= 25 and self.temp > 10 and self.structure == "H2O" and self.ammount >= 2:
            compounds.append(Compound(self.x, self.y, "OH", self.temp, 3))
            compounds.append(Compound(self.x + 10, self.y + 40, "H", self.temp, 3))
            self.ammount -= 1
        if self.temp <= 75 and self.temp > 10 and self.structure == "H" and self.ammount >= 2:
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
                    if compound.structure == "H2O" and self.structure == "H":
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x-10, self.y-40, "H3O", self.temp, 3))
                    if compound.structure == "OH" and self.structure == "H":
                        compound.ammount -= 1
                        self.ammount -= 1
                        compounds.append(Compound(self.x-10, self.y, "H2O", self.temp, 2))
                    if compound.structure == "CH2O" and self.structure == "CH2OHCHO" and ("Mg(OH)2" in compoundins or "Ca(OH)2" in compoundins or "NaOH" in compoundins):
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y-40, "CH2OHCHOHCHO", self.temp, 2))
                    if compound.structure == "CH2O" and self.structure == "CH2OHCHOHCHOHCHO" and self.temp > 40 and ("Mg(OH)2" in compoundins or "Ca(OH)2" in compoundins or "NaOH" in compoundins):
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y-40, "CH2OHCHOHCHOHCHOHCH2OH", self.temp, 2))
                    if compound.structure == "CH2O" and self.structure == "CH2OHCHOHCHOHCHO" and (not self.temp > 40) and ("Mg(OH)2" in compoundins or "Ca(OH)2" in compoundins or "NaOH" in compoundins):
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y-40, "C5H10O5(lin-rib)", self.temp, 2))
                    if compound.structure == "CH2O" and self.structure == "C5H10O5(lin-rib)" and (not self.temp > 40) and ("Mg(OH)2" in compoundins or "Ca(OH)2" in compoundins or "NaOH" in compoundins):
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y-40, "C6H12O6(lin-glu)", self.temp, 2))
                    if compound.structure == "CO2" and self.structure == "H2O":
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y+40, "H2CO3", self.temp-1, 2))
                    if compound.structure == "Na" and self.structure == "H2O" and self.ammount >= 2 and compound.ammount >= 2:
                        self.ammount -= 2
                        compound.ammount -= 2
                        compounds.append(Compound(self.x-10, self.y-40, "NaOH", self.temp+10, 2, 2))
                        compounds.append(Compound(self.x-10, self.y+40, "H2", self.temp+10, 3))
                    if compound.structure == "CH2O" and self.structure == "CH2OHCHOHCHO" and ("Mg(OH)2" in compoundins or "Ca(OH)2" in compoundins or "NaOH" in compoundins):
                        self.ammount -= 1
                        compound.ammount -= 1
                        compounds.append(Compound(self.x, self.y-40, "CH2OHCHOHCHOHCHO", self.temp, 2))


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

        if self.structure == "h":
            for compound in compounds:
                if compound.structure == "e" and self.rect.colliderect(compound.rect):
                    self.ammount -= 1
                    compound.ammount -= 1
                    compounds.append(Compound(self.x, self.y-40, "H", self.temp, 3))

        for compound in compounds:
            if compound != self and self.rect.colliderect(compound.rect):
                if compound.structure == self.structure:
                    self.ammount += compound.ammount
                    compounds.remove(compound)
                else:
                    self.temp, compound.temp = (self.temp + (compound.temp//2)) - self.temp//2, (compound.temp + (self.temp//2)) - self.temp//2

        if self.rect.colliderect(thermometer) and therm:
            global thermometer_temp
            thermometer_temp = int(self.temp) if self.temp != float("inf") else 99999999999
        if self.rect.colliderect(heater) and temp:
            self.temp += 0.2
        if self.rect.colliderect(cooler) and temp:
            self.temp -= 0.2 if self.temp > -400 else 0
        if self.rect.colliderect(anode) and elec:
            if self.structure == "H2O" and self.ammount >= 2:
                self.ammount -= 2
                compounds.append(Compound(self.x, self.y-40, "h", self.temp, 3))
                compounds.append(Compound(self.x, self.y-80, "h", self.temp, 3))
                compounds.append(Compound(self.x, self.y-120, "h", self.temp, 3))
                compounds.append(Compound(self.x, self.y-160, "h", self.temp, 3))
                compounds.append(Compound(self.x, self.y+80, "e", self.temp, 3))
                compounds.append(Compound(self.x, self.y+120, "e", self.temp, 3))
                compounds.append(Compound(self.x, self.y+160, "e", self.temp, 3))
                compounds.append(Compound(self.x, self.y-200, "e", self.temp, 3))
                compounds.append(Compound(self.x, self.y+40, "O2", self.temp, 3))
            if self.structure == "e":
                compounds.remove(self)
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
                        k = random.randint(0, len(rmap[map]["compounds"])-1)
                        temp = rmap[map]["temperature"]
                        structure = rmap[map]["compounds"][k]
                        state = rmap[map]["states"][k]
                        compounds.append(Compound(random.randint(50, width-50), random.randint(32, height-32), structure, temp, state))
                    if pygame.Rect(0, 110, 100, 100).collidepoint(mouse):
                        temp = not temp
                    if pygame.Rect(0, 220, 100, 100).collidepoint(mouse):
                        elec = not elec
                    if pygame.Rect(0, 330, 100, 100).collidepoint(mouse):
                        therm = not therm
                    if pygame.Rect(0, 440, 100, 100).collidepoint(mouse):
                        dis = not dis
                    if pygame.Rect(0, 550, 100, 100).collidepoint(mouse):
                        scene1 = True
                        running = False
                    if cathode.collidepoint(mouse) and elec:
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
            surf.blit(font.render(f"{thermometer_temp}°C", True, (150, 150, 150)), (0, thermometer.height//2-32))
            screen.blit(surf, thermometer)
        if dis:
            pygame.draw.rect(screen, (140, 140, 140), disector)

        for compound in compounds[:]:
            if compound.ammount <= 0:
                compounds.remove(self)
            if compound.rect.colliderect(screen.get_rect(x=0, y=0)):
                compound.draw()
            if grabbed:
                if grabbing == compound:
                    grabbing.x, grabbing.y = mouse[0] - grabbing.rect.width//2, mouse[1] - grabbing.rect.height//2
                    compound = grabbing
            else:
                grabbing = None

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

    land = pygame.image.load("land.png")
    sea = pygame.image.load("sea.png")

    # Create a combined surface
    surf = pygame.Surface(((land.get_width()+sea.get_width())//2, land.get_height()+sea.get_height()), pygame.SRCALPHA)
    surf.blit(land, (0, 0))
    surf.blit(sea, (0, land.get_height()))

    surf = pygame.transform.scale(surf, (land.get_width()+1500, land.get_height()+1500))

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen with a blue background

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
            elif event.type == pygame.MOUSEMOTION and dragging:  # For boost-up
                if pygame.Rect(0, 0, 200, height).collidepoint(mouse):
                    campos[0] += 5
                if pygame.Rect(width-200, 0, 200, height).collidepoint(mouse):
                    campos[0] -= 5
                if pygame.Rect(0, 0, width, 200).collidepoint(mouse):
                    campos[1] += 5
                if pygame.Rect(0, height-200, width, 200).collidepoint(mouse):
                    campos[1] -= 5

        # Keep the camera horizontally wrapping around
        if campos[0] < 0:
            campos[0] = surf.get_width() + campos[0]  # Wrap to the right
        if campos[0] > surf.get_width():
            campos[0] = campos[0] - surf.get_width()  # Wrap to the left

        # Force vertical position to be 0 (no vertical movement)
        if campos[1] < -650:
            campos[1] = -650
        if campos[1] > 0:
            campos[1] = 0

        if dragging:
            if pygame.Rect(0, 0, 200, height).collidepoint(mouse):
                campos[0] += 5
            if pygame.Rect(width-200, 0, 200, height).collidepoint(mouse):
                campos[0] -= 5
            if pygame.Rect(0, 0, width, 200).collidepoint(mouse):
                campos[1] += 5
            if pygame.Rect(0, height-200, width, 200).collidepoint(mouse):
                campos[1] -= 5

        # Blit surfaces with horizontal wrapping
        screen.blit(surf, (campos[0], campos[1]))
        screen.blit(surf, (campos[0] + surf.get_width(), campos[1]))
        screen.blit(surf, (campos[0] - surf.get_width(), campos[1]))

        # Draw the map keys with offsets
        for key, data in rmap.items():
            rect = data["position"][2]  # Use the rect from rmap
            rect_offset = rect.move(campos[0], campos[1])  # Offset by camera position
            text = font.render(key, True, (100, 100, 100))
            rect_offs = screen.blit(text, (rect_offset.x, rect_offset.y))  # Display key name
            if dragging and rect_offs.collidepoint(mouse):
                text = font.render(key, True, (100, 100, 100))
                running = False
                scene1 = False
                map = key
            else:
                text = font.render(key, True, (200, 200, 200))
            screen.blit(text, (rect_offset.x, rect_offset.y))

        for key, data in rmap.items():
            rect = data["position"][2]  # Use the rect from rmap
            rect_offset = rect.move(campos[0], campos[1])  # Offset by camera position
            text = font.render(key, True, (100, 100, 100))
            rect_offs = screen.blit(text, (rect_offset.x-surf.get_width(), rect_offset.y))  # Display key name
            if dragging and rect_offs.collidepoint(mouse):
                text = font.render(key, True, (100, 100, 100))
                running = False
                scene1 = False
                map = key
            else:
                text = font.render(key, True, (200, 200, 200))
            screen.blit(text, (rect_offset.x-surf.get_width(), rect_offset.y))

        for key, data in rmap.items():
            rect = data["position"][2]  # Use the rect from rmap
            rect_offset = rect.move(campos[0], campos[1])  # Offset by camera position
            text = font.render(key, True, (100, 100, 100))
            rect_offs = screen.blit(text, (rect_offset.x+surf.get_width(), rect_offset.y))  # Display key name
            if dragging and rect_offs.collidepoint(mouse):
                text = font.render(key, True, (100, 100, 100))
                running = False
                scene1 = False
                map = key
            else:
                 text = font.render(key, True, (200, 200, 200))
            screen.blit(text, (rect_offset.x+surf.get_width(), rect_offset.y))

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