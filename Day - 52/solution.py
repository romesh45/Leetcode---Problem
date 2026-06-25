from typing import List


class Solution:
    def countSubarrays(self, nums: List[int], target: int) -> int:
        # Reduce to a prefix-sum problem.
        #
        # "target is majority in nums[i..j]"
        #   ⟺ count(target) > (j - i + 1) / 2
        #   ⟺ count(target) > count(non-target)
        #   ⟺ count(target) - count(non-target) > 0
        #
        # Map each element: +1 if == target, -1 otherwise.
        # Let prefix[k] = sum of mapped[0..k-1].
        #
        # Then for subarray nums[i..j]:
        #   mapped sum = prefix[j+1] - prefix[i]
        #
        # Target is majority  ⟺  prefix[j+1] - prefix[i] > 0
        #                     ⟺  prefix[j+1] > prefix[i]
        #
        # For every right endpoint j, count left endpoints i ∈ [0, j]
        # with prefix[i] < prefix[j+1].
        #
        # n ≤ 1000 → O(n²) is fine.

        n = len(nums)

        # Build prefix sums of the ±1 mapped array.
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + (1 if nums[i] == target else -1)

        count = 0
        for j in range(n):              # right endpoint (inclusive)
            pj = prefix[j + 1]
            for i in range(j + 1):     # left endpoint
                if pj > prefix[i]:
                    count += 1

        return count


# ── Reference: explicit brute force ──────────────────────────────────────────
class SolutionBrute:
    def countSubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        count = 0
        for i in range(n):
            for j in range(i, n):
                sub = nums[i:j + 1]
                if sub.count(target) * 2 > len(sub):
                    count += 1
        return count


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.countSubarrays([1, 2, 2, 3], 2))   # 5
    print(sol.countSubarrays([1, 1, 1, 1], 1))   # 10
    print(sol.countSubarrays([1, 2, 3], 4))       # 0

    # Edge cases
    print(sol.countSubarrays([5], 5))             # 1  single target
    print(sol.countSubarrays([5], 3))             # 0  single non-target
    print(sol.countSubarrays([2, 2, 2, 2], 2))   # 10 all target

    # Randomised cross-check against brute force
    import random
    random.seed(42)
    ref = SolutionBrute()
    for _ in range(500):
        n = random.randint(1, 20)
        nums = [random.randint(1, 5) for _ in range(n)]
        t = random.randint(1, 5)
        a = sol.countSubarrays(nums, t)
        b = ref.countSubarrays(nums, t)
        assert a == b, f"MISMATCH nums={nums} target={t}: got {a} expected {b}"
    print("randomised cross-check passed ✓")
