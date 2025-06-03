import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
button_font = pygame.font.SysFont("Monospace", 20, bold=True)
warning_font = pygame.font.SysFont("Monospace", 50)

num_attr = {
    1: 0.5,
    2: 0.3,
    3: 0.1,
    4: 0.06,
    5: 0.03,
}
font_rarities = {
    "Arial": 0.5,
    "Times New Roman": 0.3,
    "Courier New": 0.1,
    "Verdana": 0.06,
    "Georgia": 0.03,
    "Comic Sans MS": 0.02,
    "Trebuchet MS": 0.017,
    "Impact": 0.01,
    "Lucida Console": 0.005,
    "Palatino Linotype": 0.0025,
    "Consolas": 0.001,
    "Lucida Sans Unicode": 0.0005,
}
attr_rarities = {
    "commonly": 0.5,
    "rarely": 0.3,
    "aromatic": 0.1,
    "infected": 0.06,
    "atomic": 0.03,
    "frozen": 0.02,
    "special": 0.017,
    "legendary": 0.01,
    "leaking": 0.005,
}
type_rarities = {
    "rocky": 0.5,
    "dusty": 0.3,
    "lumpy": 0.1,
    "gaseous": 0.06,
    "crystal": 0.03,
    "liquid": 0.02,
    "solid": 0.017,
    "plasma": 0.01,
    "black holed": 0.005,
    "universal": 0.0025,
    "": 0.0 # Did this so the bug won't happen again
}

def get_item_rarity(item):
    rarity = 1
    for attr, value in item["attr"].items():
        if value:
            rarity *= attr_rarities[attr]
    rarity *= font_rarities[item["font"]]
    rarity *= type_rarities[item["type"]]
    rarity *= 0.2 if item["inverted"] else 0.5
    rarity *= 0.1 if item["bold"] else 0.5
    return rarity

def invert_color(color):
    return (255 - color[0], 255 - color[1], 255 - color[2])

def get_item_color(item):
    rarity = get_item_rarity(item)
    font_rarity = font_rarities[item["font"]]
    type_rarity = type_rarities[item["type"]]
    r = int(255 * rarity)
    g = int(255 * (rarity * (font_rarity + type_rarity)))
    b = int((r*rarity) + (g*rarity))
    return invert_color((r, g, b)) if item["inverted"] else (r, g, b)

def get_item_name(item):
    name = item["type"].capitalize()
    attrs = 0

    for attr, value in item["attr"].items():
        if value:
            name += f" {attr.capitalize()}"
            attrs += 1
        if attrs >= 2:
            break

    if item["inverted"]:
        name = "Inverted " + name

    return name

def get_item_tier(item):
    rarity = get_item_rarity(item)
    if rarity >= 0.01: return "Common"
    elif rarity >= 0.001: return "Uncommon"
    elif rarity >= 0.0006: return "Rare"
    elif rarity >= 0.0001: return "Epic"
    elif rarity >= 0.00005: return "Legendary"
    elif rarity >= 0.00002: return "Mythic"
    elif rarity >= 0.00001: return "Ancient"
    elif rarity >= 0.000005: return "Divine"
    elif rarity >= 0.0000025: return "Celestial"
    elif rarity >= 0.000001: return "Cosmic"
    elif rarity >= 0.0000005: return "Quantumificated String"

def get_item(luck):
    item = {
        "type": "",
        "font": random.choices(list(font_rarities.keys()), weights=list(font_rarities.values()))[0],
        "inverted": random.choices([True, False], [0.2, 0.5])[0],
        "bold": random.choices([True, False], [0.1, 0.5])[0],
        "num_agents": random.randint(1, 5),
        "attr": {
            "commonly": False,
            "rarely": False,
            "aromatic": False,
            "infected": False,
            "atomic": False,
            "frozen": False,
            "special": False,
            "legendary": False,
            "leaking": False,
        }
    }

    for _ in range(random.choices(list(num_attr.keys()), weights=list(num_attr.values()))[0]):
        for attr, rarity in attr_rarities.items():
            if random.random() < rarity * (1+(luck/2)):
                item["attr"][attr] = True
                break

    for type, rarity in type_rarities.items():
        if random.random() < rarity * luck:
            item["type"] = type

    while item["type"] == "":
        item["type"] = random.choices(list(type_rarities.keys()), weights=list(type_rarities.values()))[0]

    print(item)

    return item

