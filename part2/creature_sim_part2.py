"""
Creature Simulation - Part 2 (Worksheet 7.5): Extension
IB Computer Science HL - B3.2.2 Polymorphism, B3.2.3 Abstraction,
                         B3.2.5 Design Patterns (Factory, Singleton, Observer)
Name: TODO (your name)

How to start: copy your finished Part 1 creature code (attributes,
move() and draw() of CreatureTypeA / CreatureTypeB) into the marked
places below. Then do as many of Tasks 1-6 as you like - they are
independent. Read part2/README.md for explanations.

This file runs as it is: you will see a black window. Close it to quit.

Why does it run before you write anything?
    In Task 2 the parent's move() and draw() raise NotImplementedError.
    If a child class did NOT override them, the main loop would crash
    on the first frame. So every placeholder child class below already
    contains stub move()/draw() methods that do nothing (`pass`).
    Replace each stub with real behaviour - but do not delete the
    method, or you will see the NotImplementedError (that is the point!).
"""

import os
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creature Simulation - Part 2")


# =====================================================================
# --- Part 2 Task 4: Singleton (GameSettings) ---
# The whole program should share ONE GameSettings object. Everyone asks
# for it with GameSettings.get() instead of calling GameSettings()
# directly. (That is an agreement: GameSettings() would still create a
# separate second object - see part2/README.md.)
# =====================================================================
class GameSettings:
    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = GameSettings()
        return cls._instance

    def __init__(self):
        self.background_colour = (0, 0, 0)
        # TODO (Task 4): add at least one more adjustable setting, and
        #   USE it somewhere in the program. Ideas:
        #   frames per second, number of creatures to spawn,
        #   a speed multiplier, a default creature size ...


# =====================================================================
# --- Part 2 Task 2: Abstraction ---
# The parent no longer says HOW a creature moves or is drawn. It only
# says THAT every creature must be able to move() and draw().
# =====================================================================
class Creature:
    def __init__(self, x, y, speed):
        # TODO: paste your attributes from Part 1 here (self.x = x, ...)
        pass

    def move(self):
        raise NotImplementedError("Subclasses must implement move()")

    def draw(self, screen):
        raise NotImplementedError("Subclasses must implement draw()")

    # TODO (Task 2): write a short comment here (2-4 lines) explaining
    #   how this parent class now acts as an ABSTRACT INTERFACE.
    #   Think: what does it promise? what does it leave to the subclasses?
    #   What happens if a subclass forgets to implement move()?


# =====================================================================
# Your Part 1 subclasses
# =====================================================================
class CreatureTypeA(Creature):
    # TODO: paste your Part 1 CreatureTypeA code here.

    def move(self):
        # TODO: replace this stub with your Part 1 movement
        pass

    def draw(self, screen):
        # TODO: replace this stub with your Part 1 drawing
        pass


class CreatureTypeB(Creature):
    # TODO: paste your Part 1 CreatureTypeB code here.

    def move(self):
        # TODO: replace this stub with your Part 1 movement
        pass

    def draw(self, screen):
        # TODO: replace this stub with your Part 1 drawing
        pass


# =====================================================================
# --- Part 2 Task 1: Strengthen polymorphism ---
# Add at least one NEW subclass. Ideas:
#   - follows the mouse slowly     (pygame.mouse.get_pos())
#   - bounces off the walls        (compare x / y with WIDTH / HEIGHT)
#   - changes colour while moving
#   - teleports to a random place  (random.randint)
# Rename the class to something meaningful if you like (and update the
# factory below).
# =====================================================================
class CreatureTypeC(Creature):
    # TODO (Task 1): give this creature its own behaviour.

    def move(self):
        # TODO (Task 1)
        pass

    def draw(self, screen):
        # TODO (Task 1)
        pass


# =====================================================================
# --- Part 2 Task 3: Simple Factory (CreatureFactory) ---
# The rest of the program asks the factory for a creature by name and
# does not need to know which class is used to build it.
# =====================================================================
class CreatureFactory:
    @staticmethod
    def create(kind, x, y, speed):
        if kind == "A":
            return CreatureTypeA(x, y, speed)
        elif kind == "B":
            return CreatureTypeB(x, y, speed)
        # TODO (Task 3): add a branch for your new creature type(s).
        else:
            raise ValueError(f"CreatureFactory does not know kind {kind!r}")


# =====================================================================
# --- Part 2 Task 5 (optional): Observer (EventManager) ---
# Something happens (an EVENT) -> the EventManager tells every
# registered OBSERVER by calling observer.update(event).
#   Event ideas:    a creature hits a wall, reaches the centre,
#                   moves off-screen
#   Observer ideas: update a score, change a creature's colour,
#                   spawn a new creature
# =====================================================================
class EventManager:
    def __init__(self):
        self.observers = []

    def add(self, obs):
        self.observers.append(obs)

    def notify(self, event):
        for obs in self.observers:
            obs.update(event)


# TODO (Task 5): write an observer class here. It needs one method:
#     def update(self, event):
#         ...react to the event (event can be a simple string like "hit_wall")
# Then: register it with event_manager.add(...) below, and call
# event_manager.notify("...") at the moment the event happens
# (for example inside a creature's move()). How will the creature
# get hold of event_manager? (as an attribute? a parameter? a global?)

event_manager = EventManager()


# =====================================================================
# Main program
# =====================================================================
settings = GameSettings.get()

# --- Part 2 Task 3: build the creatures with the factory ---
creatures = []
creatures.append(CreatureFactory.create("A", 100, 200, 3))
creatures.append(CreatureFactory.create("B", 400, 300, 2))
# TODO (Task 1 + 3): add your new creature type(s) through the factory.

clock = pygame.time.Clock()

# (Teacher tool: lets the file be tested automatically. You can ignore it.)
MAX_FRAMES = int(os.environ.get("CREATURE_SIM_MAX_FRAMES", "0"))
frame = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(settings.background_colour)  # Task 4: colour comes from the Singleton

    # Polymorphism: the loop does not care which type each creature is.
    for creature in creatures:
        creature.move()
        creature.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # TODO (Task 4): could this number come from settings?

    frame += 1
    if MAX_FRAMES and frame >= MAX_FRAMES:
        running = False

pygame.quit()


# =====================================================================
# --- Part 2 Task 6: Reflection ---
# Answer each question in 2-4 sentences, pointing to YOUR code
# (class and method names).
#
# 1. How does the parent class (Creature) demonstrate abstraction?
#    TODO
#
# 2. Which new subclasses demonstrate polymorphism, and how?
#    TODO
#
# 3. Where did you apply a design pattern, and why is it useful here?
#    TODO
# =====================================================================
