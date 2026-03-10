"""
================================================================================
  DYNAMIC PROGRAMMING TUTORIAL — 10 Progressive Examples
================================================================================

A comprehensive, visual guide to dynamic programming with step-by-step ASCII
table visualizations, detailed explanations, and Python implementations.

Usage:
    python dp_tutorial.py          # Run all 10 examples
    python dp_tutorial.py 1        # Run just Example 1 (Fibonacci)
    python dp_tutorial.py 3 7      # Run Examples 3 and 7

Examples (progressive difficulty):
    1. Fibonacci Numbers          — Intro to memoization & tabulation
    2. Climbing Stairs            — State definition, Fibonacci variant
    3. Coin Change (Min Coins)    — Iterating over choices
    4. 0/1 Knapsack              — 2D DP, take-or-leave pattern
    5. Longest Common Subsequence — String DP, match/no-match
    6. Edit Distance             — Three operations (insert/delete/replace)
    7. Matrix Chain Multiply     — Interval DP, diagonal fill
    8. Longest Increasing Subseq — 1D DP with inner loop
    9. Rod Cutting               — Unbounded knapsack, cut reconstruction
   10. Unique Paths in Grid      — 2D grid DP with obstacles

Requirements: Python 3.6+  (no external dependencies)
"""

import sys
import time


# =============================================================================
#  SHARED UTILITIES
# =============================================================================

def section_header(num, title):
    """Print a clear visual separator between examples."""
    print()
    print("=" * 70)
    print(f"  EXAMPLE {num}: {title}")
    print("=" * 70)
    print()


def print_1d_table(table, labels=None, highlight=None, title=""):
    """Render a 1D list as a formatted ASCII table.

    Args:
        table: list of values
        labels: optional list of column labels (same length as table)
        highlight: index to mark with [*val*]
        title: optional title above the table
    """
    if title:
        print(f"  {title}")

    # Determine column widths
    str_vals = []
    for i, v in enumerate(table):
        s = str(v)
        if i == highlight:
            s = f"[*{v}*]"
        str_vals.append(s)

    if labels is not None:
        label_strs = [str(l) for l in labels]
        widths = [max(len(sv), len(lb)) + 1 for sv, lb in zip(str_vals, label_strs)]
        print("  " + "".join(lb.rjust(w) for lb, w in zip(label_strs, widths)))
        print("  " + "".join(sv.rjust(w) for sv, w in zip(str_vals, widths)))
    else:
        widths = [len(sv) + 1 for sv in str_vals]
        print("  " + "".join(sv.rjust(w) for sv, w in zip(str_vals, widths)))
    print()


def print_2d_table(table, row_labels=None, col_labels=None, highlight=None, title=""):
    """Render a 2D list as a formatted ASCII table.

    Args:
        table: 2D list of values
        row_labels: optional list of row labels
        col_labels: optional list of column labels
        highlight: (row, col) tuple to mark with [*val*]
        title: optional title above the table
    """
    if title:
        print(f"  {title}")

    rows = len(table)
    cols = len(table[0]) if rows > 0 else 0

    # Build string grid
    str_grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            v = table[r][c]
            if highlight and (r, c) == highlight:
                row.append(f"[*{v}*]")
            else:
                row.append(str(v))
        str_grid.append(row)

    # Compute column widths
    col_widths = []
    for c in range(cols):
        w = 0
        if col_labels:
            w = len(str(col_labels[c]))
        for r in range(rows):
            w = max(w, len(str_grid[r][c]))
        col_widths.append(w + 1)

    row_label_width = 0
    if row_labels:
        row_label_width = max(len(str(rl)) for rl in row_labels) + 2

    # Print column headers
    if col_labels:
        header = " " * row_label_width
        header += "".join(str(cl).rjust(cw) for cl, cw in zip(col_labels, col_widths))
        print(f"  {header}")

    # Print rows
    for r in range(rows):
        prefix = ""
        if row_labels:
            prefix = str(row_labels[r]).rjust(row_label_width - 1) + " "
        row_str = "".join(str_grid[r][c].rjust(col_widths[c]) for c in range(cols))
        print(f"  {prefix}{row_str}")
    print()


def complexity_box(time_cplx, space_cplx, notes=""):
    """Print a formatted complexity analysis box."""
    print("  ┌─ Complexity ─────────────────────────────────┐")
    print(f"  │  Time:  {time_cplx:<40s}│")
    print(f"  │  Space: {space_cplx:<40s}│")
    if notes:
        print(f"  │  Note:  {notes:<40s}│")
    print("  └─────────────────────────────────────────────────┘")
    print()


