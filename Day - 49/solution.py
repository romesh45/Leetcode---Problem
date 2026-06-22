from collections import Counter


class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        # "balloon" recipe: b×1, a×1, l×2, o×2, n×1.
        # Each required letter alone supports have[ch] // need[ch] full words.
        # The scarcest letter is the bottleneck → answer is the MIN ratio.
        #
        # Using Counter("balloon") for `need` bakes in the ×2 for 'l' and 'o',
        # so the integer division handles the doubled letters automatically
        # (forgetting to halve l/o is the classic bug here).
        have = Counter(text)
        need = Counter("balloon")        # {b:1, a:1, l:2, o:2, n:1}

        # Counter returns 0 for missing letters, so an absent ingredient
        # correctly drives the answer to 0.
        return min(have[ch] // cnt for ch, cnt in need.items())


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxNumberOfBalloons("nlaebolko"))          # 1
    print(sol.maxNumberOfBalloons("loonbalxballpoon"))   # 2
    print(sol.maxNumberOfBalloons("leetcode"))           # 0
    print(sol.maxNumberOfBalloons("balloon"))            # 1
    print(sol.maxNumberOfBalloons("balon"))              # 0  (only one l and one o)
    print(sol.maxNumberOfBalloons("balllllloooonn"))     # 1  (b:1 and a:1 are the bottleneck)
    print(sol.maxNumberOfBalloons("balloonballoon"))     # 2
