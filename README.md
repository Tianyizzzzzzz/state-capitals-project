
# state-capitals-project

## 📁 Project Structure

```
.
├── data/
│   ├── state_capitals_addresses.json         # Original address file
│   └── state_capitals_with_coords.json       # Enriched with coordinates
├── scripts/
│   └── generate_coords.py                    # Python script to append lat/lon
├── reports/
│   └── [weekly reports]
├── requirements.txt                          # Dependencies
└── README.md                                 # Project overview
```

## ✅ How to Run

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the script:
```
python scripts/generate_coords.py
```

This will create a new file in `data/state_capitals_with_coords.json` with added `latitude` and `longitude` for each capital.

## 🔗 Author
Tianyi Zhang – [GitHub](https://github.com/Tianyizzzzzzz)
