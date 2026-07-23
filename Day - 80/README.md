# 3501. Maximize Active Section with Trade II

[LeetCode problem](https://leetcode.com/problems/maximize-active-section-with-trade-ii/) · Hard

## Problem summary

You're given a binary string `s` (`'1'` = active, `'0'` = inactive). You may perform **at most one trade**: pick a maximal run of `'1'`s that has `'0'`s on both sides, flip it to `'0'`s, then pick a maximal run of `'0'`s that now has `'1'`s on both sides and flip it to `'1'`s.

You're also given `queries`, where each `queries[i] = [l, r]` asks: if the trade could only be applied inside the substring `s[l..r]` — treated in isolation and padded with a `'1'` on each side (`t = '1' + s[l..r] + '1'`, and those padding `1`s don't count toward the answer) — what's the maximum number of active sections in the whole string `s` afterward?

Queries are independent; `s` itself is never actually modified between them.

## Approach

**Key simplification.** Nothing outside `[l, r]` ever changes, so:

```
answer(l, r) = (total ones in s) + gain(l, r)
```

where `gain(l, r)` is the extra `1`s created by the best trade inside the padded window (0 if no trade helps).

**Only adjacent merges matter.** A trade zeroes one interior run of `1`s, `Z`, then converts some run of `0`s back to `1`s. It's tempting to think a small `Z` could be sacrificed to unlock a large, *unrelated* `0`-run elsewhere — but that's never better than zeroing whichever interior `1`-run already sits next to that large `0`-run: its own other neighboring `0`-run comes along for free, so the result is at least as good. So the optimal gain always comes from a single interior `1`-run merging its two immediate `0`-neighbors:

```
gain(l, r) = max over every interior 1-run Z strictly inside (l, r) of:
             size(0-run to the left of Z) + size(0-run to the right of Z)
```

with sizes clipped to `[l, r]` wherever a `0`-run is the first or last one touching the query boundary.

**Implementation.**
1. Extract every maximal `0`-run of `s` once, up front.
2. Build `pair_sum[i] = size(zero_run[i]) + size(zero_run[i+1])` — the gain from the interior `1`-run between two consecutive `0`-runs — stored in a sparse table for O(1) range-max queries.
3. Per query: binary-search for the first/last `0`-run touching `[l, r]`, handle the (possibly clipped) boundary pair(s) directly, and take a range-max over everything strictly in between.

**Complexity:** `O((n + q) log n)` time, `O(n log n)` space.

Verified against a brute force that tries every possible trade — including non-adjacent ones — exhaustively over all binary strings of length 1–12 and every query range (~550,000 checks), plus random strings up to length 40 and the full `n = q = 10^5` case.

## Files

- [`solution.py`](./solution.py) — the `Solution` class
