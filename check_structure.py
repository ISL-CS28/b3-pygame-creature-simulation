"""
Self-check for the Creature Simulation.

    python check_structure.py          # checks part1/creature_sim.py
    python check_structure.py part2    # checks part2/creature_sim_part2.py

It only checks STRUCTURE (do the classes exist, inherit, override, store
attributes, draw something ...). It cannot tell you whether your idea is
good - that is up to you and your teacher.
  [NOT YET]      not an error: that part of the task is still to do.
  [CAN'T CHECK]  this script could not test it automatically (for example a
                 class that is not in the creatures list yet). Check it yourself.

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


LABELS = {True: "  [DONE]       ", False: "  [NOT YET]    ", None: "  [CAN'T CHECK]"}


def report(ok, text, why=""):
    """ok: True = done, False = not yet, None = could not be checked automatically."""
    results.append(ok)
    print(f"{LABELS[ok]} {text}")
    if ok is None and why:
        print(f"                  ({why})")


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


def creatures_in(m):
    """The objects in the program's own `creatures` list (we never build creatures ourselves,
    because your classes may need extra constructor arguments)."""
    creatures = getattr(m, "creatures", None)
    return list(creatures) if isinstance(creatures, (list, tuple)) else []


def draw_status(obj):
    """True = drew something. False = draw() is not implemented yet (only a stub).
    None = can't tell (draw() raised, or it has real code but drew nothing this frame)."""
    import pygame
    draw = getattr(type(obj), "draw", None)  # the draw() this object really uses (may be inherited)
    if draw is None or is_stub(draw):
        return False, ""
    surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # fully transparent: anything drawn shows up
    try:
        obj.draw(surface)
    except Exception as e:  # noqa: BLE001 - report, don't crash
        return None, f"draw() raised {e!r} when drawing on a test surface"
    if surface.get_bounding_rect().width > 0:
        return True, ""
    return None, "draw() has code but drew nothing on the test surface (off-screen?)"


def check_drawing(m, subs):
    by_type = {}
    for c in creatures_in(m):
        by_type.setdefault(type(c), c)
    for cls in subs:
        if cls not in by_type:
            report(None, f"{cls.__name__} draws something on screen",
                   "no object of this class is in the creatures list yet")
            continue
        ok, why = draw_status(by_type[cls])
        report(ok, f"{cls.__name__} draws something on screen", why)


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
    creatures = creatures_in(m)
    print("\nTask A - parent class")
    if not creatures:
        report(None, "creatures store attributes (at least x, y, speed)",
               "the creatures list is empty")
    else:
        report(all(len(vars(c)) >= 3 for c in creatures),
               "creatures store attributes (at least x, y, speed)")
    print("\nTask B - child classes")
    subs = check_common(m)
    print("\nTask C - polymorphism")
    kinds = {type(c) for c in creatures}
    report(len(kinds) >= 2, f"the creatures list mixes different types ({len(kinds)} type(s))")
    check_drawing(m, subs)


def factory_kinds(factory):
    """The kind names the factory compares against, read from its source code."""
    try:
        tree = ast.parse(textwrap.dedent(inspect.getsource(factory.create)))
    except (OSError, TypeError, SyntaxError, AttributeError):
        return []
    kinds = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            values = [node.left, *node.comparators]
        elif isinstance(node, ast.Dict):
            values = node.keys
        else:
            continue
        for v in values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str) and v.value not in kinds:
                kinds.append(v.value)
    return kinds


def check_factory(m):
    factory = getattr(m, "CreatureFactory", None)
    if factory is None:
        report(False, "class CreatureFactory exists")
        return
    kinds = factory_kinds(factory)
    made, errors = set(), []
    for kind in kinds:
        try:
            obj = factory.create(kind, 100, 100, 2)
        except Exception as e:  # noqa: BLE001
            errors.append(f"create({kind!r}, 100, 100, 2) raised {e!r}")
            continue
        if hasattr(m, "Creature") and isinstance(obj, m.Creature):
            made.add(type(obj))
    # The kind names are guessed from the source (an `else:` branch has no name), so a
    # short count only means "couldn't confirm", never "not done".
    found = (f"kinds found in create(): {', '.join(map(repr, kinds)) or 'none'}; "
             f"{len(made)} creature type(s) built")
    why = "; ".join([found, *errors])
    report(True if len(made) >= 2 else None,
           "CreatureFactory creates at least 2 creature types", why)
    report(True if len(made) >= 3 else None,
           "(optional, with Task 1) the factory also creates your new type(s)", why)


def check_part2(m):
    print("\nYour Part 1 classes")
    subs = check_common(m)
    print("\nTask 1 - new subclass")
    working = [c for c in subs if real_override(c, "move") or real_override(c, "draw")]
    report(len(working) >= 3,
           f"at least 3 Creature subclasses with real behaviour ({len(working)} found)")
    check_drawing(m, subs)
    print("\nTask 2 - abstraction")
    if hasattr(m, "Creature"):
        bare = object.__new__(m.Creature)  # skip __init__: we only call the parent's methods
        for name, args in (("move", ()), ("draw", (None,))):
            try:
                getattr(m.Creature, name)(bare, *args)
                ok = False
            except NotImplementedError:
                ok = True
            except Exception:  # noqa: BLE001
                ok = False
            report(ok, f"Creature.{name}() raises NotImplementedError")
    print("\nTask 3 - factory")
    check_factory(m)
    print("\nTask 4 - singleton")
    gs = getattr(m, "GameSettings", None)
    if gs is None:
        report(False, "class GameSettings exists")
    else:
        try:
            first, second = gs.get(), gs.get()
        except Exception as e:  # noqa: BLE001
            report(None, "GameSettings.get() works", f"raised {e!r}")
        else:
            report(first is second, "GameSettings.get() always returns the same object")
            report(len(vars(first)) >= 2, "GameSettings has at least one extra setting")
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
    done, not_yet = results.count(True), results.count(False)
    unknown = results.count(None)
    print(f"\n{done} done, {not_yet} not yet, {unknown} can't check (out of {len(results)}).")
    if unknown:
        print("[CAN'T CHECK] is not a mistake: it means this script could not test it.")
        print("Check that part yourself by running your program.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
