# Quickstart: WARScribe OCR Parser

This package provides a CLI and Python API to parse Warscribe app screenshots into structured JSON data.

## Prerequisites

Tesseract OCR must be installed on your system.

**Windows**:
```powershell
winget install UB-Mannheim.TesseractOCR
```

**Linux/Devcontainer**:
```bash
sudo apt-get update && sudo apt-get install -y tesseract-ocr
```

## Installation

```bash
uv pip install -e .
```

## CLI Usage

Parse an image and print JSON to stdout:
```bash
parse-warscribe path/to/screenshot.jpg --pretty
```

Save to a file:
```bash
parse-warscribe path/to/screenshot.jpg -o result.json
```

Debug raw OCR lines:
```bash
parse-warscribe path/to/screenshot.jpg --dump-lines
```

## API Usage

```python
from warscribe_parser.ocr.preprocessor import preprocess_for_ocr
from warscribe_parser.ocr.ocr_engine import extract_text_lines
from warscribe_parser.ocr.parser import parse_lines

# 1. Clean image for OCR
img = preprocess_for_ocr("screenshot.jpg")

# 2. Extract lines of text
lines = extract_text_lines(img)

# 3. Parse into GameResult Pydantic model
result = parse_lines(lines)

# 4. Serialize
print(result.model_dump_json(indent=2))
```
