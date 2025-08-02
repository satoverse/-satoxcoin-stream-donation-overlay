#!/bin/bash
# Comprehensive Test Runner for Satoxcoin Stream Donation Overlay
# Runs all tests across all platforms and test types

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
START_TIME=$(date +%s)

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "PASS")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "FAIL")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
    esac
}

# Function to run Python tests
run_python_tests() {
    local test_path=$1
    local test_name=$2
    
    print_status "INFO" "Running $test_name..."
    
    # Check if test directory exists
    if [ ! -d "$test_path" ]; then
        print_status "WARN" "Test directory not found: $test_path"
        return 0
    fi
    
    # Try pytest first, then unittest
    if command -v pytest >/dev/null 2>&1; then
        if python3 -m pytest "$test_path" -v --tb=short >/tmp/test_output.txt 2>&1; then
            print_status "PASS" "$test_name"
            return 0
        fi
    fi
    
    # Fallback to unittest
    if python3 -m unittest discover "$test_path" -v >/tmp/test_output.txt 2>&1; then
        print_status "PASS" "$test_name"
        return 0
    fi
    
    # If we get here, tests failed
    print_status "FAIL" "$test_name"
    echo "Test output:"
    cat /tmp/test_output.txt
    return 1
}

# Function to run shell script tests
run_shell_tests() {
    local test_path=$1
    local test_name=$2
    
    print_status "INFO" "Running $test_name..."
    
    # Check if test script exists
    if [ ! -f "$test_path/test.sh" ]; then
        print_status "WARN" "No test script found in $test_path"
        return 0
    fi
    
    # Make script executable and run it
    chmod +x "$test_path/test.sh"
    if (cd "$test_path" && ./test.sh) >/tmp/test_output.txt 2>&1; then
        print_status "PASS" "$test_name"
        return 0
    else
        print_status "FAIL" "$test_name"
        echo "Test output:"
        cat /tmp/test_output.txt
        return 1
    fi
}

# Function to run unit tests
run_unit_tests() {
    echo "==================== Unit Tests ===================="
    if run_python_tests "test/unit" "Unit Tests"; then
        ((PASSED_TESTS++))
    else
        ((FAILED_TESTS++))
    fi
    ((TOTAL_TESTS++))
}

# Function to run integration tests
run_integration_tests() {
    echo "================ Integration Tests ================"
    if run_python_tests "test/integration" "Integration Tests"; then
        ((PASSED_TESTS++))
    else
        ((FAILED_TESTS++))
    fi
    ((TOTAL_TESTS++))
}

# Function to run end-to-end tests
run_e2e_tests() {
    echo "================ End-to-End Tests ================="
    if run_python_tests "test/e2e" "End-to-End Tests"; then
        ((PASSED_TESTS++))
    else
        ((FAILED_TESTS++))
        fi
    ((TOTAL_TESTS++))
}

# Function to run performance tests
run_performance_tests() {
    echo "================ Performance Tests ================"
    if run_python_tests "test/performance" "Performance Tests"; then
        ((PASSED_TESTS++))
    else
        ((FAILED_TESTS++))
    fi
    ((TOTAL_TESTS++))
}