# =============================================================================
#  EXAMPLE 1: Fibonacci Numbers
# =============================================================================

def example_1_fibonacci():
    section_header(1, "Fibonacci Numbers")

    print("  PROBLEM: Compute the n-th Fibonacci number.")
    print("  F(0)=0, F(1)=1, F(n) = F(n-1) + F(n-2)")
    print()
    print("  WHY DP? Naive recursion recomputes the same subproblems:")
    print()
    print("                        fib(6)")
    print("                     /          \\")
    print("                fib(5)          fib(4)   <-- computed twice!")
    print("               /     \\          /     \\")
    print("          fib(4)   fib(3)  fib(3)  fib(2)")
    print("          /   \\    /   \\    /   \\")
    print("      fib(3) fib(2) ...  ...  ...")
    print()
    print("  The tree has O(2^n) nodes — exponential blowup!")
    print("  DP eliminates redundancy by storing computed results.")
    print()

    n = 10

    # --- Top-Down (Memoization) ---
    print("  ── Approach 1: Top-Down (Memoization) ──")
    print("  Store results in a dictionary as we recurse.")
    print()

    memo = {}
    call_count = [0]

    def fib_memo(k):
        call_count[0] += 1
        if k in memo:
            return memo[k]
        if k <= 1:
            memo[k] = k
            return k
        memo[k] = fib_memo(k - 1) + fib_memo(k - 2)
        return memo[k]

    result_td = fib_memo(n)
    print(f"  fib({n}) = {result_td}  (total function calls: {call_count[0]})")
    print()

    # --- Bottom-Up (Tabulation) ---
    print("  ── Approach 2: Bottom-Up (Tabulation) ──")
    print("  Fill a table from left to right.")
    print()
    print("  Recurrence: dp[i] = dp[i-1] + dp[i-2]")
    print()

    dp = [0] * (n + 1)
    dp[1] = 1
    print("  Step-by-step table filling:")
    print_1d_table(dp, labels=list(range(n + 1)), title="Initial:")

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        if i <= 6 or i == n:
            print_1d_table(dp, labels=list(range(n + 1)), highlight=i,
                           title=f"dp[{i}] = dp[{i-1}] + dp[{i-2}] = {dp[i-1]} + {dp[i-2]} = {dp[i]}:")

    print(f"  Result: fib({n}) = {dp[n]}")
    print()

    # --- Space-Optimized ---
    print("  ── Approach 3: Space-Optimized ──")
    print("  We only need the last two values — no array needed!")
    print()

    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    print(f"  fib({n}) = {b}  (O(1) space)")
    print()

    complexity_box("O(n)", "O(n) tabulation / O(1) optimized",
                   "Naive recursion is O(2^n)")


# =============================================================================
#  EXAMPLE 2: Climbing Stairs
# =============================================================================

def example_2_climbing_stairs():
    section_header(2, "Climbing Stairs")

    print("  PROBLEM: You are climbing a staircase with n steps.")
    print("  Each time you can climb 1 or 2 steps.")
    print("  How many distinct ways can you reach the top?")
    print()
    print("  Staircase visualization (n=5):")
    print()
    print("      Step 5:  ___          GOAL")
    print("      Step 4: |  |___")
    print("      Step 3: |     |___")
    print("      Step 2: |        |___")
    print("      Step 1: |           |___")
    print("      Step 0: |              |  START")
    print()
    print("  At each step, you choose: go up 1 or go up 2.")
    print("  dp[i] = number of ways to reach step i")
    print()
    print("  Recurrence: dp[i] = dp[i-1] + dp[i-2]")
    print("  (ways via 1-step from i-1) + (ways via 2-step from i-2)")
    print()

    n = 7

    # --- Top-Down ---
    print("  ── Top-Down (Memoization) ──")

    def climb_memo(k, memo={}):
        if k in memo:
            return memo[k]
        if k <= 1:
            return 1
        memo[k] = climb_memo(k - 1) + climb_memo(k - 2)
        return memo[k]

    print(f"  climb({n}) = {climb_memo(n)}")
    print()

    # --- Bottom-Up ---
    print("  ── Bottom-Up (Tabulation) ──")

    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1

    print_1d_table(dp, labels=[f"s{i}" for i in range(n + 1)], title="Initial: dp[0]=1, dp[1]=1")

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        print_1d_table(dp, labels=[f"s{i}" for i in range(n + 1)], highlight=i,
                       title=f"dp[{i}] = dp[{i-1}] + dp[{i-2}] = {dp[i-1]} + {dp[i-2]} = {dp[i]}:")

    print(f"  Result: {dp[n]} distinct ways to climb {n} stairs")
    print()

    complexity_box("O(n)", "O(n) tabulation / O(1) optimized",
                   "Same recurrence as Fibonacci!")


