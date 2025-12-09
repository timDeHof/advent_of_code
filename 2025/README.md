# Advent of Code (Python)

This project uses **advent-of-code-data** to automatically fetch puzzle input
and provides a clean structure for daily solutions and tests.

## Setup
1. Create a virtual environment:
```bash
python -m venv venv
  # On Windows use `venv\Scripts\activate`
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your session token in `.env`:
```bash
AOC_SESSION=your_session_token
```

## Quick Start

```bash
# Setup today's puzzle
python setup.py 8

# Setup specific year
python setup.py 1 --year 2023

# Custom folder
python setup.py 5 --folder day_05_custom
```

## Files

- `setup.py` - Simple, clean setup script
- `day-setup-improved.py` - Feature-rich version with error handling
- `day-setup-auto.py` - Auto-detecting seasonal version
- `day-setup-universal.py` - Universal version with interactive mode
- `day-setup-solid.py` - SOLID principles implementation
- `cli-solid.py` - CLI wrapper for SOLID version

## Structure

```
src/
├── day_01/
│   ├── input.txt
│   ├── test-input.txt
│   └── solution.py
└── day_02/
    ├── input.txt
    ├── test-input.txt
    └── solution.py
```
