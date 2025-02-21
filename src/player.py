import pygame
from .bullet import Bullet
import time

class Player:
    def __init__(self):
        self.size = 25
        self.radius = self.size // 2
        self.x = 400 - self.radius
        self.y = 300 - self.radius
        self.speed = 5
        # 그라데이션을 위한 색상
        self.colors = {
            'main': (41, 128, 185),  # 밝은 파랑
            'core': (52, 152, 219),  # 더 밝은 파랑
            'outline': (25, 181, 254)  # 하이라이트 색상
        }
        self.bullets = []
        self.last_shot_time = 0
        self.shot_cooldown = 0.5

    def draw_player(self, screen):
        # 플레이어의 외부 원
        pygame.draw.circle(screen, self.colors['main'], (int(self.x), int(self.y)), self.radius)
        
        # 플레이어의 내부 원 (코어)
        inner_radius = int(self.radius * 0.7)
        pygame.draw.circle(screen, self.colors['core'], (int(self.x), int(self.y)), inner_radius)
        
        # 하이라이트 효과 (왼쪽 상단에 작은 원)
        highlight_pos = (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3))
        pygame.draw.circle(screen, self.colors['outline'], highlight_pos, int(self.radius * 0.2))

    def update(self, screen):
        keys = pygame.key.get_pressed()
        
        # 이동 처리
        if keys[pygame.K_LEFT] and self.x > self.radius:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen.get_width() - self.radius:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > self.radius:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < screen.get_height() - self.radius:
            self.y += self.speed

        # 총알 발사
        current_time = time.time()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            if keys[pygame.K_w]:
                self.bullets.append(Bullet(self.x - self.radius, self.y - self.radius, 'up', self.speed))
                self.last_shot_time = current_time
            elif keys[pygame.K_s]:
                self.bullets.append(Bullet(self.x - self.radius, self.y - self.radius, 'down', self.speed))
                self.last_shot_time = current_time
            elif keys[pygame.K_a]:
                self.bullets.append(Bullet(self.x - self.radius, self.y - self.radius, 'left', self.speed))
                self.last_shot_time = current_time
            elif keys[pygame.K_d]:
                self.bullets.append(Bullet(self.x - self.radius, self.y - self.radius, 'right', self.speed))
                self.last_shot_time = current_time

        # 총알 업데이트
        for bullet in self.bullets[:]:
            if not bullet.update(screen.get_width(), screen.get_height()):
                self.bullets.remove(bullet)
            else:
                bullet.draw(screen)

        # 플레이어 그리기
        self.draw_player(screen)
