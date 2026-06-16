# Day 43 — LeetCode Challenge

## 3612. Process String with Special Operations I

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | String · Simulation · Stack |
| **LeetCode Link** | [3612. Process String with Special Operations I](https://leetcode.com/problems/process-string-with-special-operations-i/) |

---

## Problem Statement

Given a string `s` of lowercase letters and the special characters `*`, `#`, `%`, build `result` by processing `s` left to right:

- **lowercase letter** → append it to `result`.
- **`*`** → remove the last character from `result` (if any).
- **`#`** → duplicate `result` (append it to itself).
- **`%`** → reverse `result`.

Return the final `result`.

---

## Examples

### Example 1

```
Input:  s = "a#b%*"
Output: "ba"
```

| i | char | op | result |
|:-:|:-:|---|:-:|
| 0 | `a` | append | `"a"` |
| 1 | `#` | duplicate | `"aa"` |
| 2 | `b` | append | `"aab"` |
| 3 | `%` | reverse | `"baa"` |
| 4 | `*` | remove last | `"ba"` |

### Example 2

```
Input:  s = "z*#"
Output: ""
```

`z` → `"z"`; `*` → `""`; `#` → duplicate of empty → `""`.

---

## Constraints

- `1 <= s.length <= 20`
- `s` contains only lowercase letters and `*`, `#`, `%`.

---

## Intuition

### Pure simulation — no cleverness needed

Each character is a command on a mutable buffer. Walk `s` once and apply the matching operation. A **list** is the right buffer because:

- `append` / `pop` are O(1) amortized
- `reverse()` is in place
- strings are immutable, so using one would rebuild the whole thing on every edit

### The four commands, one-to-one

| Char | List operation |
|:-:|---|
| lowercase | `result.append(ch)` |
| `*` | `result.pop()` — guarded by `if result` |
| `#` | `result += result` (append a copy of itself) |
| `%` | `result.reverse()` |

### The single guard that matters

`*` on an empty buffer must be a **no-op**, not an error. The `if result:` check before `pop()` enforces the "if it exists" clause. Everything else is unconditional.

### Why the size stays manageable

`#` *doubles* the buffer, so in principle the length grows exponentially in the number of `#`s. But `|s| ≤ 20` caps the damage — at most a handful of doublings, so the buffer stays tiny. (The harder "II" version raises limits and forces you to answer queries *without* materializing the full string.)

---

## Algorithm

```
result = []
for ch in s:
    if   ch == '*': if result: result.pop()
    elif ch == '#': result += result
    elif ch == '%': result.reverse()
    else:           result.append(ch)
return "".join(result)
```

---

## Solution

```python
class Solution:
    def processStr(self, s: str) -> str:
        result = []
        for ch in s:
            if ch == '*':
                if result:
                    result.pop()
            elif ch == '#':
                result += result
            elif ch == '%':
                result.reverse()
            else:
                result.append(ch)
        return "".join(result)
```

---

## Complexity Analysis

Let `L` be the final buffer length (bounded by `~2^(#count)` but tiny here).

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(L)** total | Each op is O(1) except `#`/`%` which are O(current length); summed, dominated by the final length |
| **Space** | **O(L)** | The buffer |

For `|s| ≤ 20` this is effectively instant.

---

## Full Trace — Example 1: `s = "a#b%*"`

| step | char | action | buffer |
|:-:|:-:|---|:-:|
| 1 | `a` | append | `['a']` |
| 2 | `#` | `result += result` | `['a','a']` |
| 3 | `b` | append | `['a','a','b']` |
| 4 | `%` | reverse | `['b','a','a']` |
| 5 | `*` | pop | `['b','a']` |

Join → **`"ba"`** ✓

---

## Full Trace — Example 2: `s = "z*#"`

| step | char | action | buffer |
|:-:|:-:|---|:-:|
| 1 | `z` | append | `['z']` |
| 2 | `*` | pop | `[]` |
| 3 | `#` | `result += result` (empty + empty) | `[]` |

Join → **`""`** ✓ — note `#` on an empty buffer stays empty, and `*` earlier didn't error.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **It's a command interpreter** | Each char mutates a buffer; walk once and dispatch. |
| **List > string for mutation** | O(1) append/pop and in-place reverse; strings would rebuild each time. |
| **Guard `*` on empty** | The only conditional op — `if result` before `pop()`. |
| **`#` doubles the buffer** | Length can grow fast, but `|s| ≤ 20` keeps it tiny in version I. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `*` on empty buffer | No-op (guarded) |
| `#` on empty buffer | Stays empty |
| `%` on empty/single char | No visible change |
| All letters | Plain concatenation |
| Trailing `*` removes last char | As in Example 1 |

---

## Looking Ahead — The "II" Version

A typical **"II"** escalation raises `|s|` and asks for **specific characters by index** in the (possibly astronomically large) final string. Since `#` can blow the length up to `2^k`, you can't build it. The trick there is to track the **length after each operation**, then answer an index query by **walking the operations backward** — mapping the queried position through reversals, duplications, and deletions to the original letter that produced it. Not needed here, but it's the natural next step.

---

## Approach Tags

`Simulation` · `Stack/Buffer` · `Command Dispatch` · `In-Place Operations`

---

*Day 43 of the LeetCode Daily Challenge*