# =============================================================================
#  EXAMPLE 3: Coin Change (Minimum Coins)
# =============================================================================

def example_3_coin_change():
    section_header(3, "Coin Change (Minimum Coins)")

    print("  PROBLEM: Given coin denominations and a target amount,")
    print("  find the minimum number of coins needed to make the amount.")
    print("  You have unlimited coins of each denomination.")
    print()

    coins = [1, 5, 6]
    amount = 11

    print(f"  Coins: {coins}     Target amount: {amount}")
    print()
    print("  Recurrence:")
    print("  dp[a] = min(dp[a - coin] + 1) for each coin <= a")
    print("  dp[0] = 0  (base case: 0 coins to make amount 0)")
    print()

    # --- Top-Down ---
    print("  ── Top-Down (Memoization) ──")

    def coin_change_memo(coins, amount):
        memo = {}

        def helper(rem):
            if rem == 0:
                return 0
            if rem < 0:
                return float('inf')
            if rem in memo:
                return memo[rem]
            best = float('inf')
            for c in coins:
                best = min(best, helper(rem - c) + 1)
            memo[rem] = best
            return best

        result = helper(amount)
        return result if result != float('inf') else -1

    print(f"  min_coins({amount}) = {coin_change_memo(coins, amount)}")
    print()

    # --- Bottom-Up ---
    print("  ── Bottom-Up (Tabulation) ──")

    INF = float('inf')
    dp = [0] + [INF] * amount
    choice = [-1] * (amount + 1)  # track which coin was used

    print_1d_table(
        [0 if v == 0 else "∞" for v in dp],
        labels=list(range(amount + 1)),
        title="Initial: dp[0]=0, rest=∞"
    )

    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                choice[a] = c

        display = [v if v != INF else "∞" for v in dp]
        if a <= 7 or a == amount:
            detail = ", ".join(
                f"dp[{a}-{c}]+1={dp[a-c]+1 if a-c >= 0 and dp[a-c] != INF else '∞'}"
                for c in coins if c <= a
            )
            print_1d_table(display, labels=list(range(amount + 1)), highlight=a,
                           title=f"dp[{a}] = min({detail}) = {dp[a]}:")

    print(f"  Result: min_coins({amount}) = {dp[amount]}")
    print()

    # Backtrack to find which coins were used
    print("  Coins used (backtracking):")
    used = []
    rem = amount
    while rem > 0:
        used.append(choice[rem])
        rem -= choice[rem]
    print(f"  {amount} = {' + '.join(str(c) for c in used)}")
    print()

    complexity_box("O(amount × len(coins))", "O(amount)")


# =============================================================================
#  EXAMPLE 4: 0/1 Knapsack
# =============================================================================

def example_4_knapsack():
    section_header(4, "0/1 Knapsack")

    print("  PROBLEM: Given items with weights and values, and a knapsack")
    print("  with a weight capacity, maximize the total value you can carry.")
    print("  Each item can be taken at most once (0/1 choice).")
    print()

    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    n = len(weights)

    print(f"  Items:")
    for i in range(n):
        print(f"    Item {i}: weight={weights[i]}, value={values[i]}")
    print(f"  Knapsack capacity: {capacity}")
    print()
    print("  Recurrence:")
    print("  dp[i][w] = max(dp[i-1][w],                   # skip item i")
    print("                 dp[i-1][w-wt[i]] + val[i])     # take item i")
    print()

    # --- Bottom-Up ---
    print("  ── Bottom-Up (Tabulation) ──")

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    col_labels = ["cap"] + list(range(capacity + 1))
    row_labels = ["--"] + [f"i{i}(w{weights[i]},v{values[i]})" for i in range(n)]

    for i in range(1, n + 1):
        wi, vi = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # skip
            if wi <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wi] + vi)  # take

        print_2d_table(dp, row_labels=row_labels,
                       col_labels=list(range(capacity + 1)),
                       title=f"After considering item {i-1} (w={wi}, v={vi}):")

    print(f"  Maximum value: {dp[n][capacity]}")
    print()

    # Backtrack to find which items were selected
    print("  Items selected (backtracking):")
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    selected.reverse()
    print(f"  Items: {selected}")
    total_w = sum(weights[i] for i in selected)
    total_v = sum(values[i] for i in selected)
    print(f"  Total weight: {total_w}, Total value: {total_v}")
    print()

    # --- Top-Down ---
    print("  ── Top-Down (Memoization) ──")

    def knapsack_memo(weights, values, capacity):
        memo = {}

        def helper(i, w):
            if i == 0 or w == 0:
                return 0
            if (i, w) in memo:
                return memo[(i, w)]
            if weights[i - 1] > w:
                result = helper(i - 1, w)
            else:
                result = max(helper(i - 1, w),
                             helper(i - 1, w - weights[i - 1]) + values[i - 1])
            memo[(i, w)] = result
            return result

        return helper(len(weights), capacity)

    print(f"  max_value = {knapsack_memo(weights, values, capacity)}")
    print()

    complexity_box("O(n × W)", "O(n × W)",
                   "W = capacity, can optimize space to O(W)")


