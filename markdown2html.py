#!/usr/bin/python3
"""Script that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name"""

import sys
import os
import re

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
        
    if not os.path.exists(sys.argv[1]):
        print(f"Missing {sys.argv[1]}", file=sys.stderr)
        exit(1)
        
    readme = sys.argv[1]
    readhtml = sys.argv[2]
    count = 0
    
    # Définir une expression régulière pour trouver les titres
    with open(readme, 'r', encoding='utf-8') as readme:
            lines = readme.readlines()
            with open(readhtml, 'w', encoding='utf-8') as tohtml:
                for line in lines:
                    count=0
                    for char in line:
                        if char == '#':
                            count += 1
                        elif char == '-':
                            print("TIRET")
                            tohtml.write(f"<ul>\n<li>{line.strip('-').strip()}</li>\n</ul>\n")
                
                    if count > 0:
                            tohtml.write(f"<h{count}>{line.strip('#').strip()}</h{count}>\n")
                tohtml.write(f"de la boucle")