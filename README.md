<div align="center">

# 🧠 LeetCode Daily Challenge

### A disciplined log of daily problem solving — one question, every day, no skips.

![Language](https://img.shields.io/badge/Language-Python%203-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)
![Days](https://img.shields.io/badge/Days%20Completed-4-f59e0b?style=for-the-badge)
![Profile](https://img.shields.io/badge/LeetCode-romesh45-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)

</div>

---

## 📌 What is this?

This repository tracks my **daily LeetCode problem-solving streak**. Every day I solve at least one problem, understand it deeply, and commit both the solution and a full breakdown README.

Each day's folder contains:
- `solution.py` — clean, commented Python 3 solution
- `README.md` — problem statement, intuition, algorithm walkthrough, dry run, and complexity analysis

---

## 🗂️ Problem Index

| Day | Problem | Difficulty | Topics | Solution |
|:---:|---------|:----------:|--------|:--------:|
| [Day 1](./Day%20-%201) | <!-- Fill in: Problem Name + LC link --> | <!-- Easy / Medium / Hard --> | <!-- e.g. Array, Greedy --> | [→](./Day%20-%201/solution.py) |
| [Day 2](./Day%20-%202) | <!-- Fill in: Problem Name + LC link --> | <!-- Easy / Medium / Hard --> | <!-- e.g. DP, Stack --> | [→](./Day%20-%202/solution.py) |
| [Day 3](./Day%20-%203) | [3660. Jump Game IX](https://leetcode.com/problems/jump-game-ix/) | ![Medium](https://img.shields.io/badge/-Medium-f59e0b) | Monotonic Stack · Union-Find · Graph | [→](./Day%20-%203/solution.py) |
| [Day 4](./Day%20-%204) | [3629. Minimum Jumps via Prime Teleportation](https://leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation/) | ![Medium](https://img.shields.io/badge/-Medium-f59e0b) | BFS · SPF Sieve · Number Theory | [→](./Day%20-%204/solution.py) |

> **How to update:** When you add a new day, paste a new row at the bottom. Replace `Day X` with the folder name, link to the LeetCode problem, pick difficulty, and add the topic tags.

---

## 📊 Stats

| Metric | Count |
|--------|------:|
| Total Problems Solved | 4 |
| Easy | — |
| Medium | 2+ |
| Hard | 0 |
| Current Streak | 4 days 🔥 |
| Language | Python 3 |

---

## 🔍 Topics Covered

`Union-Find` · `Monotonic Stack` · `BFS` · `Number Theory` · `SPF Sieve` · `Graph Components` · `Greedy`

*(This section grows as new topics appear)*

---

## 📁 Repository Structure

```
Leetcode---Problem/
│
├── Day - 1/
│   ├── solution.py        # Accepted solution with comments
│   └── README.md          # Full problem breakdown
│
├── Day - 2/
│   ├── solution.py
│   └── README.md
│
├── Day - 3/               # 3660. Jump Game IX
│   ├── solution.py        # Union-Find + Monotonic Stack, O(n·α(n))
│   └── README.md
│
├── Day - 4/               # 3629. Minimum Jumps via Prime Teleportation
│   ├── solution.py        # BFS + SPF Sieve + Bucket Clearing, O(n log V)
│   └── README.md
│
└── README.md              ← you are here
```

---

## 💡 What Each README Contains

Every day's README is structured identically so it's easy to navigate:

1. **Problem Statement** — constraints and examples
2. **Intuition** — why the naive approach fails and what the insight is
3. **Algorithm** — step-by-step breakdown of the approach
4. **Solution** — fully commented Python code
5. **Dry Run** — state-by-state trace through an example
6. **Complexity Analysis** — time and space, with justification

---

## 🚀 Highlighted Solutions

### Day 3 — Jump Game IX
**The trick:** Forward and backward jumps are symmetric — any two indices with `a < b` and `nums[a] > nums[b]` can reach each other. The graph is undirected. Find connected components and return the max value per component.

**The non-obvious fix:** Nearest-neighbor (PGE/NSE) spanning fails for arrays like `[30, 21, 5, 35, 24]`. The correct approach: maintain a stack tracking **component max values** (not individual values). When a component's max exceeds the current element, merge them.

### Day 4 — Minimum Jumps via Prime Teleportation
**The trick:** Naive BFS is O(n²) — a single prime like 2 can fan out to half the array. Fix: group all indices by their prime factors upfront into buckets. First time a prime is activated, drain and **clear** its bucket. Future activations find it empty → zero redundant work.

---

## 📬 Connect

- **GitHub:** [romesh45](https://github.com/romesh45)
- **LeetCode:** [romesh45](https://leetcode.com/romesh45)

---

<div align="center">

*Building consistency, one problem at a time.*

</div>
