# Pygame cheat sheet

Only what you need for the Creature Simulation. Full docs: <https://pyga.me/docs/> (pygame-ce).

## Window

```python
import pygame
pygame.init()                                  # start pygame (once, at the top)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # note: ONE tuple argument
pygame.display.set_caption("My title")
```

## Coordinates

```
(0, 0) ──────────── x grows → ──────────── (800, 0)
  │
  y grows ↓
  │
(0, 600)                                   (800, 600)
```

- The origin `(0, 0)` is the **top-left** corner.
- `x` increases to the **right**, and `y` increases **downwards** (the opposite of maths class).
- Moving up means `self.y -= ...`.
- Drawing positions must be whole numbers, so use `int(self.x)` if you store floats.

## Colours

Colours are **RGB tuples**: `(red, green, blue)`, each from `0` to `255`.

```python
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
random_colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
```

## Drawing

```python
pygame.draw.circle(screen, colour, (x, y), radius)        # (x, y) = centre
pygame.draw.rect(screen, colour, (x, y, width, height))   # (x, y) = top-left corner
pygame.draw.ellipse(screen, colour, (x, y, width, height))
pygame.draw.line(screen, colour, (x1, y1), (x2, y2), thickness)
pygame.draw.polygon(screen, colour, [(x1, y1), (x2, y2), (x3, y3)])
```

Add a last argument `width` (e.g. `2`) to `circle`/`rect` to draw only the outline.

## The game loop

Every frame does the same four things:

```python
clock = pygame.time.Clock()
running = True
while running:
    # 1. handle events (keyboard, mouse, closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:          # the window's close button
            running = False

    # 2. update: move things
    # 3. draw: clear the screen first, then draw everything
    screen.fill((0, 0, 0))

    # 4. show the new frame and wait
    pygame.display.flip()                      # nothing appears until you flip!
    clock.tick(60)                             # at most 60 frames per second

pygame.quit()
```

- **Forgot `screen.fill(...)`?** Moving shapes leave trails.
- **`clock.tick(60)`** keeps the speed the same on fast and slow computers. With 60 FPS,
  `speed = 3` means 3 pixels per frame = 180 pixels per second.

## Keyboard and mouse

```python
# inside the event loop: something happened ONCE
if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    ...
if event.type == pygame.MOUSEBUTTONDOWN:
    mx, my = event.pos

# anywhere: what is the state RIGHT NOW?
mx, my = pygame.mouse.get_pos()
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    ...
```

## Random numbers

```python
import random
random.randint(1, 6)          # whole number 1..6 (both ends included)
random.uniform(-1.0, 1.0)     # decimal number between -1.0 and 1.0
random.choice([-1, 1])        # pick one item from a list
```

## Staying inside the window

```python
if self.x < 0 or self.x > WIDTH:
    ...   # off the left or right edge: what should happen?
if self.y < 0 or self.y > HEIGHT:
    ...   # off the top or bottom edge
```
