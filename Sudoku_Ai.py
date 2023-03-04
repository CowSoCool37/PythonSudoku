"""
Sudoku Solver
Raymond K.
Solves a Sudoku puzzle importing manually or from a file
"""

#import stuff
import pygame, sys, math, time
import pygame.freetype
from collections import Counter

#finds the clicked tile
def clicked_tile(position):
    click_x = math.floor(position[0]/100)
    click_y = math.floor(position[1]/100)
    return(click_x + 9 * click_y)

#checks if a board state is valid
def check_validity():
    for i in range(9):
        counter1 = Counter(board[i*9:i*9+9])
        counter2 = Counter(board[i::9])
        counter3 = Counter(board[(i%3)*3 + math.floor(i/3)*27:(i%3)*3 + math.floor(i/3)*27 + 3] + board[(i%3)*3 + math.floor(i/3)*27 + 9:(i%3)*3 + math.floor(i/3)*27 + 12] + board[(i%3)*3 + math.floor(i/3)*27 + 18:(i%3)*3 + math.floor(i/3)*27 + 21])
        for j in range(9):
            if counter1[j+1] > 1 or counter2[j+1] > 1 or counter3[j+1] > 1:
                return(False)
    return(True)

#fills a tile with a number from 1 to 9
def fill_tile(key):
    global tile_change
    global solve_status
    global logic_solves
    logic_solves = []
    for i in range(81):
        logic_solves.append(False)
    if key == pygame.K_1 or key == pygame.K_KP1:
        board[tile_change] = 1
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_2 or key == pygame.K_KP2:
        board[tile_change] = 2
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_3 or key == pygame.K_KP3:
        board[tile_change] = 3
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_4 or key == pygame.K_KP4:
        board[tile_change] = 4
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_5 or key == pygame.K_KP5:
        board[tile_change] = 5
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_6 or key == pygame.K_KP6:
        board[tile_change] = 6
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_7 or key == pygame.K_KP7:
        board[tile_change] = 7
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_8 or key == pygame.K_KP8:
        board[tile_change] = 8
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_9 or key == pygame.K_KP9:
        board[tile_change] = 9
        givens[tile_change] = True
        tile_change = -1
        solve_status = "unsolved"
    if key == pygame.K_BACKSPACE:
        board[tile_change] = 0
        givens[tile_change] = False
        tile_change = -1
        solve_status = "unsolved"

#solves the sudoku
def solve():
    global start
    global valid_numbers_list
    global pointer
    global status
    global action
    global end
    global solve_status
    global logic_solved_tiles
    for i in range(500):
        if action == "solve":
            if givens[pointer] == True or logic_solves[pointer] == True:
                pointer += 1
                if pointer >= 81:
                    end = time.time()
                    solve_status = "solved"
                    status = "starting"
                    return
            elif check_validity() == False and board[pointer] != valid_numbers_list[pointer][-1]:
                board[pointer] = valid_numbers_list[pointer][valid_numbers_list[pointer].index(board[pointer]) + 1]
            elif check_validity() == True and board[pointer] == 0:
                board[pointer] = valid_numbers_list[pointer][0]
            elif check_validity() == True and board[pointer] >= 0:
                pointer += 1
                if pointer >= 81:
                    end = time.time()
                    solve_status = "solved"
                    status = "starting"
                    return
            else:
                board[pointer] = 0
                pointer -= 1 
                action = "backtrack"
        else:
            if givens[pointer] == True or logic_solves[pointer] == True:
                pointer -= 1
            elif board[pointer] == valid_numbers_list[pointer][-1]:
                board[pointer] = 0
                pointer -= 1
            else:
                board[pointer] = valid_numbers_list[pointer][valid_numbers_list[pointer].index(board[pointer]) + 1]
                action = "solve"

#finds the valid numbers for each tile from the starting configuration and does a bit of solving with logic, increasing solve speed
def find_valid_numbers():
    global board
    global logic_solves
    logic_solved_tiles = 0
    global valid_numbers_list
    valid_numbers_list = []
    global givens
    for i in range(81):
        if givens[i] == False and logic_solves[i] == False:
            valid_numbers = []
            for j in range(9):
                board[i] = j + 1
                if check_validity():
                    valid_numbers.append(j + 1)
            board[i] = 0
            valid_numbers_list.append(valid_numbers)
        else: valid_numbers_list.append(0)

    for i in range(81):
        if givens[i] == False and logic_solves[i] == False:
            if len(valid_numbers_list[i]) == 1:
                board[i] = valid_numbers_list[i][0]
                logic_solves[i] = True
                logic_solved_tiles += 1

    if logic_solved_tiles > 0:
        find_valid_numbers()


