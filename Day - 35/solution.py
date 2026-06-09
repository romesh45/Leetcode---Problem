class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        less = []
        greater = []
        equal_count = 0
        for x in nums:
            if x < pivot:
                less.append(x)        
            elif x > pivot:
                greater.append(x)     
            else:
                equal_count += 1      
        return less + [pivot] * equal_count + greater


# ── Quick tests ──────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.pivotArray([9, 12, 5, 10, 14, 3, 10], 10))   # [9, 5, 3, 10, 10, 12, 14]
    print(sol.pivotArray([-3, 4, 3, 2], 2))                # [-3, 2, 4, 3]
    print(sol.pivotArray([1], 1))                          # [1]
    print(sol.pivotArray([3, 3, 3], 3))                    # [3, 3, 3]
    print(sol.pivotArray([5, 1, 5, 1, 5], 5))              # [1, 1, 5, 5, 5]
    print(sol.pivotArray([2, 1, 3], 2))                    # [1, 2, 3]
    print(sol.pivotArray([4, 5, 6, 1], 4))                 # [1, 4, 5, 6]
