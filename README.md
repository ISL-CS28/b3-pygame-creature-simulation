# Creature Simulation (IB Computer Science HL, Theme B3: OOP)

In this project you build a small **Pygame** simulation of creatures that move around a window.
It is a template: it contains explanations and **skeleton code with `TODO` comments**. You
write the creatures yourself.

| Part | Worksheet | Focus | Start here |
|------|-----------|-------|------------|
| Part 1 | 5.5 | B3.1 classes and objects, B3.2 inheritance and polymorphism (intro) | [`part1/README.md`](part1/README.md) |
| Part 2 | 7.5 | B3.2.2 polymorphism, B3.2.3 abstraction, B3.2.5 design patterns | [`part2/README.md`](part2/README.md) |

Both skeleton files **run straight away**. You will see an empty black window, and you close it
to quit. Run your file again after every TODO you finish and watch your creatures appear.

---

## 1. Setup (one time)

You need Python 3.10 or newer.

### Option A: PyCharm (recommended)

1. **File → Open…** and choose this folder (the one that contains this `README.md`).
2. Create a virtual environment: **Settings / Preferences → Project → Python Interpreter →
   Add Interpreter → Add Local Interpreter → Virtualenv Environment → New**.
   Set the location to `.venv` inside this folder and click **OK**.
3. Open `requirements.txt`. PyCharm shows a banner, *"Package requirements are not
   satisfied"*. Click **Install requirements**.
   (Or open PyCharm's **Terminal** tab and run `pip install -r requirements.txt`.)
4. Right-click `part1/creature_sim.py` and choose **Run 'creature_sim'**. A black window
   should open.

### Option B: terminal

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python part1/creature_sim.py
```

### Why `pygame-ce` and not `pygame`?

`requirements.txt` installs **pygame-ce** (community edition). It is a drop-in replacement
maintained by most of the original pygame developers. The original `pygame` package does not
offer ready-made installers for the newest Python versions, so `pip install pygame` can fail.
`pygame-ce` installs cleanly. Your code stays exactly the same, and you still write
`import pygame`.

> Don't install both `pygame` and `pygame-ce` in the same environment. They clash. If you
> installed `pygame` by mistake, run `pip uninstall pygame`, then `pip install -r requirements.txt`.

---

## 2. Repository map

```
README.md                     ← you are here
requirements.txt              ← the one library we need (pygame-ce)
check_structure.py            ← self-check: is my code structured correctly?
docs/pygame_cheatsheet.md     ← the few pygame commands you need
part1/
  README.md                   ← Part 1 guide: concepts + Tasks A, B, C
  creature_sim.py             ← Part 1 skeleton (edit this)
part2/
  README.md                   ← Part 2 guide: abstraction + design patterns, Tasks 1–6
  creature_sim_part2.py       ← Part 2 skeleton (edit this)
```

---

## 3. Checking your progress

```bash
python check_structure.py          # Part 1
python check_structure.py part2    # Part 2
```

The checker runs your program for one frame without opening a window. It then lists each task
as `[DONE]` or `[NOT YET]`. It only checks **structure** (classes exist, inherit, override
methods, draw something). It cannot judge whether your creatures are interesting. That part is
your job.

In PyCharm, right-click `check_structure.py` and choose **Run**. For Part 2, add `part2` under
**Run → Edit Configurations… → Script parameters**.

---

## 4. Submission checklist

Before you hand in, check:

- [ ] The program runs without errors and closes cleanly when you close the window.
- [ ] `python check_structure.py` (and `part2` if you did Part 2) shows no unexpected `[NOT YET]`.
- [ ] Every `TODO` you completed has been **replaced** by your code or comment (don't leave stale TODOs).
- [ ] Your classes and methods have meaningful names and short comments explaining *why*.
- [ ] Part 1: the self-check table in [`part1/README.md`](part1/README.md#self-check) is filled in.
- [ ] Part 2: the **reflection** questions at the bottom of `creature_sim_part2.py` are answered.
- [ ] Your name is at the top of each `.py` file you changed.
