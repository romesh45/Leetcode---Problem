class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        # Absolute angle of each hand measured clockwise from 12 o'clock:
        #
        #   minute hand: 6° per minute              (360° / 60 min)
        #   hour hand:   30° per hour + 0.5° per min
        #     • 360° / 12 hours          = 30° per hour
        #     • the hour hand also creeps forward as minutes pass:
        #       30° over 60 min          = 0.5° per minute
        #
        # Two gotchas:
        #   • hour % 12  → at 12 o'clock the hour hand is at 0°, not 360°.
        #   • the +0.5°/min creep — forgetting it is THE classic bug
        #     (e.g. 3:30 the hour hand is at 105°, not 90°).
        minute_angle = minutes * 6
        hour_angle = (hour % 12) * 30 + minutes * 0.5

        # The hands cut the circle into two arcs summing to 360°; take the
        # smaller one.
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
