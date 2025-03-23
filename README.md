# Human Activity Detection using Wi-Fi RSSI

## Introduction

### Objective
The goal of this project is to recognize human activities — specifically detecting an empty room, moving, or stationary individuals — using Wi-Fi Received Signal Strength Indication (RSSI) without the need for wearable devices.

### Motivation
Privacy concerns surrounding camera-based monitoring systems drive the need for low-cost, non-invasive, and privacy-friendly solutions. This project leverages Wi-Fi RSSI data and machine learning (ML) techniques to address these needs.

## Technology
- **Wi-Fi RSSI (Received Signal Strength Indication)**
- **Machine Learning (Random Forest, Convolutional Neural Network)**

## Hardware and Software Requirements

### Hardware
- Four ESP32 S2-mini microcontrollers
  - 1x acts as an Access Point (AP) emitter
  - 3x act as receivers (R1, R2, R3)

### Software
- Python (for data processing and model training)
- TensorFlow/PyTorch (for CNN implementation)
- Scikit-learn (for Random Forest model)

## Methodology

### 1. System Setup
- **Environment**: Small indoor space
- **Hardware configuration**: One ESP32 as an AP emitter, three ESP32s as receivers

### 2. Data Collection
- **RSSI Measurement**: Gather RSSI values from multiple wireless links between the AP and receivers
- **Synchronization**: Use Wi-Fi broadcast to trigger simultaneous RSSI collection at the receivers via POST requests
- **Observation Window**: Define a collection duration (e.g., 10-20 seconds)
- **Data Classes**:
  - "0" - Empty Room
  - "1" - Moving
  - "2" - Stationary
- **Storage**: Data saved to an SD card on the ESP32 microcontroller

### 3. Data Pre-Processing
- **Normalization**: Standardize RSSI values to zero mean and unit variance
- **Labeling**: Assign numeric labels to data (0 for empty, 1 for moving, 2 for stationary)

### 4. Machine Learning Models
- **Models**:
  - Random Forest
  - Convolutional Neural Network (CNN)
- **Training**: Split data into 80% training and 20% testing
- **Prediction**: Classify room state as "empty," "moving," or "stationary"

## Experiments and Results

### Random Forest Model
- **Precision**: 0.98 (Empty), 0.96 (Stationary), 0.98 (Moving)
- **Recall**: 0.98 (Empty), 0.98 (Stationary), 0.96 (Moving)
- **F1-Score**: High consistency across classes
- **Support**: 126 (Empty), 147 (Stationary), 164 (Moving)
- **Overall Accuracy**: 97%
- **Macro and Weighted Averages**: Precision, recall, F1-score ~0.97-0.98

### Convolutional Neural Network (CNN)
- **Precision**: 0.99 (Empty), 0.97 (Stationary), 0.99 (Moving)
- **Recall**: 0.99 (Empty), 0.98 (Stationary), 0.98 (Moving)
- **F1-Score**: Consistently high
- **Support**: 126 (Empty), 147 (Stationary), 164 (Moving)
- **Overall Accuracy**: 98%
- **Macro and Weighted Averages**: Precision, recall, F1-score ~0.98

### Comparison
- CNN outperformed Random Forest slightly in all metrics
- Both models proved effective, with CNN excelling in precision and recall for "Empty" and "Moving" classes

## Challenges and Lessons Learned
- **Position Prediction**: We attempted a room grid approach (40cm x 40cm) to predict a person’s exact position, but accuracy was too low due to RSSI's sensitivity to noise, interference, and environmental factors like obstacles and multipath propagation.
- **Key Limitation**: RSSI alone proved insufficient for reliable localization.

### Future Improvements
- Incorporate additional data sources (e.g., time-of-flight, angle of arrival, inertial sensors)
- Integrate multiple sensor modalities for improved accuracy

## Conclusion
This project successfully implemented a device-free human activity detection system using Wi-Fi RSSI and machine learning. The system effectively detects room states — empty, moving, and stationary — with high accuracy. Future work involves exploring additional data sources to enhance room positioning accuracy and robustness.