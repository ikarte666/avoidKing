import pygame
import sys
from src.game import Game

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 창 이름 설정
pygame.display.set_caption("AVOID KING")

# 게임 객체 생성
game = Game(screen)

# 게임 루프
clock = pygame.time.Clock()  # FPS 제어를 위한 Clock 객체 생성
font = pygame.font.Font(None, 24)  # FPS 표시용 폰트

while True:
    # FPS 설정
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game.game_over:
                game.restart()

    # 게임 업데이트
    game.update()

    # FPS 표시
    fps = font.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
    screen.blit(fps, (SCREEN_WIDTH - 100, 10))

    # 화면 업데이트
    pygame.display.flip()