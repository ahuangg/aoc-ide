"""
Advent of Code IDE Setup

This script automates the daily setup process for Advent of Code challenges by creating
a new directory structure and fetching necessary problem data. It creates a template
for solving the day's puzzle with basic input parsing and solution structure.

Usage:
    python3 main.py
    
Note:
    Input parsing is template-based and may need modification depending on the specific
    problem requirements. Each day's puzzle might require different parsing strategies.
    
@author ahuangg
@date: 2024-12-01
@version: 1.0.0
"""

import requests
import os
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

class Client:
    def __init__(self, session_id):
        self.session = requests.Session()
        self.session.cookies.set('session', session_id)
        self.session.headers.update({
            'User-Agent': 'github.com/ahuangg/advent-of-code-2024 by ahuang7840@gmail.com'
        })
        
        now = datetime.now()
        self.year = now.year
        self.day = now.day
        
        self.dir_name = f"aoc_{self.year}/day_{self.day}"
        self.notebook = None
        
        self.solved = {1: False, 2: False}
        self.solution = None
        
        self.submitted = set([None])
    
    def run(self): 
        self.check_solved()
        
        if self.confirm_solved():
            return
        
        if not os.path.exists(self.dir_name): 
            self.create_template()
    
        self.load_notebook()
        
        while self.notebook and (not self.solved[1] or not self.solved[2]):
            if 0 <= len(self.notebook["cells"]) < 3:
                part_1 = self.get_problem_part_1()
                self.update_template("input1", part_1)
                self.get_input("input1")
                print(f"Updated notebook for {self.year} day {self.day} - Part 1")
                continue
                
            if self.solved[1] and len(self.notebook["cells"]) < 5: 
                part_2 = self.get_problem_part_2()
                self.update_template("input2", part_2)
                self.get_input("input2")
                print(f"Updated notebook for {self.year} day {self.day} - Part 2")
                continue
            
            if not self.solved[1]:
                self.solution = self.read_solution(3)
            else:
                self.solution = self.read_solution(6)
                
            if self.solution and self.solution not in self.submitted:
                self.submitted.add(self.solution)
                self.submit_solution(1 if not self.solved[1] else 2)
                
            time.sleep(1)
            
        self.confirm_solved()     
        
    def create_template(self):
        os.makedirs(self.dir_name, exist_ok=True)
        file_path = os.path.join(self.dir_name, "solutions.ipynb")
        self.notebook = {
				"cells": [{ "cell_type": "code", "metadata": {}, "source":[
        			"def parse_input(file_path):\n",
					"    with open(file_path, 'r') as file:\n",
					"        for line in file:\n",
					"            pass\n",
					"    return"
          		] }],
				"metadata": {
					"kernelspec": {
						"display_name": "Python 3",
						"language": "python",
						"name": "python3"
					}
				},
				"nbformat": 4,
				"nbformat_minor": 4
			}
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.notebook, f)
        
        print(f"Created template for {self.year} day {self.day}")
                
    def update_template(self, input, content):
        markdown_cell = { "cell_type": "markdown", "metadata": {}, "source": content }
        code_cell = { "cell_type": "code", "metadata": {}, "source": [
			"def solution():\n",
            "    pass\n",
            "\n",
            f"input = parse_input('{input}.txt')\n",
            "solution()"
		] }
        submission_cell = { "cell_type": "code", "metadata": {}, "source": [
			"# Submission\n",
		] }
        
        self.notebook["cells"].append(markdown_cell)
        self.notebook["cells"].append(code_cell)
        self.notebook["cells"].append(submission_cell)
        
        with open(self.dir_name + "/solutions.ipynb", 'w', encoding='utf-8') as f:
            json.dump(self.notebook, f)
    
    def load_notebook(self):
        with open(self.dir_name + "/solutions.ipynb", 'r') as f:
            time.sleep(1)  
            self.notebook = json.load(f)


    def get_problem_part_1(self):
        url = f'https://adventofcode.com/{self.year}/day/{self.day}'
        response = self.session.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article = soup.find_all('article', class_='day-desc')
            
            if len(article) > 1:
                self.solved[1] = True
            
            if article:
                return str(article[0])
            
        return None
    
    def get_problem_part_2(self):
        url = f'https://adventofcode.com/{self.year}/day/{self.day}'
        response = self.session.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article = soup.find_all('article', class_='day-desc')
    
            if article:
                return str(article[1])
            
        return None
    
    def get_input(self, filename):
        url = f'https://adventofcode.com/{self.year}/day/{self.day}/input'
        response = self.session.get(url)
        
        with open(self.dir_name + f"/{filename}.txt", 'w') as f:
            f.write(response.text)
            
    def read_solution(self, index):
        self.load_notebook()
            
        cell = self.notebook['cells'][index]
        outputs = cell.get('outputs', [])
        
        for output in outputs:
            if output.get('output_type') == 'error':
                break
            
            return output.get('data', {}).get('text/plain')[0]
			
        return None
    
    def submit_solution(self, level):
        payload = {
			"level": level,
			"answer": self.solution
		}
        
        url = f'https://adventofcode.com/{self.year}/day/{self.day}/answer'
        response = self.session.post(url, data=payload)
    
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('article')
    
        if article:
            text = article.get_text().strip()
            print(text)
            
            if "That's not the right answer." in text:
                return
            elif "You gave an answer too recently" in text:
                return 
            elif "You don't seem to be solving the right level." in text:
                return 
            else:
                self.solved[level] = True
                self.solution = None
                
    def check_solved(self):
        url = f'https://adventofcode.com/{self.year}/day/{self.day}'
        response = self.session.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            p = soup.find_all('p', class_='day-success')
    
            if p:
                self.solved[1] = True
                self.solved[2] = True
            
        return None
        
    def confirm_solved(self):
        if self.solved[1] and self.solved[2]:
            print(f"Completed {self.year} day {self.day}")
            return True

        return False

def main():
    load_dotenv('.env')
    
    client = Client(os.getenv('SESSION_ID'))
    client.run()
    
if __name__ == '__main__':
    main()