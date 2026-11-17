"""
Creature Simulation - Part 1 (Worksheet 5.5)
IB Computer Science HL - Theme B3.1 / B3.2 (OOP)
Name: TODO (your name)

Goal: build ONE parent class (Creature) and AT LEAST TWO child classes
(CreatureTypeA, CreatureTypeB) that behave differently.

This file runs as it is: you will see a black window. Close it to quit.
Each time you finish a TODO, run the file again and watch your creatures appear.

Read part1/README.md for the full instructions and explanations.
"""

import os
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creature Simulation - Part 1")


# =====================================================================
# --- Task A: the parent class ---
# =====================================================================
class Creature:
    def __init__(self, x, y, speed):
        # TODO (Task A): store the attributes on the object.
        #   Every creature needs at least a position (x, y) and a speed.
        #   Hint: an attribute is stored with  self.<name> = <value>
        #   Also think about: colour (an RGB tuple such as (255, 0, 0)),
        #   size / radius, direction ... anything ALL creatures share.
        pass

    def move(self):
        # TODO (Task A): base movement, OR leave empty so that each
        #   child class overrides it with its own movement.
        #   Hint: moving right means changing self.x by self.speed.
        pass

    def draw(self, screen):
        # TODO (Task A): draw a basic shape for the creature.
        #   Hint: pygame.draw.circle(surface, colour, (x, y), radius)
        #         e.g. pygame.draw.circle(screen, (255, 255, 255), (100, 100), 20)
        #   Positions must be whole numbers -> int(self.x) may help.
        pass


# =====================================================================
# --- Task B: two child classes ---
# Each one must: inherit from Creature, override at least one method,
# and introduce new behaviour so the two types are meaningfully different.
# =====================================================================
class CreatureTypeA(Creature):
    # TODO (Task B): override move() and/or draw()
    #   Ideas: move in a zig-zag, wander randomly (random.randint),
    #   bounce off the edges of the window (WIDTH, HEIGHT) ...
    #   Optional: write your own __init__ and call super().__init__(x, y, speed)
    #   to add extra attributes that only this type has.
    pass


class CreatureTypeB(Creature):
    # TODO (Task B): override move() and/or draw()
    #   Make it clearly different from CreatureTypeA
    #   (different movement, shape, colour, size ...).
    #   Hint for a square: pygame.draw.rect(screen, colour, (x, y, width, height))
    pass


# =====================================================================
# --- Task C: polymorphism ---
# One list holding DIFFERENT kinds of creature. The loop below calls
# c.move() and c.draw(screen) without knowing which type c is -
# each object answers in its own way.
# TODO (Task C): add more creatures (of both types) to this list.
# =====================================================================
creatures = [CreatureTypeA(100, 200, 3), CreatureTypeB(400, 300, 2)]

clock = pygame.time.Clock()

# (Teacher tool: lets the file be tested automatically. You can ignore it.)
MAX_FRAMES = int(os.environ.get("CREATURE_SIM_MAX_FRAMES", "0"))
frame = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # clear the screen to black every frame

    for c in creatures:
        c.move()
        c.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # at most 60 frames per second

    frame += 1
    if MAX_FRAMES and frame >= MAX_FRAMES:
        running = False

pygame.quit()
