#!/usr/bin/env python
"""
Backend Integration Test Script

Tests the Smart Building Energy Prediction FastAPI backend endpoints.

This script verifies:
1. Health check endpoint
2. Prediction endpoint with real model
3. Insights endpoint
4. Stats endpoint

Usage:
    python test.py              # Run all tests
    python test.py --no-server  # Test without running server
    python test.py --endpoint http://localhost:8001  # Custom endpoint
"""

import sys
import argparse
import time
import subprocess
import requests
import json
from pathlib import Path
from typing import Dict, Optional

# Add backend app to path for direct testing
backend_path = Path(__file__).parent / "app"
sys.path.insert(0, str(backend_path.parent))


class BackendTester:
    """Test harness for the FastAPI backend."""
    
    def __init__(self, endpoint: str = "http://localhost:8000"):
        """Initialize the tester with the API endpoint."""
        self.endpoint = endpoint.rstrip("/")
        self.session = requests.Session()
        self.results = {
            "passed": 0,
            "failed": 0,
            "tests": []
        }
    
    def test_health(self) -> bool:
        """Test the health check endpoint."""
        print("\n[TEST 1] Health Check (GET /)")
        print("-" * 60)
        
        try:
            response = self.session.get(f"{self.endpoint}/")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Status: {response.status_code}")
                print(f"✓ Message: {data.get('message')}")
                print(f"✓ Version: {data.get('version')}")
                self._record_test("Health Check", True)
                return True
            else:
                print(f"✗ Unexpected status: {response.status_code}")
                self._record_test("Health Check", False)
                return False
        
        except Exception as e:
            print(f"✗ Error: {e}")
            self._record_test("Health Check", False)
            return False
    
    def test_predict(self) -> bool:
        """Test the prediction endpoint with sample data."""
        print("\n[TEST 2] Prediction (POST /predict)")
        print("-" * 60)
        
        # Sample feature values
        test_data = {
            "RH_6": 50.0,
            "Windspeed": 5.0,
            "Visibility": 40.0,
            "Tdewpoint": 5.0,
            "rv1": 100.0,
            "hour": 14.0,
            "hour_sin": 0.951,
            "hour_cos": -0.309
        }
        
        try:
            print(f"Sending prediction request with features:")
            for key, value in test_data.items():
                print(f"  {key}: {value}")
            
            response = self.session.post(
                f"{self.endpoint}/predict",
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n✓ Status: {response.status_code}")
                print(f"✓ Energy: {result['energy_wh']:.2f} Wh")
                print(f"✓ Cost: {result['cost_inr']:.3f} INR")
                print(f"✓ CO2: {result['co2_kg']:.4f} kg")
                
                # Validate response format
                if all(k in result for k in ["energy_wh", "cost_inr", "co2_kg"]):
                    if result['energy_wh'] > 0:
                        print(f"✓ Prediction is realistic (non-zero)")
                        self._record_test("Prediction", True)
                        return True
                    else:
                        print(f"⚠ Warning: Zero or negative prediction")
                        self._record_test("Prediction", False)
                        return False
                else:
                    print(f"✗ Missing fields in response")
                    self._record_test("Prediction", False)
                    return False
            else:
                print(f"✗ Unexpected status: {response.status_code}")
                print(f"Response: {response.text}")
                self._record_test("Prediction", False)
                return False
        
        except Exception as e:
            print(f"✗ Error: {e}")
            self._record_test("Prediction", False)
            return False
    
    def test_insights(self) -> bool:
        """Test the insights endpoint."""
        print("\n[TEST 3] Insights (GET /insights)")
        print("-" * 60)
        
        try:
            response = self.session.get(f"{self.endpoint}/insights", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Status: {response.status_code}")
                
                if "top_drivers" in data and "descriptions" in data:
                    print(f"✓ Top drivers: {', '.join(data['top_drivers'][:3])}...")
                    print(f"✓ Descriptions: {len(data['descriptions'])} items")
                    self._record_test("Insights", True)
                    return True
                else:
                    print(f"✗ Missing required fields")
                    self._record_test("Insights", False)
                    return False
            else:
                print(f"✗ Unexpected status: {response.status_code}")
                self._record_test("Insights", False)
                return False
        
        except Exception as e:
            print(f"✗ Error: {e}")
            self._record_test("Insights", False)
            return False
    
    def test_stats(self) -> bool:
        """Test the stats endpoint."""
        print("\n[TEST 4] Stats (GET /stats)")
        print("-" * 60)
        
        try:
            response = self.session.get(f"{self.endpoint}/stats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Status: {response.status_code}")
                
                if all(k in data for k in ["model_type", "features_used", "co2_factor"]):
                    print(f"✓ Model Type: {data['model_type']}")
                    print(f"✓ Features: {len(data['features_used'])} total")
                    print(f"✓ CO2 Factor: {data['co2_factor']} kg CO2/kWh")
                    self._record_test("Stats", True)
                    return True
                else:
                    print(f"✗ Missing required fields")
                    self._record_test("Stats", False)
                    return False
            else:
                print(f"✗ Unexpected status: {response.status_code}")
                self._record_test("Stats", False)
                return False
        
        except Exception as e:
            print(f"✗ Error: {e}")
            self._record_test("Stats", False)
            return False
    
    def test_direct_model(self) -> bool:
        """Test the model loading and prediction directly (no HTTP)."""
        print("\n[TEST 5] Direct Model Loading (No HTTP)")
        print("-" * 60)
        
        try:
            from app.predict import get_predictor
            from app.schemas import PredictRequest
            
            predictor = get_predictor()
            print(f"✓ Model loaded successfully")
            
            # Create test request
            req = PredictRequest(
                RH_6=50.0,
                Windspeed=5.0,
                Visibility=40.0,
                Tdewpoint=5.0,
                rv1=100.0,
                hour=14.0,
                hour_sin=0.951,
                hour_cos=-0.309
            )
            
            result = predictor.predict(req)
            print(f"✓ Prediction made directly")
            print(f"  - Energy: {result.energy_wh:.2f} Wh")
            print(f"  - Cost: {result.cost_inr:.3f} INR")
            print(f"  - CO2: {result.co2_kg:.4f} kg")
            
            self._record_test("Direct Model Loading", True)
            return True
        
        except Exception as e:
            print(f"✗ Error: {e}")
            self._record_test("Direct Model Loading", False)
            return False
    
    def _record_test(self, name: str, passed: bool):
        """Record test result."""
        status = "PASS" if passed else "FAIL"
        self.results["tests"].append({"name": name, "status": status})
        if passed:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        for test in self.results["tests"]:
            status_symbol = "✓" if test["status"] == "PASS" else "✗"
            print(f"{status_symbol} {test['name']}: {test['status']}")
        
        total = self.results["passed"] + self.results["failed"]
        print(f"\nTotal: {self.results['passed']}/{total} tests passed")
        
        if self.results["failed"] == 0:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n⚠️  {self.results['failed']} test(s) failed")
        
        print("="*70 + "\n")


def run_tests(endpoint: str, include_direct: bool = True):
    """Run all backend tests."""
    tester = BackendTester(endpoint)
    
    print("\n" + "="*70)
    print("SMART BUILDING ENERGY PREDICTION - BACKEND TESTS")
    print("="*70)
    print(f"API Endpoint: {endpoint}")
    
    # Wait for server to be ready
    max_retries = 30
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{endpoint}/", timeout=2)
            if response.status_code == 200:
                print("✓ Server is ready\n")
                break
        except:
            if attempt == max_retries - 1:
                print(f"✗ Server not responding after {max_retries} attempts")
                print("  Make sure the backend is running with: python run.py")
                return
            time.sleep(0.5)
    
    # Run tests
    tester.test_health()
    tester.test_predict()
    tester.test_insights()
    tester.test_stats()
    
    if include_direct:
        tester.test_direct_model()
    
    # Print summary
    tester.print_summary()


def main():
    """Parse arguments and run tests."""
    parser = argparse.ArgumentParser(
        description="Test the Smart Building Energy Prediction FastAPI backend"
    )
    parser.add_argument(
        "--endpoint",
        default="http://localhost:8000",
        help="API endpoint URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--no-direct",
        action="store_true",
        help="Skip direct model loading test"
    )
    
    args = parser.parse_args()
    
    run_tests(args.endpoint, include_direct=not args.no_direct)


if __name__ == "__main__":
    main()
