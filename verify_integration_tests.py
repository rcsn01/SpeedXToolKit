import os
import sys
import pandas as pd
import glob

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPECTED_DIR = os.path.join(BASE_DIR, 'intergration-test-files', 'expected')
ACTUAL_DIR = os.path.join(BASE_DIR, 'intergration-test-files', 'actual')

def compare_csv_files(expected_path, actual_path):
    try:
        # Try reading as CSV
        df_expected = pd.read_csv(expected_path)
        df_actual = pd.read_csv(actual_path)
        
        # Compare DataFrames
        pd.testing.assert_frame_equal(df_expected, df_actual)
        return True, "Files match (CSV comparison)"
    except AssertionError as e:
        return False, f"CSV content mismatch: {e}"
    except Exception as e:
        # Fallback to text comparison if CSV reading fails
        try:
            with open(expected_path, 'r', encoding='utf-8') as f1, open(actual_path, 'r', encoding='utf-8') as f2:
                if f1.read() == f2.read():
                    return True, "Files match (Text comparison)"
                else:
                    return False, "Text content mismatch"
        except Exception as e2:
            return False, f"Comparison failed: {e} | {e2}"

def main():
    print(f"Checking integration tests...")
    print(f"Expected Directory: {EXPECTED_DIR}")
    print(f"Actual Directory:   {ACTUAL_DIR}")
    print("-" * 60)

    if not os.path.exists(EXPECTED_DIR):
        print(f"Error: Expected directory not found at {EXPECTED_DIR}")
        sys.exit(1)
    
    if not os.path.exists(ACTUAL_DIR):
        print(f"Error: Actual directory not found at {ACTUAL_DIR}")
        sys.exit(1)

    files = os.listdir(EXPECTED_DIR)
    passed = 0
    failed = 0
    missing = 0

    for filename in files:
        expected_file = os.path.join(EXPECTED_DIR, filename)
        actual_file = os.path.join(ACTUAL_DIR, filename)

        # Skip directories
        if os.path.isdir(expected_file):
            continue

        if not os.path.exists(actual_file):
            print(f"[MISSING] {filename} - File not found in actual folder")
            missing += 1
            continue

        is_match, message = compare_csv_files(expected_file, actual_file)

        if is_match:
            print(f"[PASS]    {filename}")
            passed += 1
        else:
            print(f"[FAIL]    {filename} - {message}")
            failed += 1

    print("-" * 60)
    print(f"Summary: {passed} Passed, {failed} Failed, {missing} Missing")
    
    if failed > 0 or missing > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
