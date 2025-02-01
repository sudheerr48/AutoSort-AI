# Document Classifier

A professional document classification system that automatically categorizes PDF documents into predefined categories using LLMs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

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
export OUTPUT_PATH=/path/to/output/directory
```

2. Run the classifier:

```bash
python document_classifier.py
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

MIT License

