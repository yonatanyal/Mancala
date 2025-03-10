import pygame
import numpy
from State import State
from Constants import *
from Button import *

class Graphics:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.header_surf = pygame.Surface((H_WIDTH,H_HEIGHT))
        self.main_surf = pygame.Surface((M_WIDTH,M_HEIGHT))
        self.score1_surf = pygame.Surface((SCORES_WIDTH,SCORES_HEIGHT))
        self.score2_surf = pygame.Surface((SCORES_WIDTH,SCORES_HEIGHT))
        pygame.display.set_caption("Mancala")
        self.load_img()           
        self.load_menu_items()           
    

    def load_img(self):
        self.board_img = pygame.image.load('images/board/empty board.png') 
        self.header_img = pygame.image.load('images/board/wooden header.png')  
        self.score1_img = pygame.image.load('images/board/score1.png')  
        self.score2_img = pygame.image.load('images/board/score2.png')  
        self.stone1_img = pygame.image.load('images/stones/stone1.png')
        self.stones2_img = pygame.image.load('images/stones/stones2.png')
        self.stones3_img = pygame.image.load('images/stones/stones3.png')
        self.stones4_img = pygame.image.load('images/stones/stones4.png')
        self.stones5_img = pygame.image.load('images/stones/stones5.png')
        self.stones6_img = pygame.image.load('images/stones/stones6.png')
        self.stones7_img = pygame.image.load('images/stones/stones7.png')
        self.pit1_img = pygame.image.load('images/pits/pit1.png')
        self.pit2_img = pygame.image.load('images/pits/pit2.png')
        self.pit3_img = pygame.image.load('images/pits/pit3.png')
        self.pit4_img = pygame.image.load('images/pits/pit4.png')
        self.pit5_img = pygame.image.load('images/pits/pit5.png')
        self.pit6_img = pygame.image.load('images/pits/pit6.png')
        self.pit7_img = pygame.image.load('images/pits/pit7.png')
        self.pit8_img = pygame.image.load('images/pits/pit8.png')
        self.pit9_img = pygame.image.load('images/pits/pit9.png')
        self.pit10_img = pygame.image.load('images/pits/pit10.png')
        self.pit11_img = pygame.image.load('images/pits/pit11.png')
        self.pit12_img = pygame.image.load('images/pits/pit12.png')
        self.pit13_img = pygame.image.load('images/pits/pit13.png')
        self.pit14_img = pygame.image.load('images/pits/pit14.png')
        self.pit15_img = pygame.image.load('images/pits/pit15.png')
        self.pit16_img = pygame.image.load('images/pits/pit16.png')
        self.pit17_img = pygame.image.load('images/pits/pit17.png')
        self.pit18_img = pygame.image.load('images/pits/pit18.png')
        self.pit19_img = pygame.image.load('images/pits/pit19.png')
        self.pit20_img = pygame.image.load('images/pits/pit20.png')
        self.pit21_img = pygame.image.load('images/pits/pit21.png')
        self.pit22_img = pygame.image.load('images/pits/pit22.png')
        self.pit23_img = pygame.image.load('images/pits/pit23.png')
        self.pit24_img = pygame.image.load('images/pits/pit24.png')
        self.pit25_img = pygame.image.load('images/pits/pit25.png')
        

    def load_menu_items(self):
        self.bg = pygame.image.load('menu/Background.png') 
        self.MENU_TEXT = self.get_font(100).render("Mancala", True, "#b68f40")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(WIDTH/2, 100))

        self.P1_TEXT = self.get_font(40).render("Player 1:", True, "#b68f40")
        self.P1_RECT = self.P1_TEXT.get_rect(center=(WIDTH/2, 325))

        self.P2_TEXT = self.get_font(40).render("Player 2:", True, "#b68f40")
        self.P2_RECT = self.P2_TEXT.get_rect(center=(WIDTH/2, 475))

        self.RESULT_TEXT = self.get_font(70).render("TIE", True, "#b68f40")
        self.RESULT_RECT = self.RESULT_TEXT.get_rect(center=(WIDTH/2, 250))

        self.player_img = pygame.image.load("menu/Player Rect.png")
        self.selected_player_img = pygame.image.load("menu/Selected Player Rect.jpg")

        self.PLAY_BUTTON = Button(image=pygame.image.load("menu/Play Rect.png"), pos=(WIDTH/2, 225), 
                            text_input="PLAY", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
        
        self.HUMANP1_BUTTON = Button(image=self.selected_player_img, pos=(WIDTH/4, 400), 
                            text_input="HUMAN", font=self.get_font(25), base_color="#d7fcd4", hovering_color="White")
        self.RANDOMP1_BUTTON = Button(image=self.player_img, pos=(WIDTH/2 - 100, 400), 
                            text_input="RANDOM", font=self.get_font(25), base_color="#d7fcd4", hovering_color="White")
        self.DQNP1_BUTTON = Button(image=self.player_img, pos=(3*WIDTH/4 - 200, 400), 
                            text_input="DQN", font=self.get_font(25), base_color="#d7fcd4", hovering_color="White")
        self.ADVANCED1_BUTTON = Button(image=self.player_img, pos=(WIDTH - 300, 400), 
                            text_input="ADV", font=self.get_font(25), base_color="#d7fcd4", hovering_color="White")
        
        self.HUMANP2_BUTTON = Button(image=self.selected_player_img, pos=(WIDTH/4, 550), 
                            text_input="HUMAN", font=self.get_font(25), base_color="#d7fcd4", hovering_color="White")
        self.RANDOMP2_BUTTON = Button(image=self.player_img, pos=(WIDTH/2 - 100, 550), 
                            text_input="RANDOM", font=self.get_font(25), base_color="#d7fcd4", hovering_color="White")
        self.DQNP2_BUTTON = Button(image=self.player_img, pos=(3*WIDTH/4 - 200, 550), 
                            text_input="DQN", font=self.get_font(25), base_color="#d7fcd4", hovering_color="White")
        self.ADVANCED2_BUTTON = Button(image=self.player_img, pos=(WIDTH - 300, 550), 
                            text_input="ADV", font=self.get_font(25), base_color="#d7fcd4", hovering_color="White")
        
        self.RETURN_BUTTON = Button(image=pygame.image.load("menu/Return Rect.png"), pos=(WIDTH/2, 400), 
                            text_input="RETURN TO MAIN MENU", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")


    def draw(self, state: State) -> None:
        self.header_surf.blit(self.header_img,(0, 0))
        self.score1_surf.blit(self.score1_img,(0, 0))
        self.main_surf.blit(self.board_img,(0, 0))
        self.score2_surf.blit(self.score2_img,(0, 0))

        self.draw_pieces(state)
        self.draw_score(state)

        if state.end_of_game == 1:
            self.write('Player 1 Won')
        elif state.end_of_game == 2:
            self.write('Player 2 Won')
        elif state.end_of_game == -1:
            self.write('Tie')
        else:
            txt = f'Player {state.player}'
            if state.curr_extra_turn:
                txt += ': extra turn'
            self.write(txt)

        self.screen.blit(self.header_surf, (0,0))
        self.screen.blit(self.score1_surf, (0, 70))
        self.screen.blit(self.main_surf, (0, 160))
        self.screen.blit(self.score2_surf, (0, 560))
        pygame.display.update()
        # pygame.display.flip()
        

    def write(self, txt) -> None:
        text = self.get_font(30).render(txt, True, WHITE)
        text_rect = text.get_rect(center=(H_WIDTH/2, H_HEIGHT/2))
        self.header_surf.blit(text, text_rect)

    

    def draw_pieces(self, state: State) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                if (row == 0 and col == 0):
                    img = self.match_base(state.board[row][col])
                    x, y = 20, 40

                elif (row == 1 and col == 6):
                    img = self.match_base(state.board[row][col])
                    x, y = 1068, 40

                else:
                    img = self.match_stones(state.board[row][col])
                    x, y = self.calc_pos((row, col))
                
                if img:
                    self.main_surf.blit(img, (x,y))


    def draw_score(self, state: State) -> None:
        font = self.get_font(30)

        for col in range(COLS):
            score = state.board[0][col]
            score = font.render(str(score), True, WHITE)
            self.score1_surf.blit(score, (col*150+60,20))

        for col in range(COLS):
            score = state.board[1][col]
            score = font.render(str(score), True, WHITE)
            self.score2_surf.blit(score, ((col+1)*150+60,40))

    
    def match_stones(self, num) -> pygame.Surface | None:
        match num:
            case 0:
                return
            case 1:
                return self.stone1_img
            case 2:
                return self.stones2_img
            case 3:
                return self.stones3_img
            case 4:
                return self.stones4_img
            case 5:
                return self.stones5_img
            case 6:
                return self.stones6_img
            case _:
                return self.stones7_img


    def match_base(self, num) -> pygame.Surface | None:
        match num:
            case 0:
                return
            case 1:
                return self.pit1_img
            case 2:
                return self.pit2_img
            case 3:
                return self.pit3_img
            case 4:
                return self.pit4_img
            case 5:
                return self.pit5_img
            case 6:
                return self.pit6_img
            case 7:
                return self.pit7_img
            case 8:
                return self.pit8_img
            case 9:
                return self.pit9_img
            case 10:
                return self.pit10_img
            case 11:
                return self.pit11_img
            case 12:
                return self.pit12_img
            case 13:
                return self.pit13_img
            case 14:
                return self.pit14_img
            case 15:
                return self.pit15_img
            case 16:
                return self.pit16_img
            case 17:
                return self.pit17_img
            case 18:
                return self.pit18_img
            case 19:
                return self.pit19_img
            case 20:
                return self.pit20_img
            case 21:
                return self.pit21_img
            case 22:
                return self.pit22_img
            case 23:
                return self.pit23_img
            case 24:
                return self.pit24_img
            case _:
                return self.pit25_img


    def calc_pos(self, row_col) -> tuple:
        row, col = row_col
        x = (row + col) * SQUARE_WIDTH
        y = row * SQUARE_HEIGHT 
        return x, y
    
    
    def calc_row_col(self, pos) -> tuple:
        x, y = pos
        if (y < H_HEIGHT + SCORES_HEIGHT) or (y > H_HEIGHT + SCORES_HEIGHT + M_HEIGHT):
            return None
        
        row = (y - H_HEIGHT - SCORES_HEIGHT) // SQUARE_HEIGHT
        col = x // SQUARE_WIDTH - row
        if col > 6:
            col = 6
            row = 1
        if col < 0:
            col = 0
            row = 0
            
        return row, col


    def main_menu(self, events) -> int:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.MENU_TEXT, self.MENU_RECT)
        self.screen.blit(self.P1_TEXT, self.P1_RECT)
        self.screen.blit(self.P2_TEXT, self.P2_RECT)

        buttons = [
            self.HUMANP1_BUTTON, self.RANDOMP1_BUTTON, self.DQNP1_BUTTON, self.ADVANCED1_BUTTON,
            self.HUMANP2_BUTTON, self.RANDOMP2_BUTTON, self.DQNP2_BUTTON, self.ADVANCED2_BUTTON,
            self.PLAY_BUTTON
        ]

        for button in buttons:
            button.change_color(MENU_MOUSE_POS)
            button.update(self.screen)


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.check_for_input(MENU_MOUSE_POS):
                        for j, b in enumerate(buttons):
                            if b is not button and j//4 == i//4:
                                b.image = self.player_img
                            
                        if button is not self.PLAY_BUTTON:
                            button.image = self.selected_player_img

                        return i+1
        return 0
    

    def end_menu(self, result: int, events) -> int:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.change_result_text(result)

        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.RESULT_TEXT, self.RESULT_RECT)

        self.RETURN_BUTTON.change_color(MENU_MOUSE_POS)
        self.RETURN_BUTTON.update(self.screen)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.RETURN_BUTTON.check_for_input(MENU_MOUSE_POS):
                    return 1
        
        return 0


    # Returns Press-Start-2P in the desired size
    def get_font(self, size): 
        return pygame.font.Font("menu/font.ttf", size)
    

    # changes the result text to the winner
    def change_result_text(self, result: int):
        if result == 1:
            self.RESULT_TEXT = self.get_font(70).render("PLAYER 1 WON", True, "#b68f40")
        elif result == 2:
            self.RESULT_TEXT = self.get_font(70).render("PLAYER 2 WON", True, "#b68f40")
        elif result == -1:
            self.RESULT_TEXT = self.get_font(70).render("TIE", True, "#b68f40")
        self.RESULT_RECT = self.RESULT_TEXT.get_rect(center=(WIDTH/2, 250))


    def __call__(self, state) -> None:
            self.draw(state)

