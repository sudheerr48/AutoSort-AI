# Document Classifier

A professional document classification system that automatically categorizes PDF documents into predefined categories using LLMs.

## Prerequisites

- Python 3.8 or higher
- pip3 (Python3 package installer)

To verify your Python installation:
```bash
python3 --version  # Should show Python 3.x.x
pip3 --version    # Should show pip 21.x.x or higher
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Features

- Automatic classification of PDF documents into detailed categories
- Uses Ollama with Mistral model for classification
- Supports multiple document categories and subcategories
- Efficient batch processing of documents

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd document-classifier
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

# On Windows:
python3 -m venv .venv
.venv\Scripts\activate
```

After activation, your prompt should change to show (.venv).

3. Install dependencies:
```bash
# Make sure you're in the virtual environment (should see (.venv) in prompt)
pip3 install --upgrade pip  # Upgrade pip first
pip3 install -r requirements.txt

# Verify installation
pip3 list | grep langchain  # Should show langchain and langchain-community
```

4. Install and start Ollama:
- Follow instructions at [Ollama's website](https://ollama.ai)
- Pull the Mistral model: `ollama pull mistral`

## Troubleshooting

If you encounter installation issues:

1. Verify Python3 and pip3 installation:
```bash
which python3  # Should point to Python 3.x installation
which pip3     # Should point to pip3 installation
```

2. If pip3 commands fail, try:
```bash
python3 -m pip install -r requirements.txt  # Alternative installation method
```

3. If you see package conflicts:
```bash
# Clean install in a fresh virtual environment
deactivate  # If already in a virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

4. For macOS users:
- If Python3 is not installed:
```bash
brew install python3  # Installs both Python3 and pip3
```

## Usage

1. Set your documents path:
```bash
export DOCUMENTS_PATH=/path/to/your/documents
export OUTPUT_PATH=/path/to/output/directory
```

2. Run the classifier:
```bash
python3 document_classifier.py
```

The script will:
- Load PDF documents from the input directory
- Classify each document
- Create category folders in the output directory
- Move classified documents to their respective category folders

## Output Structure

```
classified_documents/
├── Work-Related/
│   ├── Employment Contracts/
│   ├── Technical Documentation/
│   └── Payslips & Financial Records/
├── College/Academics/
│   ├── Lecture Notes/
│   └── Research Papers/
└── ...
```

## Project Structure

```
document-classifier/
├── document_classifier.py   # Main script
├── config/
│   └── categories.py       # Category configurations
├── utils/
│   └── document_processor.py # Utility functions
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

