import os
def generate_negative_lookup_file():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('negative'):
            f.write(f'negative/{filename}\n')