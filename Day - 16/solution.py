class Solution:
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        n = len(A)
        C = [0] * n
        seen_A = 0
        seen_B = 0

        for i in range(n):
            seen_A |= (1 << A[i])
            seen_B |= (1 << B[i])
            C[i] = bin(seen_A & seen_B).count("1")

        return C


# ── Alternative: set-based (more readable, same complexity) ────────



class SolutionSets:
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        seen_A, seen_B = set(), set()
        C = []
        for a, b in zip(A, B):
            seen_A.add(a)
            seen_B.add(b)
            C.append(len(seen_A & seen_B))
        return C


# ── Quick tests ────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.findThePrefixCommonArray([1, 3, 2, 4], [3, 1, 2, 4]))   # [0, 2, 3, 4]
    print(sol.findThePrefixCommonArray([2, 3, 1], [3, 1, 2]))         # [0, 1, 3]
    print(sol.findThePrefixCommonArray([1], [1]))                     # [1]
    print(sol.findThePrefixCommonArray([1, 2], [2, 1]))               # [0, 2]
    print(sol.findThePrefixCommonArray([1, 2, 3], [1, 2, 3]))         # [1, 2, 3]

    sol2 = SolutionSets()
    print(sol2.findThePrefixCommonArray([1, 3, 2, 4], [3, 1, 2, 4]))  # [0, 2, 3, 4]
    print(sol2.findThePrefixCommonArray([2, 3, 1], [3, 1, 2]))        # [0, 1, 3]
