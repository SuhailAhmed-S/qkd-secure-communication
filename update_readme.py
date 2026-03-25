#!/usr/bin/env python3
"""Replace old README with new comprehensive version"""

import shutil
import os

# Backup old README
if os.path.exists('README.md'):
    shutil.copy('README.md', 'README_BACKUP.md')
    print('✓ Backed up old README.md → README_BACKUP.md')

# Replace with new README
if os.path.exists('README_NEW.md'):
    shutil.move('README_NEW.md', 'README.md')
    print('✓ Replaced README.md with new comprehensive version')
    
# Verify
if os.path.exists('README.md'):
    size = os.path.getsize('README.md')
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
        print(f'✓ New README.md: {size:,} bytes, {lines} lines')
        print('✓ Documentation update complete!')
    except UnicodeDecodeError:
        print('✓ README.md updated successfully')

