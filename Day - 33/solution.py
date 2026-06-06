class Solution:
    def leftRightDifference(self, nums: List[int]) -> List[int]:
        total = sum(nums)
        left = 0
        answer = []
        for x in nums:
            right = total - left - x       
            answer.append(abs(left - right))
            left += x                     
        return answer


# ── Quick tests ─────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.leftRightDifference([10, 4, 8, 3]))   # [15, 1, 11, 22]
    print(sol.leftRightDifference([1]))             # [0]
    print(sol.leftRightDifference([1, 2, 3, 4, 5])) # [14, 11, 6, 1, 10]
    print(sol.leftRightDifference([5, 5]))          # [5, 5]
    print(sol.leftRightDifference([100]))           # [0]
    print(sol.leftRightDifference([2, 2, 2, 2]))    # [6, 2, 2, 6]
