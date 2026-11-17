# Part 1: Creature Simulation (Worksheet 5.5)

**Focus:** B3.1 classes and objects · B3.2 inheritance and polymorphism (introduction)

## Objective

Build a small simulation with:

- **one parent class**, `Creature`
- **at least two child classes**, `CreatureTypeA` and `CreatureTypeB`, that behave **differently**

Your code must show: **constructors, attributes, method overriding, inheritance and
polymorphism**. This is a creative task, so you decide what your creatures look like and how
they move.

File to edit: [`creature_sim.py`](creature_sim.py). It already runs and shows a black window.
New to pygame? Keep [`../docs/pygame_cheatsheet.md`](../docs/pygame_cheatsheet.md) open.

---

## Key concepts

The examples below are deliberately **not** about creatures. Use them to understand the idea,
then apply it in your own way.

### Class and object

A **class** is a blueprint. An **object** (or *instance*) is one thing built from that blueprint.

```python
class Lamp:
    ...

desk_lamp = Lamp()     # one object
floor_lamp = Lamp()    # another object, built from the same class
```

### Constructor

The **constructor** is the special method `__init__`. Python runs it automatically when a new
object is created. Its job is to set the object up.

```python
class Lamp:
    def __init__(self, brightness):
        self.brightness = brightness

desk_lamp = Lamp(60)   # __init__ runs with brightness = 60
```

### Attribute

An **attribute** is a piece of data stored *inside* an object: `self.<name>`. Each object keeps
its own values.

```python
desk_lamp = Lamp(60)
floor_lamp = Lamp(100)
print(desk_lamp.brightness, floor_lamp.brightness)   # 60 100
```

### Inheritance

A **child class** (subclass) gets all attributes and methods of its **parent class**
(superclass) for free. You write the parent in brackets.

```python
class Vehicle:
    def __init__(self, wheels):
        self.wheels = wheels

    def describe(self):
        return f"I have {self.wheels} wheels"

class Bicycle(Vehicle):          # Bicycle IS-A Vehicle
    pass

print(Bicycle(2).describe())     # "I have 2 wheels" (inherited)
```

A child can add its own attributes. It calls the parent's constructor with `super()`:

```python
class Car(Vehicle):
    def __init__(self, wheels, fuel):
        super().__init__(wheels)   # let Vehicle set up self.wheels
        self.fuel = fuel           # extra attribute only Car has
```

### Method overriding

A child **overrides** a method by defining a method with the **same name**. The child's version
replaces the parent's for objects of that child class.

```python
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):          # overrides Animal.sound
        return "Woof"
```

### Polymorphism

*Poly* means "many" and *morph* means "form". You can call **the same method** on objects of
**different classes**, and each one responds **in its own way**. The calling code doesn't need
to know or check which class each object is.

```python
class Cat(Animal):
    def sound(self):
        return "Meow"

for a in [Dog(), Cat(), Dog()]:
    print(a.sound())          # Woof, Meow, Woof: one line of code, different behaviour
```

Notice there is **no** `if type(a) == Dog:` anywhere. That's the point.

---

## Tasks

### Task A: complete the parent class `Creature`

1. **Constructor:** store the attributes every creature needs: position (`x`, `y`), `speed`,
   and anything else all creatures share (colour, size, direction …).
2. **`move()`** *(optional)*: write a basic movement, **or** leave it empty so each child class
   overrides it.
3. **`draw(screen)`:** draw a simple shape (for example a circle) at the creature's position.

### Task B: create two subclasses

Create `CreatureTypeA` and `CreatureTypeB`. Each one must:

- **inherit** from `Creature`
- **override at least one method** (`move()` and/or `draw()`)
- **introduce new behaviour**, such as a new movement pattern, shape, colour change or extra attribute
- be **meaningfully different** from the other type ("same thing, different colour" is not enough)

### Task C: polymorphism

In the main program, put **several creatures of different types** in **one list**. Every frame,
the loop calls

```python
for c in creatures:
    c.move()
    c.draw(screen)
```

and each creature behaves according to its own class. Add more creatures to the list and check
that the loop doesn't need any `if` statements about types.

---

## Optional challenges

Pick any that interest you:

- Add a **third** creature type.
- **Colour changes**, simple **animations**, or reactions to the **mouse**.
- Creatures that **bounce off the edges** of the window.
- **Encapsulation:** make attributes private (`self.__speed`) and add getters/setters.
- A **class variable** that counts how many creatures have been created.
- A **static method** (`@staticmethod`) for a simulation rule, e.g. "is this point inside the window?".
- A creature that **follows the mouse** (`pygame.mouse.get_pos()`).

---

## Self-check

Fill in the right-hand column (class name and method or line numbers) before you submit.
You can also run `python check_structure.py` from the project folder.

| Concept | Where it should appear | Where it is in **my** code |
|---------|------------------------|----------------------------|
| Constructor | `Creature.__init__` (and maybe a child `__init__` using `super()`) | |
| Attributes | `self.x`, `self.y`, `self.speed`, … set in the constructor | |
| Inheritance | `class CreatureTypeA(Creature)`, `class CreatureTypeB(Creature)` | |
| Method overriding | `move()` and/or `draw()` redefined in each child class | |
| New behaviour | something a child class does that the parent doesn't | |
| Polymorphism | the `creatures` list with mixed types + `c.move()` / `c.draw(screen)` loop | |

When Part 1 is finished, continue with [Part 2](../part2/README.md).
