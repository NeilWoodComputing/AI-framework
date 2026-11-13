#!/usr/bin/env python3
"""
Test that links in changed files resolve (file paths exist).

This checks internal file references in the modified documentation.
"""

import sys
import subprocess
from pathlib import Path
import re

def test_links():
    """Test that file links in changed files resolve"""
    repo_root = Path(__file__).parent.parent.parent
    
    try:
        # Get the list of modified files
        result = subprocess.run(
            ["git", "diff", "main...HEAD", "--name-only"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"FAIL: git diff command failed: {result.stderr}")
            return False
        
        modified_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        # Filter for markdown files
        md_files = [f for f in modified_files if f.endswith('.md')]
        
        if not md_files:
            print("PASS: No markdown files to check")
            return True
        
        broken_links = []
        
        for md_file in md_files:
            file_path = repo_root / md_file
            if not file_path.exists():
                continue
            
            content = file_path.read_text(encoding="utf-8")
            file_dir = file_path.parent
            
            # Find relative file path references (../something or ./something)
            # Look for both markdown links and plain references
            patterns = [
                r'\[([^\]]+)\]\(([^)]+)\)',  # [text](link)
                r'`(\.\./[^`]+)`',  # `../path`
                r'`(\./[^`]+)`',    # `./path`
            ]
            
            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    if len(match.groups()) == 2:
                        # Markdown link
                        link = match.group(2)
                    else:
                        # Plain reference
                        link = match.group(1)
                    
                    # Skip URLs
                    if link.startswith(('http://', 'https://', '#', 'mailto:')):
                        continue
                    
                    # Remove anchor
                    link = link.split('#')[0]
                    
                    if not link:
                        continue
                    
                    # Resolve relative path
                    if link.startswith('..') or link.startswith('.'):
                        target_path = (file_dir / link).resolve()
                        
                        # Check if the path exists
                        if not target_path.exists():
                            broken_links.append({
                                'file': md_file,
                                'link': link,
                                'resolved': str(target_path.relative_to(repo_root))
                            })
        
        if broken_links:
            print(f"FAIL: Found {len(broken_links)} broken file link(s):")
            for item in broken_links:
                print(f"  - In {item['file']}: {item['link']} -> {item['resolved']}")
            return False
        
        print(f"PASS: All file links in {len(md_files)} changed markdown file(s) resolve")
        return True
        
    except Exception as e:
        print(f"FAIL: Error checking links: {e}")
        return False

if __name__ == "__main__":
    success = test_links()
    sys.exit(0 if success else 1)
