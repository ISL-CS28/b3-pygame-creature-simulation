# Part 2: Extension (Worksheet 7.5)

**Focus:** B3.2.2 polymorphism · B3.2.3 abstraction · B3.2.5 design patterns (Factory, Singleton, Observer)

You extend your Part 1 simulation. The **tasks are independent**, so do as many as you can, in
any order. Task 6 (reflection) is for everyone.

## How to start

1. Finish Part 1 first.
2. Open [`creature_sim_part2.py`](creature_sim_part2.py). It already contains the Part 2
   structures (`CreatureFactory`, `GameSettings`, `EventManager`) and **runs as it is**.
3. **Copy your Part 1 code into it:** paste your `Creature` attributes into `Creature.__init__`,
   and your `CreatureTypeA` / `CreatureTypeB` code into the placeholder classes. Replace the
   `pass` stubs with your real `move()` / `draw()`.
4. Run it. It should look the same as your finished Part 1.

> Your `part1/creature_sim.py` stays as it is, so you keep a record of Part 1.

**Why do the placeholder classes have empty `move()`/`draw()` methods?** In Task 2 the
parent's methods raise `NotImplementedError`. A subclass *without* its own `move()` would
crash the program on the first frame. The empty stubs keep the skeleton running until you fill
them in. Don't delete a stub without replacing it.

---

## Key concepts

### Abstraction (B3.2.3)

**Abstraction** means showing *what* something does and hiding *how* it does it. An **abstract
class** defines an **interface**: a list of methods every subclass *must* provide. It doesn't
implement them itself.

```python
class Shape:
    def area(self):
        raise NotImplementedError("Subclasses must implement area()")

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2
```

Code that uses shapes only relies on "every shape has `area()`". It doesn't need to know any
formula. If someone writes a new subclass and forgets `area()`, they get a clear error
straight away instead of silently wrong behaviour.

*(Python also has a module, `abc`, for formal abstract classes. Raising `NotImplementedError`
is the simple version used in this worksheet.)*

### Design patterns (B3.2.5)

A **design pattern** is a well-known, reusable solution to a problem that keeps coming up in
software design. It's a *shape* for your code, not a library you install.

#### Simple Factory

**Problem:** the code that *creates* objects is spread around the program, and every part
must know every class name and constructor.
**Solution:** one place, the factory, creates objects from a simple description (e.g. a string).

```python
class PizzaFactory:
    @staticmethod
    def create(kind):
        if kind == "margherita":
            return Margherita()
        elif kind == "veggie":
            return Veggie()
```

**Why it's useful:** to add a new type, you change *one* place. The rest of the program only
says `PizzaFactory.create("veggie")`. The input could even come from a file or a key press.

#### Singleton

**Problem:** some things should exist **exactly once**, such as game settings, a score board or
a log. If different parts of the program each create their own copy, they get out of sync.
**Solution:** the class keeps its single instance in a class variable and hands out that same
object every time.

```python
class Logbook:
    _instance = None

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = Logbook()
        return cls._instance

assert Logbook.get() is Logbook.get()   # always the same object
```

**Why it's useful:** one shared source of truth that any part of the program can reach,
without passing it around everywhere.

#### Observer

**Problem:** when something happens, several *other* objects need to react, but the object
where it happens shouldn't need to know about all of them.
**Solution:** a *subject* (here `EventManager`) keeps a list of **observers**. When an event
happens, it calls `update(event)` on each one.

```python
class Doorbell:                       # the subject
    def __init__(self):
        self.observers = []
    def add(self, obs):
        self.observers.append(obs)
    def notify(self, event):
        for obs in self.observers:
            obs.update(event)

class Dog:                            # an observer
    def update(self, event):
        print("Woof!")

bell = Doorbell()
bell.add(Dog())
bell.notify("ring")                   # Dog reacts, but Doorbell never mentions Dog
```

**Why it's useful:** you can add new reactions (new observers) without touching the code that
triggers the event. This is called *loose coupling*.

---

## Tasks

### Task 1: strengthen polymorphism

Add **at least one new subclass** of `Creature` (the skeleton has a placeholder,
`CreatureTypeC`). Ideas:

- follows the mouse slowly
- bounces off walls
- changes colour when moving
- teleports randomly

The main loop must stay exactly this, with no type checks:

```python
for creature in creatures:
    creature.move()
    creature.draw(screen)
```

### Task 2: abstraction

The parent's `move()` and `draw()` now raise `NotImplementedError`. Write a **short comment**
in `Creature` explaining how the parent class now acts as an **abstract interface**.

*Try it:* temporarily delete `move()` from one subclass and run the program. What happens, and
why is that useful? (Put it back afterwards.)

### Task 3: Simple Factory

`CreatureFactory.create(kind, x, y, speed)` is given for `"A"` and `"B"`. Extend it with your
new type(s), and create **at least two types** in the main program through the factory:

```python
creatures.append(CreatureFactory.create("A", 100, 200, 3))
```

### Task 4: Singleton settings

`GameSettings` is given with one setting, `background_colour`, used by
`screen.fill(settings.background_colour)`. **Add at least one more adjustable setting** (FPS,
number of creatures, speed multiplier, …) and **use it** in the program. Always get the
settings with `GameSettings.get()`, never with `GameSettings()`.

### Task 5: Observer *(optional)*

Use `EventManager` to connect **one event** with **one observer** that reacts.

| Event ideas | Observer ideas |
|-------------|----------------|
| a creature hits a wall | update a score |
| a creature reaches the centre | change a creature's colour |
| a creature moves off-screen | spawn a new creature |

Steps: write an observer class with an `update(self, event)` method → register it with
`event_manager.add(...)` → call `event_manager.notify("...")` where the event happens.

### Task 6: reflection

Answer the three questions in the comment block at the **bottom** of `creature_sim_part2.py`:

1. How does the parent class demonstrate **abstraction**?
2. Which new subclasses demonstrate **polymorphism**?
3. Where did you apply a **design pattern**, and why is it useful?

---

## Checklist

Run `python check_structure.py part2` from the project folder, then tick:

- [ ] My Part 1 classes are copied in and work (no `pass` stubs left in `move()`/`draw()`).
- [ ] **Task 1:** at least one new subclass with its own behaviour, and the main loop has no type checks.
- [ ] **Task 2:** `Creature.move()`/`draw()` raise `NotImplementedError`, plus my comment explaining the abstract interface.
- [ ] **Task 3:** `CreatureFactory` knows my new type(s), and creatures are created through the factory.
- [ ] **Task 4:** at least one extra setting in `GameSettings`, actually used, obtained via `GameSettings.get()`.
- [ ] **Task 5** *(optional):* one event → `notify` → one observer's `update` reacts visibly.
- [ ] **Task 6:** all three reflection questions answered, pointing to my own class and method names.
