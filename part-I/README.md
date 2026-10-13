# Pioneer Delivery, Part I: Greedy Algorithms

CS 413 — Analysis of Algorithms

This folder is the first part of the Pioneer Delivery scheduling portfolio. It answers three operational questions with greedy algorithms, and it gives a counterexample for a fourth greedy rule that is not always optimal.

## Language

Python 3. The program uses only the standard library (`heapq` for the min-heap in Task B). No packages need to be installed, and there is no compile step.

## How to run

From this `part-I` directory:

```bash
python3 run.py data/sample_deliveries.txt
python3 run.py --task a data/sample_deliveries.txt
python3 run.py --task b data/sample_deliveries.txt
python3 run.py --task c data/sample_deliveries.txt
python3 run.py --required
python3 task_d.py
python3 -m unittest tests.test_required_cases -v
```

- `run.py` with a file answers Tasks A, B, and C for that file. `--task` limits the output to one task.
- `--required` runs every required test-case file under `data/required/`.
- `task_d.py` prints the Task D counterexample and both schedule values.
- The unit tests check the required answers and check that no driver is given overlapping deliveries.

## Input-file format

Each delivery is one line with three whitespace-separated fields:

```text
<id> <start_time> <finish_time>
```

Times are integers, and `start_time` must be strictly less than `finish_time`. A delivery that finishes at time `t` is compatible with a delivery that starts at time `t`. Blank lines are ignored, and so are lines that start with `#`.

The handout sample is `data/sample_deliveries.txt`:

```text
D01 10 13
D02 2 5
D03 4 7
D04 1 8
D05 8 11
D06 11 14
D07 13 16
```

The required cases are stored as the same kind of file under `data/required/task_a/`, `data/required/task_b/`, and `data/required/task_c/`.

## Program organization

| File | Role |
| --- | --- |
| `delivery.py` | `Delivery` records and `load_deliveries` |
| `task_a.py` | Largest compatible set for one driver |
| `task_b.py` | Minimum-driver assignment, using a min-heap |
| `task_c.py` | Minimum rejections, built on Task A |
| `task_d.py` | Counterexample to the profit-ordered greedy rule |
| `run.py` | Command-line program that reads a file and prints the schedules |
| `tests/test_required_cases.py` | The required cases from the handout |
| `data/` | Sample file and required test-case files |

`run.py` only parses arguments, loads the file, and prints results. The algorithms live in the task modules.

## Task A: maximum deliveries for one driver

**Greedy choice.** Sort the deliveries by finish time. Scan that list once, and take a delivery whenever it starts at or after the finish time of the last delivery taken. That choice is the compatible delivery that finishes earliest.

**Why it is optimal.** Let G be the greedy schedule and let O be any optimal schedule, both written in order of finish time. Walk through them from the start. They agree until the first index where they differ. At that position the greedy rule picked a delivery that finishes no later than the delivery O picked, and that greedy delivery is still compatible with everything chosen before it. Swap it into O. Every later delivery in O still fits, because those deliveries started at or after a finish time that is at least as late as the new one. The swapped schedule is still feasible and has the same size. Repeating the swap shows that G is at least as large as O, so G is optimal. When several optimal schedules exist, any one of them is acceptable; this program returns the one produced by earliest finish time.

**Running time.** Sorting is O(n log n). The scan is O(n). The total is O(n log n).

### Required results

| Test | Intervals | Maximum selected | Program result |
| --- | --- | --- | --- |
| 1 | no deliveries | 0 | 0, no deliveries selected |
| 2 | (1, 3) | 1 | D1 |
| 3 | (1, 3), (3, 5), (5, 7) | 3 | D1, D2, D3 |
| 4 | (1, 5), (2, 6), (3, 7) | 1 | D1 |
| 5 | (5, 7), (1, 3), (3, 5), (2, 4) | 3 | D2 (1, 3), D3 (3, 5), D1 (5, 7) |
| 6 | (1, 4), (2, 4), (4, 6) | 2 | D1 (1, 4), D3 (4, 6) |

On the handout sample the program selects D02 (2, 5), D05 (8, 11), and D06 (11, 14), for a total of 3.

## Task B: minimum number of drivers

**What is stored in the priority queue.** A min-heap of `(free_time, driver_index)`. `free_time` is the finish time of that driver's latest delivery, so it is the earliest time that driver can take another request. The driver who becomes free soonest is at the front of the heap.

**How a driver is selected.** Sort the deliveries by start time. For each delivery, look at the front of the heap. If that driver's free time is less than or equal to the delivery's start time, assign the delivery to that driver and set the driver's free time to this delivery's finish time. If the heap is empty or every driver is still busy, open a new driver.

