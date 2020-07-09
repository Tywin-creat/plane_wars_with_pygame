import pygame
import random
from os import path

WIDTH, HEIGHT = 480, 600
WHITE = (255, 255, 255) # 用全部大写表示常量 RGB
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREE = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.flip(player_img, False, True)
		self.image = pygame.transform.scale(self.image, (53, 40))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect() # 获取精灵的位置信息
		self.rect.centerx = WIDTH/2		# 初始状态的飞船位置
		self.rect.bottom = HEIGHT
		self.radius = 20


	def update(self):
		key_state = pygame.key.get_pressed()
		if key_state[pygame.K_LEFT]:
			self.rect.x -= 5
		if key_state[pygame.K_RIGHT]:
			self.rect.x += 5
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.centery)
		bullets.add(bullet)		


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_img
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.last_time = pygame.time.get_ticks()

		self.radius = 35
		#pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)
		self.rect.x = random.randint(0, WIDTH - self.rect.w) # self.rect.w 敌人精灵的宽度

		self.vx = random.randint(-2, 2)
		self.vy = random.randint(2, 10)

	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.image = pygame.transform.scale(self.image, (5, 10))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y

	def update(self):
		self.rect.y -= 10


class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(explosion_animation[0], (80,80))
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_time = pygame.time.get_ticks()

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_time > 30:
			if self.frame<len(explosion_animation):
				self.image = pygame.transform.scale(explosion_animation[self.frame], (80,80))
				self.image.set_colorkey((0,0,0))
				self.frame += 1
				self.last_time = now
			else:
				self.kill()



clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # set_mode函数就一个参数，是一个元组
pygame.display.set_caption('My Game')

img_dir = path.join(path.dirname(__file__), 'img')
background_dir = path.join(img_dir, 'background.png')
background_img = pygame.image.load(background_dir).convert()
background_rect = background_img.get_rect()

player_dir = path.join(img_dir, 'spaceShips_008.png')
player_img = pygame.image.load(player_dir).convert()
enemy_dir = path.join(img_dir, 'spaceMeteors_001.png')
enemy_img = pygame.image.load(enemy_dir).convert()
bullet_dir = path.join(img_dir, 'spaceMissiles_010.png')
bullet_img = pygame.image.load(bullet_dir).convert()

explosion_animation = []
for i in range(9):
	explosion_dir = path.join(img_dir, 'regularExplosion0{}.png'.format(i))
	explosion_img = pygame.image.load(explosion_dir).convert()
	explosion_animation.append(explosion_img)

player = Player()
enemys = pygame.sprite.Group()
for i in range(10):
	enemy = Enemy()
	enemys.add(enemy)
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()

game_over = False
arrow_key_status = [0, 0]

last = pygame.time.get_ticks()
while not game_over:
	clock.tick(60)
	event_list = pygame.event.get()
	for event in event_list:
		if event.type == pygame.QUIT:
			game_over = True	
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				game_over = True

			elif event.key == pygame.K_SPACE:
				player.shoot()

	now1 = pygame.time.get_ticks()
	if now1 - last > 1200:
		for i in range(5):
			enemy = Enemy()
			enemys.add(enemy)
		last = now1

	screen.fill(WHITE) # 系统的双缓冲机制
	screen.blit(background_img,background_rect)

	player.update()
	enemys.update()
	explosions.update()
	pygame.sprite.spritecollide(player, enemys, False, pygame.sprite.collide_circle)
	hits = pygame.sprite.groupcollide(enemys, bullets, True, True)
	for hit in hits:
		explosion = Explosion(hit.rect.center)
		explosions.add(explosion)

	bullets.update()

	screen.blit(player.image, player.rect)      
	enemys.draw(screen)
	bullets.draw(screen)
	explosions.draw(screen)

	pygame.display.flip() #这句话一般放在最后

