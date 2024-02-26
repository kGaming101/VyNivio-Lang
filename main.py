variables = {}


def has_indentation(line, start):
  start *= 2
  indent = 0
  for char in line[start:start+2]:
    if char == " ":
      indent += 1
    if indent == 2:
      return True
  return False


def interpret_line(line_num, line, indent_level):
  global variables
  global gline_num

  parts = line.split()

  if not parts:
    return

  if indent_level == 0 and has_indentation(line, indent_level):
    raise SyntaxError(f"Line {line_num} has unexpected indentation ->{line}")

  if parts[0] == "output":
    try:
      print(eval(" ".join(parts[1:]), variables))
    except:
      raise SyntaxError(f"Error on {line_num} -> {line}")

  elif parts[0] == "make":
    changable = "undefined"

    allowed_var_types = {"string", "boolean", "decimal", "list", "dictionary", "multiline_sting"}

    if parts[1] not in ["a", "an"]:
      raise SyntaxError(f"On line {line_num} expected \"a\" or \"an\" -> {line}")

    if parts[1] == "a":
      if parts[2] == "changable":
        changable = True
      elif parts[2] in allowed_var_types:
        var_type = parts[2]
      else:
        raise SyntaxError(f"On line {line_num} expected {', '.join(allowed_var_types)} after \"a\" -> {line}")

    else:
      if parts[2] == "unchangable":
        changable = False
      elif parts[2] in ["integer", "array"]:
        var_type = parts[2]
      else:
        raise SyntaxError(f"On line {line_num} expected unchangable, integer or array after \"an\" -> {line}")

    modifier = 0
    allowed_var_types.remove("list")
    allowed_var_types.add("integer")

    if changable != "undefined":
      modifier = 1
      if parts[3] in allowed_var_types:
        var_type = parts[3]
      else:
        raise SyntaxError(f"On line {line_num} expected {', '.join(allowed_var_types)} -> {line}")

    if parts[3+modifier] != "called":
      raise SyntaxError(f"Line {line_num} is missing \"called\" after \"{parts[2]}\" -> {line}")

    var_name = parts[4+modifier]

    if parts[5+modifier] != "with":
      raise SyntaxError(f"Line {line_num} is missing \"with\" -> {line}")

    if parts[6+modifier] != "value:":
      raise SyntaxError(f"Line {line_num} is missing \"value:\" -> {line}")

    value = None

    if var_type == "string":
      value = " ".join(parts[7+modifier:])

    elif var_type == "integer":
      value = int(parts[7+modifier])

    elif var_type == "boolean":
      value = parts[7+modifier].lower() == "true"

    elif var_type == "decimal":
      value = float(parts[7+modifier])

    elif var_type in ["list", "array"]:
      value = [item.strip() for item in " ".join(parts[7+modifier:]).split(",")]
      if var_type == "list":
        value = list(value)

    elif var_type == "dictionary":
      value = {key.strip(): data.strip() for key, data in [item.split("-") for item in " ".join(parts[7+modifier:]).split(",")]}

    elif var_type == "multiline_sting":
      value = ""
      gline_num += 1
      while True:
        parts = lines[gline_num].split()
        if parts[0] == "end" and parts[1] == "multiline_sting":
          break
        value += lines[gline_num]
        gline_num += 1

    variables[var_name] = value

  else:
    raise SyntaxError(f"On line {line_num} expected \"command\" -> {line}")


file_path = "test_file.vy"

with open(file_path, "r") as file:
    lines = file.readlines()

gline_num = 0
end = len(lines)

try:
    while gline_num < end:
        interpret_line(gline_num, lines[gline_num], 0)
        gline_num += 1

except SyntaxError as e:
    print(f"Syntax Error: {e}")
