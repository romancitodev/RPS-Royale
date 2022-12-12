import sys
import pygame

from config import *
from entity import Entity, EntityType


def handle_event(event: pygame.event.Event):
    match event.type:
        case pygame.QUIT:
            sys.exit(1)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    entities_sprites: pygame.sprite.Group = pygame.sprite.Group()

    for _ in range(3):
        for __ in range(MAX_ENTITY_SPAWN):
            if _ == 0:
                rock = Entity(EntityType.ROCK, ROCK_IMG, ROCK_SOUND)
                entities_sprites.add(rock)
            elif _ == 1:
                paper = Entity(EntityType.PAPER, PAPER_IMG, PAPER_SOUND)
                entities_sprites.add(paper)
            elif _ == 2:
                scissors = Entity( EntityType.SCISSORS, SCISSORS_IMG, SCISSORS_SOUND)
                entities_sprites.add(scissors)

    while True:
        screen.fill(WHITE_BG)
        entities_sprites.draw(screen)

        for entity in entities_sprites:
            rock_list = [e for e in entities_sprites if e.type == EntityType.ROCK.value] #type: ignore
            paper_list = [e for e in entities_sprites if e.type == EntityType.PAPER.value] #type: ignore
            scissors_list = [e for e in entities_sprites if e.type == EntityType.SCISSORS.value] #type: ignore
            if all(x.type == EntityType.ROCK.value for x in entities_sprites) or all(x.type == EntityType.PAPER.value for x in entities_sprites) or all(x.type == EntityType.SCISSORS.value for x in entities_sprites): #type: ignore
                break
            if entity.type == EntityType.ROCK.value: #type: ignore
                entity.update(scissors_list) #type: ignore
            elif entity.type == EntityType.PAPER.value: #type: ignore
                entity.update(rock_list)
            elif entity.type == EntityType.SCISSORS.value: #type: ignore
                entity.update(paper_list)
        pygame.display.set_caption(f"FPS: {clock.get_fps()//1}")
        pygame.display.update()
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            handle_event(event)

        # for entity in entities:
        #     if target:=pygame.sprite.spritecollideany(entity, entities_sprites):
