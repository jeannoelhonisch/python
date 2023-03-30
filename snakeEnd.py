import pygame
import time
import random

# Initialisiert und lädt in Arbeitsspeicher 
pygame.init()
# Musik und Soundeffekte/ mixer.sound klasse 
sound = pygame.mixer.Sound("resources/hintergrundmusik.mp3")
montana = pygame.mixer.Sound("resources/jippie.mp3")
crash = pygame.mixer.Sound("resources/futter.mp3")

#Farben
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Displaygröße festgelegt und Display eingeladen
dis_width = 800
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))


pygame.display.set_caption('Snake Game by Mert, Jean-Noel')
clock = pygame.time.Clock()

#Größe der Schlangenblöcke
snake_block = 10
snake_speed = 10

#score
font_style = pygame.font.SysFont("Retro Gaming", 20)
score_font = pygame.font.SysFont("Retro Gaming", 20)

# Funktion um Score einzublenden 
# blit überträgt auf Display und mit render.text erstellt
def Your_score(score):
    value = score_font.render("Dein Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

# Die Funktion nimmt meine Schlange und für i in Schlange[] malt sie dort block
def erstellt_snake(snake_block, snake_list):
    for i in snake_list:
        pygame.draw.rect(dis, black, [i[0], i[1], snake_block, snake_block])
 
# Unsere Nachricht, wenn neu startet
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
 #
 ##
 ###
 ####
 #####
 ####
 ###
 ##
 #

 # Gameloop wiederholt das Spielgeschehen und wartet auf Input
def gameLoop():

    # Hintergrund musik eingefügt
    pygame.mixer.Sound.play(sound)

    # Variablen für GameLoop While-Schleife
    game_over = False
    game_close = False
 
    #
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
    
    # Gibt random Werte an food weiter in Range von Display
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
        
        # Aus seiten wieder raus kommen 
        # Koordinate mit Displaygröße abgeglichen dann immer gegenteilige Seite raus 
        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width
        elif y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height

        # Wenn spiel close dann Anleitung und Score
        while game_close == True:
            #Musik bei Aus langsam aus 
            sound.fadeout(2000)
            dis.fill(black)
            message("You lose. Drück C für Play Again or Q für Quit", white)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            
            # Mit event.get() Klasse festlegen wann gameover oder neustart
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        #Wartet auf Input und ändert die position von x1_change/ y1_change zur position der Schlange
        #Die Bedingung die überprüft, ob die Richtungsumkehrung mit der aktuellen Bewegunsrichtung übereinstimmt,
        #falls ja wird die Richtungsumkehrung ignoriert.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
 
        # Erstellt die Kooridinaten der und fügt meine Tastenänderungen hinzu
        x1 += x1_change
        y1 += y1_change
        # Malt den Hintergrund
        dis.fill(green)
        # Malt das Rechteck
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        # Kopf der Schlange und fügt in Liste
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        # Schlangenkopf in Liste
        snake_List.append(snake_Head)

        # entfernt die erste Koordiante aus Liste um Kopf nicht mit zu zählen damit selbst nicht triffst
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        
        # Wenn du selber triffst stirbst du 
        for i in snake_List[:-1]:
            if i == snake_Head:
                pygame.mixer.Sound.play(crash)
                game_close = True
                    
        erstellt_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        
        pygame.display.update()
        
        # Erstelle neues Food, wenn schlange Food frisst.
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

            if Length_of_snake == 5:
                pygame.mixer.Sound.play(montana)
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()