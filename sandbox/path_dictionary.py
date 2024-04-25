test = {
    'A': 'a',
    'B': 'b',
    'C': 'c',
    'D': 'd'
}

from pathlib import Path

p = Path('sandbox')

p2 = p /test['A'] / test['B'] / test['C'] / test['D']

test['A'] = 'A12'

print(p2)