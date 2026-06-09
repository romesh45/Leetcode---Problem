from typing import List


class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        # Stable 3-way partition.
        # Scan left to right ONCE, bucketing into:
        #   less    — elements < pivot, in original order
        #   greater — elements > pivot, in original order
        #   equal_count — how many elements == pivot (all identical, just count)
        # Then stitch: [less...] + [pivot repeated] + [greater...].
        less = []
        greater = []
        equal_count = 0

        for x in nums:
            if x < pivot:
                less.append(x)        # append in scan order ⇒ relative order kept
            elif x > pivot:
                greater.append(x)     # same — relative order kept
            else:
                equal_count += 1      # every pivot value is identical → count only

        return less + [pivot] * equal_count + greater


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.pivotArray([9, 12, 5, 10, 14, 3, 10], 10))   # [9, 5, 3, 10, 10, 12, 14]
    print(sol.pivotArray([-3, 4, 3, 2], 2))                # [-3, 2, 4, 3]
    print(sol.pivotArray([1], 1))                          # [1]
    print(sol.pivotArray([3, 3, 3], 3))                    # [3, 3, 3]
    print(sol.pivotArray([5, 1, 5, 1, 5], 5))              # [1, 1, 5, 5, 5]
    print(sol.pivotArray([2, 1, 3], 2))                    # [1, 2, 3]
    print(sol.pivotArray([4, 5, 6, 1], 4))                 # [1, 4, 5, 6]
