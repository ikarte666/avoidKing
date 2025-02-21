import pygame
import sys
from src.game import Game

# 창 이름 설정
pygame.display.set_caption("AVOID KING")

# 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((800, 600))

# 게임 객체 생성
game = Game(screen)

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 게임 업데이트
    game.update()

    # 화면 업데이트
    pygame.display.flip()