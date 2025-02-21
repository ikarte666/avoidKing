import pygame
import math

class Bullet:
    def __init__(self, x, y, direction, player_speed):
        self.size = 25
        self.radius = self.size // 2
        self.x = x + self.radius
        self.y = y + self.radius
        self.direction = direction
        self.speed = player_speed * 3
        self.birth_time = pygame.time.get_ticks()
        self.colors = {
            'core': (255, 255, 255),  # 흰색 중심
            'main': (255, 223, 0),    # 금색
            'trail': (255, 140, 0)    # 주황색 꼬리
        }

    def update(self, screen_width, screen_height):
        if self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed

        if (self.x < 0 or self.x > screen_width or 
            self.y < 0 or self.y > screen_height):
            return False
        return True

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        
        if self.direction == 'up':
            trail_x, trail_y = self.x, self.y + self.radius
        elif self.direction == 'down':
            trail_x, trail_y = self.x, self.y - self.radius
        elif self.direction == 'left':
            trail_x, trail_y = self.x + self.radius, self.y
        else:
            trail_x, trail_y = self.x - self.radius, self.y

        for i in range(3):
            trail_alpha = 150 - (i * 40)
            trail_radius = self.radius - (i * 2)
            trail_surface = pygame.Surface((trail_radius * 2, trail_radius * 2), pygame.SRCALPHA)
            trail_color = (*self.colors['trail'], trail_alpha)
            pygame.draw.circle(trail_surface, trail_color, (trail_radius, trail_radius), trail_radius)
            screen.blit(trail_surface, (trail_x - trail_radius, trail_y - trail_radius))

        pygame.draw.circle(screen, self.colors['main'], (int(self.x), int(self.y)), self.radius)
        
        core_radius = int(self.radius * 0.5)
        pygame.draw.circle(screen, self.colors['core'], (int(self.x), int(self.y)), core_radius)
        
        glow_size = math.sin(current_time / 100) * 2
        glow_radius = int(self.radius + glow_size)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        glow_color = (*self.colors['main'], 50)
        pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surface, (self.x - glow_radius, self.y - glow_radius))

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.size, self.size)