class Solution:
    def smallestNumber(self, num: str, t: int) -> str:
        # ---- 1. Factor t into powers of 2,3,5,7 (digit products only ever have these primes) ----
        tt = t
        a = 0
        while tt % 2 == 0:
            tt //= 2; a += 1
        b = 0
        while tt % 3 == 0:
            tt //= 3; b += 1
        c = 0
        while tt % 5 == 0:
            tt //= 5; c += 1
        d = 0
        while tt % 7 == 0:
            tt //= 7; d += 1
        if tt != 1:
            return "-1"

        A, B, C, D = a, b, c, d

        DIGIT_EXP = [None,
                     (0,0,0,0),  # 1
                     (1,0,0,0),  # 2
                     (0,1,0,0),  # 3
                     (2,0,0,0),  # 4
                     (0,0,1,0),  # 5
                     (1,1,0,0),  # 6
                     (0,0,0,1),  # 7
                     (3,0,0,0),  # 8
                     (0,2,0,0)]  # 9
        reducing_digits = DIGIT_EXP[2:10]

        # ---- 2. dist[a2,b2,c2,d2] = min # of digits (2-9) needed to cover a deficiency ----
        Bp1, Cp1, Dp1 = B+1, C+1, D+1
        size = (A+1)*Bp1*Cp1*Dp1
        dist = [0]*size

        def idx(a2,b2,c2,d2):
            return ((a2*Bp1 + b2)*Cp1 + c2)*Dp1 + d2

        INF = float('inf')
        for a2 in range(A+1):
            base_a = a2*Bp1
            for b2 in range(B+1):
                base_ab = (base_a+b2)*Cp1
                for c2 in range(C+1):
                    base_abc = (base_ab+c2)*Dp1
                    for d2 in range(D+1):
                        if a2==0 and b2==0 and c2==0 and d2==0:
                            continue
                        cur_idx = base_abc + d2
                        best = INF
                        for (e2,e3,e5,e7) in reducing_digits:
                            na = a2-e2
                            if na<0: na=0
                            nb = b2-e3
                            if nb<0: nb=0
                            nc = c2-e5
                            if nc<0: nc=0
                            nd = d2-e7
                            if nd<0: nd=0
                            if na==a2 and nb==b2 and nc==c2 and nd==d2:
                                continue
                            cand = dist[idx(na,nb,nc,nd)] + 1
                            if cand < best:
                                best = cand
                        dist[cur_idx] = best

        def get_dist(ra,rb,rc,rd):
            return dist[idx(ra,rb,rc,rd)]

        n = len(num)
        digits = [ord(ch)-48 for ch in num]

        # ---- 3. Prefix exponent sums, and how far a zero-free prefix can extend ----
        first_zero = -1
        for i, dg in enumerate(digits):
            if dg == 0:
                first_zero = i
                break
        limit = first_zero if first_zero != -1 else n

        P2 = [0]*(limit+1)
        P3 = [0]*(limit+1)
        P5 = [0]*(limit+1)
        P7 = [0]*(limit+1)
        for i in range(1, limit+1):
            e2,e3,e5,e7 = DIGIT_EXP[digits[i-1]]
            P2[i] = P2[i-1]+e2
            P3[i] = P3[i-1]+e3
            P5[i] = P5[i-1]+e5
            P7[i] = P7[i-1]+e7

        def build_suffix(ra, rb, rc, rd, m):
            # smallest zero-free length-m sequence covering deficiency (ra,rb,rc,rd)
            res = [0]*m
            for pos in range(m):
                rem_after = m - pos - 1
                for dg in range(1,10):
                    e2,e3,e5,e7 = DIGIT_EXP[dg]
                    na = ra-e2
                    if na<0: na=0
                    nb = rb-e3
                    if nb<0: nb=0
                    nc = rc-e5
                    if nc<0: nc=0
                    nd = rd-e7
                    if nd<0: nd=0
                    if get_dist(na,nb,nc,nd) <= rem_after:
                        res[pos] = dg
                        ra,rb,rc,rd = na,nb,nc,nd
                        break
            return res

        # ---- 4. Try S == num exactly ----
        if limit == n:
            ra = A - P2[n]
            if ra<0: ra=0
            rb = B - P3[n]
            if rb<0: rb=0
            rc = C - P5[n]
            if rc<0: rc=0
            rd = D - P7[n]
            if rd<0: rd=0
            if ra==0 and rb==0 and rc==0 and rd==0:
                return num

        # ---- 5. Try same length: match num's prefix as long as possible, bump one digit up ----
        jmax = min(limit, n-1)

        found = False
        chosen_j = -1
        chosen_digit = None
        chosen_state = None

        for j in range(jmax, -1, -1):
            p2j,p3j,p5j,p7j = P2[j],P3[j],P5[j],P7[j]
            m = n-1-j
            start_digit = digits[j]+1
            for dg in range(start_digit,10):
                e2,e3,e5,e7 = DIGIT_EXP[dg]
                ra = A-(p2j+e2)
                if ra<0: ra=0
                rb = B-(p3j+e3)
                if rb<0: rb=0
                rc = C-(p5j+e5)
                if rc<0: rc=0
                rd = D-(p7j+e7)
                if rd<0: rd=0
                if get_dist(ra,rb,rc,rd) <= m:
                    found = True
                    chosen_j = j
                    chosen_digit = dg
                    chosen_state = (ra,rb,rc,rd,m)
                    break
            if found:
                break

        if found:
            ra,rb,rc,rd,m = chosen_state
            suffix = build_suffix(ra,rb,rc,rd,m)
            prefix_str = num[:chosen_j]
            return prefix_str + str(chosen_digit) + ''.join(map(str,suffix))

        # ---- 6. No same-length answer: need a longer number ----
        L = n+1
        needed = get_dist(A,B,C,D)
        if needed > L:
            L = needed
        full = build_suffix(A,B,C,D,L)
        return ''.join(map(str,full))


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("1234", 256, "1488"),
        ("12355", 50, "12355"),
        ("11111", 26, "-1"),
    ]
    for num, t, expected in tests:
        got = sol.smallestNumber(num, t)
        status = "OK" if got == expected else "FAIL"
        print(f"{status}: num={num} t={t} -> got={got} expected={expected}")
