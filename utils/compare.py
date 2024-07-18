def parse_styles(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    styles = {}
    current_element = ''
    
    for line in lines:
        line = line.strip()
        if '<' in line and '>' in line:  # Detects the start of a new element description
            current_element = line
            styles[current_element] = {}
        elif line.startswith('Computed Styles:'):
            continue  # Skip the label line
        elif ': ' in line:
            prop, value = line.split(': ', 1)
            styles[current_element][prop] = value
    
    return styles

def compare_styles(old_styles, new_styles):
    differences = {}
    # Check for changes and additions
    for element, props in new_styles.items():
        old_props = old_styles.get(element, {})
        for prop, new_value in props.items():
            old_value = old_props.get(prop)
            if old_value != new_value:
                if element not in differences:
                    differences[element] = {}
                if old_value:
                    differences[element][prop] = f"Changed: Old: {old_value}, New: {new_value}"
                else:
                    differences[element][prop] = f"Added: {new_value}"
    
    # Check for deletions
    for element, props in old_styles.items():
        if element not in new_styles:
            differences[element] = {'Removed': 'Entire element removed'}
        else:
            for prop in props:
                if prop not in new_styles[element]:
                    if element not in differences:
                        differences[element] = {}
                    differences[element][prop] = f"Removed: {props[prop]}"
                    
    return differences

def write_differences_to_file(differences, file_path):
    with open(file_path, 'w') as file:
        file.write('Differences:\n')
        for element, changes in differences.items():
            file.write(f"{element}\n")
            for prop, desc in changes.items():
                file.write(f"  {prop}: {desc}\n")

# Usage example:
old_output_path = 'old.yaml'  # Adjust these file paths as needed
new_output_path = 'new.yaml'
output_differences_path = 'compared.yaml'

old_styles = parse_styles(old_output_path)
new_styles = parse_styles(new_output_path)

differences = compare_styles(old_styles, new_styles)
write_differences_to_file(differences, output_differences_path)