# Function to run platform tests
run_platform_tests() {
    echo "================ Platform Tests ==================="
    
    local platforms_dir="test/platforms"
    if [ ! -d "$platforms_dir" ]; then
        print_status "WARN" "No platform tests found"
        return 0
    fi
    
    local platform_failed=false
    
    for platform in "$platforms_dir"/*; do
        if [ -d "$platform" ]; then
            platform_name=$(basename "$platform")
            if run_python_tests "$platform" "Platform Tests ($platform_name)"; then
                ((PASSED_TESTS++))
            else
                ((FAILED_TESTS++))
                platform_failed=true
            fi
            ((TOTAL_TESTS++))
        fi
    done
    
    if [ "$platform_failed" = true ]; then
        return 1
    fi
    return 0
}

# Function to run system health checks
run_health_checks() {
    echo "================ Health Checks ===================="
    
    local health_passed=0
    local health_total=0
    
    # Check Python version
    if python3 --version >/dev/null 2>&1; then
        print_status "PASS" "Python 3 available"
        ((health_passed++))
    else
        print_status "FAIL" "Python 3 not available"
    fi
    ((health_total++))
    
    # Check required Python modules
    local required_modules=("requests" "unittest" "json" "time" "os" "sys")
    for module in "${required_modules[@]}"; do
        if python3 -c "import $module" >/dev/null 2>&1; then
            print_status "PASS" "Module $module available"
            ((health_passed++))
        else
            print_status "FAIL" "Module $module not available"
            fi
        ((health_total++))
    done
    
    # Check required files
    local required_files=("alert.html" "demo.html" "wallet_monitor.py" "satox-logo.png" "coin.mp3")
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            if [ -r "$file" ]; then
                print_status "PASS" "File $file readable"
                ((health_passed++))
            else
                print_status "FAIL" "File $file not readable"
            fi
        else
            print_status "FAIL" "File $file not found"
        fi
        ((health_total++))
    done
    
    echo "Health checks: $health_passed/$health_total passed"
    
    if [ $health_passed -eq $health_total ]; then
        return 0
    else
        return 1
    fi
}

# Function to print test summary
print_summary() {
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    
    echo ""
    echo "=================================================="
    echo "📊 TEST SUMMARY"
    echo "=================================================="
    echo "Total Test Suites: $TOTAL_TESTS"
    echo "Passed: $PASSED_TESTS"
    echo "Failed: $FAILED_TESTS"
    
    if [ $TOTAL_TESTS -gt 0 ]; then
        local success_rate=$(echo "scale=1; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc -l 2>/dev/null || echo "N/A")
        echo "Success Rate: ${success_rate}%"
    else
        echo "Success Rate: N/A"
    fi
    
    echo "Duration: ${duration} seconds"
    echo ""
    
    if [ $FAILED_TESTS -eq 0 ]; then
        print_status "PASS" "ALL TESTS PASSED!"
    else
        print_status "FAIL" "$FAILED_TESTS test(s) failed"
    fi
}

# Function to save results
save_results() {
    local results_file="test/test_results.json"
    local timestamp=$(date -Iseconds)
    
    # Create JSON summary
    cat > "$results_file" << EOF
{
  "timestamp": "$timestamp",
  "total_tests": $TOTAL_TESTS,
  "passed_tests": $PASSED_TESTS,
  "failed_tests": $FAILED_TESTS,
  "success_rate": $(echo "scale=1; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc -l 2>/dev/null || echo "null"),
  "duration": $(( $(date +%s) - START_TIME )),
  "results": {
    "unit_tests": $([ $PASSED_TESTS -gt 0 ] && echo "true" || echo "false"),
    "integration_tests": $([ $PASSED_TESTS -gt 0 ] && echo "true" || echo "false"),
    "e2e_tests": $([ $PASSED_TESTS -gt 0 ] && echo "true" || echo "false"),
    "performance_tests": $([ $PASSED_TESTS -gt 0 ] && echo "true" || echo "false"),
    "platform_tests": $([ $PASSED_TESTS -gt 0 ] && echo "true" || echo "false")
  }
}
EOF
    
    echo "📄 Results saved to: $results_file"
}

# Main function
main() {
    echo "🚀 Starting Comprehensive Test Suite"
    echo "=================================================="
    echo "Started at: $(date)"
    echo "Working directory: $(pwd)"
    echo ""
    
    # Run health checks first
    if run_health_checks; then
        ((PASSED_TESTS++))
    else
        ((FAILED_TESTS++))
    fi
    ((TOTAL_TESTS++))
    
    # Run all test suites
    run_unit_tests
    run_integration_tests
    run_e2e_tests
    run_performance_tests
    run_platform_tests
    
    # Print summary and save results
    print_summary
    save_results
    
    # Exit with appropriate code
    if [ $FAILED_TESTS -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@" 