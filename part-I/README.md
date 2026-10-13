# Part I: Greedy Algorithms

CS 413, Pioneer Delivery

Written in Python 3. Nothing to install and nothing to compile. Task B uses `heapq` from the standard library.

## Running it

From this folder, type deliveries yourself:

```bash
python3 run.py
```

It asks for one delivery per line. These all work:

```text
D1 1 3
1 3
(1, 3)
D2 4-7
D3, 5, 9
```

A blank line, `done`, or `q` finishes. If a line is bad, it tells you and you can type the next one. You can also put several deliveries on one line with `;`.

To use a file instead:

```bash
python3 run.py data/sample_deliveries.txt
```

That runs Tasks A, B, and C on the sample file. For one task:

```bash
python3 run.py --task a data/sample_deliveries.txt
python3 run.py --task b data/sample_deliveries.txt
python3 run.py --task c data/sample_deliveries.txt
```

`python3 run.py --required` runs the files in `data/required/`.

Task D is separate:

```bash
python3 task_d.py
```

To check the required cases:

```bash
python3 -m unittest tests.test_required_cases -v
```

## Input format

One delivery per line:

```text
id start finish
```

Times are integers and start has to be less than finish. If a delivery ends at time t, the same driver can start another one at t. Blank lines are skipped, and so are lines that start with `#`.

Typing it in works the same way. An id is optional (`1 3` becomes D1, D2, and so on). Commas, parentheses, and `start-finish` are fine. Several deliveries can go on one line if you separate them with `;`.

The sample from the handout is `data/sample_deliveries.txt`:

```text
D01 10 13
D02 2 5
D03 4 7
D04 1 8
D05 8 11
D06 11 14
D07 13 16
```

The required tests are the same format, under `data/required/task_a/`, `data/required/task_b/`, and `data/required/task_c/`.

## How the files are split up

`delivery.py` is the `Delivery` object and the file reader. `task_a.py`, `task_b.py`, and `task_c.py` are the three algorithms. `task_d.py` is the counterexample. `run.py` just reads a file and prints the answers. `tests/test_required_cases.py` checks the cases from the handout.

## Task A

Greedy choice: sort by finish time, then take the next delivery if it starts at or after the finish time of the last one I kept. That is the compatible delivery that ends soonest.

Why it is optimal: compare the greedy schedule with some optimal schedule, both in finish order. They match until the first spot where the optimal schedule picked a different delivery. That other delivery cannot finish earlier, or the greedy step would have taken it. Swap the greedy delivery in. Later deliveries in the optimal schedule still fit, because they already started after something that finished at least as late. The schedule is still valid and the same size. After swapping every difference, the greedy set is at least as big, so it is optimal. If more than one optimal schedule exists, the program just returns the earliest-finish one.

Running time: sorting is O(n log n), then one pass over the list. Total O(n log n).

Required cases:

1. No deliveries. Selected 0.
2. (1, 3). Selected D1. Total 1.
3. (1, 3), (3, 5), (5, 7). Selected D1, D2, D3. Total 3.
4. (1, 5), (2, 6), (3, 7). Selected D1. Total 1.
5. (5, 7), (1, 3), (3, 5), (2, 4). Selected D2 (1, 3), D3 (3, 5), D1 (5, 7). Total 3.
6. (1, 4), (2, 4), (4, 6). Selected D1 (1, 4), D3 (4, 6). Total 2.

On the sample file it picks D02 (2, 5), D05 (8, 11), and D06 (11, 14). Total 3.

## Task B

The priority queue is a min-heap of `(free_time, driver_index)`. `free_time` is when that driver finishes their last delivery. The driver who is done first sits at the front.

Deliveries are sorted by start time. For each one, look at the driver on top of the heap. If their free time is at or before this start time, give them the delivery and set their free time to its finish time. If the heap is empty, or every driver is still busy, add a new driver.

That count is minimum because a new driver is added only when everyone else is busy at the new start time. Those drivers are each in the middle of a delivery, and the new one overlaps them too, so the number of drivers never goes past the biggest overlap. You need at least that many anyway. A driver only gets a new delivery at or after their previous finish, so nobody gets two overlapping jobs. Ending at t and starting at t is allowed, since the free time check uses `<=`.

Running time: the sort is O(n log n). Each delivery does a couple of heap operations at O(log n) each. Total O(n log n).

Required cases:

1. No deliveries. 0 drivers.
2. (1, 3). Driver 1: D1. 1 driver.
3. (1, 3), (3, 5), (5, 7). Driver 1: D1 D2 D3. 1 driver.
4. (1, 5), (2, 6), (3, 7). Driver 1: D1. Driver 2: D2. Driver 3: D3. 3 drivers.
5. (1, 4), (2, 5), (4, 7), (5, 8). Driver 1: D1 D3. Driver 2: D2 D4. 2 drivers.
6. (5, 8), (1, 4), (2, 5), (4, 6), (6, 9). Driver 1: D2 D4 D5. Driver 2: D3 D1. 2 drivers.

Sample file, 3 drivers:

```text
Driver 1: D04 D06
Driver 2: D02 D05 D07
Driver 3: D03 D01
```

A different program could number the drivers differently. The count has to be 3, and no driver can have an overlap.

## Task C

This is the same problem as Task A. One driver can keep at most k compatible deliveries, so the smallest number to reject is whatever is left over.

If the biggest compatible set has size k, reject n - k.

Running time is the same as Task A, O(n log n). Writing down the rejected ids is one extra pass.

Required cases:

1. No deliveries. Reject 0.
2. (1, 3). Reject 0.
3. (1, 3), (3, 5), (5, 7). Reject 0.
4. (1, 5), (2, 6), (3, 7). Reject 2 (D2 and D3). Keeps D1.
5. (5, 7), (1, 3), (3, 5), (2, 4). Reject 1 (D4, which is (2, 4)).
6. (1, 2), (2, 3), (3, 4), (1, 3). Reject 1 (D4, which is (1, 3)).

On the sample, k = 3 and n = 7, so 4 are rejected: D01, D03, D04, and D07.

## Task D

Each of these deliveries takes one time slot. Delivery j is ready at Rj (a nonnegative integer) and has profit Pj > 0. No two profits are equal. The slot T has to be at least Rj, and two deliveries cannot use the same slot. Delay is T - R. The value of a delivery is Pj / (1 + delay), and V is the sum of those.

Greedy strategy G goes through the deliveries from highest profit to lowest. Each one gets the earliest open slot at or after its ready time.

Counterexample:

- A: R = 0, P = 5
- B: R = 0, P = 4
- C: R = 1, P = 3

What G does, in profit order A, then B, then C:

- A goes in slot 0. Delay 0. Value 5/1 = 5.
- B's earliest open slot at or after 0 is slot 1. Delay 1. Value 4/2 = 2.
- C's earliest open slot at or after 1 is slot 2. Delay 1. Value 3/2.

V(G) = 5 + 2 + 3/2 = 17/2.

A better schedule S:

- A in slot 0. Delay 0. Value 5.
- C in slot 1. Delay 0. Value 3.
- B in slot 2. Delay 2. Value 4/3.

V(S) = 5 + 3 + 4/3 = 28/3.

Both schedules are legal: every slot is at or after the ready time, and no slot is used twice. G follows the rule and still gets 17/2. 28/3 is larger (the difference is 5/6). So G does not always give an optimal schedule.

`python3 task_d.py` prints both schedules.
