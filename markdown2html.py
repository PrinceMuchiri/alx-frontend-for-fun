#!/usr/bin/python3

"""
Markdown script using python.
"""

import sys
import os.path
import re
import hashlib

def handle_bold_and_emphasis(line):
    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
    return line

def handle_md5(line):
    md5_matches = re.findall(r'\[\[(.+?)\]\]', line)
    for md5_match in md5_matches:
        line = line.replace(f"[[{md5_match}]]", hashlib.md5(md5_match.encode()).hexdigest())
    return line

def handle_remove_letter_c(line):
    remove_letter_c_matches = re.findall(r'\(\((.+?)\)\)', line)
    for match in remove_letter_c_matches:
        line = line.replace(f"(({match}))", match.replace('C', '').replace('c', ''))
    return line

def convert_markdown_to_html(markdown_file, output_file):
    unordered_start, ordered_start, paragraph = False, False, False

    with open(markdown_file) as read:
        with open(output_file, 'w') as html:
            for line in read:
                line = line.strip()

                line = handle_bold_and_emphasis(line)
                line = handle_md5(line)
                line = handle_remove_letter_c(line)

                length = len(line)
                headings = line.lstrip('#')
                heading_num = length - len(headings)
                unordered = line.lstrip('-')
                unordered_num = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_num = length - len(ordered)

                if 1 <= heading_num <= 6:
                    line = f"<h{heading_num}>{headings.strip()}</h{heading_num}>"

                if unordered_num:
                    if not unordered_start:
                        html.write('<ul>\n')
                        unordered_start = True
                    line = f"<li>{unordered.strip()}</li>"

                if unordered_start and not unordered_num:
                    html.write('</ul>\n')
                    unordered_start = False

                if ordered_num:
                    if not ordered_start:
                        html.write('<ol>\n')
                        ordered_start = True
                    line = f"<li>{ordered.strip()}</li>"

                if ordered_start and not ordered_num:
                    html.write('</ol>\n')
                    ordered_start = False

                if not (heading_num or unordered_start or ordered_start):
                    if not paragraph and length > 1:
                        html.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        html.write('<br/>\n')
                    elif paragraph:
                        html.write('</p>\n')
                        paragraph = False

                if length > 1:
                    html.write(line + '\n')

            if unordered_start:
                html.write('</ul>\n')
            if ordered_start:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')

def main():
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        print(f'Missing {markdown_file}', file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(markdown_file, output_file)
    sys.exit(0)

if __name__ == '__main__':
    main()