# =============================================================================
#  EXAMPLE 5: Longest Common Subsequence (LCS)
# =============================================================================

def example_5_lcs():
    section_header(5, "Longest Common Subsequence (LCS)")

    print("  PROBLEM: Given two strings, find the length of their")
    print("  longest common subsequence (characters in order, not contiguous).")
    print()

    s1 = "AGGTAB"
    s2 = "GXTXAYB"

    print(f'  String 1: "{s1}"')
    print(f'  String 2: "{s2}"')
    print()
    print("  Recurrence:")
    print("  If s1[i-1] == s2[j-1]:  dp[i][j] = dp[i-1][j-1] + 1   (match!)")
    print("  Else:                   dp[i][j] = max(dp[i-1][j], dp[i][j-1])")
    print()

    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    col_labels = ['""'] + list(s2)
    row_labels = ['""'] + list(s1)

    print("  ── Bottom-Up (Tabulation) — Step-by-Step ──")
    print()

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Print table after each row
        match_info = ""
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                match_info = f" ('{s1[i-1]}' matched!)"
                break
        print_2d_table(dp, row_labels=row_labels, col_labels=col_labels,
                       title=f"Row '{s1[i-1]}'{match_info}:")

    print(f"  LCS length: {dp[m][n]}")
    print()

    # Reconstruct the LCS
    print("  Reconstructing LCS (backtracking):")
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs.reverse()
    print(f'  LCS: "{"".join(lcs)}"')
    print()

    # --- Top-Down ---
    print("  ── Top-Down (Memoization) ──")

    def lcs_memo(s1, s2):
        memo = {}

        def helper(i, j):
            if i == 0 or j == 0:
                return 0
            if (i, j) in memo:
                return memo[(i, j)]
            if s1[i - 1] == s2[j - 1]:
                memo[(i, j)] = helper(i - 1, j - 1) + 1
            else:
                memo[(i, j)] = max(helper(i - 1, j), helper(i, j - 1))
            return memo[(i, j)]

        return helper(len(s1), len(s2))

    print(f"  LCS length: {lcs_memo(s1, s2)}")
    print()

    complexity_box("O(m × n)", "O(m × n)",
                   "m, n = lengths of the two strings")


# =============================================================================
#  EXAMPLE 6: Edit Distance (Levenshtein)
# =============================================================================

