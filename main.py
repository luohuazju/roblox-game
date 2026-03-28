import pygame
import random
import sys
import math
import os

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 750, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WOLF GOD - Supernatural Chaos!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 22)
tiny_font = pygame.font.SysFont(None, 18)

game_dir = os.path.dirname(os.path.abspath(__file__))
try:
    coin_sfx = pygame.mixer.Sound(os.path.join(game_dir, "coin.wav"))
    coin_sfx.set_volume(0.4)
except: coin_sfx = None
try:
    explode_sfx = pygame.mixer.Sound(os.path.join(game_dir, "explode.wav"))
    explode_sfx.set_volume(0.5)
except: explode_sfx = None
try:
    pygame.mixer.music.load(os.path.join(game_dir, "bgm.wav"))
    pygame.mixer.music.set_volume(0.3)
except: pass

# Colors
SKY = (135, 206, 235)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
DARK_GRAY = (60, 60, 60)
ORANGE = (255, 140, 0)
GROUND_GREEN = (80, 160, 50)
GROUND_DARK = (60, 130, 40)
BIRD_BROWN = (120, 80, 40)
BIRD_DARK = (90, 60, 30)
TANK_GREEN = (70, 110, 50)
TANK_DARK = (50, 80, 35)
BULLET_COLOR = (200, 200, 50)
PANCAKE_TAN = (210, 180, 120)
PANCAKE_DARK = (180, 150, 90)
SYRUP = (139, 90, 43)
SYRUP_LIGHT = (180, 120, 60)
HOT_SAUCE_RED = (200, 20, 20)
HOT_SAUCE_DARK = (150, 10, 10)
HOT_SAUCE_DROP = (255, 60, 30)
PTERO_GREEN = (50, 130, 80)
PTERO_DARK = (30, 100, 60)
PTERO_BELLY = (120, 180, 120)
LASER_GLOW = (255, 180, 180)
SPATULA_SILVER = (180, 180, 190)
SPATULA_DARK = (120, 120, 130)
SPATULA_HANDLE = (80, 60, 40)
HEART_RED = (220, 30, 50)
GOLD = (255, 215, 0)
SHIELD_BLUE = (50, 150, 255)
SHOP_BG = (20, 15, 35)
SHOP_ITEM = (40, 35, 65)
SHOP_HOVER = (60, 55, 95)
GREEN = (50, 200, 50)
PURPLE = (160, 50, 255)
CYAN = (50, 255, 255)
WOLF_GRAY = (140, 140, 155)
WOLF_DARK = (90, 90, 105)
WOLF_LIGHT = (180, 180, 195)
WOLF_EYE = (255, 200, 0)
SPIRIT_BLUE = (100, 150, 255)
FIRE_ORANGE = (255, 120, 20)
LIGHTNING = (200, 200, 255)
PLANE_X = 80
GROUND_Y = HEIGHT - 45

# ═══ LEVELS ═══
LEVELS = [
    {'name':'Moonlit Meadow','sky':(40,50,100),'ground':GROUND_GREEN,'ground_d':GROUND_DARK,
     'coins_needed':6,'enemies':['bomb'],'spawn_rate':1.2,'speed':2.8,
     'desc':'A gentle start under the moon.'},
    {'name':'Windy Peaks','sky':(100,150,200),'ground':GROUND_GREEN,'ground_d':GROUND_DARK,
     'coins_needed':8,'enemies':['bomb','bird'],'spawn_rate':1.0,'speed':3.0,
     'desc':'Birds soar on mountain winds.'},
    {'name':'Breakfast Blitz','sky':(255,180,120),'ground':(194,178,128),'ground_d':(170,155,110),
     'coins_needed':10,'enemies':['bomb','bird','pancake','spatula'],'spawn_rate':0.9,'speed':3.3,
     'desc':'Dodge flying breakfast!'},
    {'name':'Spicy Desert','sky':(220,150,80),'ground':(194,160,100),'ground_d':(170,140,80),
     'coins_needed':12,'enemies':['bomb','bird','hot_sauce','tank'],'spawn_rate':0.85,'speed':3.5,
     'desc':'Tanks and hot sauce in the heat!'},
    {'name':'Syrup Swamp','sky':(80,100,60),'ground':(90,70,40),'ground_d':(70,50,25),
     'coins_needed':14,'enemies':['bomb','pancake','spatula','syrup','hot_sauce'],'spawn_rate':0.8,'speed':3.8,
     'desc':'Everything is sticky!'},
    {'name':'Dino Jungle','sky':(60,120,60),'ground':(40,100,40),'ground_d':(30,80,30),
     'coins_needed':16,'enemies':['bomb','bird','ptero','pancake','tank'],'spawn_rate':0.75,'speed':4.0,
     'desc':'Pterodactyls hunt from above!'},
    {'name':'Neon Lab','sky':(15,10,40),'ground':(30,25,50),'ground_d':(20,15,35),
     'coins_needed':18,'enemies':['bomb','laser','ptero','hot_sauce','spatula'],'spawn_rate':0.7,'speed':4.3,
     'desc':'Lasers in the dark!'},
    {'name':'Volcano Peak','sky':(60,20,10),'ground':(150,40,15),'ground_d':(120,30,10),
     'coins_needed':20,'enemies':['bomb','bird','pancake','tank','hot_sauce','ptero'],'spawn_rate':0.65,'speed':4.6,
     'desc':'Fire and fury!'},
    {'name':'Storm Fortress','sky':(40,40,60),'ground':(50,50,60),'ground_d':(35,35,45),
     'coins_needed':22,'enemies':['bomb','bird','laser','tank','ptero','spatula','syrup'],'spawn_rate':0.6,'speed':4.9,
     'desc':'Thunder and steel!'},
    {'name':'Alien Dimension','sky':(20,5,30),'ground':(40,20,60),'ground_d':(30,10,45),
     'coins_needed':25,'enemies':['bomb','bird','pancake','spatula','tank','hot_sauce','syrup','ptero','laser'],'spawn_rate':0.55,'speed':5.2,
     'desc':'Reality bends here!'},
    {'name':'Shadow Realm','sky':(5,0,10),'ground':(15,10,20),'ground_d':(10,5,15),
     'coins_needed':28,'enemies':['bomb','bird','pancake','spatula','tank','hot_sauce','syrup','ptero','laser'],'spawn_rate':0.5,'speed':5.5,
     'desc':'Darkness consumes all!'},
    {'name':'WOLF GOD FINALE','sky':(0,0,0),'ground':(80,0,0),'ground_d':(60,0,0),
     'coins_needed':999,'enemies':['bomb','bird','pancake','spatula','tank','hot_sauce','syrup','ptero','laser'],'spawn_rate':0.4,'speed':6.0,
     'desc':'ENDLESS CHAOS! How long can the Wolf God survive?'},
]

