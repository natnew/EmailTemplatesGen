#!/usr/bin/env python3
"""Test script for the updated EmailTemplatesGen configuration system."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_configuration():
    """Test the configuration system."""
    print("🧪 Testing EmailTemplatesGen Configuration System")
    print("=" * 50)
    
    try:
        from email_templates_gen.config import get_configuration_health
        
        print("1. Testing configuration health check...")
        health = get_configuration_health()
        
        print(f"   Status: {health['status']}")
        print(f"   Settings loaded: {health['settings_loaded']}")
        
        if health['issues']:
            print("   Issues found:")
            for issue in health['issues']:
                print(f"     - {issue}")
        else:
            print("   ✅ No issues found!")
            
        print("\n2. Environment variables status:")
        for var, is_set in health.get('environment_variables', {}).items():
            status = "✅ Set" if is_set else "❌ Missing"
            print(f"   {var}: {status}")
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False
    
    return True


def test_logging():
    """Test the logging system."""
    print("\n🪵 Testing Logging System")
    print("=" * 30)
    
    try:
        from email_templates_gen.utils import setup_logging, get_logger
        
        # Setup logging
        setup_logging("INFO", debug=True)
        logger = get_logger("test")
        
        print("1. Testing basic logging...")
        logger.info("Test info message", test_field="test_value")
        logger.warning("Test warning message", component="test")
        logger.error("Test error message", error_code=123)
        
        print("   ✅ Logging system working!")
        
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        return False
    
    return True


def test_error_handling():
    """Test the error handling system."""
    print("\n🚨 Testing Error Handling")
    print("=" * 30)
    
    try:
        from email_templates_gen.utils.error_handler import (
            OpenAIError, 
            OutlookIntegrationError,
            ConfigurationError
        )
        from email_templates_gen.utils.decorators import log_api_call
        
        print("1. Testing custom exceptions...")
        
        # Test OpenAI error
        try:
            raise OpenAIError("Test OpenAI error", status_code=401)
        except OpenAIError as e:
            print(f"   ✅ OpenAI error caught: {e}")
        
        # Test decorator
        @log_api_call("test_service")
        def test_function():
            return "success"
        
        result = test_function()
        print(f"   ✅ Decorator test: {result}")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("🚀 EmailTemplatesGen - Technical Debt Fix Verification")
    print("=" * 60)
    
    tests = [
        test_configuration,
        test_logging,  
        test_error_handling,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Test Results")
    print("=" * 20)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The technical debt fixes are working correctly.")
        print("\n📝 Next Steps:")
        print("1. Copy .env.example to .env and configure your API keys")
        print("2. Run the Streamlit app: streamlit run app.py")
        print("3. Check the logs/ directory for application logs")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
