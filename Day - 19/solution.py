from typing import List


class Solution:
    def check(self, nums: List[int]) -> bool:
        # A non-decreasing array, rotated by any amount, has the shape
        # "one ascending run, then another ascending run" — joined circularly.
        # So when scanned as a circular array there can be AT MOST ONE "drop":
        # a position i where nums[i] > nums[(i + 1) % n].
        #
        # Using (i + 1) % n includes the wrap-around comparison nums[n-1] vs
        # nums[0], which is the right thing in all cases:
        #   • If the array is unrotated (e.g. [1,2,3]), the wrap nums[n-1] →
        #     nums[0] is itself the single allowed drop.
        #   • If rotated (e.g. [3,4,5,1,2]), the drop sits inside the array
        #     (5 → 1) and the wrap is fine (2 < 3 → no extra drop).
        # In both cases, total drops ≤ 1 ⇔ valid.
        n = len(nums)
        drops = 0
        for i in range(n):
            if nums[i] > nums[(i + 1) % n]:
                drops += 1
                if drops > 1:           # short-circuit as soon as we exceed 1
                    return False
        return True


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.check([3, 4, 5, 1, 2]))      # True
    print(sol.check([2, 1, 3, 4]))         # False
    print(sol.check([1, 2, 3]))            # True
    print(sol.check([1]))                  # True
    print(sol.check([1, 1, 1]))            # True
    print(sol.check([2, 1]))               # True   (rotated [1, 2])
    print(sol.check([6, 10, 6]))           # True   ([6,6,10] rotated by 2 → single drop 10→6)
    print(sol.check([1, 3, 2]))            # False  (drops: 3>2 and wrap 2>1 → 2 drops)
