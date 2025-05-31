#!/usr/bin/env python3
"""
Step 2: Verify that the JSON file is valid
"""

import json
import sys

def verify_json_file(filename):
    """Verify that the JSON file is valid and has correct structure."""
    
    print(f"Step 2: Verifying JSON file validity...")
    print(f"Checking file: {filename}")
    
    try:
        # Test 1: Can we load the JSON file?
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON syntax is valid")
        
        # Test 2: Does it have the expected structure?
        if 'metadata' not in data:
            print("❌ Missing 'metadata' section")
            return False
        print("✅ Metadata section found")
        
        if 'states' not in data:
            print("❌ Missing 'states' section")
            return False
        print("✅ States section found")
        
        # Test 3: Do we have 50 states?
        states_count = len(data['states'])
        if states_count != 50:
            print(f"❌ Expected 50 states, found {states_count}")
            return False
        print(f"✅ Correct number of states: {states_count}")
        
        # Test 4: Check required fields in each state
        required_fields = ['state', 'state_abbr', 'capital', 'address_line_1', 'city', 'zip_code_5']
        missing_fields = []
        
        for i, state in enumerate(data['states']):
            for field in required_fields:
                if field not in state:
                    missing_fields.append(f"State {i+1}: missing {field}")
        
        if missing_fields:
            print("❌ Missing required fields:")
            for missing in missing_fields[:5]:  # Show first 5 errors
                print(f"   {missing}")
            return False
        print("✅ All required fields present")
        
        # Test 5: Check for empty critical fields
        empty_fields = []
        for i, state in enumerate(data['states']):
            state_name = state.get('state', f'State {i+1}')
            if not state.get('state', '').strip():
                empty_fields.append(f"{state_name}: empty state name")
            if not state.get('capital', '').strip():
                empty_fields.append(f"{state_name}: empty capital name")
            if not state.get('address_line_1', '').strip():
                empty_fields.append(f"{state_name}: empty address")
        
        if empty_fields:
            print("❌ Found empty critical fields:")
            for empty in empty_fields[:5]:
                print(f"   {empty}")
            return False
        print("✅ No empty critical fields")
        
        # Test 6: Quick data sample check
        sample_state = data['states'][0]  # Check first state (Alabama)
        if sample_state['state'] == 'Alabama' and sample_state['capital'] == 'Montgomery':
            print("✅ Data sample verification passed")
        else:
            print("❌ Data sample verification failed")
            return False
        
        print(f"\n🎉 Step 2 Complete: JSON file is valid!")
        print(f"   📊 Verified {states_count} state records")
        print(f"   ✅ All structural requirements met")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

if __name__ == "__main__":
    filename = 'data/state_capitals.json'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    success = verify_json_file(filename)
    sys.exit(0 if success else 1)
