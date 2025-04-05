import os

def generate_code_structure(directory, indent=0):
    """Recursively generate the project code structure."""
    structure = ""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            structure += "  " * indent + f"{item}/\n"
            structure += generate_code_structure(item_path, indent + 1)  # Recursively call for subdirectories
        else:
            structure += "  " * indent + f"{item}\n"
    return structure

def save_structure_to_file(directory, output_file):
    """Save the generated code structure to a file."""
    structure = generate_code_structure(directory)
    with open(output_file, 'w') as file:
        file.write(structure)

if __name__ == "__main__":
    project_directory = "C:/Users/Hi/Recruitment-optimizer-agent"  # Replace with your project directory
    output_file = "project_structure.txt"  # The file to save the structure
    save_structure_to_file(project_directory, output_file)
    print(f"Code structure has been saved to {output_file}")
