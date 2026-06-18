# Day 45 — LeetCode Challenge

## 1344. Angle Between Hands of a Clock

| Field | Details |
|---|---|
| **Difficulty** | Medium |
| **Topics** | Math · Geometry |
| **LeetCode Link** | [1344. Angle Between Hands of a Clock](https://leetcode.com/problems/angle-between-hands-of-a-clock/) |

---

## Problem Statement

Given `hour` and `minutes`, return the **smaller** angle (in degrees) between the hour and minute hands. Answers within `10⁻⁵` of the true value are accepted.

---

## Examples

### Example 1
```
Input:  hour = 12, minutes = 30
Output: 165
```

### Example 2
```
Input:  hour = 3, minutes = 30
Output: 75
```

### Example 3
```
Input:  hour = 3, minutes = 15
Output: 7.5
```

---

## Constraints

- `1 <= hour <= 12`
- `0 <= minutes <= 59`

---

## Intuition

### Measure each hand from 12 o'clock

Pick a reference (12 o'clock = `0°`, increasing clockwise) and compute each hand's absolute angle. The answer is the difference, folded to the smaller arc.

### Hand speeds

**Minute hand:** sweeps a full `360°` in 60 minutes → **`6°` per minute**.
```
minute_angle = minutes × 6
```

**Hour hand:** sweeps `360°` in 12 hours → `30°` per hour. **But it also creeps** as the minutes tick: `30°` spread over 60 minutes = **`0.5°` per minute**.
```
hour_angle = (hour % 12) × 30 + minutes × 0.5
```

### The two bugs everyone hits

1. **`hour % 12`.** At `hour = 12` the hand points straight up at `0°`, not `360°`. The modulo maps `12 → 0`. (`12 × 30 = 360` would be wrong; `0 × 30 = 0` is right.)

2. **The minute creep on the hour hand.** This is the classic trap. At **3:30**, the hour hand is *not* pointing at the 3 (`90°`) — it's halfway toward the 4, at `90 + 30×0.5 = 105°`. That's exactly why the answer is `75°`, not `90°`. Omitting `+ minutes × 0.5` quietly fails this kind of case.

### Fold to the smaller arc

The two hands divide the circle into two arcs that sum to `360°`. Whichever is smaller is the answer:
```
diff = |hour_angle − minute_angle|
return min(diff, 360 − diff)
```

---

## Algorithm

```
minute_angle = minutes × 6
hour_angle   = (hour % 12) × 30 + minutes × 0.5
diff         = |hour_angle − minute_angle|
return min(diff, 360 − diff)
```

---

## Solution

```python
class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        minute_angle = minutes * 6
        hour_angle = (hour % 12) * 30 + minutes * 0.5
        diff = abs(hour_angle - minute_angle)
        return min(diff, 360 - diff)
```

---

## Complexity Analysis

| | Complexity | Reason |
|---|---|---|
| **Time** | **O(1)** | Constant arithmetic |
| **Space** | **O(1)** | A couple of scalars |

---

## Worked Verification

| Time | `minute_angle` | `hour_angle` | `diff` | `min(diff, 360−diff)` |
|:-:|:-:|:-:|:-:|:-:|
| 12:30 | `30×6 = 180` | `0×30 + 30×0.5 = 15` | `165` | **165** ✓ |
| 3:30 | `180` | `3×30 + 15 = 105` | `75` | **75** ✓ |
| 3:15 | `90` | `90 + 7.5 = 97.5` | `7.5` | **7.5** ✓ |
| 12:00 | `0` | `0` | `0` | **0** |
| 6:00 | `0` | `180` | `180` | **180** |
| 12:01 | `6` | `0.5` | `5.5` | **5.5** |

---

## Why the Hour Hand Creeps — A Closer Look

Think of the hour hand's position as continuous, not snapping between numbers:

```
at H:00  → hour hand exactly on number H        →  H×30°
at H:30  → hour hand halfway between H and H+1   →  H×30° + 15°
at H:59  → hour hand almost on H+1               →  H×30° + 29.5°
```

The minute hand "drags" the hour hand forward proportionally. Modeling this with `+ minutes × 0.5` is the entire difficulty of the problem — the rest is plain subtraction.

---

## Key Insights

| Insight | Explanation |
|---|---|
| **Minute hand: `6°/min`** | `360° / 60`. |
| **Hour hand: `30°/hr + 0.5°/min`** | Base `30°` per hour plus continuous minute creep. |
| **`hour % 12`** | Maps 12 → 0 so the hour hand sits at the top, not at `360°`. |
| **`min(diff, 360 − diff)`** | The hands bound two complementary arcs; return the smaller. |
| **The creep is the whole trick** | Forgetting `+ minutes × 0.5` fails cases like 3:30. |

---

## Edge Cases

| Case | Behavior |
|---|---|
| `12:00` | Both hands at `0°` → `0` |
| `6:00` | Opposite hands → `180` (the maximum) |
| `12:30` | Hour hand crept to `15°` → `165` |
| `hour = 12` | `hour % 12 = 0` keeps the hand at the top |
| Difference > 180° | `360 − diff` returns the smaller arc |

---

## Approach Tags

`Clock Geometry` · `Angular Speed` · `Smaller Arc` · `Constant-Time Math`

---

*Day 45 of the LeetCode Daily Challenge*
