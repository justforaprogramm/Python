'''https://www.mit.edu/~ecprice/wordlist.10000, https://lingojam.com/TexttoOneLine
'''
from pathlib import Path

def main(sequence) -> str:
    return '\x20'.join(reversed([i for i in sequence.split('\x20') if i]))

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    file_path = script_dir / "rev.txt"
    out_path = script_dir / "out.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        sequence = f.readline().strip()

    result = main(sequence)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)