<div align="center">

# 🧠 LeetCode Daily Mission

### A disciplined log of daily problem solving — one question, every day, no skip and work

![Language](https://img.shields.io/badge/Language-Python%203-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)
![Days](https://img.shields.io/badge/Days%20Completed-7-f59e0b?style=for-the-badge)
![Profile](https://img.shields.io/badge/LeetCode-romesh45-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)

</div>

---

## 📌 What is this?

This repository tracks my **daily LeetCode problem-solving streak**. Every day I solve at least one problem, understand it deeply, and commit both the solution and a full breakdown README.

Each day's folder contains:
- `solution.py` — clean, commented Python 3 solution
- `README.md` — problem statement, intuition, dry run, and complexity analysis

---

## 🗂️ Problem Index

| Day | Problem | Difficulty | Topics |
|:---:|---------|:----------:|--------|
| [Day 1](./Day%20-%201) | [61. Rotate List](https://leetcode.com/problems/rotate-list/) | ![Medium](https://img.shields.io/badge/-Medium-f59e0b) | Linked List · Two Pointers |
| [Day 2](./Day%20-%202) | [1861. Rotating the Box](https://leetcode.com/problems/rotating-the-box/) | ![Medium](https://img.shields.io/badge/-Medium-f59e0b) | Array · Two Pointers · Matrix |
| [Day 3](./Day%20-%203) | [3660. Jump Game IX](https://leetcode.com/problems/jump-game-ix/) | ![Medium](https://img.shields.io/badge/-Medium-f59e0b) | Monotonic Stack · Union-Find · Graph |
| [Day 4](./Day%20-%204) | [3629. Minimum Jumps via Prime Teleportation](https://leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation/) | ![Medium](https://img.shields.io/badge/-Medium-f59e0b) | BFS · SPF Sieve · Number Theory |
| [Day 5](./Day%20-%205) | [13. Roman to Integer](https://leetcode.com/problems/roman-to-integer/) | ![Easy](https://img.shields.io/badge/-Easy-00c4cc) | Hash Table · Math · String |
| [Day 6](./Day%20-%206) | [1914. Cyclically Rotating a Grid](https://leetcode.com/problems/cyclically-rotating-a-grid/) | ![Medium](https://img.shields.io/badge/-Medium-f59e0b) | Array · Matrix · Simulation |
| [Day 7](./Day%20-%207) | [2770. Maximum Number of Jumps to Reach the Last Index](https://leetcode.com/problems/maximum-number-of-jumps-to-reach-the-last-index/) | ![Medium](https://img.shields.io/badge/-Medium-f59e0b) | Array · Dynamic Programming |

---

## 📊 Stats

| Metric | Count |
|--------|------:|
| Total Problems Solved | 7 |
| Easy | 1 |
| Medium | 6 |
| Hard | 0 |
| Current Streak | 7 days 🔥 |
| Language | Python 3 |

---

## 🔍 Topics Covered

`Linked List` · `Two Pointers` · `Matrix` · `Union-Find` · `Monotonic Stack` · `BFS` · `Number Theory` · `SPF Sieve` · `Graph Components` · `Dynamic Programming` · `Simulation` · `Greedy` · `Hash Table` · `Math`

---

## 📁 Repository Structure

```
Leetcode---Problem/
│
├── Day - 1/               # 61. Rotate List
│   ├── solution.py        # Circular link & break — O(n) time, O(1) space
│   └── README.md
│
├── Day - 2/               # 1861. Rotating the Box
│   ├── solution.py        # Gravity simulation + 90° CW rotation — O(m×n)
│   └── README.md
│
├── Day - 3/               # 3660. Jump Game IX
│   ├── solution.py        # Component-max stack + Union-Find — O(n·α(n))
│   └── README.md
│
├── Day - 4/               # 3629. Minimum Jumps via Prime Teleportation
│   ├── solution.py        # BFS + SPF Sieve + Bucket Clearing — O(n log V)
│   └── README.md
│
├── Day - 5/               # 13. Roman to Integer
│   ├── solution.py        # Hash Table + Math + String — O(n)
│   └── README.md
│
├── Day - 6/               # 1914. Cyclically Rotating a Grid
│   ├── solution.py        # Layer extraction + 1D rotation — O(m×n)
│   └── README.md
│
├── Day - 7/               # 2770. Maximum Number of Jumps to Reach Last Index
│   ├── solution.py        # Bottom-up DP — O(n²) time, O(n) space
│   └── README.md
│
└── README.md              ← you are here
```

---

## 🚀 Problem Highlights

### Day 1 — Rotate List
**The trick:** Don't shift nodes one by one. Connect the tail to the head to make a circle, walk to the new tail at index `length − k − 1`, then break the circle. Two passes, no extra memory.

### Day 2 — Rotating the Box
**The trick:** The 90° clockwise rotation maps "rightward" in the original to "downward" in the result. Apply gravity first (stones slide right per row using a two-pointer), then apply the standard rotation formula `result[j][m-1-i] = box[i][j]`. Each obstacle resets the gravity pointer independently.

### Day 3 — Jump Game IX
**The non-obvious bug fix:** The standard PGE + NSE spanning tree fails for arrays like `[30, 21, 5, 35, 24]`. When components merge, a future small element must compare against the **component's max value**, not the individual element's value. Maintain a stack of `(component_root, component_max)` pairs — pop and union whenever `component_max > nums[i]`. Single pass, no second scan needed.

### Day 4 — Minimum Jumps via Prime Teleportation
**The trick:** Naive BFS is O(n²) — prime 2 alone could fan out to half the array. Fix: group all indices by their prime factors into `prime_buckets[p]` upfront. First time any index with `nums[i] = p` is dequeued, drain and **clear** its bucket. Future activations find it empty → zero re-work. Uses a smallest-prime-factor (SPF) sieve for O(log V) factorization per number.

### Day 5 — Roman to Integer
**The trick:** Iterating right-to-left turns the subtraction rule into a simple comparison. If the current numeral is smaller than the one to its right (e.g., `I` before `V`), subtract it; otherwise add it. No look-ahead needed — a clean single pass with a fixed 7-entry hash map keeps it at O(n) time and O(1) space.

### Day 6 — Cyclically Rotating a Grid
**The trick:** A 2D ring rotation is just a 1D list rotation in disguise. Traverse each layer clockwise into a flat list, shift it left by `k % layer_size` positions (`elements[k:] + elements[:k]`), then write values back in the same traversal order. Each layer is fully independent — no other layer is affected.

### Day 7 — Maximum Number of Jumps to Reach the Last Index
**The trick:** Unlike most jump games that ask for the minimum, this one asks for the maximum — so we want as many small hops as possible. Greedy fails because an "easy" jump now can lead to a dead end. Bottom-up DP fills `dp[j] = max(dp[i] + 1)` for all valid predecessors `i`, where validity means `|nums[j] - nums[i]| ≤ target`. Mark unreachable indices as `-1` so they're never used as springboards.

---

## 📬 Connect

- **GitHub:** [romesh45](https://github.com/romesh45)
- **LeetCode:** [romesh45](https://leetcode.com/romesh45)

---

<div align="center">

*Building consistency, one problem at a time.*

</div>
