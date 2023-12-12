#!/usr/bin/python3
"""Script that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name"""

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
        
    if not os.path.exists(sys.argv[1]):
        print(f"Missing {sys.argv[1]}", file=sys.stderr)
        exit(1)
        
    readme = sys.argv[1]
    readhtml = sys.argv[2]
    
    with open(readme, 'r', encoding='utf-8') as readme_file:
        lines = readme_file.readlines()
        
        with open(readhtml, 'w', encoding='utf-8') as tohtml:
            in_list = False
            
            for line in lines:
                if line.startswith('-'):
                    if not in_list:
                        tohtml.write("<ul>\n")
                        in_list = True
                    tohtml.write(f"<li>{line.lstrip('-').strip()}</li>\n")
                else:
                    if in_list:
                        tohtml.write("</ul>\n")
                        in_list = False
                    count = 0
                    for char in line:
                        if char == '#':
                            count += 1
                    if count > 0:
                        tohtml.write(f"<h{count}>{line.strip('#').strip()}</h{count}>\n")

            if in_list:
                tohtml.write("</ul>\n")

