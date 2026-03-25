#!/usr/bin/env python3
"""
Project cleanup script - removes redundant/temporary files
"""

import os
import sys

# Files to delete (redundant markdown files)
CLEANUP_MD_FILES = [
    'QUANTUM_THEME.md',           # Old version
    'QUANTUM_THEME_FINAL.md',     # Old version
    'QUANTUM_THEME_SUMMARY.md',   # Old version
    'PRIVACY_AMPLIFICATION_SUMMARY.md',  # Duplicate content
    'README_PRIVACY_AMPLIFICATION.md',   # Duplicate content
    'CLEANUP_SUMMARY.md',         # Temporary
    'PROJECT_STRUCTURE.md',       # Temporary
    'LIVE_FEED_VERIFICATION.md',  # Temporary verification
]

# Test/utility scripts that were used during development (optional deletion)
CLEANUP_TEST_FILES = [
    'test_fix.py',
    'test_integration.py',
    'test_privacy_amplification.py',
    'test_qkd.py',
    'test_quick.py',
    'fix_simulator.py',
    'build_simulator.py',
    'verify_sim.py',
    'update_simulator.py',
    'clean_simulator.py',
    'privacy_amplification_integration.py',  # This is just a guide, not used
    'CHECK_DELIVERY.py',
    'PRIVACY_AMPLIFICATION_GUIDE.py',  # This is a guide file, not used in code
]

# Output log files that can be deleted
CLEANUP_LOG_FILES = [
    'guide_output.log',
    'integration_output.txt',
    'pa_output.txt',
]

def cleanup_files(file_list, description):
    """Delete files from the list"""
    deleted = []
    failed = []
    
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    
    for filename in file_list:
        filepath = os.path.join(os.getcwd(), filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                deleted.append(filename)
                print(f"  ✓ Deleted {filename}")
            except Exception as e:
                failed.append((filename, str(e)))
                print(f"  ✗ Failed to delete {filename}: {e}")
        else:
            print(f"  - {filename} (not found, skipped)")
    
    return deleted, failed

def main():
    """Main cleanup routine"""
    print("\n" + "="*60)
    print("  QKD PROJECT CLEANUP")
    print("="*60)
    
    total_deleted = []
    total_failed = []
    
    # Clean up redundant markdown files
    deleted, failed = cleanup_files(CLEANUP_MD_FILES, "Removing redundant markdown files")
    total_deleted.extend(deleted)
    total_failed.extend(failed)
    
    # Clean up test/utility files
    deleted, failed = cleanup_files(CLEANUP_TEST_FILES, "Removing development/test scripts")
    total_deleted.extend(deleted)
    total_failed.extend(failed)
    
    # Clean up log files
    deleted, failed = cleanup_files(CLEANUP_LOG_FILES, "Removing temporary log files")
    total_deleted.extend(deleted)
    total_failed.extend(failed)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"  CLEANUP SUMMARY")
    print(f"{'='*60}")
    print(f"  ✓ Deleted: {len(total_deleted)} files")
    print(f"  ✗ Failed:  {len(total_failed)} files")
    
    if total_deleted:
        print(f"\n  Files deleted:")
        for f in total_deleted:
            print(f"    - {f}")
    
    if total_failed:
        print(f"\n  Files failed to delete:")
        for f, reason in total_failed:
            print(f"    - {f} ({reason})")
    
    print(f"\n  ✓ Cleanup complete!\n")

if __name__ == '__main__':
    main()