#draws info on screen
def draw_controls():
    global screen
    global rainbow_color
    global start
    global end
    global solve_status
    rainbow_color += 1
    if rainbow_color > 359: rainbow_color = 0
    tiny_font.render_to(screen, (950,20), "Sudoku Solver", (max(0, 255 * (math.sin(math.radians(rainbow_color)))), max(0, 255 * (math.sin(math.radians(rainbow_color + 120)))), max(0, 255 * (math.sin(math.radians(rainbow_color + 240))))))
    tiny_font.render_to(screen, (1000,90), "Controls:", (25,25,25))
    tinier_font.render_to(screen, (915,150), "Click a tile then press 1-9 to set it", (25,25,25))
    tinier_font.render_to(screen, (915,200), "I to import puzzle from file", (25,25,25))
    tinier_font.render_to(screen, (915,250), "C to clear", (25,25,25))
    tinier_font.render_to(screen, (915,300), "Space to start", (25,25,25))
    if solve_status == "solved":
        tinier_font.render_to(screen, (915,500), "Time taken: " + str(round(end - start, 5)), (25,25,25))
    if solve_status == "invalid":
        tinier_font.render_to(screen, (915,500), "This puzzle is invalid", (25,25,25))
    if solve_status == "import_invalid":
        tinier_font.render_to(screen, (915,500), "That file does not exist", (25,25,25))
        tinier_font.render_to(screen, (915,530), "or is invalid", (25,25,25))
    if solve_status == "import_valid":
        tinier_font.render_to(screen, (915,500), "Import successful!", (25,25,25))
    
    
#main function
def main():
    #starts pygame and set up variables
    pygame.init()
    global tile_change
    global screen
    screen = pygame.display.set_mode((1300,900))
    global small_font
    small_font = pygame.freetype.SysFont('Arial', 80)
    global tiny_font
    tiny_font = pygame.freetype.SysFont('Arial', 50)
    global tinier_font
    tinier_font = pygame.freetype.SysFont('Arial', 25)
    pygame.display.set_caption("Sudoku Ai")
    global board
    board = []
    global givens
    givens = []
    global status
    status = "starting"
    tile_change = -1
    clock = pygame.time.Clock()
    for i in range(81):
        board.append(0)
        givens.append(False)
    global rainbow_color
    rainbow_color = 0
    global solve_status
    solve_status = "unsolved"
    global logic_solves
    logic_solves = []
    for i in range(81):
        logic_solves.append(False)

    #main loop
    while 1:
        #get inputs from user
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if status == "starting" and mouse_pos[0] < 900:
                    if tile_change >= 0:
                        board[tile_change] = 0
                        givens[tile_change] = False
                    tile_change = clicked_tile(mouse_pos)
                    board[tile_change] = 0
                    givens[tile_change] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and status == "starting":
                    if tile_change > -1:
                        board[tile_change] = 0
                        givens[tile_change] = False
                        tile_change = -1
                    status = "solving"
                if event.key == pygame.K_i:
                    #importing puzzle from file
                    importing = True
                    text = ""
                    while importing == True:
                        screen.fill((200,200,200))
                        tiny_font.render_to(screen, (20,200), "Enter file name:", (25,25,25))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    importing = False
                                elif event.key == pygame.K_BACKSPACE:
                                    text = text[:-1]
                                else:
                                    text += event.unicode
                        tiny_font.render_to(screen, (20,300), text, (50,50,50))
                        pygame.display.flip()
                        clock.tick(60)

                    try:
                        read_file = open(text, "r")
                        file_text = (read_file.read())
                        file_text = file_text.replace("\n","")
                        for i in range(81):
                            board[i] = int(file_text[i])
                            if file_text[i] == "0":
                                givens[i] = False
                            else:
                                givens[i] = True
                        read_file.close()
                        solve_status = "import_valid"
                        logic_solves = []
                        for i in range(81):
                            logic_solves.append(False)
                    except:
                        solve_status = "import_invalid"
                        logic_solves = []
                        for i in range(81):
                            logic_solves.append(False)
                if event.key == pygame.K_c:
                        board = []
                        givens = []
                        status = "starting"
                        solve_status = "unsolved"
                        tile_change = -1
                        for i in range(81):
                            board.append(0)
                            givens.append(False)
                        logic_solves = []
                        for i in range(81):
                            logic_solves.append(False)
                                
                        
                if tile_change >= 0:
                    fill_tile(event.key)

        #draw the board and numbers on board
        screen.fill((200,200,200))
        for i in range(9):
            pygame.draw.polygon(screen, (50,50,50),((0,i*100+99),(900,i*100+99),(900,i*100+101),(0,i*100+101)))
            pygame.draw.polygon(screen, (50,50,50),((i*100+99,0),(i*100+99,900),(i*100+101,900),(i*100+101,0)))
        for i in range(2):
            pygame.draw.polygon(screen, (50,50,50),((0,i*300+297),(900,i*300+297),(900,i*300+303),(0,i*300+303)))
            pygame.draw.polygon(screen, (50,50,50),((i*300+297,0),(i*300+297,900),(i*300+303,900),(i*300+303,0)))
        for i in range(81):
            if board[i] != 0:
                if givens[i] == True:
                    small_font.render_to(screen, ((i%9)*100 + 35, math.floor(i/9)*100 + 20), str(board[i]), (25,25,25))
                else:
                    small_font.render_to(screen, ((i%9)*100 + 35, math.floor(i/9)*100 + 20), str(board[i]), (25,25,200))
        if tile_change >= 0:
            small_font.render_to(screen, ((tile_change%9)*100 + 35, math.floor(tile_change/9)*100 + 20), "?", (25,25,25))
        

        draw_controls()

        #run the solve function
        if status == "solving":
            find_valid_numbers()
            global pointer
            global action
            pointer = 0
            action = "solve"
            status = "solving1"
            global start
            start = time.time()
        
        if status == "solving1":
            try:
                solve_status = "unsolved"
                solve()
            except:
                solve_status = "invalid"
                status = "starting"
        
        pygame.display.flip()
        if status == "starting":
            clock.tick(60)
        


main()