from typing import List


class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        i, j = 0, 0
        n1, n2 = len(nums1), len(nums2)

        while i < n1 and j < n2:
            if nums1[i] == nums2[j]:
                return nums1[i]

            elif nums1[i] < nums2[j]:
                i += 1

            else:
                j += 1
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
