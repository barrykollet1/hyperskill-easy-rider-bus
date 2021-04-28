import re


# put your regex in the variable template
template = r"^(\d{1,2}(\/|\.)){2}(\d{4}).*"
string = input()
# compare the string and the template
match = re.match(template, string)
print(match.group(3) if match else None)

