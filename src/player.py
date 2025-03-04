import pygame
import math
from .bullet import Bullet
import time

class Player:
    def __init__(self):
        self.size = 30  # 25에서 30으로 변경 (1.2배)
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
        self.animation_offset = 0

    def draw_player(self, screen):
        # 별의 중심점
        center = (int(self.x), int(self.y))
        points = []
        
        # 5개의 점을 가진 별 모양 생성
        outer_radius = self.radius  # 외부 점 반지름
        inner_radius = self.radius * 0.5  # 내부 점 반지름 (0.4에서 0.5로 조정)
        
        for i in range(5):
            # 외부 점
            angle = math.pi * 2 * i / 5 - math.pi / 2
            outer_x = center[0] + outer_radius * math.cos(angle)
            outer_y = center[1] + outer_radius * math.sin(angle)
            points.append((outer_x, outer_y))
            
            # 내부 점
            inner_angle = angle + math.pi / 5
            inner_x = center[0] + inner_radius * math.cos(inner_angle)
            inner_y = center[1] + inner_radius * math.sin(inner_angle)
            points.append((inner_x, inner_y))

        # 별 그리기
        pygame.draw.polygon(screen, self.colors['main'], points)
        
        self.animation_offset += 0.1
        if self.animation_offset > 2 * math.pi:
            self.animation_offset = 0
        animation_scale = 1 + 0.1 * math.sin(self.animation_offset)
        scaled_radius = int(self.radius * animation_scale)

        # 중심 원 (크기 조정)
        pygame.draw.circle(screen, self.colors['core'], center, int(scaled_radius * 0.35))
        
        # 하이라이트 효과 (위치 조정)
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