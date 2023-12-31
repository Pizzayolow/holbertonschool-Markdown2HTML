#!/usr/bin/python3
"""Script that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name"""

import sys
import os
import re
import hashlib

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print(f"Missing {sys.argv[1]}", file=sys.stderr)
        exit(1)

    readme = sys.argv[1]
    readhtml = sys.argv[2]

    with open(readme, "r", encoding="utf-8") as readme_file:
        lines = readme_file.readlines()

        with open(readhtml, "w", encoding="utf-8") as tohtml:
            in_list = False
            in_ord_list = False
            p_open = False

            for i, line in enumerate(lines):
                # Search ** ** and replace by <b> </b>
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                
                # Search __ __ and replace by <em> </em>
                line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
                
                if in_list and not (line.startswith('-')):
                    tohtml.write("</ul>\n")
                    in_list = False
                if in_ord_list and not (line.startswith('*')):
                    tohtml.write("</ol>\n")
                    in_ord_list = False
                    
                if p_open and (
                    line.startswith("*")
                    or line.startswith("#")
                    or line.startswith("-")
                    or line.startswith("\n") 
                ):
                    tohtml.write(f"</p>\n")
                    p_open = False
                
                if re.search(r'\(\((.*?)\)\)', line):
                    # Search (( )) in line and remove all c
                    match = re.search(r'\(\((.*?)\)\)', line)
                    without_c = match.group(1)
                    line_without_c = re.sub(r'c', r'', without_c, flags=re.IGNORECASE)
                    line = re.sub(without_c, line_without_c, line, flags=re.IGNORECASE)
                line = re.sub(r'\(\(|\)\)', r'', line)
                
                
                if re.search(r'\[\[(.*?)\]\]', line):
                    match = re.search(r'\[\[(.*?)\]\]', line)
                    content = match.group(1)
                    hashed = hashlib.md5(content.encode('utf-8')).hexdigest()
                    line = re.sub(content, hashed, line, flags=re.IGNORECASE)
                line = re.sub(r'\[\[|\]\]', r'', line)
                

                if line.startswith("#"):
                    count = 0
                    for char in line:
                        if char == "#":
                            count += 1
                    if count > 0:
                        tohtml.write(
                            f"<h{count}>{line.strip('#').strip()}</h{count}>\n"
                        )
                elif line.startswith("-"):
                    if not in_list:
                        tohtml.write("<ul>\n")
                        in_list = True
                    tohtml.write(f"<li>{line.lstrip('-').strip()}</li>\n")
                elif line.startswith("*"):
                    if not in_ord_list:
                        tohtml.write("<ol>\n")
                        in_ord_list = True
                    tohtml.write(f"<li>{line.lstrip('*').strip()}</li>\n")
                elif not line.startswith("\n"):
                    if not p_open:
                        tohtml.write(f"<p>\n")
                        p_open = True
                    else:
                        tohtml.write(f"<br />\n")

                    tohtml.write(f"{line.strip()}\n")
   
