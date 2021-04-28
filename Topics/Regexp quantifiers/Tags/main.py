import re


template = r'<[a-z]+>.*?</[a-z]+>'

# <start></start><start></start>, should be <start></start>
