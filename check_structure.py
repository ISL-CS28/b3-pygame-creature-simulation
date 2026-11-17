"""
Self-check for the Creature Simulation.

    python check_structure.py          # checks part1/creature_sim.py
    python check_structure.py part2    # checks part2/creature_sim_part2.py

It only checks STRUCTURE (do the classes exist, inherit, override, store
attributes, draw something ...). It cannot tell you whether your idea is
good - that is up to you and your teacher. "NOT YET" is not an error:
it just means that part of the task is still to do.

You do not need to read or change this file.
"""

import ast
import importlib.util
import inspect
import os
import sys
import textwrap
import traceback

# Run pygame without opening a window, and stop the main loop after 1 frame.
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["CREATURE_SIM_MAX_FRAMES"] = "1"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = {
    "part1": os.path.join(HERE, "part1", "creature_sim.py"),
    "part2": os.path.join(HERE, "part2", "creature_sim_part2.py"),
}

results = []


def report(ok, text):
    results.append(ok)
    print(("  [DONE]    " if ok else "  [NOT YET] ") + text)


def load(path):
    spec = importlib.util.spec_from_file_location("student_sim", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # runs the file for 1 frame
    return module


def is_stub(func):
    """True if a method body is only `pass`, a docstring, `...` or raise NotImplementedError."""
    try:
        tree = ast.parse(textwrap.dedent(inspect.getsource(func)))
    except (OSError, TypeError, SyntaxError):
        return False
    for stmt in tree.body[0].body:
        if isinstance(stmt, ast.Pass):
            continue
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            continue  # docstring or ...
        if isinstance(stmt, ast.Raise) and "NotImplementedError" in ast.dump(stmt):
            continue
        return False
    return True


def subclasses_in(module, parent):
    return [obj for obj in vars(module).values()
            if inspect.isclass(obj) and issubclass(obj, parent) and obj is not parent]


def real_override(cls, name):
    return name in vars(cls) and not is_stub(vars(cls)[name])


def make(cls):
    try:
        return cls(100, 100, 2)
    except Exception as e:  # noqa: BLE001 - report, don't crash
        print(f"      (could not create {cls.__name__}(100, 100, 2): {e!r})")
        return None


def draws_something(obj):
    import pygame
    surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # fully transparent: anything drawn shows up
    try:
        obj.draw(surface)
    except Exception:  # noqa: BLE001
        return False
    return surface.get_bounding_rect().width > 0


def check_common(m):
    report(hasattr(m, "Creature"), "class Creature exists")
    if not hasattr(m, "Creature"):
        return []
    subs = subclasses_in(m, m.Creature)
    for name in ("CreatureTypeA", "CreatureTypeB"):
        cls = getattr(m, name, None)
        report(cls is not None and cls in subs, f"{name} exists and inherits from Creature")
    for cls in subs:
        overridden = [n for n in ("move", "draw") if real_override(cls, n)]
        report(bool(overridden),
               f"{cls.__name__} overrides move() and/or draw() with real code"
               + (f" ({', '.join(overridden)})" if overridden else ""))
    return subs


def check_part1(m):
    print("\nTask A - parent class")
    if hasattr(m, "Creature"):
        obj = make(m.Creature)
        report(obj is not None and len(vars(obj)) >= 3,
               "Creature.__init__ stores attributes (at least x, y, speed)")
    print("\nTask B - child classes")
    subs = check_common(m)
    print("\nTask C - polymorphism")
    creatures = getattr(m, "creatures", [])
    kinds = {type(c) for c in creatures}
    report(len(kinds) >= 2, f"the creatures list mixes different types ({len(kinds)} type(s))")
    for cls in subs:
        obj = make(cls)
        report(obj is not None and draws_something(obj), f"{cls.__name__} draws something on screen")


def check_part2(m):
    print("\nYour Part 1 classes")
    subs = check_common(m)
    print("\nTask 1 - new subclass")
    working = [c for c in subs if real_override(c, "move") or real_override(c, "draw")]
    report(len(working) >= 3,
           f"at least 3 Creature subclasses with real behaviour ({len(working)} found)")
    for cls in subs:
        obj = make(cls)
        report(obj is not None and draws_something(obj), f"{cls.__name__} draws something on screen")
    print("\nTask 2 - abstraction")
    if hasattr(m, "Creature"):
        obj = make(m.Creature)
        try:
            obj.move()
            ok = False
        except NotImplementedError:
            ok = True
        except Exception:  # noqa: BLE001
            ok = False
        report(ok, "Creature.move() raises NotImplementedError")
    print("\nTask 3 - factory")
    factory = getattr(m, "CreatureFactory", None)
    made = set()
    if factory is not None:
        for kind in "ABCDEFGH":
            try:
                made.add(type(factory.create(kind, 100, 100, 2)))
            except Exception:  # noqa: BLE001
                pass
    report(len(made) >= 3, f"CreatureFactory builds a new kind besides 'A' and 'B' ({len(made)} kinds found)")
    print("\nTask 4 - singleton")
    gs = getattr(m, "GameSettings", None)
    if gs is not None:
        report(gs.get() is gs.get(), "GameSettings.get() always returns the same object")
        report(len(vars(gs.get())) >= 2, "GameSettings has at least one extra setting")
    print("\nTask 5 - observer (optional)")
    observers = [obj for obj in vars(m).values()
                 if inspect.isclass(obj) and "update" in vars(obj)]
    report(bool(observers), "an observer class with an update(event) method exists")
    em = getattr(m, "event_manager", None)
    report(em is not None and len(getattr(em, "observers", [])) > 0,
           "at least one observer is registered with event_manager")


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "part1"
    if which not in TARGETS:
        print(f"Usage: python check_structure.py [{' | '.join(TARGETS)}]")
        return 2
    path = TARGETS[which]
    print(f"Checking {os.path.relpath(path, HERE)} ...")
    try:
        module = load(path)
    except Exception:  # noqa: BLE001
        print("\nYour program crashed while running. Fix this error first:\n")
        traceback.print_exc(file=sys.stdout)
        return 1
    import pygame
    pygame.init()
    (check_part1 if which == "part1" else check_part2)(module)
    print(f"\n{sum(results)} / {len(results)} checks done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
