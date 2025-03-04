import pygame
import random
import math

class Enemy:
    def __init__(self, screen_width, screen_height, speed):
        self.size = 25
        self.radius = self.size // 2
        self.x, self.y = self.random_position(screen_width, screen_height)
        self.speed = speed  # 속도를 초기화
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.base_color = self.random_color()
        # 각 적마다 고유한 진동 타이밍을 가지도록
        self.pulse_offset = random.random() * math.pi * 2
        self.birth_time = pygame.time.get_ticks()
        self.animation_offset = random.random() * math.pi * 2

    def random_color(self):
        # 더 세련된 색상 팔레트
        colors = [
            (231, 76, 60),   # 빨강
            (230, 126, 34),  # 주황
            (241, 196, 15),  # 노랑
            (46, 204, 113),  # 초록
            (52, 152, 219),  # 파랑
            (155, 89, 182)   # 보라
        ]
        return random.choice(colors)

    def random_position(self, screen_width, screen_height):
        # 화면 테두리에서 랜덤하게 생성
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            return random.randint(0, screen_width - self.size), -self.size
        elif side == 'bottom':
            return random.randint(0, screen_width - self.size), screen_height
        elif side == 'left':
            return -self.size, random.randint(0, screen_height - self.size)
        else:  # right
            return screen_width, random.randint(0, screen_height - self.size)

    def check_collision(self, other_enemy):
        # 두 적 사이의 거리 계산
        dx = self.x - other_enemy.x
        dy = self.y - other_enemy.y
        distance = math.sqrt(dx * dx + dy * dy)
            
        # 충돌 발생 (두 적의 크기 합보다 거리가 작을 때)
        if distance < self.size:
            # 겹침을 방지하기 위해 서로를 밀어냄
            if distance > 0:
                # 방향 벡터 정규화
                dx = dx / distance
                dy = dy / distance
                
                # 겹친 정도의 절반만큼 각각 밀어냄
                push = (self.size - distance) / 2
                self.x += dx * push
                self.y += dy * push
                other_enemy.x -= dx * push
                other_enemy.y -= dy * push

    def update(self, player_x, player_y, other_enemies=None):
        # 플레이어 방향으로 이동
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance != 0:
            # 정규화된 방향 벡터 계산
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
            self.x += dx
            self.y += dy

        # 다른 적들과의 충돌 검사
        if other_enemies:
            for other in other_enemies:
                if other != self:  # 자기 자신과는 충돌 검사 하지 않음
                    self.check_collision(other)

    def get_pulse_color(self):
        # 시간에 따라 밝기가 변하는 효과
        current_time = pygame.time.get_ticks()
        pulse = math.sin((current_time / 500) + self.pulse_offset) * 0.2 + 0.8
        return tuple(int(c * pulse) for c in self.base_color)

    def draw(self, screen):
        # 메인 사각형
        color = self.get_pulse_color()
        self.animation_offset += 0.1
        if self.animation_offset > 2 * math.pi:
            self.animation_offset = 0
        animation_scale = 1 + 0.1 * math.sin(self.animation_offset)
        scaled_size = int(self.size * animation_scale)
        rect = pygame.Rect(int(self.x - scaled_size / 2), int(self.y - scaled_size / 2), scaled_size, scaled_size)
        pygame.draw.rect(screen, color, rect)
        
        # 내부 사각형 (코어)
        inner_size = int(self.size * 0.6)
        inner_offset = (self.size - inner_size) // 2
        inner_rect = pygame.Rect(int(self.x - self.radius + inner_offset), 
                               int(self.y - self.radius + inner_offset), 
                               inner_size, inner_size)
        inner_color = tuple(min(255, int(c * 1.3)) for c in color)
        pygame.draw.rect(screen, inner_color, inner_rect)
        
        # 외곽선 효과
        glow_size = int(self.size * 1.2)
        glow_offset = (glow_size - self.size) // 2
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_color = (*color[:3], 100)
        glow_rect = pygame.Rect(0, 0, glow_size, glow_size)
        pygame.draw.rect(glow_surface, glow_color, glow_rect)
        screen.blit(glow_surface, 
                   (int(self.x - self.radius - glow_offset), 
                    int(self.y - self.radius - glow_offset)))