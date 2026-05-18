# palindrome – CLI Help

A command-line tool that checks whether strings are **palindromes** or
**palindrome sentences**.

> A palindrome reads the same forwards and backwards (e.g. `racecar`).  
> A palindrome sentence ignores spaces, punctuation, and casing
> (e.g. `A man a plan a canal Panama`).

---

## Usage

```
python3 main.py <STR|FILE> [--json] [--help] [--version]
```

| Argument / Flag | Description |
|-----------------|-------------|
| `STR`           | Any string to check, passed directly on the command line. |
| `FILE`          | Path to a `.json` file containing a string or list of strings. |
| `--json`        | Output results as JSON instead of human-readable text. |
| `--help`        | Show the built-in help message and exit. |
| `--version`     | Show the version number and exit. |

---

## Examples

### Single string

```bash
python3 main.py "racecar"
```
```
  'racecar'  →  ✓ IS a palindrome
```

### Palindrome sentence

```bash
python3 main.py "A man a plan a canal Panama"
```
```
  'A man a plan a canal Panama'  →  ✓ IS a palindrome
```

### Non-palindrome

```bash
python3 main.py "hello"
```
```
  'hello'  →  ✗ is NOT a palindrome
```

### JSON file – list of strings

Create `words.json`:
```json
["racecar", "level", "A man a plan a canal Panama", "hello"]
```

Then run:
```bash
python3 main.py words.json
```
```
  'racecar'                      →  ✓ IS a palindrome
  'level'                        →  ✓ IS a palindrome
  'A man a plan a canal Panama'  →  ✓ IS a palindrome
  'hello'                        →  ✗ is NOT a palindrome
```

### JSON output flag

```bash
python3 main.py words.json --json
```
```json
[
  { "input": "racecar",                      "is_palindrome": true  },
  { "input": "level",                        "is_palindrome": true  },
  { "input": "A man a plan a canal Panama",  "is_palindrome": true  },
  { "input": "hello",                        "is_palindrome": false }
]
```

---

## JSON file format

The file must contain **one of**:

| Format | Example |
|--------|---------|
| A single string | `"racecar"` |
| An array of strings | `["racecar", "level", "hello"]` |

Any other structure causes an error with a clear message.

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0`  | All inputs are palindromes (or `--help` / `--version` was used). |
| `1`  | At least one input is **not** a palindrome. |
| `2`  | Bad arguments or file error. |

This lets you use the tool in shell scripts:

```bash
python3 main.py "racecar" && echo "Yep, palindrome!"
```

---

## Requirements

- Python **3.10+** (uses `list[str]` type hint in function signature)
- No third-party packages – standard library only