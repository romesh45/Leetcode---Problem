from typing import List


class Solution:
    def validSequence(self, word1: str, word2: str) -> List[int]:
        n, m = len(word1), len(word2)

        # R[j] = largest starting index x such that word2[j:] is an EXACT
        # subsequence of word1[x:]. One backward pass (greedy rightmost match).
        R = [-1] * (m + 1)
        R[m] = n
        j = m - 1
        for i in range(n - 1, -1, -1):
            if j >= 0 and word1[i] == word2[j]:
                R[j] = i
                j -= 1
            if j < 0:
                break

        result = []
        ptr = 0
        jj = 0
        mismatch_used = False
        while jj < m:
            if ptr >= n:
                return []
            if word1[ptr] == word2[jj]:
                result.append(ptr)
                ptr += 1
                jj += 1
            elif not mismatch_used and ptr + 1 <= R[jj + 1]:
                result.append(ptr)
                ptr += 1
                jj += 1
                mismatch_used = True
            else:
                ptr += 1
        return result


# Quick tests
if __name__ == "__main__":
    sol = Solution()

    print(sol.validSequence("vbcca", "abc"))    # [0, 1, 2]
    print(sol.validSequence("bacdc", "abc"))    # [1, 2, 4]
    print(sol.validSequence("aaaaaa", "aaabc")) # []
    print(sol.validSequence("abc", "ab"))       # [0, 1]