def example_6_edit_distance():
    section_header(6, "Edit Distance (Levenshtein)")

    print("  PROBLEM: Find the minimum number of single-character edits")
    print("  (insert, delete, replace) to transform one string into another.")
    print()

    s1 = "sunday"
    s2 = "saturday"

    print(f'  Transform: "{s1}" → "{s2}"')
    print()
    print("  Three operations at dp[i][j]:")
    print("    Insert:  dp[i][j-1] + 1     (insert s2[j-1] into s1)")
    print("    Delete:  dp[i-1][j] + 1     (delete s1[i-1])")
    print("    Replace: dp[i-1][j-1] + 1   (replace s1[i-1] with s2[j-1])")
    print("    Match:   dp[i-1][j-1]       (characters equal, no cost)")
    print()
    print("  Direction arrows at each cell:")
    print("       ↖ diagonal = match/replace")
    print("       ← left     = insert")
    print("       ↑ up       = delete")
    print()

    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    col_labels = ['""'] + list(s2)
    row_labels = ['""'] + list(s1)

    print("  ── Bottom-Up (Tabulation) ──")
    print_2d_table(dp, row_labels=row_labels, col_labels=col_labels,
                   title="Base cases filled (row 0 and col 0):")

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # match
            else:
                dp[i][j] = 1 + min(
                    dp[i][j - 1],      # insert
                    dp[i - 1][j],      # delete
                    dp[i - 1][j - 1]   # replace
                )

        ops = []
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                ops.append("match")
                break
        op_str = f" ('{s1[i-1]}' matches found)" if ops else ""
        print_2d_table(dp, row_labels=row_labels, col_labels=col_labels,
                       title=f"Row '{s1[i-1]}'{op_str}:")

    print(f'  Edit distance("{s1}", "{s2}") = {dp[m][n]}')
    print()

    # Backtrack to find the operations
    print("  Operations (backtracking):")
    operations = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            operations.append(f"  MATCH  '{s1[i-1]}'")
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j] == dp[i][j - 1] + 1):
            operations.append(f"  INSERT '{s2[j-1]}'")
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j] == dp[i - 1][j] + 1):
            operations.append(f"  DELETE '{s1[i-1]}'")
            i -= 1
        else:
            operations.append(f"  REPLACE '{s1[i-1]}' → '{s2[j-1]}'")
            i -= 1
            j -= 1
    operations.reverse()
    for op in operations:
        print(f"    {op}")
    print()

    # --- Top-Down ---
    print("  ── Top-Down (Memoization) ──")

    def edit_memo(s1, s2):
        memo = {}

        def helper(i, j):
            if i == 0:
                return j
            if j == 0:
                return i
            if (i, j) in memo:
                return memo[(i, j)]
            if s1[i - 1] == s2[j - 1]:
                memo[(i, j)] = helper(i - 1, j - 1)
            else:
                memo[(i, j)] = 1 + min(
                    helper(i, j - 1),
                    helper(i - 1, j),
                    helper(i - 1, j - 1)
                )
            return memo[(i, j)]

        return helper(len(s1), len(s2))

    print(f"  Edit distance = {edit_memo(s1, s2)}")
    print()

    complexity_box("O(m × n)", "O(m × n)",
                   "Can optimize space to O(min(m, n))")


# =============================================================================
#  EXAMPLE 7: Matrix Chain Multiplication
# =============================================================================

def example_7_matrix_chain():
    section_header(7, "Matrix Chain Multiplication")

    print("  PROBLEM: Given a chain of matrices, find the most efficient")
    print("  way to parenthesize their multiplication to minimize total")
    print("  scalar multiplications.")
    print()
    print("  KEY INSIGHT: This is INTERVAL DP — the table is filled")
    print("  diagonally (by increasing chain length), not row-by-row.")
    print()

    # dims[i-1] x dims[i] gives dimensions of matrix i
    dims = [10, 30, 5, 60, 10]
    n = len(dims) - 1  # number of matrices

    print(f"  Matrix dimensions: {dims}")
    print(f"  Matrices:")
    for i in range(n):
        print(f"    M{i+1}: {dims[i]} × {dims[i+1]}")
    print()
    print("  Recurrence (for chain from matrix i to matrix j):")
    print("  dp[i][j] = min over k in [i, j-1]:")
    print("             dp[i][k] + dp[k+1][j] + dims[i-1]*dims[k]*dims[j]")
    print()

    dp = [[0] * (n + 1) for _ in range(n + 1)]
    split = [[0] * (n + 1) for _ in range(n + 1)]

    print("  ── Bottom-Up (Diagonal Fill) ──")
    print()

    col_labels = [""] + [f"M{i}" for i in range(1, n + 1)]
    row_labels = [f"M{i}" for i in range(1, n + 1)]

    # Fill by chain length
    for length in range(2, n + 1):
        print(f"  --- Chain length {length} ---")
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')
            details = []
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                details.append(f"k={k}: {dp[i][k]}+{dp[k+1][j]}+{dims[i-1]}*{dims[k]}*{dims[j]}={cost}")
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

            # Print the choices for this cell
            print(f"  dp[{i}][{j}] candidates:")
            for d in details:
                print(f"    {d}")
            print(f"  → dp[{i}][{j}] = {dp[i][j]} (split at k={split[i][j]})")
            print()

        # Show table after this diagonal
        display = [["." if dp[r][c] == 0 and r != c else str(dp[r][c])
                     for c in range(1, n + 1)] for r in range(1, n + 1)]
        # Upper triangular only
        for r in range(n):
            for c in range(r):
                display[r][c] = "-"
        print_2d_table(display, row_labels=row_labels,
                       col_labels=[f"M{i}" for i in range(1, n + 1)],
                       title=f"Table after chain length {length}:")

    print(f"  Minimum multiplications: {dp[1][n]}")
    print()

    # Reconstruct optimal parenthesization
    def build_parens(i, j):
        if i == j:
            return f"M{i}"
        k = split[i][j]
        left = build_parens(i, k)
        right = build_parens(k + 1, j)
        return f"({left} × {right})"

    print(f"  Optimal parenthesization: {build_parens(1, n)}")
    print()

    complexity_box("O(n³)", "O(n²)",
                   "n = number of matrices")


