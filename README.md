# Jarvis-NLP

An intelligent AI-based voice/text assistant built using Natural Language Processing (NLP) techniques.

## 🧠 Project Description

Jarvis-NLP is a simple virtual assistant that can understand user queries through text or voice input and respond accordingly. It uses intent classification via a deep learning model and supports easy customization through an `intents.json` file.

## 🔍 Features

- 🎤 Voice and text-based interaction
- 🤖 Intent recognition using NLP and deep learning (Keras)
- 🗂️ Easily customizable intents (`intents.json`)
- 🌐 Simple HTML + JS frontend
- 🧠 Pre-trained model (`chat_model.h5`) and label encoder included

## 📁 Project Structure

Jarvis-NLP/
├── chat_model.h5 # Trained model for intent classification
├── label_encoder.pkl # Label encoder for intent labels
├── intents.json # Intent definitions
├── command.py # Python script to handle chat logic
├── controller.js # Frontend interaction logic
├── index.html # Web interface
├── README.md # Project documentation
├── LICENSE # MIT License
├── pycache/ # Cached Python bytecode
└── Note_2025-04-24_19-51-04.txt # Notes or logs (optional)


## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/vg-gupta/Jarvis-NLP.git
cd Jarvis-NLP
```
2. Install dependencies
```bash
pip install tensorflow numpy scikit-learn
```


## 🚀 Usage
1. Start the assistant

```bash
python command.py
```
2. Access the interface
Open index.html in your browser to interact with Jarvis using text or voice.

## 🛠️ Customization
To add or modify intents:
-Open intents.json
-Add new patterns and responses
-Retrain the model (you can modify the training logic in command.py)

## 🧪 Model Files
-chat_model.h5 — Trained neural network for intent classification

-label_encoder.pkl — Encodes class labels
If you want to retrain:
-Update intents.json
-Include retraining script (not provided in this version)

## 🧾 License
This project is licensed under the MIT License. See the LICENSE file for details.