# ═══ SHOP ═══
UPGRADES = [
    {'name':'Extra Life','desc':'+1 Life','cost':8,'max':10,'key':'extra_life','cat':'Defense'},
    {'name':'Spirit Shield','desc':'Block 1 hit at start','cost':12,'max':3,'key':'shield','cat':'Defense'},
    {'name':'Wolf Speed','desc':'Faster movement','cost':10,'max':5,'key':'speed_boost','cat':'Movement'},
    {'name':'Ghost Form','desc':'Smaller hitbox','cost':15,'max':1,'key':'tiny','cat':'Movement'},
    {'name':'Coin Magnet','desc':'Coins fly to you','cost':18,'max':1,'key':'magnet','cat':'Utility'},
    {'name':'Double Coins','desc':'2x coin value','cost':22,'max':1,'key':'double_coins','cat':'Utility'},
    {'name':'Soul Fang','desc':'Auto-shoot spirit fangs','cost':15,'max':1,'key':'machine_gun','cat':'Weapon'},
    {'name':'Rapid Fangs','desc':'Shoot faster (needs Fang)','cost':20,'max':3,'key':'rapid_fire','cat':'Weapon'},
    {'name':'Howl Missile','desc':'SPACE: homing spirit wolf','cost':30,'max':1,'key':'missiles','cat':'Weapon'},
    {'name':'Moon Beam','desc':'Hold SPACE: laser beam','cost':35,'max':1,'key':'laser_gun','cat':'Weapon'},
    {'name':'Thunder Clap','desc':'D: lightning blast forward','cost':40,'max':1,'key':'thunder','cat':'Power'},
    {'name':'Spirit Explosion','desc':'F: destroy all nearby','cost':50,'max':1,'key':'spirit_bomb','cat':'Power'},
    {'name':'Healing Howl','desc':'H: restore 1 life (60s cd)','cost':45,'max':1,'key':'heal','cat':'Power'},
    {'name':'Time Slow','desc':'G: slow enemies 5s','cost':40,'max':1,'key':'time_slow','cat':'Power'},
]

total_coins = 0
current_level = 0
purchased = {u['key']: 0 for u in UPGRADES}
high_scores = [0] * len(LEVELS)

STATE_MENU = 0; STATE_SHOP = 1; STATE_PLAYING = 2; STATE_LEVEL_CLEAR = 3; STATE_GAMEOVER = 4
game_state = STATE_MENU
shop_selected = 0
shop_scroll = 0

def get_max_lives(): return 30 + purchased['extra_life']
def get_plane_speed(): return 4.5 + purchased['speed_boost'] * 0.7
def get_plane_size(): return 18 if purchased['tiny'] else 28

def reset_game(level):
    lv = LEVELS[level]
    return {
        'plane_y': HEIGHT // 2 - 40, 'frame': 0,
        'clouds': [[random.randint(200,900),random.randint(20,GROUND_Y-100),random.randint(30,60)] for _ in range(6)],
        'coins':[],'bombs':[],'birds':[],'tanks':[],'bullets':[],
        'pancakes':[],'hot_sauces':[],'sauce_drops':[],
        'pteros':[],'lasers':[],'spatulas':[],'syrup_streams':[],
        'timers':{k:0 for k in ['coin','bomb','bird','tank','pancake','sauce','ptero','laser','spatula','syrup']},
        'score':0,'level_coins':0,'alive':True,
        'lives':get_max_lives(),'shield':purchased['shield'],
        'hit_flash':0,'killed_by':'','invincible':0,
        'game_speed':lv['speed'],'spawn_rate':lv['spawn_rate'],
        'my_bullets':[],'my_missiles':[],'shoot_timer':0,'laser_on':False,
        'thunder_cd':0,'spirit_cd':0,'heal_cd':0,'slow_cd':0,'slow_timer':0,
        'particles':[],'kills':0,
    }

g = {}

def spawn_enemy(g, etype):
    GY = GROUND_Y
    if etype=='bomb': g['bombs'].append([WIDTH,random.randint(30,GY-40)])
    elif etype=='bird': g['birds'].append([WIDTH,random.randint(30,GY-60),random.uniform(0,6.28),random.choice([-1,1])])
    elif etype=='pancake': g['pancakes'].append([WIDTH,random.randint(40,GY-50),random.uniform(0,6.28)])
    elif etype=='spatula': g['spatulas'].append([WIDTH,random.randint(30,GY-50),random.uniform(0,6.28),False])
    elif etype=='tank': g['tanks'].append([WIDTH,0])
    elif etype=='hot_sauce': g['hot_sauces'].append([WIDTH,random.randint(50,GY-80),0])
    elif etype=='syrup':
        sy=random.randint(40,GY-60)
        g['syrup_streams'].append([WIDTH,sy,sy,40+random.randint(0,30),0])
    elif etype=='ptero': g['pteros'].append([WIDTH+20,random.randint(30,GY-80),0,g['plane_y']])
    elif etype=='laser':
        gap_y=random.randint(50,GY-120)
        g['lasers'].append([WIDTH,gap_y,max(get_plane_size()+35,70),0])

def add_particles(g, x, y, color, count=5):
    for _ in range(count):
        g['particles'].append([x,y,random.uniform(-3,3),random.uniform(-3,3),color,random.randint(15,30)])