# =============================================================================
#  EXAMPLE 8: Longest Increasing Subsequence (LIS)
# =============================================================================

def example_8_lis():
    section_header(8, "Longest Increasing Subsequence (LIS)")

    print("  PROBLEM: Find the length of the longest strictly increasing")
    print("  subsequence in an array.")
    print()

    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    n = len(arr)

    print(f"  Array: {arr}")
    print()
    print("  Recurrence:")
    print("  dp[i] = 1 + max(dp[j] for j < i if arr[j] < arr[i])")
    print("  (length of LIS ending at index i)")
    print()

    # --- Bottom-Up O(n²) ---
    print("  ── Bottom-Up O(n²) ──")
    print()

    dp = [1] * n
    parent = [-1] * n

    for i in range(1, n):
        comparisons = []
        for j in range(i):
            if arr[j] < arr[i]:
                comparisons.append((j, arr[j], dp[j]))
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j

        comp_str = ", ".join(f"arr[{j}]={v}→dp={d}" for j, v, d in comparisons)
        if not comp_str:
            comp_str = "no smaller elements found"

        print(f"  i={i}, arr[{i}]={arr[i]}: {comp_str}")
        print(f"    dp[{i}] = {dp[i]}")

        # Show current state
        arr_labels = [f"i{k}" for k in range(n)]
        print(f"    arr: {arr}")
        print(f"    dp:  {dp}")
        print()

    lis_length = max(dp)
    print(f"  LIS length: {lis_length}")
    print()

    # Reconstruct one LIS
    print("  Reconstructing one LIS:")
    idx = dp.index(lis_length)
    seq = []
    while idx != -1:
        seq.append(arr[idx])
        idx = parent[idx]
    seq.reverse()
    print(f"  LIS: {seq}")
    print()

    # Visual with arrows
    print("  Visual (arrows show LIS chain):")
    print(f"  Index:  {list(range(n))}")
    print(f"  Array:  {arr}")
    print(f"  dp:     {dp}")

    # Mark LIS elements
    lis_set = set(range(n))
    idx = dp.index(lis_length)
    lis_indices = []
    while idx != -1:
        lis_indices.append(idx)
        idx = parent[idx]
    lis_indices.reverse()

    markers = [" "] * n
    for idx in lis_indices:
        markers[idx] = "^"
    print(f"  LIS:   {markers}")
    print()

    # --- Top-Down ---
    print("  ── Top-Down (Memoization) ──")

    def lis_memo(arr):
        memo = {}

        def helper(i):
            if i in memo:
                return memo[i]
            best = 1
            for j in range(i):
                if arr[j] < arr[i]:
                    best = max(best, helper(j) + 1)
            memo[i] = best
            return best

        return max(helper(i) for i in range(len(arr)))

    print(f"  LIS length: {lis_memo(arr)}")
    print()

    complexity_box("O(n²)", "O(n)",
                   "O(n log n) possible with patience sorting")


# =============================================================================
#  EXAMPLE 9: Rod Cutting
# =============================================================================

def example_9_rod_cutting():
    section_header(9, "Rod Cutting")

    print("  PROBLEM: Given a rod of length n and a price table for each")
    print("  length, determine the maximum revenue from cutting the rod.")
    print("  You can cut into any combination of lengths (unbounded).")
    print()

    prices = [0, 1, 5, 8, 9, 10, 17, 17, 20]
    n = len(prices) - 1

    print(f"  Rod length: {n}")
    print(f"  Price table:")
    print_1d_table(prices, labels=[f"len{i}" for i in range(n + 1)], title="")

    print("  Rod visualization:")
    print(f"  |{'=' * n * 2}|  (uncut, price = {prices[n]})")
    print()
    print("  Recurrence:")
    print("  dp[i] = max(price[k] + dp[i-k]) for k in [1, i]")
    print("  (try every possible first cut of length k)")
    print()

    # --- Bottom-Up ---
    print("  ── Bottom-Up (Tabulation) ──")

    dp = [0] * (n + 1)
    first_cut = [0] * (n + 1)

    for i in range(1, n + 1):
        best = -1
        candidates = []
        for k in range(1, i + 1):
            val = prices[k] + dp[i - k]
            candidates.append(f"price[{k}]+dp[{i-k}]={prices[k]}+{dp[i-k]}={val}")
            if val > best:
                best = val
                first_cut[i] = k
        dp[i] = best

        if i <= 5 or i == n:
            print(f"  dp[{i}]: {', '.join(candidates)}")
            print_1d_table(dp[:i+1], labels=[f"len{j}" for j in range(i + 1)],
                           highlight=i, title=f"  → dp[{i}] = {dp[i]} (cut={first_cut[i]}):")

    print(f"  Maximum revenue: {dp[n]}")
    print()

    # Reconstruct cuts
    print("  Optimal cuts (backtracking):")
    cuts = []
    remaining = n
    while remaining > 0:
        cuts.append(first_cut[remaining])
        remaining -= first_cut[remaining]

    cut_visual = "|".join("=" * (c * 2) for c in cuts)
    print(f"  |{cut_visual}|")
    print(f"  Cuts: {cuts} → Revenue: {' + '.join(str(prices[c]) for c in cuts)} = {dp[n]}")
    print()

    # --- Top-Down ---
    print("  ── Top-Down (Memoization) ──")

    def rod_memo(prices, n):
        memo = {}

        def helper(length):
            if length == 0:
                return 0
            if length in memo:
                return memo[length]
            best = -1
            for k in range(1, length + 1):
                best = max(best, prices[k] + helper(length - k))
            memo[length] = best
            return best

        return helper(n)

    print(f"  Maximum revenue: {rod_memo(prices, n)}")
    print()

    complexity_box("O(n²)", "O(n)",
                   "Similar to unbounded knapsack")


