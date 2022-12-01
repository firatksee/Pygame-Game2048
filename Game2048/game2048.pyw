import pygame
import random
import sys
import time

class Game2048(pygame.sprite.Sprite):
	def __init__(self, size, screen_size):
		super().__init__()
		self.size = size
		self.game_board = [[0 for x in range(self.size)] for y in range(self.size)]
		self.screen_size = screen_size
		self.gap_size = (15*self.screen_size[0]/100) / (self.size + 1)
		self.plate_size = (self.screen_size[0] - self.gap_size*(self.size + 1)) / self.size
		self.plate_coor = self.calc_plate_coor()
		self.plate_coor_center = []

		self.image = pygame.Surface((self.plate_size,self.plate_size))
		self.image.fill('#656c75')
		self.rect = self.image.get_rect(topleft = (self.plate_coor[0]))

		self.text_size = 50
		self.font = pygame.font.SysFont('cambria', self.text_size)

		self.colors = {
			0:'#656c75',
			2:'#ffba08',
			4:'#f48c06',
			8:'#e85d04',
			16:'#dc2f02',
			32:'#d00000',
			64:'#9d0208',
			128:'#0466c8',
			256:'#0353a4',
			512:'#023e7d',
			1024:'#002855',
			2048:'#001845',
			4096:'#98bd6f',
			8192:'#7d8f69',
			16384:'#557153',
			32768:'#4e6c50',
			65536:'#395144',
			131072:'#61481C',
			262144:'#3c2317'
		}

		self.place_two()

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r and self.game_over():
					self.game_board = [[0 for x in range(self.size)] for y in range(self.size)]
					self.place_two()
				if event.key == pygame.K_UP:
					self.move_input(0, 1, (self.size,), (self.size-1,))
				if event.key == pygame.K_DOWN:
					self.move_input(0, -1, (self.size,), (self.size-1, 0, -1))
				if event.key == pygame.K_LEFT:
					self.move_input(1, 0, (self.size-1,), (self.size,))
				if event.key == pygame.K_RIGHT:
					self.move_input(-1, 0, (self.size-1, 0, -1), (self.size,))


	def draw(self, surface):
		for coor in self.plate_coor:
			self.rect.topleft = coor
			self.plate_coor_center.append(self.rect.center)
			surface.blit(self.image,self.rect)
		
		coor_index = 0
		for y in self.game_board:
			for x in y:
				self.rect.topleft = self.plate_coor[coor_index]
				self.plate_coor_center.append(self.rect.center)
				try:
					self.image.fill(self.colors[x])
				except:
					self.image.fill(self.colors[262144])
				surface.blit(self.image,self.rect)

				text = self.font.render(str(x if x != 0 else ""), True, 'white')
				text_rect = text.get_rect(center = self.plate_coor_center[coor_index])
				surface.blit(text, text_rect)
				coor_index += 1

		if self.is_board_full():
			if self.game_over():
				text_bg = pygame.Surface((self.text_size * 5, self.text_size * 1.5))
				text_bg.fill('#a11d33')
				text_bg_rect = text_bg.get_rect(center = (self.screen_size[0]/2, self.screen_size[1]/2))
				surface.blit(text_bg,text_bg_rect)

				text = self.font.render("Game Over", True, 'white')
				text_rect = text.get_rect(center = (self.screen_size[0]/2, self.screen_size[1]/2))
				surface.blit(text,text_rect)

	def move_input(self, ax, ay, x_range, y_range):
		move = False
		mergable_board = [[1 for x in range(self.size)] for y in range(self.size)]
		for _ in range(self.size-1):
			for y in range(*y_range):
				for x in range(*x_range):
					if self.game_board[y][x] == 0 and self.game_board[y+ay][x+ax] != 0:
						self.game_board[y][x] = self.game_board[y+ay][x+ax]
						self.game_board[y+ay][x+ax] = 0
						move = True
					if (self.game_board[y][x] != 0 and self.game_board[y][x] == self.game_board[y+ay][x+ax]) and (mergable_board[y][x] == 1 and mergable_board[y+ay][x+ax] == 1):
						self.game_board[y][x] *= 2
						self.game_board[y+ay][x+ax] = 0
						mergable_board[y][x] = 0
						move = True
		if move: self.place_two()


	def place_two(self):
		if not self.is_board_full():
			while True:
				y = random.randint(0,self.size-1)
				x = random.randint(0,self.size-1)
				if self.game_board[y][x] == 0:
					self.game_board[y][x] = 2
					break

	def calc_plate_coor(self):
		coors = []
		for y in range(self.size):
			for x in range(self.size):
				coor_x = self.gap_size + x * (self.gap_size + self.plate_size)
				coor_y = self.gap_size + y * (self.gap_size + self.plate_size)
				coors.append((coor_x,coor_y))
		return coors

	def is_board_full(self):
		for y in self.game_board:
			for x in y:
				if x == 0:
					return False
		return True

	def game_over(self):
		if self.is_board_full():
			for y in range(self.size):
				for x in range(self.size):
					try:
						if self.game_board[y][x] == self.game_board[y+1][x]:
							return False
						if self.game_board[y][x] == self.game_board[y][x+1]:
								return False
					except:
						try:
							if self.game_board[y][x] == self.game_board[y][x+1]:
								return False
						except:
							continue
			return True
		return False
