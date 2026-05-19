from typing import List


class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        # Two-pointer scan — both arrays are sorted non-decreasing, so we
        # never need to back up. Each step either finds the answer or
        # eliminates one element from consideration.
        i, j = 0, 0
        n1, n2 = len(nums1), len(nums2)

        while i < n1 and j < n2:
            if nums1[i] == nums2[j]:
                # First match is necessarily the minimum common value:
                # both pointers have only moved forward through sorted
                # values, so any earlier common value would have been
                # caught first.
                return nums1[i]

            elif nums1[i] < nums2[j]:
                # nums1[i] is smaller than every nums2[k] for k >= j
                # (nums2 only grows), so nums1[i] can't be common.
                # Advance i.
                i += 1

            else:
                # Symmetric: nums2[j] is too small. Advance j.
                j += 1

        # One array exhausted without ever finding a match → no common value.
        return -1


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.getCommon([1, 2, 3], [2, 4]))                  # 2
    print(sol.getCommon([1, 2, 3, 6], [2, 3, 4, 5]))         # 2
    print(sol.getCommon([1, 2, 3], [4, 5, 6]))               # -1
    print(sol.getCommon([1], [1]))                           # 1
    print(sol.getCommon([1, 1, 1], [2, 2, 2]))               # -1
    print(sol.getCommon([1, 1, 2], [2, 2, 2]))               # 2
    print(sol.getCommon([5, 10, 15], [1, 2, 3, 15, 20]))     # 15
