# Phase 0: OCR Parser Research

## Decisions

### 1. OCR Engine
- **Decision**: Tesseract OCR (`pytesseract`)
- **Rationale**: The project has a strict mandate to remain entirely free-tier and operate without external cloud reliance. Tesseract runs locally, supports Python wrapping, and provides adequate bounding-box text extraction when paired with image preprocessing.
- **Alternatives considered**: Google Cloud Vision API, Azure AI Document Intelligence. (Rejected: violation of free-tier/local dependencies constraint).

### 2. Image Preprocessing
- **Decision**: OpenCV (`opencv-python`)
- **Rationale**: The Warscribe app features a dark UI with light text, which frustrates standard OCR engines. OpenCV allows for grayscale conversion, adaptive thresholding, and median blurring to isolate the text channels effectively.
- **Alternatives considered**: Pillow exclusively. (Rejected: Pillow lacks the robust adaptive thresholding algorithms necessary to separate the text from the complex UI background reliably).

### 3. Data Modeling
- **Decision**: Pydantic V2 inheriting from `VindictaModel`
- **Rationale**: The platform constitution mandates that all shared core entities inherit from the axiomatic `VindictaModel`.
- **Alternatives considered**: Standard Python dataclasses. (Rejected: Unconstitutional and lacks the serialization guarantees required for downstream ingestion).
