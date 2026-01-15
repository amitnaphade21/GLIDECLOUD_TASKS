"""
Test Runner Script
Run all tests with detailed reporting and coverage analysis
"""
import subprocess
import sys
import os
from pathlib import Path


def run_all_tests():
    """Run all tests with pytest"""
    print("=" * 80)
    print("Running ALL Tests")
    print("=" * 80)
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    return result.returncode


def run_tests_by_category():
    """Run tests organized by category"""
    test_categories = {
        "Health Tests": "tests/test_health.py",
        "Vector API Tests": "tests/test_vectors.py",
        "Vector Store Tests": "tests/test_vector_store.py",
        "ChromaDB Storage Tests": "tests/test_chroma_storage.py",
        "Embeddings Service Tests": "tests/test_embeddings_service.py",
        "Chunking Utils Tests": "tests/test_chunking_utils.py",
        "Request Schema Tests": "tests/test_request_schemas.py",
    }
    
    results = {}
    
    for category, test_file in test_categories.items():
        print("\n" + "=" * 80)
        print(f"Running {category}")
        print("=" * 80)
        
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        results[category] = result.returncode == 0
    
    return results


def run_tests_with_coverage():
    """Run tests with coverage report"""
    print("\n" + "=" * 80)
    print("Running Tests with Coverage Report")
    print("=" * 80)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", 
             "--cov=.", "--cov-report=html", "--cov-report=term-missing"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print("\n✓ Coverage report generated in htmlcov/index.html")
        return result.returncode
    except Exception as e:
        print(f"✗ Coverage analysis failed: {str(e)}")
        print("  Install coverage: pip install pytest-cov")
        return 1


def run_quick_tests():
    """Run quick sanity tests"""
    print("\n" + "=" * 80)
    print("Running Quick Sanity Tests")
    print("=" * 80)
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_health.py", "-v"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    return result.returncode


def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run tests for RAG Backend")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tests"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick sanity tests"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run tests with coverage report"
    )
    parser.add_argument(
        "--category",
        action="store_true",
        help="Run tests by category"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Run specific test file"
    )
    
    args = parser.parse_args()
    
    # Default to all tests if no option specified
    if not any([args.all, args.quick, args.coverage, args.category, args.file]):
        args.all = True
    
    if args.quick:
        return run_quick_tests()
    elif args.coverage:
        return run_tests_with_coverage()
    elif args.category:
        results = run_tests_by_category()
        print("\n" + "=" * 80)
        print("Test Results Summary")
        print("=" * 80)
        for category, passed in results.items():
            status = "✓ PASSED" if passed else "✗ FAILED"
            print(f"{category}: {status}")
        return 0 if all(results.values()) else 1
    elif args.file:
        print(f"Running {args.file}")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", args.file, "-v"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result.returncode
    else:  # args.all
        return run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
