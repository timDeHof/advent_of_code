# Advent of Code Setup

Clean workspace for Advent of Code solutions.

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

## Dependencies

```bash
pip install aocd python-dotenv
```

Set your session token in `.env`:
```
AOC_SESSION=your_session_token
```