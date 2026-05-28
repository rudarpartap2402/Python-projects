import random
import time

print(f''' 
      .....NUMBER GUESSING GAME.....
      ''')

###############################
#
#          easy game
#
###############################
    
def easy_game(st,end,n):
        num =  random.randint(st,end)
        i = 1

        print("Game starting in...")
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("GO!")
        while True and i <= n:

            guess = (int(input("Pick A Number Between 1 to 10 : ")))

            if(guess > num):
                if abs(guess - num) <= 1:
                     print("You Are Very Close , The Number is Smaller ")
                elif abs(guess - num) <= 10:
                     print("You Are Close , The Number is Smaller ")
                else:
                    print()
                    print("You Went Over!!")
                    print()
                i+=1
            elif(guess < num):
                if abs(guess - num) <= 1:
                     print("You Are Very Close , The Number is Larger")
                elif abs(guess - num) <= 10:
                     print("You Are Close , The Number is Larger")
                else:
                    print()
                    print("You Picked A Smaller Number!!!")
                    print()
                i += 1
            else:
                print()
                print(f'''You Guessed it...
                    The Number was {guess}''')
                break

        if(i > n):
                print()
                print(f'''You Couldn't Guess it Under {n} Tries''')
                print()

###############################
#
#          medium game
#
###############################

def medium_game(st,end):

        num = random.randint(st,end)
        i = 1

        print("Game starting in...")
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("GO!")

        while True and i <= 10:
            
            guess = (int(input("Pick A Number Between 1 to 100 : ")))

            if(guess > num):
                if abs(guess - num) <= 1:
                     print("You Are Very Close , The Number is Smaller ")
                elif abs(guess - num) <= 10:
                     print("You Are Close , The Number is Smaller ")
                else:
                    print()
                    print("You Went Over!!")
                    print()
                    i+=1
            elif(guess < num):
                if abs(guess - num) <= 1:
                     print("You Are Very Close , The Number is Larger ")
                elif abs(guess - num) <= 10:
                     print("You Are Close , The Number is Larger")
                else:
                    print()
                    print("You Picked A Smaller Number!!!")
                    print()
                    i+=1
            else:
                print()
                print(f'''You Guessed it...
                    The Number was {guess}''')
                break

        if(i > 10):
                print()
                print(f'''You Couldn't Guess it Under 10 Tries''')
                print()

###############################
#
#          streak game 
#
###############################

def streak_game():

    num = random.randint(1, 100)
    count = 0

    print("Game starting in...")

    for i in ["3", "2", "1", "GO!"]:
        print(i)
        time.sleep(1)

    start_time = time.time()
    total_time = 60

    while True:

        elapsed = int(time.time() - start_time)
        remaining = total_time - elapsed

        if remaining <= 0:
            print("\nTime's Up!")
            print(f"You guessed {count} times")
            break

        print(f"\nTime left: {remaining} seconds")
        print()

        guess = int(input("Pick A Number Between 1 to 100: "))

        if guess > num:

            if abs(guess - num) <= 1:
                print("You Are Very Close, The Number is Smaller")

            elif abs(guess - num) <= 10:
                print("You Are Close, The Number is Smaller")

            else:
                print("You Went Over!!")

        elif guess < num:

            if abs(guess - num) <= 1:
                print("You Are Very Close, The Number is Larger")

            elif abs(guess - num) <= 10:
                print("You Are Close, The Number is Larger")

            else:
                print("You Picked A Smaller Number!!!")

        else:

            print(f"\nYou Guessed it... The Number was {guess}")

            count += 1
            num = random.randint(1, 100)

            print("New Number Generated!")
     
###############################
#
#       calling functions
#
###############################
      
play = input("Do You Wanna Play This Game(Yes/No) : ")
if (play == "yes" or play == "Yes"):
    print("1. Easy Mode (1 to 10) ")
    print("2. Medium Mode (1 to 100) in 10 Tries ")
    print(f'''3. Streak Challenge
Guess The Numbers in 30 sec''')
    print(f'''4. Challenge
Guess Number in 3 Tries''')

    mode  = int(input("Enter Your Mode : "))
    if mode == 1:
        easy_game(1,10,100)
    elif mode == 2:
        medium_game(1,100)
    elif mode == 3:
        streak_game()
    elif mode == 4:
         easy_game(1,10,3)  