**Why the number of drivers is minimum.** A new driver is opened only when every existing driver is busy at the new start time `s`. Each of those drivers is in the middle of a delivery that covers `s`, and the new delivery covers `s` as well, so the number of drivers never exceeds the maximum number of deliveries that overlap at one time. At least that many drivers are necessary. Touching endpoints stay compatible because a driver whose free time equals `s` is reused. No driver receives overlapping work, because a driver is reused only at or after the finish time of the previous delivery.

**Running time.** Sorting is O(n log n). Each delivery does a constant number of heap operations, each O(log n). The total is O(n log n).

### Required results

| Test | Intervals | Minimum drivers | Program assignment |
| --- | --- | --- | --- |
| 1 | no deliveries | 0 | no drivers |
| 2 | (1, 3) | 1 | Driver 1: D1 |
| 3 | (1, 3), (3, 5), (5, 7) | 1 | Driver 1: D1 D2 D3 |
| 4 | (1, 5), (2, 6), (3, 7) | 3 | Driver 1: D1; Driver 2: D2; Driver 3: D3 |
| 5 | (1, 4), (2, 5), (4, 7), (5, 8) | 2 | Driver 1: D1 D3; Driver 2: D2 D4 |
| 6 | (5, 8), (1, 4), (2, 5), (4, 6), (6, 9) | 2 | Driver 1: D2 D4 D5; Driver 2: D3 D1 |

On the handout sample the minimum is 3:

```text
Driver 1: D04 D06
Driver 2: D02 D05 D07
Driver 3: D03 D01
```

Another correct assignment can name the drivers differently. The count is the minimum, and none of these drivers has an overlapping pair.

## Task C: minimum number of deliveries to reject

**Relation to Task A.** With one driver, the deliveries that can be kept are exactly the mutually compatible sets from Task A. Rejecting as few as possible means keeping a largest compatible set and rejecting the rest.

**How many are rejected.** If the largest compatible set has size k, the minimum number of rejections is n - k.

**Running time.** Task A is O(n log n). Marking the rejected deliveries is one extra O(n) pass, so the total stays O(n log n).

### Required results

| Test | Intervals | Minimum rejected | Program result |
| --- | --- | --- | --- |
| 1 | no deliveries | 0 | 0 |
| 2 | (1, 3) | 0 | 0 |
| 3 | (1, 3), (3, 5), (5, 7) | 0 | 0 |
| 4 | (1, 5), (2, 6), (3, 7) | 2 | rejects D2 and D3; keeps D1 |
| 5 | (5, 7), (1, 3), (3, 5), (2, 4) | 1 | rejects D4 (2, 4) |
| 6 | (1, 2), (2, 3), (3, 4), (1, 3) | 1 | rejects D4 (1, 3) |

On the handout sample, k = 3 and n = 7, so 4 deliveries are rejected: D01, D03, D04, and D07.

## Task D: when a greedy choice fails

Flexible same-day deliveries each take one integer time slot. Delivery j is ready at a nonnegative integer R_j and has a positive profit P_j, with all profits distinct. A schedule assigns each delivery a slot T_j at or after R_j, and all slots are distinct. The delay is D_j = T_j - R_j. The value of the delivery is

```text
V_j = P_j / (1 + D_j)
```

and V is the sum of those values.

Strategy G considers deliveries in order of decreasing profit and schedules each one in the earliest free slot at or after its ready time.

### Counterexample

| Delivery | Ready time R_j | Profit P_j |
| --- | --- | --- |
| A | 0 | 5 |
| B | 0 | 4 |
| C | 1 | 3 |

**Schedule produced by G.** Decreasing profit is A, then B, then C.

- A is placed in slot 0. Delay 0. Value 5/1 = 5.
- B's earliest free slot at or after 0 is slot 1. Delay 1. Value 4/2 = 2.
- C's earliest free slot at or after 1 is slot 2. Delay 1. Value 3/2.

```text
V(G) = 5 + 2 + 3/2 = 17/2
```

**A better schedule S.**

- A in slot 0. Delay 0. Value 5.
- C in slot 1. Delay 0. Value 3.
- B in slot 2. Delay 2. Value 4/3.

```text
V(S) = 5 + 3 + 4/3 = 28/3
```

**Why this shows G is not always optimal.** Both schedules are feasible: every slot is at or after the delivery's ready time, and no two deliveries share a slot. Strategy G, followed exactly, produces the first schedule. But 28/3 - 17/2 = 5/6, so V(S) > V(G). A rule that returns a worse schedule on this input does not always produce an optimal schedule.

`python3 task_d.py` prints these two schedules and checks that V(S) is larger.
