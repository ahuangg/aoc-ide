## Advent of Code IDE

This script automates the daily setup process for Advent of Code challenges by creating
a new directory structure and fetching necessary problem data. It creates a template
for solving the day's puzzle with basic input parsing and solution structure.

### Prerequisites

1. Python 3.x.x

### Installation

1. Install required packages

    ```bash
    pip install -r requirements.txt
    ```

2. Get your Advent of Code session ID

    1. Log in Advent of Code
    2. Open Developer Tools (F12 or right-click -> Inspect)
    3. Go to Application/Storage -> Cookies
    4. Find the 'session' cookie for adventofcode.com
    5. Copy its value

3. Create environment file and add session ID

    ```bash
    SESSION_ID="PASTE_HERE"
    ```

### Usage

1. Start the tool

    ```bash
    python3 main.py
    ```

2. The tool will

    1. Create necessary directories
    2. Fetech problem descriptions
    3. Setup solution templates
    4. Monitor submissions

3. Submitting solutions

    1. modify the parse_input function to align with the question input and run the cell
    2. edit in the python solution code block only
    3. paste your solution value into the submission cell and run
