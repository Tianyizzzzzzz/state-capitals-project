#!/usr/bin/env python3
"""
Step 5: Verify the final JSON file with coordinates
"""

import json
import os

def verify_final_json(filename):
    """Comprehensive verification of the final JSON file with coordinates."""
    
    print("Step 5: Verifying the final JSON file...")
    print(f"Checking file: {filename}")
    
    try:
        # Basic file checks
        if not os.path.exists(filename):
            print(f"❌ File does not exist: {filename}")
            return False
        
        file_size = os.path.getsize(filename)
        print(f"📁 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        # Load and parse JSON
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ JSON syntax is valid")
        
        # Structure verification
        required_root_keys = ['metadata', 'states']
        for key in required_root_keys:
            if key not in data:
                print(f"❌ Missing root key: {key}")
                return False
        print("✅ Root structure is valid")
        
        # Metadata verification
        metadata = data['metadata']
        expected_metadata_keys = ['title', 'total_states']
        for key in expected_metadata_keys:
            if key not in metadata:
                print(f"❌ Missing metadata key: {key}")
                return False
        print("✅ Metadata structure is valid")
        
        # States data verification
        states = data['states']
        if not isinstance(states, list):
            print("❌ States should be a list")
            return False
        
        total_states = len(states)
        expected_total = 50
        
        if total_states != expected_total:
            print(f"❌ Expected {expected_total} states, found {total_states}")
            return False
        print(f"✅ Correct number of states: {total_states}")
        
        # Individual state verification
        required_fields = [
            'state', 'state_abbr', 'capital', 'address_line_1', 
            'address_line_2', 'city', 'zip_code_5', 'zip_code_4'
        ]
        
        coordinate_fields = ['latitude', 'longitude']
        
        states_with_coords = 0
        states_missing_coords = 0
        validation_errors = []
        
        print(f"\n🔍 Verifying individual state records...")
        
        for i, state in enumerate(states):
            state_name = state.get('state', f'State {i+1}')
            
            # Check required fields
            missing_fields = []
            for field in required_fields:
                if field not in state:
                    missing_fields.append(field)
            
            if missing_fields:
                validation_errors.append(f"{state_name}: Missing fields: {missing_fields}")
                continue
            
            # Check coordinate fields
            has_coordinates = True
            for field in coordinate_fields:
                if field not in state or state[field] is None:
                    has_coordinates = False
                    break
            
            if has_coordinates:
                # Validate coordinate values
                try:
                    lat = float(state['latitude'])
                    lon = float(state['longitude'])
                    
                    # Check coordinate ranges
                    if not (-90 <= lat <= 90):
                        validation_errors.append(f"{state_name}: Invalid latitude: {lat}")
                        continue
                    
                    if not (-180 <= lon <= 180):
                        validation_errors.append(f"{state_name}: Invalid longitude: {lon}")
                        continue
                    
                    states_with_coords += 1
                    
                except (ValueError, TypeError):
                    validation_errors.append(f"{state_name}: Invalid coordinate format")
                    states_missing_coords += 1
            else:
                states_missing_coords += 1
        
        # Report validation results
        print(f"\n📊 VALIDATION RESULTS:")
        print(f"   States with valid coordinates: {states_with_coords}")
        print(f"   States missing/invalid coordinates: {states_missing_coords}")
        print(f"   Coordinate completeness: {(states_with_coords / total_states * 100):.1f}%")
        
        if validation_errors:
            print(f"\n❌ Validation errors found:")
            for error in validation_errors[:10]:  # Show first 10 errors
                print(f"   • {error}")
            if len(validation_errors) > 10:
                print(f"   ... and {len(validation_errors) - 10} more errors")
        
        # Data quality assessment
        print(f"\n📈 DATA QUALITY ASSESSMENT:")
        
        # Completeness
        completeness = states_with_coords / total_states
        if completeness >= 0.95:
            print(f"   ✅ Completeness: EXCELLENT ({completeness*100:.1f}%)")
        elif completeness >= 0.90:
            print(f"   ✅ Completeness: GOOD ({completeness*100:.1f}%)")
        elif completeness >= 0.80:
            print(f"   ⚠️  Completeness: FAIR ({completeness*100:.1f}%)")
        else:
            print(f"   ❌ Completeness: POOR ({completeness*100:.1f}%)")
        
        # Check for essential states
        essential_states = ['California', 'Texas', 'Florida', 'New York', 'Alaska', 'Hawaii']
        found_essential = []
        missing_essential = []
        
        for state in states:
            if state.get('state') in essential_states:
                if state.get('latitude') is not None and state.get('longitude') is not None:
                    found_essential.append(state['state'])
                else:
                    missing_essential.append(state['state'])
        
        if not missing_essential:
            print(f"   ✅ Essential states: ALL PRESENT with coordinates")
        else:
            print(f"   ⚠️  Essential states missing coordinates: {missing_essential}")
        
        # Overall file assessment
        is_valid = (len(validation_errors) == 0 and 
                   states_with_coords >= total_states * 0.90 and  # 90% completeness
                   not missing_essential)
        
        if is_valid:
            print(f"\n🎉 FINAL VERIFICATION: PASSED")
            print(f"   ✅ File structure is correct")
            print(f"   ✅ All required data is present")
            print(f"   ✅ Coordinates are valid and complete")
            print(f"   ✅ File is ready for use and distribution")
        else:
            print(f"\n⚠️  FINAL VERIFICATION: ISSUES FOUND")
            print(f"   📝 File needs attention before final use")
        
        # File summary
        print(f"\n📋 FILE SUMMARY:")
        print(f"   Total states: {total_states}")
        print(f"   States with coordinates: {states_with_coords}")
        print(f"   File size: {file_size:,} bytes")
        print(f"   Validation errors: {len(validation_errors)}")
        
        print(f"\n✅ Step 5 Complete: Final JSON verification finished")
        
        return is_valid
        
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

if __name__ == "__main__":
    filename = 'data/state_capitals_with_coords.json'
    success = verify_final_json(filename)
    
    if success:
        print("\n🏆 Final verification PASSED! File is ready for distribution.")
    else:
        print("\n📝 Final verification completed with issues that need attention.")
