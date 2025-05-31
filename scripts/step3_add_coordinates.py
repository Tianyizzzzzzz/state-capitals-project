#!/usr/bin/env python3
"""
Step 3: Add longitude and latitude coordinates to the JSON file
This script reads the JSON file and adds geographic coordinates to each state capital.
"""

import json
import requests
import time
from datetime import datetime

def geocode_address_nominatim(address, city, state, zip_code):
    """Get coordinates using Nominatim (OpenStreetMap) geocoding service."""
    
    # Build address string for better geocoding results
    full_address = f"{address}, {city}, {state} {zip_code}, USA"
    
    # Nominatim API parameters
    params = {
        'q': full_address,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'us',  # Restrict to US addresses
        'addressdetails': 1
    }
    
    headers = {
        'User-Agent': 'StateCapitalsProject/1.0 (Educational Research)'
    }
    
    try:
        print(f"        Geocoding: {full_address}")
        
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params=params,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                result = data[0]
                latitude = float(result['lat'])
                longitude = float(result['lon'])
                
                # Validate coordinates are reasonable for US
                if 18.0 <= latitude <= 72.0 and -180.0 <= longitude <= -66.0:
                    return {
                        'success': True,
                        'latitude': round(latitude, 6),
                        'longitude': round(longitude, 6),
                        'source': 'nominatim',
                        'display_name': result.get('display_name', '')
                    }
                else:
                    return {
                        'success': False,
                        'error': f'Coordinates outside US bounds: {latitude}, {longitude}',
                        'source': 'nominatim'
                    }
        
        return {
            'success': False,
            'error': f'No results found (HTTP {response.status_code})',
            'source': 'nominatim'
        }
        
    except requests.RequestException as e:
        return {
            'success': False,
            'error': f'Request failed: {str(e)}',
            'source': 'nominatim'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Geocoding error: {str(e)}',
            'source': 'nominatim'
        }

def add_coordinates_to_json(input_file, output_file):
    """Add latitude and longitude coordinates to all state capitals."""
    
    print("Step 3: Adding longitude and latitude coordinates...")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
    # Load input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded input file successfully")
    except Exception as e:
        print(f"❌ Failed to load input file: {e}")
        return 0, 0
    
    enhanced_data = data.copy()
    successful_geocodes = 0
    failed_geocodes = 0
    failed_addresses = []
    
    print(f"\n🌍 Geocoding {len(data['states'])} state capitals...")
    print("Using Nominatim (OpenStreetMap) geocoding service")
    print("Rate limit: 1 request per second")
    print("="*60)
    
    # Process each state
    for i, state_info in enumerate(data['states']):
        state_name = state_info['state']
        capital = state_info['capital']
        
        print(f"[{i+1:2d}/50] {state_name} - {capital}")
        
        # Get coordinates
        geocode_result = geocode_address_nominatim(
            state_info['address_line_1'],
            state_info['city'],
            state_info['state_abbr'],
            state_info['zip_code_5']
        )
        
        # Add geocoding result to state data
        if geocode_result['success']:
            state_info['latitude'] = geocode_result['latitude']
            state_info['longitude'] = geocode_result['longitude']
            state_info['geocoding_status'] = 'success'
            state_info['geocoding_service'] = geocode_result['source']
            
            successful_geocodes += 1
            print(f"        ✅ Success: {geocode_result['latitude']}, {geocode_result['longitude']}")
        else:
            state_info['latitude'] = None
            state_info['longitude'] = None
            state_info['geocoding_status'] = 'failed'
            state_info['geocoding_error'] = geocode_result['error']
            state_info['geocoding_service'] = geocode_result['source']
            
            failed_geocodes += 1
            failed_addresses.append(f"{state_name} - {capital}")
            print(f"        ❌ Failed: {geocode_result['error']}")
        
        # Rate limiting: Nominatim requires at least 1 second between requests
        if i < len(data['states']) - 1:  # Don't sleep after the last request
            print(f"        ⏱️  Waiting 1 second (rate limiting)...")
            time.sleep(1.2)  # 1.2 seconds to be safe
    
    # Add geocoding metadata
    enhanced_data['metadata']['geocoding'] = {
        'geocoding_date': datetime.now().isoformat(),
        'geocoding_service': 'nominatim',
        'total_addresses': len(data['states']),
        'successful_geocodes': successful_geocodes,
        'failed_geocodes': failed_geocodes,
        'success_rate': f"{(successful_geocodes / len(data['states']) * 100):.1f}%",
        'failed_addresses': failed_addresses,
        'step': "Step 3 - Coordinate addition",
        'note': "Coordinates added using Nominatim (OpenStreetMap) geocoding service"
    }
    
    # Save enhanced data
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Output file saved successfully: {output_file}")
    except Exception as e:
        print(f"\n❌ Failed to save output file: {e}")
        return successful_geocodes, failed_geocodes
    
    print(f"\n" + "="*60)
    print(f"✅ Step 3 Complete: Coordinates added to JSON file")
    print(f"📊 Results Summary:")
    print(f"   Successfully geocoded: {successful_geocodes}/{len(data['states'])} addresses")
    print(f"   Failed geocodes: {failed_geocodes}/{len(data['states'])} addresses")
    print(f"   Success rate: {(successful_geocodes / len(data['states']) * 100):.1f}%")
    print(f"📁 Output file: {output_file}")
    
    if failed_addresses:
        print(f"\n⚠️  Failed to geocode:")
        for addr in failed_addresses:
            print(f"   • {addr}")
        print(f"\nThis is normal and can happen due to:")
        print(f"   • Network connectivity issues")
        print(f"   • API rate limiting")
        print(f"   • Address format variations")
        print(f"   • Temporary service unavailability")
    
    return successful_geocodes, failed_geocodes

if __name__ == "__main__":
    print("🌍 US State Capitals - Geocoding Tool")
    print("="*50)
    
    # File paths
    input_file = 'data/state_capitals.json'  # Can be original or validated file
    output_file = 'data/state_capitals_with_coords.json'
    
    # Check if validated file exists, use it as input
    import os
    validated_file = 'data/state_capitals_validated.json'
    if os.path.exists(validated_file):
        input_file = validated_file
        print(f"📝 Using validated addresses as input: {validated_file}")
    else:
        print(f"📝 Using original addresses as input: {input_file}")
    
    # Run geocoding
    successful, failed = add_coordinates_to_json(input_file, output_file)
    
    # Final status
    if successful > 0:
        print(f"\n🎉 Geocoding completed with {successful} successful results!")
        if failed == 0:
            print("🏆 Perfect success rate - all addresses geocoded!")
        else:
            print(f"⚠️  {failed} addresses need attention")
    else:
        print(f"\n❌ Geocoding failed - no coordinates were obtained")
        print("Check your internet connection and try again")
