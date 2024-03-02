from modules.core import *

file_path = "test_file.vy"

with open(file_path, "r") as file:
    lines = file.readlines()

gline_num = 0
end = len(lines)

try:
    while gline_num < end:
        gline_num = interpret_line(gline_num, lines, 0)
        gline_num += 1

except SyntaxError as e:
    print(f"Syntax Error: {e}")