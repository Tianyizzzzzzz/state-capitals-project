#!/usr/bin/env python3
"""
Step 4: Verify that the longitude and latitude coordinates are variable
"""

import json
import math

def calculate_statistics(values):
    """Calculate basic statistics for a list of values."""
    if not values:
        return None
    
    values_sorted = sorted(values)
    n = len(values)
    
    # Basic stats
    minimum = min(values)
    maximum = max(values)
    range_val = maximum - minimum
    mean = sum(values) / n
    
    # Standard deviation
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = math.sqrt(variance)
    
    return {
        'count': n,
        'min': minimum,
        'max': maximum,
        'range': range_val,
        'mean': mean,
        'std_dev': std_dev
    }

def verify_coordinate_variability(filename):
    """Verify that coordinates show proper variability across states."""
    
    print("Step 4: Verifying longitude and latitude coordinate variability...")
    
    # Load the JSON file with coordinates
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract coordinates
    latitudes = []
    longitudes = []
    valid_coordinates = 0
    invalid_coordinates = 0
    
    print(f"Analyzing coordinates for {len(data['states'])} states...")
    
    for state_info in data['states']:
        state_name = state_info['state']
        lat = state_info.get('latitude')
        lon = state_info.get('longitude')
        
        if lat is not None and lon is not None:
            try:
                lat_float = float(lat)
                lon_float = float(lon)
                
                # Validate coordinate ranges
                if -90 <= lat_float <= 90 and -180 <= lon_float <= 180:
                    latitudes.append(lat_float)
                    longitudes.append(lon_float)
                    valid_coordinates += 1
                else:
                    print(f"⚠️  {state_name}: Coordinates out of valid range: {lat_float}, {lon_float}")
                    invalid_coordinates += 1
            except (ValueError, TypeError):
                print(f"⚠️  {state_name}: Invalid coordinate format: {lat}, {lon}")
                invalid_coordinates += 1
        else:
            print(f"⚠️  {state_name}: Missing coordinates")
            invalid_coordinates += 1
    
    print(f"\n📊 COORDINATE SUMMARY:")
    print(f"   Valid coordinates: {valid_coordinates}")
    print(f"   Invalid/missing coordinates: {invalid_coordinates}")
    print(f"   Data completeness: {(valid_coordinates / len(data['states']) * 100):.1f}%")
    
    if valid_coordinates < 2:
        print("❌ Insufficient valid coordinates for variability analysis")
        return False
    
    # Calculate statistics
    lat_stats = calculate_statistics(latitudes)
    lon_stats = calculate_statistics(longitudes)
    
    print(f"\n📈 LATITUDE ANALYSIS:")
    print(f"   Range: {lat_stats['min']:.6f}° to {lat_stats['max']:.6f}°")
    print(f"   Span: {lat_stats['range']:.6f}° ({lat_stats['range'] * 69:.0f} miles)")
    print(f"   Mean: {lat_stats['mean']:.6f}°")
    print(f"   Standard deviation: {lat_stats['std_dev']:.6f}°")
    
    print(f"\n📈 LONGITUDE ANALYSIS:")
    print(f"   Range: {lon_stats['min']:.6f}° to {lon_stats['max']:.6f}°")
    print(f"   Span: {lon_stats['range']:.6f}° ({lon_stats['range'] * 54:.0f} miles at 40°N)")
    print(f"   Mean: {lon_stats['mean']:.6f}°")
    print(f"   Standard deviation: {lon_stats['std_dev']:.6f}°")
    
    # Variability assessment
    print(f"\n🔍 VARIABILITY ASSESSMENT:")
    
    # Check latitude variability (should span from ~21° Hawaii to ~71° Alaska)
    lat_variability_good = lat_stats['range'] > 20  # At least 20 degrees
    if lat_variability_good:
        print(f"   ✅ Latitude variability: EXCELLENT ({lat_stats['range']:.1f}° span)")
    else:
        print(f"   ❌ Latitude variability: POOR ({lat_stats['range']:.1f}° span)")
    
    # Check longitude variability (should span from ~-180° Alaska to ~-67° Maine)
    lon_variability_good = lon_stats['range'] > 50  # At least 50 degrees
    if lon_variability_good:
        print(f"   ✅ Longitude variability: EXCELLENT ({lon_stats['range']:.1f}° span)")
    else:
        print(f"   ❌ Longitude variability: POOR ({lon_stats['range']:.1f}° span)")
    
    # Check standard deviation (coordinates shouldn't be too clustered)
    lat_std_good = lat_stats['std_dev'] > 3  # At least 3 degrees standard deviation
    lon_std_good = lon_stats['std_dev'] > 10  # At least 10 degrees standard deviation
    
    if lat_std_good:
        print(f"   ✅ Latitude distribution: WELL DISTRIBUTED (σ = {lat_stats['std_dev']:.2f}°)")
    else:
        print(f"   ⚠️  Latitude distribution: CLUSTERED (σ = {lat_stats['std_dev']:.2f}°)")
    
    if lon_std_good:
        print(f"   ✅ Longitude distribution: WELL DISTRIBUTED (σ = {lon_stats['std_dev']:.2f}°)")
    else:
        print(f"   ⚠️  Longitude distribution: CLUSTERED (σ = {lon_stats['std_dev']:.2f}°)")
    
    # Geographic coverage check
    print(f"\n🗺️  GEOGRAPHIC COVERAGE:")
    
    # Check if we have Alaska (high latitude, far west longitude)
    has_alaska = any(lat > 55 for lat in latitudes)
    print(f"   Alaska coverage: {'✅ YES' if has_alaska else '❌ NO'}")
    
    # Check if we have Hawaii (low latitude, far west longitude)
    has_hawaii = any(lat < 25 for lat in latitudes)
    print(f"   Hawaii coverage: {'✅ YES' if has_hawaii else '❌ NO'}")
    
    # Check if we have East Coast (longitude > -80)
    has_east_coast = any(lon > -80 for lon in longitudes)
    print(f"   East Coast coverage: {'✅ YES' if has_east_coast else '❌ NO'}")
    
    # Check if we have West Coast (longitude < -115)
    has_west_coast = any(lon < -115 for lon in longitudes)
    print(f"   West Coast coverage: {'✅ YES' if has_west_coast else '❌ NO'}")
    
    # Overall assessment
    overall_good = (lat_variability_good and lon_variability_good and 
                   lat_std_good and lon_std_good and 
                   valid_coordinates >= len(data['states']) * 0.9)  # 90% completeness
    
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if overall_good:
        print("   ✅ EXCELLENT: Coordinates show proper variability across the United States")
        print("   📍 Data is suitable for geographic analysis and mapping")
    else:
        print("   ⚠️  NEEDS IMPROVEMENT: Coordinate variability may be insufficient")
        print("   📍 Consider checking geocoding results or data quality")
    
    # Specific examples of extreme coordinates
    if latitudes and longitudes:
        northernmost_idx = latitudes.index(max(latitudes))
        southernmost_idx = latitudes.index(min(latitudes))
        westernmost_idx = longitudes.index(min(longitudes))
        easternmost_idx = longitudes.index(max(longitudes))
        
        print(f"\n📍 EXTREME COORDINATES:")
        print(f"   Northernmost: {data['states'][northernmost_idx]['state']} ({max(latitudes):.6f}°)")
        print(f"   Southernmost: {data['states'][southernmost_idx]['state']} ({min(latitudes):.6f}°)")
        print(f"   Westernmost: {data['states'][westernmost_idx]['state']} ({min(longitudes):.6f}°)")
        print(f"   Easternmost: {data['states'][easternmost_idx]['state']} ({max(longitudes):.6f}°)")
    
    print(f"\n✅ Step 4 Complete: Coordinate variability analysis finished")
    
    return overall_good

if __name__ == "__main__":
    filename = 'data/state_capitals_with_coords.json'
    success = verify_coordinate_variability(filename)
    
    if success:
        print("\n🎉 Coordinate variability verification PASSED!")
    else:
        print("\n⚠️  Coordinate variability verification completed with issues")
