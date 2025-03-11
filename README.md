
## WiSee
# Wi-Fi Human Tracking

## Overview
This project aims to track human movement using Wi-Fi signals by analyzing variations in Channel State Information (CSI) and Received Signal Strength Indicator (RSSI).

## Requirements
- Python 3.x
- Libraries: numpy, scipy, matplotlib, scikit-learn
- Hardware: Intel 5300 NIC, Raspberry Pi, or similar

## Setup
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Collect data using the provided scripts.

## Usage
Run the main script to process Wi-Fi data and detect human presence:
```bash
python scripts/process_data.py
