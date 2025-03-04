import pygame
import sys
from .player import Player
from .enemy import Enemy
import time
import json
import os
import math

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0
        self.start_time = time.time()
        self.game_over = False
        self.end_time = None  # 게임 오버 시점의 시간을 저장
        self.score = 0  # 점수 초기화
        self.start_screen = True  # 시작 화면 플래그 추가
        
        # UI 폰트 초기화
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 74)
        self.high_score = self.load_high_score()  # 하이스코어 로드

        # 색상 정의
        self.COLORS = {
            'background': (240, 240, 245),  # 연한 청회색
            'grid': (230, 230, 235),  # 더 연한 청회색
            'ui_text': (60, 60, 80),  # 진한 남색
            'score': (46, 204, 113),  # 에메랄드 그린
            'high_score': (142, 68, 173),  # 세련된 보라색
            'enemy_count': (231, 76, 60),  # 선명한 빨강
            'game_over_overlay': (0, 0, 0, 180),  # 진한 반투명 검정
            'game_over_text': (231, 76, 60),  # 선명한 빨강
            'new_record': (241, 196, 15),  # 골드
        }

        # pygame.mixer.init()
        # pygame.mixer.music.load('bgm.mp4')  # 배경 음악 파일 경로
        # pygame.mixer.music.play(-1)  # 무한 반복 재생

        # 난이도 관련 변수 수정
        self.spawn_interval = 3.0  # 초기 적 생성 간격 (3초)
        self.spawn_count = 3  # 초기 적 생성 수 (3마리로 시작)
        self.enemy_speed = self.player.speed * 0.5  # 초기 적 속도 (플레이어 속도의 50%)
        self.last_spawn_time = time.time()
        self.last_difficulty_update = time.time()  # 마지막 난이도 업데이트 시간
        self.last_spawn_count_update = time.time()  # 적 생성 수 업데이트 타이머
        self.difficulty_level = 0  # 난이도 레벨 추적

    def update(self):
        if self.start_screen:
            self.draw_start_screen()
        elif not self.game_over:
            self.screen.fill(self.COLORS['background'])
            self.draw_grid()  # 배경 그리드 추가
            self.player.update(self.screen)
            self.spawn_enemies()
            self.update_enemies()
            self.check_collisions()
            self.check_bullet_collisions()  # 총알 충돌 검사 추가
            self.draw_ui()
            self.update_difficulty()  # 난이도 조절
        else:
            self.draw_game_over()

    def draw_grid(self):
        # 그리드 크기
        grid_size = 40
        
        # 수직선
        for x in range(0, self.screen.get_width(), grid_size):
            pygame.draw.line(self.screen, self.COLORS['grid'], (x, 0), (x, self.screen.get_height()))
        
        # 수평선
        for y in range(0, self.screen.get_height(), grid_size):
            pygame.draw.line(self.screen, self.COLORS['grid'], (0, y), (self.screen.get_width(), y))

    def spawn_enemies(self):
        current_time = time.time()
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.last_spawn_time = current_time
            for _ in range(self.spawn_count):
                enemy = Enemy(self.screen.get_width(), self.screen.get_height(), self.enemy_speed)
                self.enemies.append(enemy)

    def update_difficulty(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # 8초마다 난이도 업데이트
        if current_time - self.last_difficulty_update >= 8:
            self.last_difficulty_update = current_time
            self.difficulty_level += 1
            
            # 적 생성 간격 감소 (최소 1초)
            if self.spawn_interval > 1.0:
                self.spawn_interval = max(1.0, 3.0 - (self.difficulty_level * 0.2))
            
            # 적 속도 증가 (최대 플레이어 속도)
            if self.enemy_speed < self.player.speed:
                self.enemy_speed = min(self.player.speed, 
                                     self.player.speed * (0.5 + self.difficulty_level * 0.1))
        
        # 10초마다 적 생성 수 증가 (최대 10마리)
        if current_time - self.last_spawn_count_update >= 10:
            self.last_spawn_count_update = current_time
            if self.spawn_count < 10:
                self.spawn_count += 1

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y, self.enemies)  # 다른 적들의 목록을 전달
            enemy.draw(self.screen)

    def check_collisions(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, 25, 25)  # 크기를 25로 수정
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, 25, 25)  # 크기를 25로 수정
            if player_rect.colliderect(enemy_rect):
                self.game_over = True
                self.end_time = time.time()  # 게임 오버 시점 저장
                return

    def check_bullet_collisions(self):
        # 모든 총알에 대해 충돌 검사
        for bullet in self.player.bullets[:]:  # 리스트 복사본으로 순회
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies[:]:  # 리스트 복사본으로 순회
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
                if bullet_rect.colliderect(enemy_rect):
                    self.enemies.remove(enemy)  # 적 제거
                    self.player.bullets.remove(bullet)  # 총알 제거
                    self.score += 1  # 점수 증가
                    break

    def draw_ui(self):
        # UI 배경 패널
        panel_height = 160
        panel_surface = pygame.Surface((200, panel_height))
        panel_surface.fill(self.COLORS['background'])
        panel_surface.set_alpha(230)
        self.screen.blit(panel_surface, (10, 10))

        # 생존 시간 표시 (게임 오버가 아닐 때만 시간 증가)
        if not self.game_over:
            survival_time = int(time.time() - self.start_time)
        else:
            survival_time = int(self.end_time - self.start_time)
            
        time_text = self.font.render(f'Time: {survival_time}s', True, self.COLORS['ui_text'])
        self.screen.blit(time_text, (20, 20))

        # 적 수 표시
        enemy_count = len(self.enemies)
        enemy_text = self.font.render(f'Enemies: {enemy_count}', True, self.COLORS['enemy_count'])
        self.screen.blit(enemy_text, (20, 60))

        # 스코어 표시 추가
        score_text = self.font.render(f'Score: {self.score}', True, self.COLORS['score'])  # 초록색으로 표시
        self.screen.blit(score_text, (20, 100))

        # 하이스코어 표시
        high_score_text = self.font.render(f'High: {self.high_score}', True, self.COLORS['high_score'])  # 보라색으로 표시
        self.screen.blit(high_score_text, (20, 140))

    def draw_game_over(self):
        # 배경 유지
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # 게임오버 패널
        panel_width = 400
        panel_height = 300
        panel_x = (self.screen.get_width() - panel_width) // 2
        panel_y = (self.screen.get_height() - panel_height) // 2
        
        # 패널 배경
        panel = pygame.Surface((panel_width, panel_height))
        panel.fill(self.COLORS['background'])
        self.screen.blit(panel, (panel_x, panel_y))

        # 게임 오버 텍스트
        game_over_text = self.large_font.render('GAME OVER', True, self.COLORS['game_over_text'])
        text_rect = game_over_text.get_rect(center=(self.screen.get_width()/2, panel_y + 50))
        self.screen.blit(game_over_text, text_rect)

        # 최종 생존 시간
        survival_time = int(self.end_time - self.start_time)
        time_text = self.font.render(f'Survival Time: {survival_time}s', True, self.COLORS['ui_text'])
        time_rect = time_text.get_rect(center=(self.screen.get_width()/2, panel_y + 120))
        self.screen.blit(time_text, time_rect)

        # 최종 점수 표시 추가
        score_text = self.font.render(f'Final Score: {self.score}', True, self.COLORS['ui_text'])
        score_rect = score_text.get_rect(center=(self.screen.get_width()/2, panel_y + 160))
        self.screen.blit(score_text, score_rect)

        # 최종 점수가 하이스코어를 넘었는지 확인
        if self.score > self.high_score:
            new_record_text = self.font.render('New High Score!', True, self.COLORS['new_record'])  # 금색으로 표시
            new_record_rect = new_record_text.get_rect(center=(self.screen.get_width()/2, panel_y + 200))
            self.screen.blit(new_record_text, new_record_rect)
            # 하이스코어 저장
            self.save_high_score()

        # 재시작 안내 (위치 조정)
        restart_text = self.font.render('Press SPACE to restart', True, self.COLORS['ui_text'])
        restart_rect = restart_text.get_rect(center=(self.screen.get_width()/2, panel_y + 240))
        self.screen.blit(restart_text, restart_rect)

    def draw_start_screen(self):
        self.screen.fill(self.COLORS['background'])
        title_text = self.large_font.render('AVOID KING', True, self.COLORS['ui_text'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 50))
        self.screen.blit(title_text, title_rect)

        start_text = self.font.render('Press SPACE to Start', True, self.COLORS['ui_text'])
        start_rect = start_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 50))
        self.screen.blit(start_text, start_rect)

    def restart(self):
        self.enemies = []
        self.spawn_timer = 0
        self.start_time = time.time()
        self.game_over = False
        self.end_time = None
        self.player = Player()
        self.score = 0  # 점수 초기화
        self.start_screen = False  # 게임 시작 시 시작 화면 플래그 해제
        self.spawn_interval = 3.0  # 초기화
        self.spawn_count = 3  # 3마리로 초기화
        self.enemy_speed = self.player.speed * 0.5  # 플레이어 속도의 50%로 초기화
        self.last_spawn_time = time.time()
        self.last_difficulty_update = time.time()
        self.last_spawn_count_update = time.time()
        self.difficulty_level = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.start_screen:
                    self.start_screen = False
                elif self.game_over:
                    self.restart()

    def load_high_score(self):
        try:
            if os.path.exists('highscore.json'):
                with open('highscore.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            return 0
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open('highscore.json', 'w') as f:
                    json.dump({'high_score': self.high_score}, f)
            except:
                pass  # 파일 저장 실패시 무시
