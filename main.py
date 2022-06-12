import random
import pygame
import time
import pygame as pg
import sys
from random import randint

ask = input(
    "Would you like to play Tic Tac Toe (1) or the Snake Game (2)? ")

if ask == "1":
  WINDOW_SIZE = 300
  CELL_SIZE = WINDOW_SIZE //3
  INF = float('inf')
  vec2 = pg.math.Vector2
  CELL_CENTER = vec2(CELL_SIZE/ 2)
  
  class TicTacToe:
    def __init__(self, game):
      self.game = game
      self.board_image = self.get_scaled_image(path='img/board.png', res = [WINDOW_SIZE] *2)
      self.circle_image = self.get_scaled_image(path='img/circle.png', res=[CELL_SIZE]*2)
      self.Xyz_image = self.get_scaled_image(path='img/Xyz.png', res=[CELL_SIZE]*2)

      self.game_array = [[INF, INF, INF],
                         [INF, INF, INF],
                         [INF, INF, INF]]
      self.player = randint(0,1)
      self.line_indices_array = [[(0,0),(0,1),(0,2)],
                                 [(1,0),(1,1),(1,2)],
                                 [(2,0),(2,1),(2,2)],
                                 [(0,0),(1,0),(2,0)],
                                 [(0,1),(1,1),(2,1)],
                                 [(0,2),(1,2),(2,2)],
                                 [(0,0),(1,1),(2,2)],
                                 [(0,2),(1,1),(2,0)]]
      self.winner = None
      self.game_steps = 0

    def run_game_process(self):
      current_cell = vec2(pg.mouse.get_pos())//CELL_SIZE
      col, row = map(int, current_cell)
      click = pg.mouse.get_pressed()[0]

      if click and self.game_array[row][col] == INF and not self.winner:
        self.game_array[row][col] = self.player
        self.player = not self.player
        self.game_steps += 1
        self.check_winner() 
  
    def check_winner(self):
      for line_indices in self.line_indices_array:
        sum_line = sum([self.game_array[i][j] for i, j in line_indices])
        if sum_line in {0,3}:
          self.winner = 'XO'[sum_line == 0]
          self.winner_line = [vec2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER, vec2(line_indices[2][::-1]) *CELL_SIZE + CELL_CENTER]
          
    def draw_objects(self):
      for y, row in enumerate(self.game_array):
        for x, obj in enumerate(row):
          if obj != INF:
            self.game.screen.blit(self.Xyz_image if obj else self.circle_image, vec2(x,y) * CELL_SIZE) 

    def draw_winner(self):
      if self.winner:
        pg.draw.line(self.game.screen, 'blue', *self.winner_line, CELL_SIZE//8) 
      
    def draw(self):
      self.game.screen.blit(self.board_image,(0,0))
      self.draw_objects()
      self.draw_winner()

    @staticmethod
    def get_scaled_image(path,res):
      img = pg.image.load(path)
      return pg.transform.smoothscale(img,res)
    def print_caption(self):
      pg.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
      if self.winner:
        pg.display.set_caption(f'Player "{self.winner}" wins')
      elif self.game_steps == 9:
        pg.display.set_caption(f' Game Over')
          
    def run(self):
      self.print_caption()
      self.draw()
      self.run_game_process()
  
  class Game:
    def __init__(self):
     self.screen = pg.display.set_mode([WINDOW_SIZE] *2)
     self.clock = pg.time.Clock()
     self.tic_tac_toe = TicTacToe(self)
      
    def check_events(self):
     for event in pg.event.get():
       if event.type == pg.QUIT:
         pg.quit()
         sys.exit()
    
    def run(self):
      while True:
        self.tic_tac_toe.run()
        self.check_events()
        pg.display.update()
        self.clock.tick(60)
        
  if __name__ == '__main__':
    game = Game()
    game.run()
  
      
if ask == "2":
  pygame.init()
  width, height = 500, 500
  game_screen = pygame.display.set_mode((width, height))
  pygame.display.set_caption("Snake Game")

  clock = pygame.time.Clock()
  game_over = False

  x, y = 200, 200
  delta_x, delta_y = 10, 0

  food_x, food_y = random.randrange(0, width) // 10 * 10, random.randrange(0, height) // 10 * 10

  body_list = [(x, y)]

  font = pygame.font.SysFont("times new roman", 25)

  def snake():
      global x, y, food_x, food_y, game_over
      x = (x + delta_x) % width
      y = (y + delta_y) % height
     
      if ((x, y) in body_list):
          game_over = True
          return

      body_list.append((x, y))

      if (food_x == x and food_y == y):
          while ((food_x, food_y) in body_list):
              food_x, food_y = random.randrange(
                  0, width) // 10 * 10, random.randrange(0, width) // 10 * 10
      else:
          del body_list[0]
        
      game_screen.fill((0, 0, 0))
      score = font.render("Score: " + str(len(body_list)), True, (250, 250, 0))
      game_screen.blit(score, [0, 0])
    
      pygame.draw.rect(game_screen, (250, 0, 0), [food_x, food_y, 10, 10])
    
      for (i, j) in body_list:
          pygame.draw.rect(game_screen, (250, 250, 250), [i, j, 10, 10])
      pygame.display.update()

  while True:
    if (game_over):
        game_screen.fill((0, 0, 0))
        score = font.render("Score: " + str(len(body_list)), True, (250, 250, 250))
        game_screen.blit(score, [0, 0])
        text = font.render("Game Over", True, (250, 250, 250))
        game_screen.blit(text, [width // 3, height // 3])
        pygame.display.update()
        time.sleep(10)
        pygame.quit()
        quit()
    game = pygame.event.get()
    for event in game:
        if (event.type == pygame.QUIT):
            pygame.quit()
            quit()
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                if (delta_x != 10):
                    delta_x = -10
                delta_y = 0
            elif (event.key == pygame.K_RIGHT):
                if (delta_x != -10):
                    delta_x = 10
                delta_y = 0
            elif (event.key == pygame.K_UP):
                delta_x = 0
                if (delta_y != 10):
                    delta_y = -10
            elif (event.key == pygame.K_DOWN):
                delta_x = 0
                if (delta_y != -10):
                    delta_y = 10
            else:
                continue
            snake()
      
    if (not game):
        snake()
    clock.tick(15)