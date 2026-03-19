# IA - Assignemt 1

# Topic 1: Heuristic Search Methods for One-Player Solitaire Games

A solitaire game is characterized by the type of board and pieces, the rules of movement of the pieces, and the conditions for ending the game with defeat (impossibility to solve, maximum number of moves reached, time limit reached) or victory (solitaire solved), together with the respective score. Typically, in the event of a win, a score is awarded depending on the number of moves, resources spent, bonuses collected, and/or time spent.

In addition to implementing a solitaire game for a human player, **the program must be able to solve different versions/levels of this game:** using appropriate search methods, focusing on the comparison between uninformed search strategies (breadth-first search, depth-first search, iterative deepening, uniform cost) and heuristic search strategies (greedy search, A*, Weighted A*), exploring different heuristic functions. The algorithms employed should be compared following several criteria, with emphasis on the quality of the solution obtained, **the number of analyzed states, maximum memory used, and time spent to obtain the solution. If possible, variable board sizes should be explored, and a set of puzzles should be created with different difficulty levels.** **The program should be able to read the puzzle state (board position) from text files and store the results (including the puzzle solution, time and memory taken for each algorithm, final results, etc.) also in text files.**

Students should focus on firstly developing a simple version of the game with a small-sized board, employing simple search strategies and heuristics, and ensuring that they are able to solve these simple problem instances before proceeding to more complex ones.

**The application should have a graphical user interface to show the evolution of the board and interact with the user.** It should allow a game mode in which the PC solves the solitaire using the algorithms implemented and configuration selected by the user, giving the details of the solution and performance criteria, as specified above. The application should also allow a human game mode in which the user can interactively solve the game while asking the PC for "hints" (next move).

![Water sort game](/doc/images/logo200.png)

## Description

The **Water Sort problem** is a logic puzzle played on a set of bottles **T bottles**, each with a  **capacity of C units**. The bottles are initially filled with segments of colored water, stacked on top of one another. There are **N distinct colors**, with exactly **C units of each color** At least **2 bottles start empty**, providing the necessary room to maneuver.

A **move** consists of pouring the top color segment from one bottle into another. That is only valid if:
- the destination bottle is not full;
- the top of the destination bottle is either empty or matches the color being poured.

When pouring, **all contiguous units of the same color at the top** of the bottle are moved together as a singles segment, until it has no more space in the destination bottle or the color of the water in the source changes.

The puzzle is **solved** when every non-empty bottle contains exactly one color filling it completely.

A set of **T bottles**, each with a **capacity of C units**, are initially filled with colored water.
There are **N distinct colors**, with exactly **C units of each color** distributed across the bottles. At least 2 bottles are initially empty.

## Operations

The only operation that can be performed is:

- Pour liquid from a source bottle _i_ into a destination bottle _j_.

**This is only valid if:**

- The source bottle _i_ is **not empty**.
- The destination bottle _j_ is **not full**.
- The destination bottle _j_ is **empty**, or its **top color matches** the top color of source bottle _i_.

**When pouring, the liquid flows until one of the following occurs:**

- The source bottle _i_ becomes **empty**, or
- The destination bottle _j_ becomes **full**, or
- The **top color of source bottle _i_ changes**

## Goal

The puzzle is solved when **every bottle** is either:

- Empty, or
- Filled with **exactly one color**

# Formulation

**1.** Formulation of this problem as a search problem by defining the state representation, initial state, operators (their name, preconditions, effects, and cost), and final state(s).

**Variables:**

T - Total number of bottles <br>
C - Capacity of each bottle (the same for every bottle) <br>
N - Total number of distinct colors

**State representation:**

S = (B0, B1, ..., BT-1)

Where each B<sub>_i_</sub> is an ordered list of color units (bottom -> top), represented as integers:

Bi = (c1, c2, ..., ck), k <= C, c $\in$ {1, ..., N}

**Example:** (T=5, C=4, N=3)

B0 = (1, 2, 1, 3) # R G R B <br>
B1 = (2, 2, 1, 1) # G G R R <br>
B2 = (3, 3, 2, 3) # B B G B <br>
B3 = () <br>
B4 = ()

**Initial State:**

Read from file, any arbitrary distribution of colors across bottles. Example above.

**Goal State:**

∀<sub>i</sub> $\in$ {0, ..., T-1}: B<sub>i</sub> = () ∨ (|B<sub>i</sub>| = C ∧ | {c $\in$ B<sub>i</sub>}| = 1)

Every bottle is either empty, or full with exactly one color. The specific color in each bottle does not matter. For the previous example, this could be a final state:

B0 = () <br>
B1 = (2, 2, 2, 2) # G G G G <br>
B2 = (3, 3, 3, 3) # B B B B <br>
B3 = (1, 1, 1, 1) # R R R R <br>
B4 = ()

Operations

| Name | Preconditions                                              | Effect                                                   | Cost |
| ---- | ---------------------------------------------------------- | -------------------------------------------------------- | ---- |
| Pour | i≠j ∧ i not empty ∧ j not full ∧ (j empty ∨ top(i)=top(j)) | pours until to j until (i empty ∧ j full ∧ top(i)≠top(j) | 1    |
