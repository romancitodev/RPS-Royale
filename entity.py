import enum
import os
import random
import pygame

#from pygame import mixer
from typing_extensions import Self

from config import *


class EntityType(enum.Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_type: EntityType, image_path:str) -> None:
        super(Entity, self).__init__()
        self.type = entity_type.value
        self.image = self.load_image(image_path, 0.25)
        self.rect = pygame.rect.Rect(random.randint(0, SIZE[0]), random.randint(0, SIZE[1]), 30, 30)

    def update(self, entities: list[Self], allies: list[Self]): #type: ignore
        '''
        if entitites exists, means an enemy exists and the entity go to the enemy location, otherwise move random
        '''
        if entities:
            enemy = self.detect_closest_enemy(entities)
            diff_x = enemy.rect.x - self.rect.x #type: ignore
            diff_y = enemy.rect.y - self.rect.y #type: ignore   
            self.rect.x += int(diff_x * random.random()) * 0.009 #type: ignore
            self.rect.y += int(diff_y * random.random()) * 0.009 #type: ignore
            if self.rect.colliderect(enemy.rect): #type: ignore
                self.convert_entity(enemy)
        else:
            self.rect.x += int(random.randint(-MAX_ENTITY_SPEED, MAX_ENTITY_SPEED)) #type: ignore
            self.rect.y += int(random.randint(-MAX_ENTITY_SPEED, MAX_ENTITY_SPEED)) #type: ignore
        self.check_location()

    def check_location(self):
        if self.rect:
            if self.rect.x > (SIZE[0] - 50) or self.rect.x < 0:
                self.rect.x = 0 if self.rect.x < 0 else (SIZE[0] - 50)
            if self.rect.y > (SIZE[1] - 50) or self.rect.y < 0:
                self.rect.y = 0 if self.rect.y < 0 else (SIZE[1] - 50)

    def detect_closest_enemy(self, entities: list[Self]) -> Self:
        pos = pygame.math.Vector2(self.rect.x, self.rect.y) #type: ignore
        return min([e for e in entities], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.x, e.rect.y))) #type: ignore

    def load_image(self, path:str, scale:float = 1):
        fullname = os.path.abspath(path)
        image = pygame.image.load(fullname)

        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pygame.transform.scale(image, size)

        return image

    def change_type(self, e_type: EntityType, image_path: str):
        self.type = e_type.value
        self.image = self.load_image(image_path, 0.25)
        self.rect = pygame.rect.Rect(self.rect.x, self.rect.y, 80, 80) #type: ignore

    def convert_entity(self, target: Self):
        # os.system(f'start {os.getcwd()}/{self.sound}')
        #self.sound.play()
        match self.type:
            case EntityType.ROCK.value:
                target.change_type(EntityType.ROCK, ROCK_IMG)
            case EntityType.PAPER.value:
                target.change_type(EntityType.PAPER, PAPER_IMG)
            case EntityType.SCISSORS.value:
                target.change_type(EntityType.SCISSORS, SCISSORS_IMG)
            case _: pass