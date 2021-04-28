# the follwing line reads the list from the input, do not modify it, please
passwords = input().split()

# your code below

for pwd in sorted(passwords, key=len):
    print(pwd, len(pwd))
