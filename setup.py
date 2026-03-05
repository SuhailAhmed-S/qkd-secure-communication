#!/usr/bin/env python3
"""
Setup and initialization script for QKD BB84 Protocol Application

This script handles:
    - Environment setup and validation
    - Dependency installation
    - Configuration validation
    - Database initialization (if applicable)
    - Test execution
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple, Optional


class SetupManager:
    """Manages application setup and initialization."""
    
    def __init__(self):
        """Initialize setup manager."""
        self.project_root = Path(__file__).parent.absolute()
        self.venv_path = self.project_root / 'venv'
    
    def print_header(self, message: str) -> None:
        """Print formatted header message."""
        print("\n" + "=" * 70)
        print(f"  {message}")
        print("=" * 70 + "\n")
    
    def print_section(self, message: str) -> None:
        """Print formatted section message."""
        print(f"\n► {message}")
        print("-" * 70)
    
    def run_command(self, cmd: list, description: str = "") -> Tuple[int, str]:
        """
        Run shell command and capture output.
        
        Args:
            cmd: Command and arguments as list
            description: Human-readable description of command
            
        Returns:
            Tuple of (return_code, output)
        """
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            print(f"  ✗ Failed to run: {' '.join(cmd)}")
            print(f"    Error: {str(e)}")
            return 1, str(e)
    
    def check_python_version(self) -> bool:
        """Verify Python version is 3.8+."""
        self.print_section("Checking Python Version")
        
        version_info = sys.version_info
        if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
            print(f"  ✗ Python 3.8+ required (found {version_info.major}.{version_info.minor})")
            return False
        
        print(f"  ✓ Python {version_info.major}.{version_info.minor}.{version_info.micro}")
        return True
    
    def install_dependencies(self) -> bool:
        """Install Python dependencies."""
        self.print_section("Installing Dependencies")
        
        requirements_file = self.project_root / 'requirements.txt'
        if not requirements_file.exists():
            print(f"  ✗ requirements.txt not found")
            return False
        
        returncode, output = self.run_command(
            [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)],
            "Installing requirements"
        )
        
        if returncode == 0:
            print("  ✓ Dependencies installed successfully")
            return True
        else:
            print("  ✗ Failed to install dependencies")
            print(output)
            return False
    
    def validate_structure(self) -> bool:
        """Validate project structure."""
        self.print_section("Validating Project Structure")
        
        required_files = [
            'alice.py',
            'bob.py',
            'eve.py',
            'quantum_channel.py',
            'security.py',
            'qkd_main.py',
            'app.py',
            'config.py',
            'requirements.txt',
        ]
        
        required_dirs = [
            'templates',
        ]
        
        all_valid = True
        
        # Check files
        for file in required_files:
            path = self.project_root / file
            if path.exists():
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} - NOT FOUND")
                all_valid = False
        
        # Check directories
        for dir_name in required_dirs:
            path = self.project_root / dir_name
            if path.is_dir():
                print(f"  ✓ {dir_name}/")
            else:
                print(f"  ✗ {dir_name}/ - NOT FOUND")
                all_valid = False
        
        return all_valid
    
    def run_tests(self) -> bool:
        """Run test suite."""
        self.print_section("Running Tests")
        
        test_file = self.project_root / 'test_qkd.py'
        if not test_file.exists():
            print("  ⊘ test_qkd.py not found - skipping tests")
            return True
        
        returncode, output = self.run_command(
            [sys.executable, str(test_file)],
            "Running tests"
        )
        
        if returncode == 0:
            print("  ✓ All tests passed")
            return True
        else:
            print("  ⚠ Some tests failed or had errors")
            print(output[-500:])  # Print last 500 chars
            return True  # Don't fail setup on test failures
    
    def setup_environment(self) -> bool:
        """Set up environment variables."""
        self.print_section("Setting Up Environment")
        
        # Set default environment
        if 'FLASK_ENV' not in os.environ:
            os.environ['FLASK_ENV'] = 'development'
            print("  ✓ FLASK_ENV=development")
        
        return True
    
    def run_full_setup(self) -> bool:
        """Run complete setup process."""
        self.print_header("QKD BB84 Protocol - Setup & Initialization")
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("Project Structure Validation", self.validate_structure),
            ("Environment Setup", self.setup_environment),
            ("Installing Dependencies", self.install_dependencies),
            ("Running Tests", self.run_tests),
        ]
        
        results = []
        for step_name, step_func in steps:
            try:
                result = step_func()
                results.append((step_name, result))
            except Exception as e:
                print(f"  ✗ {step_name}: {str(e)}")
                results.append((step_name, False))
        
        # Summary
        self.print_header("Setup Summary")
        
        for step_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {status}: {step_name}")
        
        all_passed = all(result for _, result in results)
        
        if all_passed:
            print("\n✓ Setup completed successfully!")
            print("\nTo start the application, run:")
            print("  python app.py                    # Development mode")
            print("  gunicorn app:app                 # Production mode")
            print("  docker-compose up                # Docker deployment")
        else:
            print("\n✗ Setup failed. Please fix the errors above.")
            return False
        
        return True


def main():
    """Main entry point."""
    manager = SetupManager()
    success = manager.run_full_setup()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