def get_inv_len(inventory):
    count = 0
    for item in inventory.values():
        if item is not None:
            count += 1
    return count

def roll_items(num_items, luck):
    rolls = []
    for _ in range(num_items):
        rolls.append(get_item(luck))

    return rolls

is_rolling = False
rolls = []
shown_roll = 0
current_roll_timer = 0
roll_timer = 0
waiting = False

info = ""
info_color = (0, 0, 0)
info_font = pygame.font.SysFont("Monospace", 20)

warning = "Test your luck..."
warning_color = (255, 255, 0)
warning_timer = 2

inventory_shown = False

rect_of_inventory = {}
agents = []

inventory = {
    0: get_item(1), 1: None, 2: None,
    3: None, 4: None, 5: None,
    6: None, 7: None, 8: None,
}
equipped = 0

roll_button = pygame.Rect(WIDTH//2 - 100, HEIGHT - 75, 200, 50)
inv_button = pygame.Rect(10, 200, 200, 50)

inv_del_button = pygame.Rect(10, 10, 10, 10)

del_button = pygame.Rect(30, 200, 200, 50)
get_button = pygame.Rect(30, 260, 200, 50)

mbd = False
running = True
while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mbd = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if mbd:
                if roll_button.collidepoint(event.pos) and not (inventory_shown or is_rolling or waiting):
                    is_rolling = True
                    roll_timer = 0.1
                    if inventory[equipped] is not None:
                        rolls = roll_items(9, 1+(1-get_item_rarity(inventory[equipped])))
                    else:
                        rolls = roll_items(9, 1)
                elif inv_button.collidepoint(event.pos) and not (is_rolling or waiting):
                    inventory_shown = not inventory_shown
                elif del_button.collidepoint(event.pos) and waiting:
                    waiting = False
                    rolls = []
                    shown_roll = 0
                    roll_timer = 0
                    current_roll_timer = 0.1
                elif get_button.collidepoint(event.pos) and waiting:
                    found = False
                    for i in range(len(inventory)):
                        if inventory[i] is None:
                            inventory[i] = rolls[shown_roll]
                            rolls = []
                            shown_roll = 0
                            current_roll_timer = 0.1
                            roll_timer = 0
                            waiting = False
                            found = True
                            break
                    if not found:
                        warning = "Inventory is full!"
                        warning_color = (255, 0, 0)
                        warning_timer = 2
                elif inventory_shown and not (is_rolling or waiting):
                    for i in range(len(rect_of_inventory)):
                        if rect_of_inventory[i].collidepoint(event.pos) and inventory[i]:
                            equipped = i
                            warning_color = (0, 255, 0)
                            warning_timer = 2
                            warning = "Equipped Item"
                if inv_del_button.collidepoint(event.pos) and inventory_shown and not (is_rolling or waiting):
                    inv_len = get_inv_len(inventory)
                    found = False
                    index = 0
                    for i in range(len(inventory)):
                        if i != equipped and inventory[i] is not None:
                            found = True
                            index = i

                    if inv_len > 1 and found:
                        inventory[equipped] = None
                        equipped = index
                        warning = "Deleted Item"
                        warning_color = (255, 255, 0)
                        warning_timer = 2
                    else:
                        warning = "No items to delete!"
                        warning_color = (255, 0, 0)
                        warning_timer = 2

            mbd = False

    color = (255, 255, 255)
    if inventory[equipped] is not None:
        color = get_item_color(inventory[equipped])
    screen.fill(color)

    pygame.draw.rect(screen, (50, 200, 50), roll_button)
    pygame.draw.rect(screen, (50, 160, 50), roll_button, 2)
    text = button_font.render("Roll", True, (255, 255, 255))
    rect = text.get_rect(center=roll_button.center)
    screen.blit(text, rect.topleft)

    pygame.draw.rect(screen, (200, 200, 50), inv_button)
    pygame.draw.rect(screen, (160, 160, 50), inv_button, 2)
    text = button_font.render("Inventory", True, (255, 255, 255))
    rect = text.get_rect(center=inv_button.center)
    screen.blit(text, rect.topleft)

    if inventory_shown:
        items = list(inventory.values())
        items1 = items[:3]
        items2 = items[3:6]
        items3 = items[6:9]

        equipped_color = invert_color(get_item_color(inventory[equipped]))
        norm_color = get_item_color(inventory[equipped]) if inventory[equipped] else (200, 200, 200)

        surface = pygame.Surface((WIDTH//1.5 , HEIGHT//2), pygame.SRCALPHA)
        surface_rect = pygame.Rect((WIDTH - (WIDTH//1.5))//2, HEIGHT//4, WIDTH//1.5, HEIGHT//2)

        pygame.draw.rect(surface, (*equipped_color, 128), (0, 0, WIDTH//1.5, HEIGHT//2))
        pygame.draw.rect(surface, (*equipped_color, 200), (0, 0, WIDTH//1.5, HEIGHT//2), 2)

        text = button_font.render("Equipped Info", True, norm_color)
        surface.blit(text, (210, 10))

        text = button_font.render(f"Tier: {get_item_tier(inventory[equipped])}", True, norm_color)
        surface.blit(text, (210, 50))

        text = button_font.render(f"Type: {inventory[equipped]['type'].capitalize()}", True, norm_color)
        surface.blit(text, (210, 70))

        text = button_font.render(f"Font: {inventory[equipped]['font']}", True, norm_color)
        surface.blit(text, (210, 90))

        text = button_font.render("Delete Item", True, (200, 50, 50))
        inv_del_button = surface.blit(text, (210, 110))
        inv_del_button.x += surface_rect.x
        inv_del_button.y += surface_rect.y

        text = button_font.render(f"{get_item_name(inventory[equipped])} Equipped", True, norm_color)
        surface.blit(text, (10, 200))

        text = button_font.render(f"{((1-get_item_rarity(inventory[equipped]))*100) / 2}% Boost", True, norm_color)
        surface.blit(text, (10, 220))

        text = button_font.render(f"Rarity: {get_item_rarity(inventory[equipped])*100}%", True, norm_color)
        surface.blit(text, (10, 240))

        for index, item in enumerate(items1):
            rect = pygame.Rect(index * 60 + 10, 10, 50, 50)
            if item is not None:
                pygame.draw.rect(surface, get_item_color(item), rect)
                highlight = (50, 50, 50)
                if index == equipped:
                    highlight = (200, 200, 200)
                pygame.draw.rect(surface, highlight, rect, 2)
                
                relative_mouse = (mouse[0] - surface_rect.x, mouse[1] - surface_rect.y)
                if rect.collidepoint(relative_mouse):
                    info = get_item_name(item)
                    info_color = invert_color(get_item_color(item))
                    info_font = pygame.font.SysFont(item["font"], 20)
            else:
                pygame.draw.rect(surface, (100, 100, 100), rect)
                pygame.draw.rect(surface, (50, 50, 50), rect, 2)

            relative_rect = pygame.Rect(rect.x + surface_rect.x, rect.y + HEIGHT//4, rect.width, rect.height)
            rect_of_inventory[index] = relative_rect

        for index, item in enumerate(items2):
            rect = pygame.Rect(index * 60 + 10, 70, 50, 50)
            if item is not None:
                pygame.draw.rect(surface, get_item_color(item), rect)
                highlight = (50, 50, 50)
                if index + 3 == equipped:
                    highlight = (200, 200, 200)
                pygame.draw.rect(surface, highlight, rect, 2)

                relative_mouse = (mouse[0] - surface_rect.x, mouse[1] - surface_rect.y)
                if rect.collidepoint(relative_mouse):
                    info = get_item_name(item)
                    info_color = invert_color(get_item_color(item))
                    info_font = pygame.font.SysFont(item["font"], 20)
            else:
                pygame.draw.rect(surface, (100, 100, 100), rect)
                pygame.draw.rect(surface, (50, 50, 50), rect, 2)
                
            relative_rect = pygame.Rect(rect.x + surface_rect.x, rect.y + HEIGHT//4, rect.width, rect.height)
            rect_of_inventory[index + 3] = relative_rect

        for index, item in enumerate(items3):
            rect = pygame.Rect(index * 60 + 10, 130, 50, 50)
            if item is not None:
                pygame.draw.rect(surface, get_item_color(item), rect)
                highlight = (50, 50, 50)
                if index + 6 == equipped:
                    highlight = (200, 200, 200)
                pygame.draw.rect(surface, highlight, rect, 2)

                relative_mouse = (mouse[0] - surface_rect.x, mouse[1] - surface_rect.y)
                if rect.collidepoint(relative_mouse):
                    info = get_item_name(item)
                    info_color = invert_color(get_item_color(item))
                    info_font = pygame.font.SysFont(item["font"], 20)
            else:
                pygame.draw.rect(surface, (100, 100, 100), rect)
                pygame.draw.rect(surface, (50, 50, 50), rect, 2)
                
            relative_rect = pygame.Rect(rect.x + surface_rect.x, rect.y + HEIGHT//4, rect.width, rect.height)
            rect_of_inventory[index + 6] = relative_rect

        rect = surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(surface, rect.topleft)

    if is_rolling:
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        color = get_item_color(rolls[shown_roll])
        pygame.draw.rect(surface, color + (128, ), (0, 0, WIDTH, HEIGHT))

        text = pygame.font.SysFont(rolls[shown_roll]["font"], 40, bold=rolls[shown_roll]["bold"]).render(get_item_name(rolls[shown_roll]), True, invert_color(color))
        rect = text.get_rect(center=(WIDTH//2, 200))
        surface.blit(text, rect.topleft)

        screen.blit(surface, (0, 0))

        current_roll_timer -= 1 / 60
        if current_roll_timer <= 0:
            shown_roll += 1
            roll_timer += 0.1
            current_roll_timer = roll_timer
            if shown_roll >= len(rolls):
                indexes = []
                for roll in rolls:
                    rarity = get_item_rarity(roll)
                    luck = 1 + (1 - get_item_rarity(inventory[equipped])) if inventory[equipped] else 1
                    if random.random() < rarity * (1+(luck/2)):
                        indexes.append(rolls.index(roll))

                if indexes:
                    shown_roll = random.choice(indexes)
                else:
                    shown_roll = random.randint(0, len(rolls) - 1)
                waiting = True
                is_rolling = False
                roll_timer = 0.1

    if waiting:
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        color = get_item_color(rolls[shown_roll])
        pygame.draw.rect(surface, color, (0, 0, WIDTH, HEIGHT))

        text = pygame.font.SysFont(rolls[shown_roll]["font"], 40, bold=rolls[shown_roll]["bold"]).render(get_item_name(rolls[shown_roll]), True, invert_color(color))
        rect = text.get_rect(center=(WIDTH//2, 100))
        surface.blit(text, rect.topleft)

        x = WIDTH // 2

        text = button_font.render(f"[{get_item_tier(rolls[shown_roll])}]", True, invert_color(color))
        rect = text.get_rect(center=(WIDTH//2, 130))
        surface.blit(text, rect.topleft)

        text = button_font.render(f"{get_item_rarity(rolls[shown_roll])*100}% Chance", True, invert_color(color))
        rect = text.get_rect(center=(WIDTH//2, 200))
        rect.x = x
        surface.blit(text, rect.topleft)

        text = button_font.render(f"{((1-get_item_rarity(inventory[equipped]))*100) / 2 if inventory[equipped] else 0.0}% Boost", True, invert_color(color))
        rect = text.get_rect(center=(WIDTH//2, 230))
        rect.x = x
        surface.blit(text, rect.topleft)

        txt = f"{get_item_rarity(rolls[shown_roll])*100}% Total Chance"
        if inventory[equipped] is not None:
            txt = f"{get_item_rarity(rolls[shown_roll]) * (((1-get_item_rarity(inventory[equipped]))*100) / 2)}% Total Chance"
        text = button_font.render(txt, True, invert_color(color))
        rect = text.get_rect(center=(WIDTH//2, 280))
        rect.x = x
        surface.blit(text, rect.topleft)

        pygame.draw.rect(surface, (200, 50, 50), del_button)
        pygame.draw.rect(surface, (160, 60, 50), del_button, 2)
        text = button_font.render("Delete", True, (255, 255, 255))
        rect = text.get_rect(center=del_button.center)
        surface.blit(text, rect.topleft)

        pygame.draw.rect(surface, (50, 200, 50), get_button)
        pygame.draw.rect(surface, (60, 160, 50), get_button, 2)
        text = button_font.render("Get", True, (255, 255, 255))
        rect = text.get_rect(center=get_button.center)
        surface.blit(text, rect.topleft)

        screen.blit(surface, (0, 0))

    if info != "":
        text = info_font.render(info, True, info_color)
        text_rect = text.get_rect(x=mouse[0], y=mouse[1]-20)
        screen.blit(text, text_rect.topleft)
        info = ""

    if warning != "":
        text = warning_font.render(warning, True, warning_color)
        rect = text.get_rect(center=(WIDTH//2, 100))
        screen.blit(text, rect.topleft)
        warning_timer -= 1 / 60
        if warning_timer <= 0:
            warning = ""

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
exit()