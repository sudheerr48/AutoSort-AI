# Document Classifier

A professional document classification system that automatically categorizes PDF documents into predefined categories using LLMs.

## Features

- Automatic classification of PDF documents into detailed categories
- Uses Ollama with Mistral model for classification
- Supports multiple document categories and subcategories
- Efficient batch processing of documents

## Installation

1. Clone the repository:
bash
git clone <repository-url>
cd document-classifier

2. Install dependencies:
bash
pip install -r requirements.txt

3. Install and start Ollama:
- Follow instructions at [Ollama's website](https://ollama.ai)
- Pull the Mistral model: `ollama pull mistral`

## Usage

1. Set your documents path:

```bash
export DOCUMENTS_PATH=/path/to/your/documents
```

2. Run the classifier:

```bash
python document_classifier.py
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

MIT License

