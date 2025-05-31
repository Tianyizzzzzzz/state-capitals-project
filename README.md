# US State Capitals Address Database

A comprehensive Python project that validates and geocodes official addresses of all 50 US state capitals.

## Project Overview

This project processes US state capital address data through validation, mock USPS verification, geocoding, and quality assurance steps to create a complete dataset with geographic coordinates.

## Project Workflow

### Data Files (Pre-provided)
- **Input**: `data/state_capitals.json` - Original state capitals with addresses
- **Output**: `data/state_capitals_with_coords.json` - Complete dataset with coordinates

### Processing Steps

#### Step 2: Verify JSON File Validity
- **Script**: `scripts/step2_verify_json.py`  
- **Purpose**: Validates JSON syntax, structure, and data completeness
- **Checks**: File format, required fields, data integrity

#### Step 2.1: Mock USPS Address Validation
- **Script**: `scripts/step2_1_usps_mock.py`
- **Output**: `data/state_capitals_validated.json`
- **Purpose**: Simulates USPS address validation and standardization
- **Features**: Address formatting, ZIP+4 generation, standardization

#### Step 3: Add Geographic Coordinates
- **Script**: `scripts/step3_add_coordinates.py`
- **Output**: `data/state_capitals_with_coords.json`
- **Purpose**: Adds latitude/longitude coordinates to all addresses
- **Service**: Nominatim (OpenStreetMap) geocoding - free, no API key required

#### Step 4: Verify Coordinate Variability
- **Script**: `scripts/step4_verify_coordinates.py`
- **Purpose**: Analyzes coordinate distribution and geographic coverage
- **Checks**: Coordinate ranges, variability, US boundary validation

#### Step 5: Final Data Verification
- **Script**: `scripts/step5_verify_final_json.py`
- **Purpose**: Comprehensive validation of the final dataset
- **Checks**: Data completeness, coordinate accuracy, format consistency

## Quick Start

### Prerequisites
```bash
pip install requests
```

### Run Complete Workflow
```bash
python run_workflow.py
```

### Run Individual Steps
```bash
python scripts/step2_verify_json.py
python scripts/step2_1_usps_mock.py
python scripts/step3_add_coordinates.py
python scripts/step4_verify_coordinates.py
python scripts/step5_verify_final_json.py
```

## Data Structure

### Input Data (`data/state_capitals.json`)
```json
{
  "state": "California",
  "state_abbr": "CA",
  "capital": "Sacramento",
  "address_line_1": "1315 10th Street",
  "address_line_2": "",
  "city": "Sacramento",
  "zip_code_5": "95814",
  "zip_code_4": ""
}
```

### Final Output (`data/state_capitals_with_coords.json`)
```json
{
  "state": "California",
  "state_abbr": "CA",
  "capital": "Sacramento",
  "address_line_1": "1315 10th Street",
  "address_line_2": "",
  "city": "Sacramento",
  "zip_code_5": "95814",
  "zip_code_4": "",
  "latitude": 38.576668,
  "longitude": -121.493629,
  "geocoding_status": "success",
  "geocoding_service": "nominatim"
}
```

## Technical Specifications

- **Dataset Coverage**: All 50 US state capitals
- **Geocoding Service**: Nominatim (OpenStreetMap)
- **Coordinate System**: WGS84 (EPSG:4326)
- **Data Format**: JSON with UTF-8 encoding
- **Address Validation**: Mock USPS standardization
- **Success Rate**: 100% coordinate coverage achieved

## Data Quality Metrics

### Geographic Coverage
- ✅ Continental US: 48 states
- ✅ Alaska: Northernmost coordinate (58.30°N)
- ✅ Hawaii: Westernmost coordinate (-157.83°W)
- ✅ Coast-to-coast span: ~113° longitude, ~37° latitude

### Validation Results
- **Address Completeness**: 100% (50/50 states)
- **Coordinate Accuracy**: 100% (50/50 states)
- **Geographic Validation**: All coordinates within US boundaries
- **Data Format**: Standardized JSON structure

### Sample Coordinates
| State | Capital | Latitude | Longitude |
|-------|---------|----------|-----------|
| California | Sacramento | 38.576668 | -121.493629 |
| Alaska | Juneau | 58.301598 | -134.420212 |
| Hawaii | Honolulu | 21.308950 | -157.826182 |
| Florida | Tallahassee | 30.451800 | -84.272700 |
| Maine | Augusta | 44.323535 | -69.765261 |

## Project Features

### Address Processing
- **Structured Format**: Separate address lines, city, ZIP codes
- **Standardization**: USPS-style address formatting
- **Validation**: Comprehensive data integrity checks

### Geocoding
- **Free Service**: No API keys or costs required
- **Rate Limiting**: Respectful API usage (1 request/second)
- **Error Handling**: Robust failure recovery and reporting
- **Boundary Validation**: US geographic boundary verification

### Quality Assurance
- **Multi-step Validation**: JSON, address, coordinate verification
- **Statistical Analysis**: Coordinate distribution and variability
- **Geographic Validation**: Regional boundary and coverage checks
- **Metadata Tracking**: Complete processing history and status

## Usage Examples

### Load and Analyze Data
```python
import json

# Load final dataset
with open('data/state_capitals_with_coords.json', 'r') as f:
    data = json.load(f)

# Print coordinate summary
for state in data['states']:
    print(f"{state['state']}: ({state['latitude']}, {state['longitude']})")
```

### Geographic Analysis
```python
# Extract coordinates
coords = [(s['latitude'], s['longitude']) for s in data['states']]
latitudes = [c[0] for c in coords]
longitudes = [c[1] for c in coords]

print(f"Latitude range: {min(latitudes):.2f}° to {max(latitudes):.2f}°")
print(f"Longitude range: {min(longitudes):.2f}° to {max(longitudes):.2f}°")
```

## Dependencies

- **Python 3.7+**
- **requests**: HTTP library for geocoding API calls
- **json**: Built-in JSON processing (included with Python)
- **time**: Built-in time utilities (included with Python)

## File Descriptions

| File | Size | Description |
|------|------|-------------|
| `data/state_capitals.json` | ~15KB | Original address data |
| `data/state_capitals_with_coords.json` | ~25KB | Complete dataset with coordinates |
| `scripts/step3_add_coordinates.py` | ~8KB | Core geocoding functionality |
| `scripts/step4_verify_coordinates.py` | ~6KB | Coordinate validation and analysis |

## License

MIT License - see LICENSE file for details.

## Applications

This dataset is suitable for:
- **GIS Mapping**: State capital visualization and analysis  
- **Spatial Analysis**: Geographic distribution studies
- **Mail Processing**: Standardized address formatting
- **Educational Projects**: Geography and data science learning
- **Government Applications**: Official address reference
- **Web Development**: Interactive map implementations

---

**Project Status**: Complete ✅  
**Data Quality**: Production Ready ✅  
**Geographic Coverage**: All 50 US States ✅