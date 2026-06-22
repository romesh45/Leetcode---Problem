class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        have = Counter(text)
        need = Counter("balloon")        
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
