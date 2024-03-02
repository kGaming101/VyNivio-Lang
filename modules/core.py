variables = {}
metadata = {}


def has_indentation(line, start):
  start *= 2
  indent = 0
  for char in line[start:start+2]:
    if char == " ":
      indent += 1
    if indent == 2:
      return True
  return False



def output(variables,line):
    parts = line.split()
    value = ""

    for part in parts[1:]:
        
        if part.startswith("%$"):
            if part.replace("%$","") in variables:
                part = part.replace("%$","")
                value += str(variables[part]) + " "
        else:
            value += str(part) + " "

    print(value)



def make(variables,lines,line_num):
    global metadata
    parts = lines[line_num].split()
    changable = "undefined"
    modifier = 0

    allowed_var_types = {"string", "boolean", "decimal", "list", "dictionary", "multiline_sting"}


    if parts[1] not in ["a", "an"]:
        raise SyntaxError(f"On line {line_num+1} expected \"a\" or \"an\" -> {lines[line_num]}")
    
    elif parts[1] == "a":
        if parts[2] == "changable":
            changable = True
            modifier = 1
            allowed_var_types.remove("list")
            allowed_var_types.add("integer")
        elif parts[2] in allowed_var_types:
            var_type = parts[2]
        else:
            raise SyntaxError(f"On line {line_num+1} expected {', '.join(allowed_var_types)} or changable after \"a\" -> {lines[line_num]}")
    
    else:
        if parts[2] == "unchangable":
            changable = False
            modifier = 1
            allowed_var_types.remove("list")
            allowed_var_types.add("integer")
        elif parts[2] == "integer":
            var_type = parts[2]
        else:
            raise SyntaxError(f"On line {line_num+1} expected unchangable or integer after \"an\" -> {lines[line_num]}")


    if modifier == 1:
        if parts[3] in allowed_var_types:
            var_type = parts[3]
        else:
            raise SyntaxError(f"On line {line_num+1} expected {', '.join(allowed_var_types)} -> {lines[line_num]}")
        
    
    if parts[3+modifier] != "called":
        raise SyntaxError(f"Line {line_num+1} is missing \"called\" after \"{parts[2]}\" -> {lines[line_num]}")


    if parts[4+modifier][0] != "_":
        var_name = parts[4+modifier]
    else:
        raise SyntaxError(f"Line {line_num} has a variable declared starting with \"_\". Variables can't start with \"_\" --> {lines[line_num]}")


    if parts[5+modifier] != "with":
        raise SyntaxError(f"Line {line_num+1} is missing \"with\" after \"{parts[4+modifier]}\" -> {lines[line_num]}")


    if parts[6+modifier] != "value:":
        raise SyntaxError(f"Line {line_num+1} is missing \"value:\" after \"with\" -> {lines[line_num]}")


    value = ""


    if var_type == "string":
        value = " ".join(parts[7+modifier:])

    elif var_type == "integer":
        value = int(parts[7+modifier])

    elif var_type == "boolean":
        value = parts[7+modifier].lower() == "true"

    elif var_type == "decimal":
        value = float(parts[7+modifier])

    elif var_type in "list":
        value = [item.strip() for item in " ".join(parts[7+modifier:]).split(",")]

    elif var_type == "dictionary":
        value = {key.strip(): data.strip() for key, data in [item.split("-") for item in " ".join(parts[7+modifier:]).split(",")]}

    elif var_type == "multiline_sting":
        line_num += 1
        while True:
            if lines[line_num] == "end multiline_sting\n":
                break
            value += lines[line_num]
            line_num += 1
    
    variables[var_name] = value
    metadata[var_name] = {
        "type":var_type,
        "changability":changable
        }

    return variables, line_num

def interpret_line(line_num, lines, indent_level):
    global variables
    global meta_data

    parts = lines[line_num].split()

    if not parts:
        return line_num

    if has_indentation(lines[line_num], indent_level):
        raise SyntaxError(f"Line {line_num} has unexpected indentation ->{lines[line_num]}")
    
    if parts[0] == "output":
        output(variables,lines[line_num])
    
    elif parts[0] == "make":
        variables, line_num  = make(variables,lines,line_num)
        

    else:
        raise SyntaxError(f"On line {line_num+1} expected \"command\" -> {lines[line_num]}")
    
    return line_num