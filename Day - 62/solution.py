from typing import List

MOD = 10**9 + 7


class Solution:
    def pathsWithMaxScore(self, board: List[str]) -> List[int]:
        n = len(board)
        NEG_INF = float('-inf')

        # ── DP setup ─────────────────────────────────────────────────────────
        # dp_score[r][c] = maximum score collectible on any path from S to (r,c)
        # dp_count[r][c] = number of paths achieving that maximum score
        # Unreachable cells keep score = NEG_INF, count = 0.
        #
        # We move from S=(n-1,n-1) toward E=(0,0) via: up, left, up-left.
        # So the predecessors of (r,c) are the cells we stepped FROM:
        #   (r+1, c)  — came from below
        #   (r, c+1)  — came from the right
        #   (r+1,c+1) — came diagonally
        #
        # Process cells in decreasing (r,c) order so predecessors are always ready.
        #
        # Score contribution of a cell:
        #   'S' and 'E' contribute 0
        #   '1'..'9' contribute their digit value
        #   'X' is an obstacle — skip entirely

        dp_score = [[NEG_INF] * n for _ in range(n)]
        dp_count = [[0] * n for _ in range(n)]

        # Base case: standing at S, score = 0, one way to be here
        dp_score[n - 1][n - 1] = 0
        dp_count[n - 1][n - 1] = 1

        for r in range(n - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                if r == n - 1 and c == n - 1:
                    continue          # already initialised
                if board[r][c] == 'X':
                    continue          # obstacle — leave as unreachable

                val = 0 if board[r][c] in ('E', 'S') else int(board[r][c])

                # Aggregate over the three possible predecessors
                best_score = NEG_INF
                best_count = 0

                for dr, dc in [(1, 0), (0, 1), (1, 1)]:
                    pr, pc = r + dr, c + dc
                    if 0 <= pr < n and 0 <= pc < n:
                        if dp_score[pr][pc] == NEG_INF:
                            continue          # predecessor unreachable
                        s = dp_score[pr][pc] + val
                        cnt = dp_count[pr][pc]
                        if s > best_score:
                            best_score = s
                            best_count = cnt
                        elif s == best_score:
                            best_count = (best_count + cnt) % MOD

                if best_score != NEG_INF:
                    dp_score[r][c] = best_score
                    dp_count[r][c] = best_count % MOD

        # If E is unreachable, return [0, 0]
        if dp_score[0][0] == NEG_INF:
            return [0, 0]
        return [dp_score[0][0], dp_count[0][0]]


# ── Reference: DFS brute force (for cross-checking small boards) ─────────────
class SolutionBrute:
    def pathsWithMaxScore(self, board: List[str]) -> List[int]:
        n = len(board)
        results = []

        def dfs(r: int, c: int, score: int) -> None:
            v = 0 if board[r][c] in ('S', 'E') else int(board[r][c])
            total = score + v
            if r == 0 and c == 0:
                results.append(total)
                return
            for dr, dc in [(-1, 0), (0, -1), (-1, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and board[nr][nc] != 'X':
                    dfs(nr, nc, total)

        dfs(n - 1, n - 1, 0)
        if not results:
            return [0, 0]
        best = max(results)
        return [best, results.count(best) % (10**9 + 7)]


# ── Quick tests ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = Solution()

    print(sol.pathsWithMaxScore(["E23", "2X2", "12S"]))   # [7, 1]
    print(sol.pathsWithMaxScore(["E12", "1X1", "21S"]))   # [4, 2]
    print(sol.pathsWithMaxScore(["E11", "XXX", "11S"]))   # [0, 0]

    # Edge cases
    print(sol.pathsWithMaxScore(["E1", "1S"]))             # [1, 2]  (two equal paths)
    print(sol.pathsWithMaxScore(["ES"]))                   # [0, 1]  (1x... wait n>=2)
    print(sol.pathsWithMaxScore(["E9", "9S"]))             # [9, 2]

    # Randomised cross-check
    import random
    random.seed(0)
    ref = SolutionBrute()
    errors = 0
    for _ in range(1000):
        n = random.randint(2, 5)
        inner = ['X' if random.random() < 0.2 else str(random.randint(1, 9))
                 for _ in range(n * n - 2)]
        cells = ['E'] + inner + ['S']
        board = [''.join(cells[i * n:(i + 1) * n]) for i in range(n)]
        a = sol.pathsWithMaxScore(board)
        b = ref.pathsWithMaxScore(board)
        if a != b:
            if errors < 3:
                print(f"MISMATCH board={board}: got {a} expected {b}")
            errors += 1
    print("1000 random tests passed ✓" if not errors else f"errors: {errors}")

    # Timing on max-size board
    import time
    n = 100
    big = ["E" + "9" * (n - 2) + ("S" if i == 0 else "9") if i == 0
           else "9" * n for i in range(n)]
    big[-1] = "9" * (n - 1) + "S"
    big[0] = "E" + "9" * (n - 1)
    t0 = time.time()
    sol.pathsWithMaxScore(big)
    print(f"n=100 timing: {time.time()-t0:.3f}s")
