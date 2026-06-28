import re

def check_variable_naming(lines):
    variables_found = []
    naming_warnings = []
    
    for line in lines:
        line = line.strip()
        
        # Skip comments
        if line.startswith("#"):
            continue
        
        # Skip lines with == 
        if "==" in line:
            continue
        
        # Check if line has a single = sign
        if "=" in line:
            # Split only on the first =
            parts = line.split("=", 1)
            var_name = parts[0].strip()
            
            # Skip if it's not a simple variable name
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', var_name):
                continue
            
            variables_found.append(var_name)
            
            # Check snake_case
            if not re.match(r'^[a-z_][a-z0-9_]*$', var_name):
                naming_warnings.append(var_name)
    
    return {
        "variables_found": variables_found,
        "naming_warnings": naming_warnings
    }

# Test it with sample lines
test_lines = [
    "my_variable = 10",
    "totalScore = 50",
    "BadName = 5",
    "if x == 5:",
    "# this is a comment",
    "good_name_here = 100"
]

result = check_variable_naming(test_lines)
print(result)