#!/usr/bin/env python3
"""
Version bumping script for PyEPlan package.
Automates version updates across all relevant files.
"""

import re
import subprocess
import sys
from pathlib import Path


def get_current_version():
    """Get current version from __init__.py"""
    init_file = Path("pyeplan/__init__.py")
    with open(init_file, 'r') as f:
        content = f.read()
        match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", content)
        if match:
            return match.group(1)
    raise ValueError("Could not find version in __init__.py")


def update_version_files(new_version):
    """Update version in all relevant files"""
    files_to_update = [
        ("pyeplan/__init__.py", r"__version__\s*=\s*['\"][^'\"]+['\"]", f"__version__ = '{new_version}'"),
        (".bumpversion.cfg", r"current_version\s*=\s*[^\n]+", f"current_version = {new_version}"),
    ]
    
    for file_path, pattern, replacement in files_to_update:
        path = Path(file_path)
        if path.exists():
            with open(path, 'r') as f:
                content = f.read()
            
            new_content = re.sub(pattern, replacement, content)
            
            with open(path, 'w') as f:
                f.write(new_content)
            print(f"Updated {file_path} to version {new_version}")


def validate_version(version):
    """Validate semantic version format"""
    pattern = r'^\d+\.\d+\.\d+$'
    if not re.match(pattern, version):
        raise ValueError(f"Invalid version format: {version}. Expected format: X.Y.Z")
    return version


def git_operations(version):
    """Perform git operations for version bump"""
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit changes
        commit_msg = f"Bump version to {version}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Create and push tag
        tag_name = f"v{version}"
        subprocess.run(["git", "tag", tag_name], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        subprocess.run(["git", "push", "origin", tag_name], check=True)
        
        print(f"Git operations completed: committed and tagged v{version}")
        
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        return False
    return True


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print("Usage: python scripts/bump_version.py <new_version>")
        print("Example: python scripts/bump_version.py 1.1.2")
        print("\nOptions:")
        print("  -h, --help, help  Show this help message")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    try:
        # Validate version format
        new_version = validate_version(new_version)
        
        # Get current version
        current_version = get_current_version()
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")
        
        # Confirm with user
        response = input(f"Bump version from {current_version} to {new_version}? (y/N): ")
        if response.lower() != 'y':
            print("Version bump cancelled.")
            sys.exit(0)
        
        # Update files
        update_version_files(new_version)
        
        # Git operations
        if git_operations(new_version):
            print(f"Successfully bumped version to {new_version}")
        else:
            print("Version files updated but git operations failed.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 