# Day 24 — LeetCode Challenge

## 3093. Longest Common Suffix Queries

| Field | Details |
|---|---|
| **Difficulty** | Hard |
| **Topics** | Trie · String · Reverse-Trie · Multi-Criteria Tie-Breaking |
| **LeetCode Link** | [3093. Longest Common Suffix Queries](https://leetcode.com/problems/longest-common-suffix-queries/) |

---

## Problem Statement

You are given two arrays of strings, `wordsContainer` and `wordsQuery`.

For each `wordsQuery[i]`, find the index of the string in `wordsContainer` that has the **longest common suffix** with `wordsQuery[i]`. If multiple container strings share that longest common suffix, pick:

1. The **shortest** one.
2. If there's still a tie, the one with the **smallest index** (earliest in `wordsContainer`).

Return an integer array `ans` where `ans[i]` is the chosen index for query `i`.

---

## Examples

### Example 1

```
Input:  wordsContainer = ["abcd", "bcd", "xbcd"]
        wordsQuery     = ["cd", "bcd", "xyz"]
Output: [1, 1, 1]
```

- `"cd"`: every container word ends with `cd` (suffix length 2). All three are candidates → pick shortest → `"bcd"` (index 1).
- `"bcd"`: all three end with `bcd` (suffix length 3). Same tie-break → index 1.
- `"xyz"`: no shared suffix. Empty-suffix fallback among all three → shortest is `"bcd"` → index 1.

### Example 2

```
Input:  wordsContainer = ["abcdefgh", "poiuygh", "ghghgh"]
        wordsQuery     = ["gh", "acbfgh", "acbfegh"]
Output: [2, 0, 2]
```

- `"gh"`: all three end with `gh`. Shortest is `"ghghgh"` (length 6) → index 2.
- `"acbfgh"`: only `"abcdefgh"` shares the suffix `"fgh"`. Even though `"ghghgh"` is shorter, the longest common suffix wins first → index 0.
- `"acbfegh"`: only `"gh"` is shared by all (no container has `"egh"`). Shortest tied at `"gh"` → index 2.

---

## Constraints

- `1 <= wordsContainer.length, wordsQuery.length <= 10⁴`
- `1 <= wordsContainer[i].length, wordsQuery[i].length <= 5·10³`
- Lowercase English letters only.
- `Σ |wordsContainer[i]| ≤ 5·10⁵` and `Σ |wordsQuery[i]| ≤ 5·10⁵`.

---

## Intuition

### Step 1: Reverse to convert "suffix" into "prefix"

The **longest common suffix** of two strings is the **longest common prefix of their reverses**. Reversing turns a sneaky suffix problem into the classic prefix-trie problem:

```
"abcd"   reversed → "dcba"
"bcd"    reversed → "dcb"
"xbcd"   reversed → "dcbx"

trie over reverses:
                  root
                   |d
                  (d)
                   |c
                  (c)
                   |b
                  (b)
                  / \
                 a   x
                (a) (x)   ← represent "abcd" and "xbcd"
                (b is also where "bcd" terminates — its reverse "dcb" ends here)
```

A query walks `reversed(query)` down the trie. The depth reached = the matched suffix length.

### Step 2: Pre-bake tie-breaking into the trie

The naive idea — "walk the trie, then scan all container words that pass through this node" — is too slow. Instead, **pre-compute the best index at every node** during construction.

For every container word `i`, as we insert its reverse, walk through every node along the path and update that node's `best` with `i` (using the tie-break rule). At the end:

- Each node `N` stores the index of the **shortest** container word (tie: **earliest**) whose reverse passes through `N`.
- That answer is also valid for any query that descends *exactly* to `N`: such a query's longest matched suffix is depth(`N`), and it could potentially match any descendant — but if we picked the right metric, the best-among-descendants is just the best-at-N.

Wait — is that last bit actually true? Let's check:

**Claim:** If query `q` reaches node `N` (depth `d`) and stops (no child for the next reverse char), then the container words sharing exactly suffix-length `d` (or longer) are precisely those that descend through `N`. So `N.best` is correct.

That works because:
- Anyone descending through `N` shares **at least** suffix `d` with `q` (they all agree on the path `root → N`).
- The query couldn't extend deeper, so no descendant of `N` shares more than depth `d` either — they're all tied at exactly the longest common suffix the query could find.
- Among those, pick shortest then earliest → exactly what `N.best` records.

### Step 3: Handle the empty-suffix fallback

A query that doesn't even match its first reversed character stays at the **root**. The root must store the best container index over **all** container words — because every word shares the empty suffix with every query.

We initialize `root.best` with the globally best index before insertions begin (or equivalently, update root for every insertion — same outcome).

### Step 4: Trie node update — short and earliest

When inserting container word `i`, at each node visited:

```python
node.best = i, if (len(wordsContainer[i]) < len(wordsContainer[node.best]))
              or (lengths equal and i < node.best)
            else node.best
```

That's the tie-break rule encoded into the trie itself.

---

## Algorithm

```
n = |wordsContainer|
root = node(best = 0)
for i in 1..n-1: root.best = better(root.best, i)

for i in 0..n-1:
    node = root
    for ch in reversed(wordsContainer[i]):
        if ch not in node.children:
            node.children[ch] = new node(best = i)
        node = node.children[ch]
        node.best = better(node.best, i)

ans = []
for q in wordsQuery:
    node = root
    for ch in reversed(q):
        if ch in node.children: node = node.children[ch]
        else: break
    ans.append(node.best)

return ans
```

---

## Solution

```python
from typing import List


class Solution:
    def stringIndices(
        self, wordsContainer: List[str], wordsQuery: List[str]
    ) -> List[int]:
        n = len(wordsContainer)

        def better(a: int, b: int) -> int:
            la, lb = len(wordsContainer[a]), len(wordsContainer[b])
            if la != lb:
                return a if la < lb else b
            return a if a < b else b

        root = {"best": 0, "children": {}}
        for i in range(1, n):
            root["best"] = better(root["best"], i)

        for i, w in enumerate(wordsContainer):
            node = root
            for ch in reversed(w):
                if ch not in node["children"]:
                    node["children"][ch] = {"best": i, "children": {}}
                node = node["children"][ch]
                node["best"] = better(node["best"], i)

        ans = []
        for q in wordsQuery:
            node = root
            for ch in reversed(q):
                if ch in node["children"]:
                    node = node["children"][ch]
                else:
                    break
            ans.append(node["best"])
        return ans
```

---

## Complexity Analysis

Let `C = Σ |wordsContainer[i]|` and `Q = Σ |wordsQuery[i]|`.

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(C + Q)** | Each character causes O(1) trie work — node lookup + `best` update for insertions; node lookup for queries |
| **Space** | **O(C)** | At most `C` trie nodes (one per inserted character) |

For the given limits (`C, Q ≤ 5·10⁵`) this is roughly `10⁶` operations — comfortably fast.

The brute-force "compare each query against each container word" approach would be `O(|wordsQuery| × |wordsContainer| × maxLen)` ≈ `10⁴ × 10⁴ × 5·10³` = `5·10¹¹` ops → TLE.

---

## Full Trace — Example 1

`wordsContainer = ["abcd", "bcd", "xbcd"]`, query `"cd"`.

**Build phase** (reversed forms: `"dcba"`, `"dcb"`, `"dcbx"`):

After inserting all three, the trie looks like:

```
root [best = 1]                 ← shortest length is "bcd" (3), so best across all = 1
 └─ d [best = 1]
     └─ c [best = 1]
         └─ b [best = 1]
             ├─ a [best = 0]    ← only "abcd" passes here
             └─ x [best = 2]    ← only "xbcd" passes here
```

`root.best` was initialized walking through every index. Index 1 (`"bcd"`, length 3) beats 0 (`"abcd"`, length 4) and 2 (`"xbcd"`, length 4), so root settles at `1`.

Same logic at every node along `d → c → b`: among the three words passing through, `1` is the shortest.

**Query `"cd"`** → reversed is `"dc"`:

- Step 1: `'d'` exists at root → descend to node `d` (best = 1)
- Step 2: `'c'` exists → descend to node `c` (best = 1)
- Query exhausted. **Return `node.best = 1`** ✓

**Query `"xyz"`** → reversed `"zyx"`:

- Step 1: `'z'` not in root's children → stop immediately.
- **Return `root.best = 1`** ✓ (empty-suffix fallback)

---

## Full Trace — Example 2, Query `"acbfgh"`

`wordsContainer = ["abcdefgh", "poiuygh", "ghghgh"]`.

Reversed forms: `"hgfedcba"`, `"hgyuiop"`, `"hghghg"`.

Trie (partial, focused on the relevant path):

```
root [best = 2]                        ← "ghghgh" length 6 < 7 < 8
 └─ h [best = 2]
     └─ g [best = 2]
         ├─ f [best = 0]               ← only "abcdefgh" reaches here
         │   └─ e [best = 0]
         │       └─ d [best = 0] ...
         ├─ y [best = 1]               ← only "poiuygh"
         └─ h [best = 2]               ← only "ghghgh"
```

**Query `"acbfgh"`** → reversed `"hgfbca"`:

- Step 1: `'h'` → node h (best=2)
- Step 2: `'g'` → node g (best=2)
- Step 3: `'f'` → node f (best=0) ← only `"abcdefgh"` extends here
- Step 4: `'b'` → no such child of `f`. **Stop.**
- **Return `node.best = 0`** ✓

The trie correctly says: at depth 3 (suffix `"fgh"`), only `"abcdefgh"` qualifies, so index `0` is the answer — even though `"ghghgh"` (index 2) is shorter overall.

---

## Why "Best at Each Node" Is Sufficient

The deepest reachable node `N` for a query `q` partitions container words into:

- **Group A** — those whose reverse passes through `N`. They share suffix-length ≥ depth(`N`) with `q`.
- **Group B** — those that diverged earlier. They share less, so they can't win.

Among Group A, the query couldn't go deeper (it stopped at `N`), so **all** of Group A share *exactly* the same longest common suffix with `q`. The tie-break (shortest, earliest) is purely an intra-group decision — and `N.best` was constructed to be exactly that intra-group winner.

Therefore `N.best` is the correct answer. ∎

---

## Alternative — Memory-Efficient Trie (Array Children)

Replace dicts with fixed-size arrays of 26 child pointers (one per lowercase letter). Lookup becomes O(1) by index, and there's no dict overhead:

```python
class Node:
    __slots__ = ("best", "children")
    def __init__(self, best):
        self.best = best
        self.children = [None] * 26
```

Same asymptotic complexity but much faster in practice — typically a 2–5× speedup on large inputs and lower memory.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Suffix → reversed prefix** | Reversing converts a suffix-matching problem into the standard prefix trie. |
| **Pre-bake the tie-break** | Store the best index at every node during insertion → O(1) query answer per node visit. |
| **Root holds the global fallback** | Queries with no first-char match drop to root; root's `best` covers all container words. |
| **Greedy depth-first walk** | Just descend as far as the query allows — no backtracking or scanning needed. |
| **"Best at depth d" = best among all descendants** | Equivalent because all of them share exactly the same longest common suffix with that query. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| Query shares zero suffix with anyone | Stops at root → returns globally-best container index |
| Multiple container words tied on length and suffix | Earliest container index wins (rule built into `better`) |
| Container has only 1 word | Trie has one path; every query returns `0` |
| Query is identical to some container word | Walks the full path; returns the best among words sharing that suffix |
| Container word is a single character | Inserts one node beyond root; standard trie behavior |

---

## Approach Tags

`Trie` · `Reversed Strings` · `Per-Node Best Pre-Computation` · `String Matching` · `Suffix Search`

---

*Day 24 of the LeetCode Daily Challenge*
