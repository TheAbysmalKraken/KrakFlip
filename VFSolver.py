import VoltorbFlip as vf
import VFInterface as vfi
import time
import numpy as np

#Program start delay
startDelay = 5
for i in range(startDelay, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)
print("Program started.")

orig_totals = []
orig_voltorbs = []

def update_totals(voltorbs, totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    totals = orig_totals.copy()
    voltorbs = orig_voltorbs.copy()
    for v in range(0,5):
        for j in range(0,5):
            if counts[v,j] == 1:
                num = np.where(memo[v,j] == 1)[0][0]
                if memo[v,j,0] == 1:
                    voltorbs[0][j] -= 1
                    voltorbs[1][v] -= 1
                else:
                    totals[0][j] -= num
                    totals[1][v] -= num
    return (totals, voltorbs)

def no_voltorbs(voltorbs, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):
        # Columns with no Voltorbs
        if voltorbs[0][v] == 0:
            for row in range(0,5):
                if memo[row,v,0] == 1 and counts[row,v] != 1:
                    memo[row,v,0] = 0

        # Rows with no Voltorbs
        if voltorbs[1][v] == 0:
            for col in range(0,5):
                if memo[v,col,0] == 1 and counts[v,col] != 1:
                    memo[v,col,0] = 0
                    

def all_voltorbs(voltorbs, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):
        # Columns with all Voltorbs
        if voltorbs[0][v] == np.count_nonzero(counts[:,v] > 1) and voltorbs[0][v] != 0:
            for row in range(0,5):
                if counts[row,v] != 1:
                    memo[row,v,1] = 0
                    memo[row,v,2] = 0
                    memo[row,v,3] = 0

        # Rows with all Voltorbs
        if voltorbs[1][v] == np.count_nonzero(counts[v,:] > 1) and voltorbs[0][v] != 0:
            for col in range(0,5):
                if counts[v,col] != 1:
                    memo[v,col,1] = 0
                    memo[v,col,2] = 0
                    memo[v,col,3] = 0


def all_ones_voltorbs(voltorbs, totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):
        # Column total + orbs is 5 (all 1s)
        if voltorbs[0][v] + totals[0][v] == np.count_nonzero(counts[:,v] > 1):
            for row in range(0,5):
                if counts[row,v] != 1:
                    memo[row,v,2] = 0
                    memo[row,v,3] = 0

        # Row total + orbs is 5 (all 1s)
        if voltorbs[1][v] + totals[1][v] == np.count_nonzero(counts[v,:] > 1):
            for col in range(0,5):
                if counts[v,col] != 1:
                    memo[v,col,2] = 0
                    memo[v,col,3] = 0


def all_voltorbs_but_one(voltorbs, totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):
        # 4 Voltorbs (cols)
        if voltorbs[0][v] + 1 == np.count_nonzero(counts[:,v] > 1):
            for row in range(0,5):
                if counts[row,v] != 1:
                    for notnum in range(1,4):
                        if notnum != totals[0][v]:
                            memo[row,v,notnum] = 0

        # 4 Voltorbs (rows)
        if voltorbs[1][v] + 1 == np.count_nonzero(counts[v,:] > 1):
            for col in range(0,5):
                if counts[v,col] != 1:
                    for notnum in range(1,4):
                        if notnum != totals[1][v]:
                            memo[v,col,notnum] = 0


def no_threes(voltorbs, totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):
        # Column total + orbs is 6 (1s or 2s)
        if voltorbs[0][v] + totals[0][v] - 1 == np.count_nonzero(counts[:,v] > 1):
            for row in range(0,5):
                if counts[row,v] != 1:
                    memo[row,v,3] = 0

        # Row total + orbs is 6 (1s or 2s)
        if voltorbs[1][v] + totals[1][v] - 1 == np.count_nonzero(counts[v,:] > 1):
            for col in range(0,5):
                if counts[v,col] != 1:
                    memo[v,col,3] = 0


def no_ones(voltorbs, totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):
        Ncol = np.count_nonzero(counts[:,v] > 1) - voltorbs[0][v]
        Nrow = np.count_nonzero(counts[v,:] > 1) - voltorbs[1][v]
        
        # Col no 1s
        if Ncol <= (totals[0][v] + 1)/3:
            for row in range(0,5):
                if counts[row,v] != 1:
                    memo[row,v,1] = 0

        # Row no 1s
        if Nrow <= (totals[1][v] + 1)/3:
            for col in range(0,5):
                if counts[v,col] != 1:
                    memo[v,col,1] = 0

def one_remaining(totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):

        # Columns
        for row in range(0,5):
            if np.count_nonzero(counts[:,v] > 1) == 1 and counts[row,v] != 1:
                    for notnum in range(1,4):
                        if notnum != totals[0][v]:
                            memo[row,v,notnum] = 0

        # Rows
        for col in range(0,5):
            if np.count_nonzero(counts[v,:] > 1) == 1 and counts[v,col] != 1:
                for notnum in range(1,4):
                    if notnum != totals[1][v]:
                        memo[v,col,notnum] = 0

def check_remaining(totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):
        
        # Columns
        T = totals[0][v]
        N = np.count_nonzero(counts[:,v] > 1) - voltorbs[0][v]
        min_ones = -1
        min_twos = -1
        min_threes = -1
        total_ones = 0
        total_twos = 0
        total_threes = 0
        
        if T < 2 * N:
            # Minimum 1s
            min_ones = 2*N - T
        elif T > 2 * N:
            # Minimum 3s
            min_threes = T - 2*N

        if (T % 2 == 0 and N % 2 != 0) or (T % 2 != 0 and N % 2 == 0):
            # Minimum 2s
            min_twos = 1

        total_ones = np.count_nonzero(memo[:,v,1] == 1)
        total_twos = np.count_nonzero(memo[:,v,2] == 1)
        total_threes = np.count_nonzero(memo[:,v,3] == 1)

        for row in range(0,5):
            if min_ones == total_ones and memo[row,v,1] == 1:
                memo[row,v] = np.array([0,1,0,0])
            if min_twos == total_twos and memo[row,v,2] == 1:
                memo[row,v] = np.array([0,0,1,0])
            if min_threes == total_threes and memo[row,v,3] == 1:
                memo[row,v] = np.array([0,0,0,1])

        # Rows
        T = totals[1][v]
        N = np.count_nonzero(counts[v,:] > 1) - voltorbs[1][v]
        min_ones = -1
        min_twos = -1
        min_threes = -1
        total_ones = 0
        total_twos = 0
        total_threes = 0
        
        if T < 2 * N:
            # Minimum 1s
            min_ones = 2*N - T
        elif T > 2 * N:
            # Minimum 3s
            min_threes = T - 2*N

        if (T % 2 == 0 and N % 2 != 0) or (T % 2 != 0 and N % 2 == 0):
            # Minimum 2s
            min_twos = 1
        
        total_ones = np.count_nonzero(memo[v,:,1] == 1)
        total_twos = np.count_nonzero(memo[v,:,2] == 1)
        total_threes = np.count_nonzero(memo[v,:,3] == 1)

        for col in range(0,5):
            if min_ones == total_ones and memo[v,col,1] == 1:
                memo[v,col] = np.array([0,1,0,0])
            if min_twos == total_twos and memo[v,col,2] == 1:
                memo[v,col] = np.array([0,0,1,0])
            if min_threes == total_threes and memo[v,col,3] == 1:
                memo[v,col] = np.array([0,0,0,1])


def all_threes(totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):

        # Columns
        for row in range(0,5):
            if np.count_nonzero(counts[:,v] > 1) * 3 == totals[0][v] and counts[row,v] != 1:
                memo[row,v] = np.array([0,0,0,1])

        # Rows
        for col in range(0,5):
            if np.count_nonzero(counts[v,:] > 1) * 3 == totals[1][v] and counts[v,col] != 1:
                memo[v,col] = np.array([0,0,0,1])


def not_voltorb(totals, memo):
    counts = np.count_nonzero(memo, axis=2)
    for v in range(0,5):
        Ncol = np.count_nonzero(counts[:,v] > 1) - voltorbs[0][v]
        Nrow = np.count_nonzero(counts[v,:] > 1) - voltorbs[1][v]

        # Columns

        total_ones = np.count_nonzero(memo[:,v,1] == 1)
        total_twos = np.count_nonzero(memo[:,v,2] == 1)
        total_threes = np.count_nonzero(memo[:,v,3] == 1)
        
        for row in range(0,5):
            if counts[row,v] != 1:
                # Total - N = 2 -> 3 or 2,2
                if (Ncol == 2 and totals[0,v] == 4) or (Ncol == 3 and totals[0,v] == 5) or (Ncol == 4 and totals[0,v] == 6):
                    # Both
                    if memo[row,v,2] == 1 and memo[row,v,3] == 1 and total_twos == 2 and total_threes == 1:
                        memo[row,v,0] = 0
                    # Two twos
                    elif memo[row,v,2] == 1 and total_twos == 2 and total_threes == 0:
                        memo[row,v,0] = 0
                    # One three
                    elif memo[row,v,3] == 1 and total_threes == 1 and total_twos < 2:
                        memo[row,v,0] = 0

                # Total - N = 3 -> 2,3 or 2,2,2
                if (Ncol == 3 and totals[0,v] == 6) or (Ncol == 4 and totals[0,v] == 7):
                    # Both
                    if memo[row,v,2] == 1 and memo[row,v,3] == 1 and total_twos == 3 and total_threes == 1:
                        memo[row,v,0] = 0
                    # Three twos
                    elif memo[row,v,2] == 1 and total_twos == 3 and total_threes == 0:
                        memo[row,v,0] = 0
                    # One three
                    elif memo[row,v,3] == 1 and total_threes == 1 and total_twos < 2:
                        memo[row,v,0] = 0

                # Total - N = 4 -> 3,3 or 2,2,3
                if (Ncol == 3 and totals[0,v] == 7) or (Ncol == 4 and totals[0,v] == 8):
                    # Both
                    if memo[row,v,2] == 1 and memo[row,v,3] == 1 and total_twos == 2 and total_threes == 2:
                        memo[row,v,0] = 0
                    # Two twos
                    elif memo[row,v,2] == 1 and total_twos == 2 and total_threes < 2:
                        memo[row,v,0] = 0
                    # Two threes
                    elif memo[row,v,3] == 1 and total_threes == 2 and total_twos < 2:
                        memo[row,v,0] = 0

                # Total = 8 and N = 4 -> 2,2,2,2
                if Ncol == 4 and totals[0,v] == 8 and memo[row,v,2] == 1 and total_twos == 4 and total_threes == 0:
                    memo[row,v,0] = 0

                # Total = 9 and N = 4 -> 2,3,3 or 2,2,2,3
                if Ncol == 4 and totals[0,v] == 9:
                    # Both
                    if memo[row,v,2] == 1 and memo[row,v,3] == 1 and total_twos == 3 and total_threes == 2:
                        memo[row,v,0] = 0
                    # Two twos
                    elif memo[row,v,2] == 1 and total_twos == 3 and total_threes < 2:
                        memo[row,v,0] = 0
                    # Two threes
                    elif memo[row,v,3] == 1 and total_threes == 2 and total_twos < 3:
                        memo[row,v,0] = 0

                # Total = 10 and N = 4 -> 3,3,3 or 2,2,3,3
                if Ncol == 4 and totals[0,v] == 10:
                    # Both
                    if memo[row,v,2] == 1 and memo[row,v,3] == 1 and total_twos == 2 and total_threes == 3:
                        memo[row,v,0] = 0
                    # Two twos
                    elif memo[row,v,2] == 1 and total_twos == 2 and total_threes < 3:
                        memo[row,v,0] = 0
                    # Two threes
                    elif memo[row,v,3] == 1 and total_threes == 3 and total_twos < 2:
                        memo[row,v,0] = 0

        # Rows

        total_ones = np.count_nonzero(memo[v,:,1] == 1)
        total_twos = np.count_nonzero(memo[v,:,2] == 1)
        total_threes = np.count_nonzero(memo[v,:,3] == 1)
        
        for col in range(0,5):
            if counts[v,col] != 1:
                # Total - N = 2 -> 3 or 2,2
                if (Nrow == 2 and totals[1,v] == 4) or (Nrow == 3 and totals[1,v] == 5) or (Nrow == 4 and totals[1,v] == 6):
                    # Both
                    if memo[v,col,2] == 1 and memo[v,col,3] == 1 and total_twos == 2 and total_threes == 1:
                        memo[v,col,0] = 0
                    # Two twos
                    elif memo[v,col,2] == 1 and total_twos == 2 and total_threes == 0:
                        memo[v,col,0] = 0
                    # One three
                    elif memo[v,col,3] == 1 and total_threes == 1 and total_twos < 2:
                        memo[v,col,0] = 0

                # Total - N = 3 -> 2,3 or 2,2,2
                if (Nrow == 3 and totals[1,v] == 6) or (Nrow == 4 and totals[1,v] == 7):
                    # Both
                    if memo[v,col,2] == 1 and memo[v,col,3] == 1 and total_twos == 3 and total_threes == 1:
                        memo[v,col,0] = 0
                    # Three twos
                    elif memo[v,col,2] == 1 and total_twos == 3 and total_threes == 0:
                        memo[v,col,0] = 0
                    # One three
                    elif memo[v,col,3] == 1 and total_threes == 1 and total_twos < 2:
                        memo[v,col,0] = 0

                # Total - N = 4 -> 3,3 or 2,2,3
                if (Nrow == 3 and totals[1,v] == 7) or (Nrow == 4 and totals[1,v] == 8):
                    # Both
                    if memo[v,col,2] == 1 and memo[v,col,3] == 1 and total_twos == 2 and total_threes == 2:
                        memo[v,col,0] = 0
                    # Two twos
                    elif memo[v,col,2] == 1 and total_twos == 2 and total_threes < 2:
                        memo[v,col,0] = 0
                    # Two threes
                    elif memo[v,col,3] == 1 and total_threes == 2 and total_twos < 2:
                        memo[v,col,0] = 0

                # Total = 8 and N = 4 -> 2,2,2,2
                if Nrow == 4 and totals[1,v] == 8 and memo[v,col,2] == 1 and total_twos == 4 and total_threes == 0:
                    memo[v,col,0] = 0

                # Total = 9 and N = 4 -> 2,3,3 or 2,2,2,3
                if Nrow == 4 and totals[1,v] == 9:
                    # Both
                    if memo[v,col,2] == 1 and memo[v,col,3] == 1 and total_twos == 3 and total_threes == 2:
                        memo[v,col,0] = 0
                    # Two twos
                    elif memo[v,col,2] == 1 and total_twos == 3 and total_threes < 2:
                        memo[v,col,0] = 0
                    # Two threes
                    elif memo[v,col,3] == 1 and total_threes == 2 and total_twos < 3:
                        memo[v,col,0] = 0

                # Total = 10 and N = 4 -> 3,3,3 or 2,2,3,3
                if Nrow == 4 and totals[1,v] == 10:
                    # Both
                    if memo[v,col,2] == 1 and memo[v,col,3] == 1 and total_twos == 2 and total_threes == 3:
                        memo[v,col,0] = 0
                    # Two twos
                    elif memo[v,col,2] == 1 and total_twos == 2 and total_threes < 3:
                        memo[v,col,0] = 0
                    # Two threes
                    elif memo[v,col,3] == 1 and total_threes == 3 and total_twos < 2:
                        memo[v,col,0] = 0


def reveal_ones(memo, clicked, tiles_flipped):
    for v in range(0,5):
        for j in range(0,5):
            if tiles_flipped >= level:
                return
            
            # Reveal tiles that must be a one
            if memo[v,j].tolist() == [0,1,0,0] and clicked[v][j] == False:
                print("Clicking one")
                vfi.click_tile(v, j)
                tiles_flipped += 1
                clicked[v][j] = True

start_time = time.time()

# Run time in minutes
run_time = 120

while (time.time() - start_time)/60 < run_time and not vfi.check_maxed():
    vfi.click_play()

    time.sleep(0.2)

    # Read board info
    board_info = vfi.read_board()

    # Get totals and voltorbs
    orig_totals = np.array(board_info[0])
    orig_voltorbs = np.array(board_info[1])
    totals = orig_totals.copy()
    voltorbs = orig_voltorbs.copy()

    print(f"Totals: {totals}")
    print(f"Voltorbs: {voltorbs}")
    
    memo = np.tile(np.array([1,1,1,1]), (5,5,1))
    old_memo = np.tile(np.array([1,1,1,1]), (5,5,1))
    clicked = np.full((5,5),False)

    level = 5
    tiles_flipped = 0

    still_checking = True

    while still_checking:
        print("Applying logic...\n")
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        all_ones_voltorbs(voltorbs, totals, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        no_threes(voltorbs, totals, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)
        
        no_voltorbs(voltorbs, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        all_voltorbs_but_one(voltorbs, totals, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        all_voltorbs(voltorbs, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        one_remaining(totals, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        no_ones(voltorbs, totals, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        check_remaining(totals, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        all_threes(totals, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        not_voltorb(totals, memo)
        (totals, voltorbs) = update_totals(voltorbs, totals, memo)

        num = 0

        # Reveal rows with all Voltorbs revealed
        for v in range(0,5):
            for j in range(0,5):
                # Reveal tiles that can't be a voltorb
                if memo[v,j,0] == 0:
                    if clicked[v][j] == False:
                        if memo[v,j].tolist() != [0,1,0,0]:
                            print("Clicking safe")
                            num = vfi.click_tile(v, j)
                            tiles_flipped += 1
                            
                            clicked[v][j] = True
                            memo[v,j] = np.array([0,0,0,0])
                            memo[v,j,num] = 1
                            totals[0][j] -= num
                            totals[1][v] -= num
                        else:
                            num = 1

                        # Check game over
                        if num == -1:
                            print(memo)
                            print("\n\nBAD LOGIC\n\n")
                            input()
                            still_checking = False
                            break

                        # Check if solved
                        if vfi.check_solved() == True:
                            still_checking = False
                            break
                            
                # Mark voltorb tiles
                elif memo[v,j].tolist() == [1,0,0,0]:
                    if clicked[v][j] == False:
                        clicked[v][j] = True
                        voltorbs[0][j] -= 1
                        voltorbs[1][v] -= 1

            if still_checking == False:
                break

        if still_checking == False:
            break
        
        if memo.tolist() == old_memo.tolist():    # Check if can be solved further
            #print("Guessing a tile")

            print("Solved as far as possible - guessing required!")
            #input()

            counts = np.count_nonzero(memo, axis=2)

            reveal_ones(memo, clicked, tiles_flipped)

            likely_tiles = np.full((5,5),-1000)

            # Click most likely tile
            for v in range(0,5):
                for j in range(0,5):
                    if clicked[v][j] == False and counts[v,j] > 1:
                        if memo[v,j,2] == 1 or memo[v,j,3] == 1:
                            likely_tiles[v][j] = (totals[0][v] + totals[1][j]) - (voltorbs[0][v] + voltorbs[1][j])

            (x,y) = np.unravel_index(np.argmax(likely_tiles), likely_tiles.shape)
            if clicked[x][y] == False:
                print("Clicking guess")
                num = vfi.click_tile(x, y)
                tiles_flipped += 1
                clicked[x][y] = True
                memo[x,y] = np.array([0,0,0,0])
                memo[x,y,num] = 1
                totals[0][y] -= num
                totals[1][x] -= num

            # Check if solved
            if vfi.check_solved() == True:
                still_checking = False
                break

            # Check game over
            if num == -1:
                still_checking = False
                break

            # Check if solved again
            if np.count_nonzero(likely_tiles == -1000) == 25:
                print("All -1000")
                still_checking = False
                break

        old_memo = memo.copy()

    restart_time = 0.5

    print(f"Restarting in {restart_time}s...\n")
    time.sleep(restart_time)

    if vfi.is_textbox() == False:
        vfi.restart_game()


print(f"Finished. Ran for {time.time() - start_time}s")
