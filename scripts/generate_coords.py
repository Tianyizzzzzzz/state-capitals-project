
import json
import pgeocode

# Load the original state capitals address file
with open('data/state_capitals_addresses.json', 'r') as f:
    capitals = json.load(f)

# Setup pgeocode for U.S. ZIP codes
geo = pgeocode.Nominatim('us')

# Enrich each record with latitude and longitude
for item in capitals:
    zip_code = item['address'][-5:]  # Extract last 5 digits as ZIP
    result = geo.query_postal_code(zip_code)
    item['latitude'] = result.latitude
    item['longitude'] = result.longitude

# Save to new enriched JSON file
with open('data/state_capitals_with_coords.json', 'w') as f:
    json.dump(capitals, f, indent=4)

print("Finished adding coordinates.")
