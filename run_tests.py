#!/usr/bin/env python3
"""
Test runner for the tweety library.
This script allows you to run tests from the project root directory.
"""

import sys
import os
import subprocess
import argparse

def run_test(test_name):
    """Run a specific test file."""
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    test_file = os.path.join(test_dir, f"{test_name}.py")
    
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return False
    
    print(f"🧪 Running {test_name}...")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, test_file], cwd=os.path.dirname(__file__))
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

def list_tests():
    """List all available tests."""
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    if not os.path.exists(test_dir):
        print("❌ Tests directory not found")
        return
    
    print("📋 Available Tests:")
    print("=" * 40)
    
    test_files = [f for f in os.listdir(test_dir) if f.startswith('test_') and f.endswith('.py')]
    demo_files = [f for f in os.listdir(test_dir) if f.startswith('demo') and f.endswith('.py')]
    
    if test_files:
        print("\n🧪 Test Files:")
        for test_file in sorted(test_files):
            test_name = test_file[:-3]  # Remove .py extension
            print(f"  - {test_name}")
    
    if demo_files:
        print("\n🎮 Demo Files:")
        for demo_file in sorted(demo_files):
            demo_name = demo_file[:-3]  # Remove .py extension
            print(f"  - {demo_name}")
    
    print(f"\n📖 Documentation:")
    print(f"  - TESTING.md (comprehensive testing guide)")

def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description='Run tweety library tests')
    parser.add_argument('test', nargs='?', help='Test name to run (without .py extension)')
    parser.add_argument('--list', '-l', action='store_true', help='List all available tests')
    parser.add_argument('--all', '-a', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    if args.list:
        list_tests()
        return
    
    if args.all:
        print("🚀 Running all tests...")
        print("=" * 60)
        
        test_dir = os.path.join(os.path.dirname(__file__), 'tests')
        test_files = [f for f in os.listdir(test_dir) if f.startswith('test_') and f.endswith('.py')]
        
        results = []
        for test_file in sorted(test_files):
            test_name = test_file[:-3]  # Remove .py extension
            success = run_test(test_name)
            results.append((test_name, success))
            print()  # Add spacing between tests
        
        # Summary
        print("📊 Test Summary:")
        print("=" * 40)
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}: {test_name}")
        
        print(f"\nResults: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed.")
        
        return
    
    if args.test:
        success = run_test(args.test)
        sys.exit(0 if success else 1)
    
    # No arguments provided, show help
    print("🧪 Tweety Library Test Runner")
    print("=" * 40)
    print("Usage:")
    print("  python run_tests.py <test_name>     # Run specific test")
    print("  python run_tests.py --all           # Run all tests")
    print("  python run_tests.py --list          # List available tests")
    print()
    print("Examples:")
    print("  python run_tests.py test_basic")
    print("  python run_tests.py demo")
    print("  python run_tests.py --all")
    print()
    list_tests()

if __name__ == "__main__":
    main()
