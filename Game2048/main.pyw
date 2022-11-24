import pygame
import game2048

def main():
	pygame.init()

	#Setup Your Own Size Here

	grid_size = 4
	WIDTH = 600
	HEIGHT = 600

	#display set-up
	pygame.display.set_caption("2048")
	bg_color = '#393e46'
	screen = pygame.display.set_mode((WIDTH,HEIGHT))
	screen.fill(bg_color)
	clock = pygame.time.Clock()


	game = pygame.sprite.GroupSingle(game2048.Game2048(grid_size, (WIDTH,HEIGHT)))

	while True:
		screen.fill(bg_color)
		game.update()
		game.sprite.draw(screen)

		pygame.display.update()
		clock.tick(60)

if __name__ == "__main__":
	main()