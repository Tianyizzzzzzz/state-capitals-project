#!/usr/bin/env python3
"""
Step 2.1: Verify addresses using Mock USPS validation
"""

import json
import time
import re
from datetime import datetime

def mock_usps_validate_address(address_line_1, city, state, zip_code):
    """Mock USPS address validation - simulates real validation."""
    
    # Simulate processing time
    time.sleep(0.05)
    
    # Basic validation checks
    issues = []
    
    if not address_line_1.strip():
        issues.append("Missing street address")
    if not city.strip():
        issues.append("Missing city")
    if not state.strip() or len(state) != 2:
        issues.append("Invalid state abbreviation")
    if not zip_code.strip() or not zip_code.isdigit() or len(zip_code) != 5:
        issues.append("Invalid ZIP code")
    
    if issues:
        return {
            'valid': False,
            'errors': issues,
            'original': {
                'address_line_1': address_line_1,
                'city': city,
                'state': state,
                'zip_code': zip_code
            }
        }
    
    # Mock standardization (convert to USPS format)
    standardized_address = address_line_1.upper()
    # Apply common abbreviations
    standardized_address = re.sub(r'\bSTREET\b', 'ST', standardized_address)
    standardized_address = re.sub(r'\bAVENUE\b', 'AVE', standardized_address)
    standardized_address = re.sub(r'\bBOULEVARD\b', 'BLVD', standardized_address)
    standardized_address = re.sub(r'\bDRIVE\b', 'DR', standardized_address)
    standardized_address = re.sub(r'\bROAD\b', 'RD', standardized_address)
    
    # Generate mock ZIP+4
    mock_zip4 = str(hash(f"{address_line_1}{city}{state}") % 10000).zfill(4)
    
    return {
        'valid': True,
        'standardized': {
            'address_line_1': standardized_address,
            'city': city.title(),
            'state': state.upper(),
            'zip_code_5': zip_code,
            'zip_code_4': mock_zip4
        },
        'original': {
            'address_line_1': address_line_1,
            'city': city,
            'state': state,
            'zip_code': zip_code
        }
    }

def verify_addresses_usps_mock(input_file, output_file):
    """Verify addresses using mock USPS validation."""
    
    print("Step 2.1: Verifying addresses using Mock USPS validation...")
    
    # Load input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    validated_data = data.copy()
    successful_validations = 0
    failed_validations = 0
    
    print(f"Processing {len(data['states'])} addresses...")
    
    # Process each state
    for i, state_info in enumerate(data['states']):
        state_name = state_info['state']
        capital = state_info['capital']
        
        print(f"[{i+1:2d}/50] Validating {state_name} - {capital}")
        
        # Validate address
        validation_result = mock_usps_validate_address(
            state_info['address_line_1'],
            state_info['city'],
            state_info['state_abbr'],
            state_info['zip_code_5']
        )
        
        # Add validation result to state data
        state_info['usps_validation'] = validation_result
        
        if validation_result['valid']:
            # Update with standardized data
            if 'standardized' in validation_result:
                state_info['address_line_1'] = validation_result['standardized']['address_line_1']
                state_info['city'] = validation_result['standardized']['city']
                state_info['state_abbr'] = validation_result['standardized']['state']
                state_info['zip_code_5'] = validation_result['standardized']['zip_code_5']
                state_info['zip_code_4'] = validation_result['standardized']['zip_code_4']
            
            successful_validations += 1
            print(f"        ✅ Address validated and standardized")
        else:
            failed_validations += 1
            print(f"        ❌ Validation failed: {', '.join(validation_result['errors'])}")
    
    # Add validation metadata
    validated_data['metadata']['usps_validation'] = {
        'validation_date': datetime.now().isoformat(),
        'validation_type': 'mock_usps',
        'total_addresses': len(data['states']),
        'successful_validations': successful_validations,
        'failed_validations': failed_validations,
        'success_rate': f"{(successful_validations / len(data['states']) * 100):.1f}%",
        'step': "Step 2.1 - Mock USPS validation"
    }
    
    # Save validated data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(validated_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Step 2.1 Complete: Mock USPS validation finished")
    print(f"   📊 Successfully validated: {successful_validations}/{len(data['states'])} addresses")
    print(f"   📁 Output file: {output_file}")
    
    return successful_validations == len(data['states'])

if __name__ == "__main__":
    input_file = 'data/state_capitals.json'
    output_file = 'data/state_capitals_validated.json'
    
    success = verify_addresses_usps_mock(input_file, output_file)
    if not success:
        print("⚠️  Some addresses failed validation")