# =============================================================================
#  EXAMPLE 10: Unique Paths in Grid
# =============================================================================

def example_10_unique_paths():
    section_header(10, "Unique Paths in Grid")

    print("  PROBLEM: Count unique paths from top-left to bottom-right")
    print("  in a grid, moving only RIGHT or DOWN.")
    print()
    print("  Part A: No obstacles")
    print("  Part B: With obstacles")
    print()

    # --- Part A: No obstacles ---
    rows, cols = 4, 5

    print(f"  ── Part A: {rows}×{cols} Grid (No Obstacles) ──")
    print()
    print("  Recurrence: dp[r][c] = dp[r-1][c] + dp[r][c-1]")
    print("  (paths from above + paths from left)")
    print()

    dp = [[0] * cols for _ in range(rows)]

    # Base cases
    for r in range(rows):
        dp[r][0] = 1
    for c in range(cols):
        dp[0][c] = 1

    # Fill
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    # Print as grid with box drawing
    print("  Result grid:")
    print("  ┌" + "────┬" * (cols - 1) + "────┐")
    for r in range(rows):
        row_str = "  │"
        for c in range(cols):
            val = dp[r][c]
            if r == rows - 1 and c == cols - 1:
                row_str += f" *{val:>2}│"
            else:
                row_str += f" {val:>3}│"
        print(row_str)
        if r < rows - 1:
            print("  ├" + "────┼" * (cols - 1) + "────┤")
    print("  └" + "────┴" * (cols - 1) + "────┘")
    print()
    print(f"  Unique paths: {dp[rows-1][cols-1]}")
    print()

    # Step-by-step for a smaller grid
    print("  Step-by-step for 3×4 grid:")
    sr, sc = 3, 4
    dp2 = [[0] * sc for _ in range(sr)]
    for r in range(sr):
        dp2[r][0] = 1
    for c in range(sc):
        dp2[0][c] = 1

    print_2d_table(dp2,
                   row_labels=[f"r{r}" for r in range(sr)],
                   col_labels=[f"c{c}" for c in range(sc)],
                   title="Base cases (first row and column = 1):")

    for r in range(1, sr):
        for c in range(1, sc):
            dp2[r][c] = dp2[r - 1][c] + dp2[r][c - 1]
        print_2d_table(dp2,
                       row_labels=[f"r{r}" for r in range(sr)],
                       col_labels=[f"c{c}" for c in range(sc)],
                       title=f"Row {r}: dp[r][c] = dp[r-1][c] + dp[r][c-1]:")

    # --- Part B: With obstacles ---
    print("  ── Part B: Grid With Obstacles ──")
    print()

    # Define obstacle grid (1 = obstacle)
    obstacle_grid = [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
    ]
    or_rows, or_cols = len(obstacle_grid), len(obstacle_grid[0])

    print("  Grid layout (X = obstacle):")
    print("  ┌───┬───┬───┬───┐")
    for r in range(or_rows):
        row_str = "  │"
        for c in range(or_cols):
            if obstacle_grid[r][c] == 1:
                row_str += " X │"
            elif r == 0 and c == 0:
                row_str += " S │"
            elif r == or_rows - 1 and c == or_cols - 1:
                row_str += " E │"
            else:
                row_str += " . │"
        print(row_str)
        if r < or_rows - 1:
            print("  ├───┼───┼───┼───┤")
    print("  └───┴───┴───┴───┘")
    print("  S = start, E = end, X = obstacle")
    print()

    dp3 = [[0] * or_cols for _ in range(or_rows)]
    dp3[0][0] = 1 if obstacle_grid[0][0] == 0 else 0

    for r in range(or_rows):
        for c in range(or_cols):
            if obstacle_grid[r][c] == 1:
                dp3[r][c] = 0
                continue
            if r == 0 and c == 0:
                continue
            from_top = dp3[r - 1][c] if r > 0 else 0
            from_left = dp3[r][c - 1] if c > 0 else 0
            dp3[r][c] = from_top + from_left

    # Print result grid
    print("  DP result with obstacles:")
    print("  ┌────┬────┬────┬────┐")
    for r in range(or_rows):
        row_str = "  │"
        for c in range(or_cols):
            if obstacle_grid[r][c] == 1:
                row_str += "  X │"
            elif r == or_rows - 1 and c == or_cols - 1:
                row_str += f"*{dp3[r][c]:>2} │"
            else:
                row_str += f" {dp3[r][c]:>2} │"
        print(row_str)
        if r < or_rows - 1:
            print("  ├────┼────┼────┼────┤")
    print("  └────┴────┴────┴────┘")
    print()
    print(f"  Unique paths (with obstacles): {dp3[or_rows-1][or_cols-1]}")
    print()

    # --- Top-Down ---
    print("  ── Top-Down (Memoization, with obstacles) ──")

    def unique_paths_memo(grid):
        rows, cols = len(grid), len(grid[0])
        memo = {}

        def helper(r, c):
            if r < 0 or c < 0 or grid[r][c] == 1:
                return 0
            if r == 0 and c == 0:
                return 1
            if (r, c) in memo:
                return memo[(r, c)]
            memo[(r, c)] = helper(r - 1, c) + helper(r, c - 1)
            return memo[(r, c)]

        return helper(rows - 1, cols - 1)

    print(f"  Unique paths: {unique_paths_memo(obstacle_grid)}")
    print()

    complexity_box("O(m × n)", "O(m × n) or O(n) with space optimization",
                   "m, n = grid dimensions")


