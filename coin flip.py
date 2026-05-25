import random
import time
import os

# ─────────────────────────────────────────
#  COIN FLIP SIMULATOR
# ─────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("=" * 40)
    print("       🪙  COIN FLIP SIMULATOR")
    print("=" * 40)

def flip_animation():
    frames = ["( H )", "( ? )", "( T )", "( ? )", "( H )", "( ? )"]
    for frame in frames:
        print(f"\r  Flipping...  {frame}", end="", flush=True)
        time.sleep(0.15)

def flip_once():
    clear()
    banner()
    print("\n  Flipping a single coin...\n")
    flip_animation()
    result = random.choice(["HEADS", "TAILS"])
    print(f"\r  Result  →  🪙  {result}!          \n")

def flip_many():
    while True:
        try:
            n = int(input("\n  How many times to flip? "))
            if n <= 0:
                print("  ⚠  Enter a positive number.")
                continue
            break
        except ValueError:
            print("  ⚠  Please enter a valid number.")

    print(f"\n  Flipping {n} times", end="", flush=True)
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print()

    heads = 0
    tails = 0
    results = []

    for _ in range(n):
        result = random.choice(["H", "T"])
        results.append(result)
        if result == "H":
            heads += 1
        else:
            tails += 1

    heads_pct = (heads / n) * 100
    tails_pct = (tails / n) * 100

    # show last 20 results visually
    recent = results[-20:]
    visual = "  " + "  ".join("🟡" if r == "H" else "⚫" for r in recent)

    print("\n" + "─" * 40)
    print("  📊  RESULTS")
    print("─" * 40)
    print(f"  Total flips  : {n}")
    print(f"  Heads 🟡     : {heads}  ({heads_pct:.1f}%)")
    print(f"  Tails ⚫     : {tails}  ({tails_pct:.1f}%)")
    print("─" * 40)

    # bar chart
    bar_len = 20
    h_bar = "█" * int((heads / n) * bar_len)
    t_bar = "█" * int((tails / n) * bar_len)
    print(f"\n  H  {h_bar:<20} {heads_pct:.1f}%")
    print(f"  T  {t_bar:<20} {tails_pct:.1f}%")

    if n >= 5:
        print("\n  Last flips (🟡=H  ⚫=T):")
        row = "  "
        for r in recent:
            row += ("🟡" if r == "H" else "⚫") + " "
        print(row)

    print()
    if abs(heads_pct - 50) < 5:
        print("  ✅ Very balanced! Close to 50/50.")
    elif heads > tails:
        print(f"  📈 Heads won this round by {heads - tails} flips!")
    else:
        print(f"  📈 Tails won this round by {tails - heads} flips!")

def streak_challenge():
    print("\n  🎯 STREAK CHALLENGE")
    print("  Keep guessing until you get one wrong!\n")

    score = 0
    while True:
        guess = input(f"  Score: {score}  |  Your guess (h/t/quit): ").strip().lower()
        if guess == 'quit':
            break
        if guess not in ('h', 't'):
            print("  Enter h or t only.")
            continue

        result = random.choice(['h', 't'])
        result_word = "HEADS 🟡" if result == 'h' else "TAILS ⚫"

        if guess == result:
            score += 1
            print(f"  ✅ Correct! It was {result_word}. Streak: {score}\n")
        else:
            print(f"  ❌ Wrong! It was {result_word}. Game over!")
            print(f"  🏆 Final streak: {score}\n")
            break

def main():
    while True:
        clear()
        banner()
        print("\n  1. Flip a single coin")
        print("  2. Flip multiple coins + stats")
        print("  3. Streak challenge (guess streak)")
        print("  4. Exit")

        choice = input("\n  Choose (1/2/3/4): ").strip()

        if choice == '1':
            flip_once()
            input("\n  Press Enter to continue...")

        elif choice == '2':
            clear()
            banner()
            flip_many()
            input("  Press Enter to continue...")

        elif choice == '3':
            clear()
            banner()
            streak_challenge()
            input("  Press Enter to continue...")

        elif choice == '4':
            print("\n  Thanks for flipping! 🪙 Goodbye!\n")
            break

        else:
            print("  ⚠  Please choose 1, 2, 3, or 4.")
            time.sleep(1)

if __name__ == "__main__":
    main()