class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        minute_angle = minutes * 6
        hour_angle = (hour % 12) * 30 + minutes * 0.5
        diff = abs(hour_angle - minute_angle)
        return min(diff, 360 - diff)


# ── Quick tests ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()
    print(sol.angleClock(12, 30))   # 165
    print(sol.angleClock(3, 30))    # 75
    print(sol.angleClock(3, 15))    # 7.5
    print(sol.angleClock(12, 0))    # 0    (both hands at the top)
    print(sol.angleClock(6, 0))     # 180  (straight line)
    print(sol.angleClock(9, 0))     # 90
    print(sol.angleClock(1, 0))     # 30
    print(sol.angleClock(12, 1))    # 5.5  (minute=6°, hour=0.5° → diff 5.5)