# =============================================================================
#  MAIN — CLI Runner
# =============================================================================

EXAMPLES = {
    1: ("Fibonacci Numbers", example_1_fibonacci),
    2: ("Climbing Stairs", example_2_climbing_stairs),
    3: ("Coin Change (Minimum Coins)", example_3_coin_change),
    4: ("0/1 Knapsack", example_4_knapsack),
    5: ("Longest Common Subsequence", example_5_lcs),
    6: ("Edit Distance (Levenshtein)", example_6_edit_distance),
    7: ("Matrix Chain Multiplication", example_7_matrix_chain),
    8: ("Longest Increasing Subsequence", example_8_lis),
    9: ("Rod Cutting", example_9_rod_cutting),
    10: ("Unique Paths in Grid", example_10_unique_paths),
}


def print_menu():
    print()
    print("=" * 70)
    print("  DYNAMIC PROGRAMMING TUTORIAL — 10 Progressive Examples")
    print("=" * 70)
    print()
    for num, (title, _) in EXAMPLES.items():
        difficulty = ["", "Intro", "Easy", "Easy-Medium", "Medium", "Medium",
                       "Medium-Hard", "Hard", "Hard", "Hard", "Hard"][num]
        print(f"    {num:>2}. {title:<40s} [{difficulty}]")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific examples
        for arg in sys.argv[1:]:
            try:
                num = int(arg)
                if num in EXAMPLES:
                    EXAMPLES[num][1]()
                else:
                    print(f"  Unknown example: {num}. Choose 1-10.")
            except ValueError:
                print(f"  Invalid argument: {arg}. Use numbers 1-10.")
    else:
        # Run all examples
        print_menu()
        print("  Running all examples...\n")
        for num in range(1, 11):
            EXAMPLES[num][1]()

        print()
        print("=" * 70)
        print("  TUTORIAL COMPLETE!")
        print("=" * 70)
        print()
        print("  Key takeaways:")
        print("    1. Identify overlapping subproblems and optimal substructure")
        print("    2. Define the STATE (what does dp[i] or dp[i][j] represent?)")
        print("    3. Write the RECURRENCE (how does current state depend on smaller states?)")
        print("    4. Determine BASE CASES")
        print("    5. Choose top-down (memoization) or bottom-up (tabulation)")
        print("    6. Optimize space if possible")
        print()
        print("  Run individual examples: python dp_tutorial.py <number>")
        print("  Example: python dp_tutorial.py 4")
        print()
