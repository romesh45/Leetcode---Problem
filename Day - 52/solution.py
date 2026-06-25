class Solution:
    def countSubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + (1 if nums[i] == target else -1)
        count = 0
        for j in range(n):              
            pj = prefix[j + 1]
            for i in range(j + 1):     
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