def draw_wolf(surface, x, y, size, alive, frame, invincible, shield_count, slow_active):
    if not alive:
        # Death explosion - spirit dispersing
        for r in range(40, 5, -8):
            c = (100 + r*2, 50 + r, 255 - r*3)
            pygame.draw.circle(surface, c, (x+20, y+size//2), r)
        return
    if invincible > 0 and frame % 6 < 3: return
    s = size / 28.0
    cx, cy = x + int(20*s), y + size // 2
    # Aura glow
    aura_pulse = int(math.sin(frame * 0.05) * 30)
    aura_r = int(30*s) + aura_pulse // 3
    aura_color = (80, 60, 200, 40) if not slow_active else (50, 200, 255, 60)
    aura_surf = pygame.Surface((aura_r*2, aura_r*2), pygame.SRCALPHA)
    pygame.draw.circle(aura_surf, (*aura_color[:3], 30), (aura_r, aura_r), aura_r)
    surface.blit(aura_surf, (cx - aura_r, cy - aura_r))
    # Body
    pygame.draw.ellipse(surface, WOLF_GRAY, (x, y + int(4*s), int(40*s), int(20*s)))
    pygame.draw.ellipse(surface, WOLF_DARK, (x, y + int(4*s), int(40*s), int(20*s)), 1)
    # Belly
    pygame.draw.ellipse(surface, WOLF_LIGHT, (x + int(5*s), y + int(10*s), int(25*s), int(12*s)))
    # Head
    hx, hy = x + int(35*s), y + int(6*s)
    pygame.draw.circle(surface, WOLF_GRAY, (hx, hy), int(10*s))
    # Ears
    pygame.draw.polygon(surface, WOLF_DARK, [(hx-int(6*s),hy-int(8*s)),(hx-int(2*s),hy-int(18*s)),(hx+int(2*s),hy-int(8*s))])
    pygame.draw.polygon(surface, WOLF_DARK, [(hx+int(2*s),hy-int(8*s)),(hx+int(6*s),hy-int(18*s)),(hx+int(10*s),hy-int(8*s))])
    # Snout
    pygame.draw.ellipse(surface, WOLF_LIGHT, (hx+int(4*s), hy-int(3*s), int(12*s), int(8*s)))
    pygame.draw.circle(surface, BLACK, (hx+int(14*s), hy-int(1*s)), int(2*s))  # nose
    # Eyes (glowing)
    eye_glow = 200 + int(math.sin(frame * 0.1) * 55)
    pygame.draw.circle(surface, (eye_glow, eye_glow//2, 0), (hx-int(1*s), hy-int(3*s)), int(3*s))
    pygame.draw.circle(surface, (eye_glow, eye_glow//2, 0), (hx+int(5*s), hy-int(3*s)), int(3*s))
    pygame.draw.circle(surface, WHITE, (hx-int(1*s), hy-int(3*s)), int(1.5*s))
    pygame.draw.circle(surface, WHITE, (hx+int(5*s), hy-int(3*s)), int(1.5*s))
    # Tail (wavy)
    tail_wave = math.sin(frame * 0.15) * 8
    pygame.draw.line(surface, WOLF_DARK, (x, cy), (x - int(15*s), cy + int(tail_wave) - int(5*s)), int(3*s))
    pygame.draw.circle(surface, WOLF_LIGHT, (x - int(15*s), cy + int(tail_wave) - int(5*s)), int(3*s))
    # Wings (spirit wings!)
    wing_flap = int(math.sin(frame * 0.12) * 10 * s)
    wing_color = SPIRIT_BLUE if not slow_active else CYAN
    pygame.draw.polygon(surface, wing_color, [
        (cx - int(5*s), cy - int(2*s)),
        (cx + int(5*s), cy - int(25*s) + wing_flap),
        (cx + int(15*s), cy - int(5*s)),
    ])
    pygame.draw.polygon(surface, wing_color, [
        (cx - int(5*s), cy + int(2*s)),
        (cx + int(5*s), cy + int(25*s) - wing_flap),
        (cx + int(15*s), cy + int(5*s)),
    ])
    # Shield orbs
    for i in range(shield_count):
        angle = frame * 0.05 + i * 2.094
        ox = cx + int(math.cos(angle) * 20 * s)
        oy = cy + int(math.sin(angle) * 20 * s)
        pygame.draw.circle(surface, SHIELD_BLUE, (ox, oy), 4)
        pygame.draw.circle(surface, WHITE, (ox, oy), 2)

def draw_heart(surface, x, y, filled):
    c = HEART_RED if filled else DARK_GRAY
    pygame.draw.circle(surface, c, (x-5, y), 7)
    pygame.draw.circle(surface, c, (x+5, y), 7)
    pygame.draw.polygon(surface, c, [(x-12,y+2),(x,y+16),(x+12,y+2)])

running = True
while running:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()
    clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state in [STATE_SHOP,STATE_LEVEL_CLEAR,STATE_GAMEOVER]: game_state = STATE_MENU
                elif game_state == STATE_MENU: running = False
                elif game_state == STATE_PLAYING: game_state = STATE_MENU
            if event.key == pygame.K_SPACE:
                if game_state == STATE_MENU:
                    g = reset_game(current_level)
                    game_state = STATE_PLAYING
                    try: pygame.mixer.music.play(-1)
                    except: pass
                elif game_state == STATE_GAMEOVER: game_state = STATE_MENU
                elif game_state == STATE_LEVEL_CLEAR:
                    current_level = min(current_level+1, len(LEVELS)-1)
                    game_state = STATE_MENU
            if game_state == STATE_MENU:
                if event.key == pygame.K_s: game_state = STATE_SHOP
                if event.key == pygame.K_LEFT: current_level = max(0, current_level-1)
                if event.key == pygame.K_RIGHT: current_level = min(len(LEVELS)-1, current_level+1)
            if game_state == STATE_SHOP:
                if event.key == pygame.K_UP: shop_selected = max(0, shop_selected-1)
                if event.key == pygame.K_DOWN: shop_selected = min(len(UPGRADES)-1, shop_selected+1)
                if event.key == pygame.K_RETURN:
                    u = UPGRADES[shop_selected]
                    if purchased[u['key']] < u['max'] and total_coins >= u['cost']:
                        total_coins -= u['cost']
                        purchased[u['key']] += 1
        if event.type == pygame.MOUSEBUTTONDOWN: clicked = True

    # ═══ MENU ═══
    if game_state == STATE_MENU:
        screen.fill((15, 10, 30))
        # Animated stars
        for i in range(50):
            sx = (i*97 + pygame.time.get_ticks()//50) % WIDTH
            sy = (i*53) % (HEIGHT-20) + 10
            pygame.draw.circle(screen, WHITE, (sx, sy), 1)
        t = big_font.render("WOLF GOD", True, PURPLE)
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 30))
        t2 = font.render("Supernatural Chaos", True, SPIRIT_BLUE)
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 80))
        # Draw wolf preview
        draw_wolf(screen, WIDTH//2-25, 115, 28, True, pygame.time.get_ticks()//16, 0, purchased['shield'], False)
        lv = LEVELS[current_level]
        ln = font.render(f"Level {current_level+1}/{len(LEVELS)}: {lv['name']}", True, WHITE)
        screen.blit(ln, (WIDTH//2 - ln.get_width()//2, 170))
        ld = small_font.render(lv['desc'], True, (180,180,180))
        screen.blit(ld, (WIDTH//2 - ld.get_width()//2, 200))
        ct = font.render(f"Coins: {total_coins}", True, GOLD)
        screen.blit(ct, (WIDTH//2 - ct.get_width()//2, 235))
        lives_t = small_font.render(f"Lives: {get_max_lives()} | Speed: {get_plane_speed():.1f}", True, (150,150,150))
        screen.blit(lives_t, (WIDTH//2 - lives_t.get_width()//2, 265))
        # Buttons
        play_r = pygame.Rect(WIDTH//2-120, 300, 240, 45)
        shop_r = pygame.Rect(WIDTH//2-120, 355, 240, 45)
        pc = GREEN if play_r.collidepoint(mx,my) else (40,160,40)
        sc_c = GOLD if shop_r.collidepoint(mx,my) else (180,150,0)
        pygame.draw.rect(screen, pc, play_r, border_radius=8)
        pygame.draw.rect(screen, sc_c, shop_r, border_radius=8)
        screen.blit(font.render("PLAY (Space)", True, WHITE), (play_r.x+45, play_r.y+8))
        screen.blit(font.render("SHOP (S)", True, WHITE), (shop_r.x+65, shop_r.y+8))
        if clicked:
            if play_r.collidepoint(mx,my):
                g = reset_game(current_level)
                game_state = STATE_PLAYING
                try: pygame.mixer.music.play(-1)
                except: pass
            elif shop_r.collidepoint(mx,my): game_state = STATE_SHOP
        screen.blit(small_font.render("LEFT/RIGHT = Change Level | ESC = Quit", True, (100,100,100)), (WIDTH//2-150, HEIGHT-25))

    # ═══ SHOP ═══
    elif game_state == STATE_SHOP:
        screen.fill(SHOP_BG)
        screen.blit(big_font.render("SHOP", True, GOLD), (WIDTH//2-50, 8))
        screen.blit(font.render(f"Coins: {total_coins}", True, GOLD), (WIDTH//2-55, 50))
        # Scrollable items
        visible = 8
        if shop_selected < shop_scroll: shop_scroll = shop_selected
        if shop_selected >= shop_scroll + visible: shop_scroll = shop_selected - visible + 1
        for idx in range(shop_scroll, min(shop_scroll + visible, len(UPGRADES))):
            u = UPGRADES[idx]
            i = idx - shop_scroll
            y = 85 + i * 48
            r = pygame.Rect(30, y, WIDTH-60, 44)
            bg = SHOP_HOVER if idx == shop_selected else SHOP_ITEM
            if r.collidepoint(mx,my):
                bg = SHOP_HOVER
                if clicked:
                    shop_selected = idx
                    if purchased[u['key']] < u['max'] and total_coins >= u['cost']:
                        total_coins -= u['cost']; purchased[u['key']] += 1
            pygame.draw.rect(screen, bg, r, border_radius=6)
            if idx == shop_selected: pygame.draw.rect(screen, GOLD, r, 2, border_radius=6)
            owned = purchased[u['key']]
            # Category color
            cat_colors = {'Defense':HEART_RED,'Movement':GREEN,'Utility':GOLD,'Weapon':ORANGE,'Power':PURPLE}
            cat_c = cat_colors.get(u['cat'], WHITE)
            screen.blit(tiny_font.render(u['cat'], True, cat_c), (r.x+8, r.y+3))
            screen.blit(font.render(u['name'], True, WHITE), (r.x+8, r.y+14))
            screen.blit(small_font.render(u['desc'], True, (160,160,160)), (r.x+200, r.y+20))
            if owned >= u['max']:
                st = small_font.render("MAX", True, GREEN)
            elif total_coins >= u['cost']:
                st = small_font.render(f"{u['cost']}c [BUY]", True, GOLD)
            else:
                st = small_font.render(f"{u['cost']}c", True, RED)
            screen.blit(st, (r.x+r.width-st.get_width()-10, r.y+14))
            for j in range(u['max']):
                cx_d = r.x + r.width - 80 - j * 12
                cc = GREEN if j < owned else DARK_GRAY
                pygame.draw.circle(screen, cc, (cx_d, r.y+10), 4)
        screen.blit(small_font.render("UP/DOWN=Select | ENTER/Click=Buy | ESC=Back", True, (100,100,100)), (WIDTH//2-170, HEIGHT-22))

    # ═══ PLAYING ═══
    elif game_state == STATE_PLAYING:
        if g.get('hit_flash',0) > 0: g['hit_flash'] -= 1
        if g.get('invincible',0) > 0: g['invincible'] -= 1
        if g.get('thunder_cd',0) > 0: g['thunder_cd'] -= 1
        if g.get('spirit_cd',0) > 0: g['spirit_cd'] -= 1
        if g.get('heal_cd',0) > 0: g['heal_cd'] -= 1
        if g.get('slow_cd',0) > 0: g['slow_cd'] -= 1
        if g.get('slow_timer',0) > 0: g['slow_timer'] -= 1
        g['frame'] += 1
        lv = LEVELS[current_level]
        psz = get_plane_size()
        slow_active = g.get('slow_timer', 0) > 0
        speed_mult = 0.4 if slow_active else 1.0

        if g['alive']:
            keys = pygame.key.get_pressed()
            pspd = get_plane_speed()
            if keys[pygame.K_UP] or keys[pygame.K_w]: g['plane_y'] -= pspd
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: g['plane_y'] += pspd
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: pass  # reserved
            if g['plane_y'] < 10: g['plane_y'] = 10
            if g['plane_y'] > GROUND_Y - psz - 10: g['plane_y'] = GROUND_Y - psz - 10

            spd = g['game_speed'] * speed_mult
            sr = g['spawn_rate']
            frame = g['frame']

            # Powers
            # Thunder (D key)
            if purchased['thunder'] and keys[pygame.K_d] and g['thunder_cd'] <= 0:
                g['thunder_cd'] = 90
                # Kill everything in a wide horizontal strip
                ty = g['plane_y'] + psz // 2
                thunder_rect = pygame.Rect(PLANE_X, ty - 40, WIDTH, 80)
                for lst in [g['bombs'],g['birds'],g['pancakes'],g['spatulas'],g['pteros'],g['hot_sauces']]:
                    for e in lst[:]:
                        ex = e[0]; ey = e[1] if len(e) > 1 else 0
                        if thunder_rect.collidepoint(ex, ey):
                            lst.remove(e); g['kills'] += 1; g['score'] += 1; g['level_coins'] += 1
                            total_coins += 1
                            add_particles(g, ex, ey, LIGHTNING, 8)

            # Spirit bomb (F key)
            if purchased['spirit_bomb'] and keys[pygame.K_f] and g['spirit_cd'] <= 0:
                g['spirit_cd'] = 180
                cx_b = PLANE_X + 20; cy_b = g['plane_y'] + psz // 2
                for lst in [g['bombs'],g['birds'],g['pancakes'],g['spatulas'],g['pteros'],g['hot_sauces'],g['sauce_drops']]:
                    for e in lst[:]:
                        ex = e[0]; ey = e[1] if len(e) > 1 else 0
                        dist = math.sqrt((ex-cx_b)**2 + (ey-cy_b)**2)
                        if dist < 200:
                            lst.remove(e); g['kills'] += 1; g['score'] += 1; g['level_coins'] += 1
                            total_coins += 1
                            add_particles(g, ex, ey, PURPLE, 6)
                add_particles(g, cx_b, cy_b, SPIRIT_BLUE, 20)

            # Heal (H key)
            if purchased['heal'] and keys[pygame.K_h] and g['heal_cd'] <= 0 and g['lives'] < get_max_lives():
                g['heal_cd'] = 360  # 6 seconds
                g['lives'] = min(g['lives'] + 1, get_max_lives())
                add_particles(g, PLANE_X+20, g['plane_y']+psz//2, GREEN, 15)

            # Time slow (G key)
            if purchased['time_slow'] and keys[pygame.K_g] and g['slow_cd'] <= 0:
                g['slow_cd'] = 600  # 10 seconds
                g['slow_timer'] = 300  # 5 seconds of slow

            # Spawn
            g['timers']['coin'] += 1
            if g['timers']['coin'] > int(28 * sr):
                g['timers']['coin'] = 0
                g['coins'].append([WIDTH, random.randint(30, GROUND_Y-40)])
            for etype in lv['enemies']:
                g['timers'][etype] = g['timers'].get(etype,0) + 1
                intervals = {'bomb':50,'bird':55,'pancake':60,'spatula':65,'tank':90,'hot_sauce':75,'syrup':85,'ptero':95,'laser':120}
                base = intervals.get(etype, 60)
                interval = max(18, int(base * sr))
                if g['timers'][etype] > interval:
                    g['timers'][etype] = 0
                    spawn_enemy(g, etype)

            # Move
            for c in g['coins']: c[0] -= spd
            for b in g['bombs']: b[0] -= (spd+1)*speed_mult
            for bird in g['birds']:
                bird[0] -= (spd+1.5)*speed_mult; bird[2] += 0.08
                bird[1] += math.sin(bird[2])*1.5*bird[3]
                bird[1] = max(20, min(GROUND_Y-40, bird[1]))
            for p in g['pancakes']: p[0] -= (spd+0.5)*speed_mult; p[2] += 0.15
            for sp in g['spatulas']: sp[0] -= (spd+2)*speed_mult; sp[2] += 0.25
            for t in g['tanks']: t[0] -= spd*0.6*speed_mult
            for t in g['tanks']:
                if 0 < t[0] < WIDTH and frame % int(70/max(0.5,speed_mult)) < 2:
                    g['bullets'].append([t[0], GROUND_Y-25])
            for b in g['bullets']: b[1] -= 4.5*speed_mult
            for hs in g['hot_sauces']:
                hs[0] -= spd*0.8*speed_mult; hs[2] += 1
                if hs[2] % 35 == 0 and 0 < hs[0] < WIDTH:
                    for _ in range(3): g['sauce_drops'].append([hs[0],hs[1],random.uniform(-3,-1),random.uniform(-4,4)])
            for sd in g['sauce_drops']: sd[0] += sd[2]*speed_mult; sd[1] += sd[3]*speed_mult; sd[3] += 0.12
            for ss in g['syrup_streams']: ss[0] -= spd*0.6*speed_mult; ss[4] += 0.06; ss[2] = ss[1]+math.sin(ss[4])*15
            for pt in g['pteros']:
                pt[0] -= (spd+2.5)*speed_mult
                if pt[1] < g['plane_y']: pt[1] += 1.5*speed_mult
                elif pt[1] > g['plane_y']: pt[1] -= 1.5*speed_mult
                pt[1] = max(15, min(GROUND_Y-40, pt[1]))
            for lw in g['lasers']: lw[0] -= spd*0.7*speed_mult; lw[3] += 1

            # Cleanup
            g['coins']=[c for c in g['coins'] if c[0]>-20]
            g['bombs']=[b for b in g['bombs'] if b[0]>-20]
            g['birds']=[b for b in g['birds'] if b[0]>-40]
            g['pancakes']=[p for p in g['pancakes'] if p[0]>-30]
            g['spatulas']=[s for s in g['spatulas'] if s[0]>-40]
            g['tanks']=[t for t in g['tanks'] if t[0]>-60]
            g['bullets']=[b for b in g['bullets'] if b[1]>-10]
            g['hot_sauces']=[h for h in g['hot_sauces'] if h[0]>-30]
            g['sauce_drops']=[s for s in g['sauce_drops'] if -20<s[0]<WIDTH+20 and s[1]<HEIGHT+20]
            g['syrup_streams']=[s for s in g['syrup_streams'] if s[0]>-60]
            g['pteros']=[p for p in g['pteros'] if p[0]>-50]
            g['lasers']=[l for l in g['lasers'] if l[0]>-20]

            # Particles update
            for p in g['particles']: p[0]+=p[2]; p[1]+=p[3]; p[5]-=1
            g['particles']=[p for p in g['particles'] if p[5]>0]

            # Magnet
            if purchased['magnet']:
                for c in g['coins']:
                    dx=PLANE_X-c[0]; dy=g['plane_y']-c[1]
                    dist=math.sqrt(dx*dx+dy*dy)
                    if dist<120 and dist>0: c[0]+=dx/dist*4; c[1]+=dy/dist*4

            # Weapons
            g['shoot_timer'] += 1
            gun_rate = max(4, 12 - purchased['rapid_fire']*3)
            if purchased['machine_gun'] and g['shoot_timer'] % gun_rate == 0:
                g['my_bullets'].append([PLANE_X+45, g['plane_y']+psz//2])
            if purchased['missiles'] and keys[pygame.K_SPACE] and g['shoot_timer'] % 25 == 0:
                g['my_missiles'].append([PLANE_X+45, g['plane_y']+psz//2, None])
            g['laser_on'] = purchased['laser_gun'] and keys[pygame.K_SPACE]

            for b in g['my_bullets']: b[0] += 9
            g['my_bullets']=[b for b in g['my_bullets'] if b[0]<WIDTH+10]
            for m in g['my_missiles']:
                m[0] += 7
                targets=[(b[0],b[1]) for b in g['bombs']]+[(b[0],b[1]) for b in g['birds']]+[(p[0],p[1]) for p in g['pancakes']]+[(p[0],int(p[1])) for p in g['pteros']]
                nearest=None; best_d=999
                for tx,ty in targets:
                    d=math.sqrt((tx-m[0])**2+(ty-m[1])**2)
                    if d<best_d: best_d=d; nearest=(tx,ty)
                if nearest and best_d<280:
                    dx=nearest[0]-m[0]; dy=nearest[1]-m[1]; dist=math.sqrt(dx*dx+dy*dy)
                    if dist>0: m[1]+=dy/dist*5
            g['my_missiles']=[m for m in g['my_missiles'] if m[0]<WIDTH+10]

            # Weapon kills
            def kill_enemy(lst, rect_fn):
                killed=0
                for b in g['my_bullets'][:]:
                    br=pygame.Rect(b[0]-4,b[1]-4,8,8)
                    for e in lst[:]:
                        if br.colliderect(rect_fn(e)):
                            if e in lst: lst.remove(e); add_particles(g,e[0],e[1] if len(e)>1 else 0,ORANGE,4)
                            if b in g['my_bullets']: g['my_bullets'].remove(b)
                            killed+=1; break
                for m in g['my_missiles'][:]:
                    mr=pygame.Rect(m[0]-6,m[1]-6,12,12)
                    for e in lst[:]:
                        if mr.colliderect(rect_fn(e)):
                            if e in lst: lst.remove(e); add_particles(g,e[0],e[1] if len(e)>1 else 0,FIRE_ORANGE,8)
                            if m in g['my_missiles']: g['my_missiles'].remove(m)
                            killed+=1; break
                if g['laser_on']:
                    lr=pygame.Rect(PLANE_X+45,g['plane_y']+psz//2-4,WIDTH,8)
                    for e in lst[:]:
                        if lr.colliderect(rect_fn(e)):
                            lst.remove(e); add_particles(g,e[0],e[1] if len(e)>1 else 0,RED,3); killed+=1
                return killed
            ds=0
            ds+=kill_enemy(g['bombs'],lambda b:pygame.Rect(b[0]-12,b[1]-12,24,24))
            ds+=kill_enemy(g['birds'],lambda b:pygame.Rect(b[0]-15,b[1]-8,30,16))
            ds+=kill_enemy(g['pancakes'],lambda p:pygame.Rect(p[0]-14,p[1]-6,28,12))
            ds+=kill_enemy(g['spatulas'],lambda s:pygame.Rect(int(s[0])-16,int(s[1])-5,32,10))
            ds+=kill_enemy(g['pteros'],lambda p:pygame.Rect(p[0]-20,p[1]-12,40,24))
            ds+=kill_enemy(g['hot_sauces'],lambda h:pygame.Rect(h[0]-8,h[1]-15,16,30))
            if ds>0: g['score']+=ds; g['level_coins']+=ds; total_coins+=ds; g['kills']+=ds

            # Collision
            pr=pygame.Rect(PLANE_X,g['plane_y'],int(45*psz/28),psz)
            can_hit=g['invincible']<=0
            coin_val=2 if purchased['double_coins'] else 1
            for c in g['coins'][:]:
                if pr.colliderect(pygame.Rect(c[0]-8,c[1]-8,16,16)):
                    g['coins'].remove(c); g['score']+=coin_val; g['level_coins']+=coin_val; total_coins+=coin_val
                    if coin_sfx: coin_sfx.play()

            if g['level_coins']>=lv['coins_needed'] and current_level<len(LEVELS)-1:
                if g['score']>high_scores[current_level]: high_scores[current_level]=g['score']
                game_state=STATE_LEVEL_CLEAR; continue

            if can_hit:
                killer=''
                checks=[
                    (g['bombs'],lambda b:pygame.Rect(b[0]-12,b[1]-12,24,24),'Bomb'),
                    (g['birds'],lambda b:pygame.Rect(b[0]-15,b[1]-8,30,16),'Bird'),
                    (g['pancakes'],lambda p:pygame.Rect(p[0]-14,p[1]-6,28,12),'Flying Pancake'),
                    (g['spatulas'],lambda s:pygame.Rect(int(s[0])-16,int(s[1])-5,32,10),'Spatula'),
                    (g['bullets'],lambda b:pygame.Rect(b[0]-3,b[1]-3,6,6),'Tank Bullet'),
                    (g['hot_sauces'],lambda h:pygame.Rect(h[0]-8,h[1]-15,16,30),'Hot Sauce'),
                    (g['sauce_drops'],lambda s:pygame.Rect(s[0]-4,s[1]-4,8,8),'Sauce Splash'),
                    (g['pteros'],lambda p:pygame.Rect(p[0]-20,p[1]-12,40,24),'Pterodactyl'),
                ]
                for lst,rf,name in checks:
                    for item in lst:
                        if pr.colliderect(rf(item)): killer=name; break
                    if killer: break
                if not killer:
                    for ss in g['syrup_streams']:
                        if pr.colliderect(pygame.Rect(int(ss[0])-5,int(ss[2]),ss[3],12)): killer='Syrup Stream'
                if not killer:
                    for lw in g['lasers']:
                        lx=int(lw[0])
                        if PLANE_X+int(45*psz/28)>lx and PLANE_X<lx+8:
                            if not(g['plane_y']>lw[1] and g['plane_y']+psz<lw[1]+lw[2]): killer='Laser Wall'
                if killer:
                    if g['shield']>0:
                        g['shield']-=1; g['invincible']=60; g['hit_flash']=20
                        g['killed_by']=f"{killer} (Shield!)"
                        add_particles(g,PLANE_X+20,g['plane_y']+psz//2,SHIELD_BLUE,10)
                    else:
                        g['lives']-=1; g['killed_by']=killer; g['hit_flash']=30; g['invincible']=90
                        if explode_sfx: explode_sfx.play()
                        add_particles(g,PLANE_X+20,g['plane_y']+psz//2,RED,12)
                        if g['lives']<=0:
                            g['alive']=False
                            if g['score']>high_scores[current_level]: high_scores[current_level]=g['score']
                            try: pygame.mixer.music.stop()
                            except: pass

            for cloud in g['clouds']:
                cloud[0]-=1
                if cloud[0]<-80: cloud[0]=WIDTH+random.randint(20,100); cloud[1]=random.randint(20,GROUND_Y-100)

        # ── DRAW ──
        if g.get('hit_flash',0)>0 and g['hit_flash']%4<2: screen.fill((80,20,20))
        else: screen.fill(lv['sky'])
        if lv['sky'][0]<50:
            for i in range(40):
                sx=(i*97+g['frame'])%WIDTH; sy=(i*53)%(GROUND_Y-20)+10
                pygame.draw.circle(screen,WHITE,(sx,sy),1)
        for cx,cy,cr in g['clouds']: pygame.draw.ellipse(screen,WHITE,(cx,cy,cr*2,cr))
        pygame.draw.rect(screen,lv['ground'],(0,GROUND_Y,WIDTH,HEIGHT-GROUND_Y))
        pygame.draw.line(screen,lv['ground_d'],(0,GROUND_Y),(WIDTH,GROUND_Y),3)

        # Enemies draw
        for lw in g['lasers']:
            lx=int(lw[0]);gt=int(lw[1]);gb=int(lw[1]+lw[2])
            fl=180+int(math.sin(g['frame']*0.3)*75);lc=(255,max(0,min(255,fl-100)),max(0,min(255,fl-150)))
            pygame.draw.rect(screen,lc,(lx,5,6,gt-5));pygame.draw.rect(screen,lc,(lx,gb,6,GROUND_Y-gb))
            pygame.draw.circle(screen,DARK_GRAY,(lx+3,8),6);pygame.draw.circle(screen,DARK_GRAY,(lx+3,GROUND_Y-3),6)
            pygame.draw.rect(screen,(0,255,0),(lx-1,gt,8,3));pygame.draw.rect(screen,(0,255,0),(lx-1,gb-3,8,3))
        for ss in g['syrup_streams']:
            sx=int(ss[0]);sy=int(ss[2]);sw=int(ss[3])
            for i in range(0,sw,2):
                w=int(math.sin((sx+i)*0.1+ss[4])*4)
                pygame.draw.line(screen,SYRUP,(sx+i,sy+w),(sx+i,sy+w+10),3)
        for t in g['tanks']:
            tx=int(t[0]);ty=GROUND_Y
            pygame.draw.rect(screen,TANK_DARK,(tx-20,ty-12,40,12));pygame.draw.rect(screen,TANK_GREEN,(tx-14,ty-22,28,12))
            pygame.draw.circle(screen,TANK_GREEN,(tx,ty-25),8);pygame.draw.line(screen,TANK_DARK,(tx,ty-25),(tx,ty-38),3)
        for b in g['bullets']: pygame.draw.circle(screen,BULLET_COLOR,(int(b[0]),int(b[1])),3)
        for hs in g['hot_sauces']:
            hx,hy=int(hs[0]),int(hs[1])
            pygame.draw.rect(screen,HOT_SAUCE_RED,(hx-5,hy-10,10,20));pygame.draw.rect(screen,WHITE,(hx-3,hy-14,6,5))
        for sd in g['sauce_drops']: pygame.draw.circle(screen,HOT_SAUCE_DROP,(int(sd[0]),int(sd[1])),4)
        for p in g['pancakes']:
            px,py_p,ang=int(p[0]),int(p[1]),p[2];w=int(abs(math.cos(ang))*24+4)
            pygame.draw.ellipse(screen,PANCAKE_TAN,(px-w//2,py_p-5,w,10))
        for sp in g['spatulas']:
            sx,sy,ang=int(sp[0]),int(sp[1]),sp[2];ca,sa_v=math.cos(ang),math.sin(ang)
            pts=[(-14,-4),(8,-4),(10,0),(8,4),(-14,4)]
            r=[(int(sx+x*ca-y*sa_v),int(sy+x*sa_v+y*ca)) for x,y in pts]
            pygame.draw.polygon(screen,SPATULA_SILVER,r)
        for pt in g['pteros']:
            px,py_p=int(pt[0]),int(pt[1]);wf=int(math.sin(g['frame']*0.15)*12)
            pygame.draw.ellipse(screen,PTERO_GREEN,(px-18,py_p-8,36,16))
            pygame.draw.circle(screen,PTERO_GREEN,(px-20,py_p-6),8)
            pygame.draw.polygon(screen,ORANGE,[(px-28,py_p-6),(px-40,py_p-4),(px-28,py_p-2)])
            pygame.draw.polygon(screen,RED,[(px-18,py_p-12),(px-8,py_p-20),(px-5,py_p-8)])
            pygame.draw.circle(screen,YELLOW,(px-22,py_p-8),3)
            pygame.draw.polygon(screen,PTERO_DARK,[(px-8,py_p-8),(px+5,py_p-25+wf),(px+18,py_p-8)])
            pygame.draw.polygon(screen,PTERO_DARK,[(px-8,py_p+8),(px+5,py_p+25-wf),(px+18,py_p+8)])
        for bird in g['birds']:
            bx,by=int(bird[0]),int(bird[1]);wo=int(math.sin(g['frame']*0.2)*6)
            pygame.draw.ellipse(screen,BIRD_BROWN,(bx-12,by-5,24,12))
            pygame.draw.circle(screen,BIRD_BROWN,(bx-14,by-4),6)
            pygame.draw.polygon(screen,ORANGE,[(bx-20,by-4),(bx-25,by-2),(bx-20,by)])
            pygame.draw.circle(screen,WHITE,(bx-16,by-5),3)
            pygame.draw.polygon(screen,BIRD_DARK,[(bx-4,by-5),(bx+2,by-14+wo),(bx+10,by-5)])
            pygame.draw.polygon(screen,BIRD_DARK,[(bx-4,by+5),(bx+2,by+14-wo),(bx+10,by+5)])

        # Wolf
        draw_wolf(screen,PLANE_X,g['plane_y'],psz,g['alive'],g['frame'],g.get('invincible',0),g.get('shield',0),g.get('slow_timer',0)>0)

        # My weapons
        for b in g.get('my_bullets',[]):
            pygame.draw.circle(screen,SPIRIT_BLUE,(int(b[0]),int(b[1])),4)
            pygame.draw.circle(screen,WHITE,(int(b[0]),int(b[1])),2)
        for m in g.get('my_missiles',[]):
            mx_m,my_m=int(m[0]),int(m[1])
            pygame.draw.polygon(screen,PURPLE,[(mx_m+12,my_m),(mx_m-6,my_m-5),(mx_m-6,my_m+5)])
            pygame.draw.polygon(screen,SPIRIT_BLUE,[(mx_m-6,my_m-4),(mx_m-12,my_m-7),(mx_m-12,my_m+7),(mx_m-6,my_m+4)])
        if g.get('laser_on') and g.get('alive'):
            ly=g['plane_y']+psz//2
            pygame.draw.line(screen,PURPLE,(PLANE_X+45,ly),(WIDTH,ly),5)
            pygame.draw.line(screen,(200,150,255),(PLANE_X+45,ly),(WIDTH,ly),2)
            pygame.draw.circle(screen,WHITE,(PLANE_X+47,ly),7)

        # Thunder visual
        if g.get('thunder_cd',0) > 75:
            ty=g['plane_y']+psz//2
            for i in range(0,WIDTH-PLANE_X,15):
                y_off=random.randint(-30,30)
                pygame.draw.line(screen,LIGHTNING,(PLANE_X+45+i,ty+y_off),(PLANE_X+60+i,ty+random.randint(-30,30)),3)

        # Spirit bomb visual
        if g.get('spirit_cd',0) > 165:
            cx_b=PLANE_X+20;cy_b=g['plane_y']+psz//2
            r=int((180-g['spirit_cd'])*15)
            s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.circle(s,(160,50,255,80),(r,r),r)
            screen.blit(s,(cx_b-r,cy_b-r))

        # Particles
        for p in g.get('particles',[]):
            alpha=min(255,p[5]*10)
            pygame.draw.circle(screen,p[4],(int(p[0]),int(p[1])),max(1,p[5]//8))

        # Coins & bombs on top
        for c in g['coins']:
            pygame.draw.circle(screen,YELLOW,(c[0],c[1]),8);pygame.draw.circle(screen,(200,200,0),(c[0],c[1]),6)
        for b in g['bombs']:
            pygame.draw.circle(screen,DARK_GRAY,(b[0],b[1]),12);pygame.draw.circle(screen,BLACK,(b[0],b[1]),10)
            pygame.draw.line(screen,ORANGE,(b[0],b[1]-10),(b[0]+5,b[1]-16),2)
            pygame.draw.circle(screen,YELLOW,(b[0]+5,b[1]-16),3)

        pygame.draw.line(screen,RED,(0,5),(WIDTH,5),3)

        # HUD
        draw_heart(screen,WIDTH-55,18,g.get('lives',30)>0)
        screen.blit(font.render(f"x{g.get('lives',30)}",True,HEART_RED if g.get('lives',30)>10 else RED),(WIDTH-42,8))
        if g.get('shield',0)>0:
            for i in range(g['shield']): pygame.draw.circle(screen,SHIELD_BLUE,(WIDTH-70-i*15,40),6)
            screen.blit(tiny_font.render("SHIELD",True,SHIELD_BLUE),(WIDTH-70-g['shield']*15,48))

        tc=WHITE if lv['sky'][0]<80 else BLACK
        screen.blit(font.render(f"Score: {g['score']}",True,tc),(10,8))
        needed=lv['coins_needed']
        prog=min(1.0,g['level_coins']/needed)
        pygame.draw.rect(screen,DARK_GRAY,(10,40,150,12),border_radius=4)
        pygame.draw.rect(screen,GREEN,(10,40,int(150*prog),12),border_radius=4)
        screen.blit(small_font.render(f"{g['level_coins']}/{needed}",True,WHITE),(165,38))
        screen.blit(small_font.render(f"Lv{current_level+1} {lv['name']}",True,GOLD),(10,55))
        screen.blit(small_font.render(f"Kills:{g.get('kills',0)} Coins:{total_coins}",True,GOLD),(10,72))

        # Power cooldowns
        py_hud = 90
        if purchased['thunder']:
            cd=g.get('thunder_cd',0); c=GREEN if cd<=0 else RED
            screen.blit(tiny_font.render(f"[D]Thunder {'READY' if cd<=0 else f'{cd//60+1}s'}",True,c),(10,py_hud)); py_hud+=14
        if purchased['spirit_bomb']:
            cd=g.get('spirit_cd',0); c=GREEN if cd<=0 else RED
            screen.blit(tiny_font.render(f"[F]Spirit {'READY' if cd<=0 else f'{cd//60+1}s'}",True,c),(10,py_hud)); py_hud+=14
        if purchased['heal']:
            cd=g.get('heal_cd',0); c=GREEN if cd<=0 else RED
            screen.blit(tiny_font.render(f"[H]Heal {'READY' if cd<=0 else f'{cd//60+1}s'}",True,c),(10,py_hud)); py_hud+=14
        if purchased['time_slow']:
            cd=g.get('slow_cd',0); c=GREEN if cd<=0 else RED
            txt=f"[G]Slow {'READY' if cd<=0 else f'{cd//60+1}s'}"
            if g.get('slow_timer',0)>0: txt=f"[G]SLOW ACTIVE {g['slow_timer']//60+1}s"; c=CYAN
            screen.blit(tiny_font.render(txt,True,c),(10,py_hud)); py_hud+=14
        if purchased['machine_gun']:
            screen.blit(tiny_font.render("AUTO:Fangs",True,SPIRIT_BLUE),(10,py_hud)); py_hud+=14
        if purchased['missiles']:
            screen.blit(tiny_font.render("[SPC]Missile",True,PURPLE),(10,py_hud)); py_hud+=14
        if purchased['laser_gun']:
            screen.blit(tiny_font.render("[SPC]Beam",True,RED),(10,py_hud))

        if g.get('hit_flash',0)>15 and g['alive']:
            ht=small_font.render(f"OUCH! {g['killed_by']}",True,RED)
            screen.blit(ht,(WIDTH//2-ht.get_width()//2,90))
        if slow_active:
            st=font.render("TIME SLOW",True,CYAN)
            screen.blit(st,(WIDTH//2-st.get_width()//2,GROUND_Y-30))

        if not g['alive']: game_state=STATE_GAMEOVER

    # ═══ LEVEL CLEAR ═══
    elif game_state == STATE_LEVEL_CLEAR:
        screen.fill((10,30,15))
        for i in range(30):
            sx=(i*97+pygame.time.get_ticks()//30)%WIDTH;sy=(i*53)%(HEIGHT-20)+10
            pygame.draw.circle(screen,GOLD,(sx,sy),2)
        screen.blit(big_font.render("LEVEL CLEAR!",True,GREEN),(WIDTH//2-155,50))
        lv=LEVELS[current_level]
        screen.blit(font.render(f"{lv['name']} Complete!",True,WHITE),(WIDTH//2-120,120))
        screen.blit(font.render(f"Score: {g.get('score',0)}  Kills: {g.get('kills',0)}",True,YELLOW),(WIDTH//2-130,170))
        screen.blit(font.render(f"Coins Earned: {g.get('level_coins',0)}",True,GOLD),(WIDTH//2-100,210))
        screen.blit(font.render(f"Total Coins: {total_coins}",True,GOLD),(WIDTH//2-90,250))
        if current_level<len(LEVELS)-1:
            nl=LEVELS[current_level+1]
            screen.blit(small_font.render(f"Next: Lv{current_level+2} - {nl['name']}: {nl['desc']}",True,(180,180,180)),(WIDTH//2-180,300))
        screen.blit(font.render("SPACE = Next Level",True,WHITE),(WIDTH//2-110,350))
        screen.blit(small_font.render("ESC = Menu (visit Shop!)",True,(120,120,120)),(WIDTH//2-80,390))

    # ═══ GAME OVER ═══
    elif game_state == STATE_GAMEOVER:
        screen.fill((10,0,15))
        for i in range(20):
            sx=(i*97+pygame.time.get_ticks()//50)%WIDTH;sy=(i*53)%(HEIGHT-20)+10
            pygame.draw.circle(screen,RED,(sx,sy),1)
        screen.blit(big_font.render("THE WOLF FALLS...",True,RED),(WIDTH//2-175,40))
        draw_wolf(screen,WIDTH//2-20,100,28,False,pygame.time.get_ticks()//16,0,0,False)
        screen.blit(font.render(f"Level: {LEVELS[current_level]['name']}",True,WHITE),(WIDTH//2-80,160))
        screen.blit(font.render(f"Score: {g.get('score',0)}  Kills: {g.get('kills',0)}",True,YELLOW),(WIDTH//2-110,195))
        kb=g.get('killed_by','???')
        screen.blit(font.render(f"Slain by: {kb}",True,ORANGE),(WIDTH//2-font.size(f"Slain by: {kb}")[0]//2,230))
        screen.blit(font.render(f"Coins: {g.get('level_coins',0)} earned | {total_coins} total",True,GOLD),(WIDTH//2-170,270))
        screen.blit(font.render("SPACE = Rise Again",True,WHITE),(WIDTH//2-110,330))
        screen.blit(small_font.render("Tip: Visit the Shop for weapons and powers!",True,(150,150,150)),(WIDTH//2-150,370))

    pygame.display.flip()

pygame.quit()
sys.exit()
