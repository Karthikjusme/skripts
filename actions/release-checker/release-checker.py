import sys
import re
import os

def parse_tag(tag_name):
    """
    Parse a tag name to extract the version number.
    
    Args:
        tag_name (str): The name of the tag.
    
    Returns:
        tuple: A tuple containing the prefix and a tuple of integers representing the version,
               or (None, None) if no valid version is found.
    """
    # Look for a version number at the end of the tag in the format x.y.z
    match = re.match(r'^(.*-)(\d+\.\d+\.\d+)$', tag_name)
    if match:
        prefix = match.group(1)
        version_str = match.group(2)
        return prefix, tuple(map(int, version_str.split('.')))
    return None, None

def validate_tag(tag):
    """
    Validates if the given tag ends with a valid version number in the format x.y.z.
        
    Args:
        tag (str): The tag to validate.
    
    Returns:
        tuple: (bool, str) where bool is True if the tag is valid, False otherwise,
               and str is a message explaining the validation result.
    """
    prefix, version = parse_tag(tag)
    
    if not version:
        return False, "Tag should end with a version number in the format 'x.y.z' where x, y, and z are integers"
    
    if len(version) != 3:
        return False, f"Version should have exactly 3 parts (x.y.z), but it has {len(version)}"
    
    return True, f"Tag '{tag}' is valid. Detected prefix: '{prefix}', version: {'.'.join(map(str, version))}"

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Please provide a tag as a command-line argument.")
    #     sys.exit(1)

    # current_tag = sys.argv[1]
    current_tag = os.environ.get('GITHUB_REF').replace('refs/tags/', '')
    is_valid, message = validate_tag(current_tag)

    print(message)
    if not is_valid:
        sys.exit(1)