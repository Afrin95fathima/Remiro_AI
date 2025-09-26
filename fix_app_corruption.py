"""
Fix the corrupted app.py file by removing duplicate content
"""

def fix_app_file():
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the first occurrence of if __name__ == "__main__":
    first_main_index = None
    for i, line in enumerate(lines):
        if 'if __name__ == "__main__":' in line:
            first_main_index = i
            break
    
    if first_main_index is not None:
        # Keep everything up to and including the main() call after the first if __name__
        end_index = first_main_index + 2  # if __name__ line + main() line
        
        # Write the cleaned file
        with open('app_fixed.py', 'w', encoding='utf-8') as f:
            f.writelines(lines[:end_index])
        
        print(f"Fixed app.py - kept first {end_index} lines")
        print("Saved as app_fixed.py")
    else:
        print("Could not find if __name__ == '__main__': line")

if __name__ == "__main__":
    fix_app_file()
