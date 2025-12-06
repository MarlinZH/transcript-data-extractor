# Transcript Data Extractor

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python tool for extracting school names and CEEB codes from educational transcript documents.

## Features

- 📄 **PDF Support**: Extract data from PDF transcripts
- 🏫 **School Information**: Automatically identifies school names
- 🔢 **CEEB Codes**: Extracts College Entrance Examination Board codes
- 📊 **CSV Export**: Export results to CSV for analysis
- 🔒 **Privacy-Focused**: Does NOT extract Social Security Numbers or sensitive PII
- 📁 **Batch Processing**: Process entire directories of transcripts
- 📝 **Detailed Logging**: Track extraction progress and issues

## Privacy & Compliance

**Important:** This tool is designed to extract institutional data only and does NOT extract Social Security Numbers or other highly sensitive personally identifiable information. 

For educational institutions:
- Always follow FERPA compliance requirements
- Implement proper access controls
- Use secure storage for any extracted data
- Maintain audit logs of data access

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

**Process a single transcript:**
```bash
python transcript_extractor.py transcript.pdf
```

**Process a directory of transcripts:**
```bash
python transcript_extractor.py ./transcripts/
```

**Specify output file:**
```bash
python transcript_extractor.py ./transcripts/ -o results.csv
```

**Enable verbose logging:**
```bash
python transcript_extractor.py ./transcripts/ -v
```

### Python API

```python
from transcript_extractor import TranscriptExtractor

# Initialize extractor
extractor = TranscriptExtractor()

# Process a single file
info = extractor.extract_from_pdf("transcript.pdf")
print(f"School: {info.school_name}")
print(f"CEEB: {info.ceeb_code}")

# Process a directory
results = extractor.process_directory("./transcripts")

# Export to CSV
extractor.export_to_csv(results, "output.csv")

# Print summary
extractor.print_summary(results)
```

## Output Format

The tool exports data to CSV with the following columns:

| Column | Description |
|--------|-------------|
| `file_path` | Path to the source transcript file |
| `school_name` | Extracted school name |
| `ceeb_code` | Extracted CEEB code (6 digits) |
| `student_id` | Extracted student ID (if present) |

## Supported Formats

### CEEB Codes
- Standard format: `CEEB: 123456`
- Alternative: `ACT: 123456`
- Pattern: 6-digit numeric codes

### School Names
- High schools, universities, and colleges
- Various formatting styles supported
- Automatic whitespace cleanup

## Examples

### Sample Output

```
==================================================
EXTRACTION SUMMARY
==================================================
Total transcripts processed: 25
School names found: 23 (92.0%)
CEEB codes found: 21 (84.0%)
Student IDs found: 18 (72.0%)
==================================================
```

### Sample CSV

```csv
file_path,school_name,ceeb_code,student_id
transcript_001.pdf,Lincoln High School,123456,1001234
transcript_002.pdf,Washington University,654321,2005678
```

## Development

### Project Structure

```
transcript-data-extractor/
├── transcript_extractor.py    # Main extractor class
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── LICENSE                    # MIT License
├── SECURITY.md               # Security and privacy guidelines
└── .gitignore                # Git ignore rules
```

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

This project follows PEP 8 guidelines. Run linting with:

```bash
flake8 transcript_extractor.py
```

## Use Cases

- **Admissions Processing**: Extract school data from applicant transcripts
- **Transfer Credit Evaluation**: Identify source institutions
- **Data Migration**: Extract structured data from legacy documents
- **Reporting & Analytics**: Aggregate institutional data

## Limitations

- Extraction accuracy depends on transcript format consistency
- OCR quality affects PDF text extraction
- Custom transcript formats may require pattern adjustments
- Does not validate CEEB codes against official databases

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Marlin Z**
- GitHub: [@MarlinZH](https://github.com/MarlinZH)
- Affiliation: Johnson C. Smith University - Data Management & Analytics

## Acknowledgments

- Built with PyPDF2 for PDF processing
- Developed for educational data analytics workflows
- Part of the Harvard Strategic Data Project fellowship work

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Review existing issues for solutions

---

**Note:** This tool is intended for institutional use by authorized personnel only. Always comply with applicable privacy laws and institutional policies when handling student data.
