units = int(input())

if units < 1:
    print("no army")
elif 1 <= units <= 9:
    print("few")
elif 10 <= units <= 49:
    print("pack")
elif 50 <= units <= 499:
    print("horde")
elif 500 <= units <= 999:
    print("swarm")
elif units >= 1000:
    print("legion")
