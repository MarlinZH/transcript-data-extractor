"""Transcript Data Extractor

Extracts school names and CEEB codes from educational transcript documents.

Author: Marlin Z
License: MIT
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import PyPDF2
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TranscriptInfo:
    """Store extracted transcript information"""
    school_name: Optional[str] = None
    ceeb_code: Optional[str] = None
    student_id: Optional[str] = None
    file_path: str = ""


class TranscriptExtractor:
    """Extract school information from transcript documents
    
    This class provides methods to extract educational institution data
    from transcript PDFs and text files, including:
    - School names
    - CEEB (College Entrance Examination Board) codes
    - Student identifiers (non-SSN)
    
    Privacy Note:
    This tool is designed to extract institutional data only.
    It does NOT extract Social Security Numbers or other sensitive PII.
    """
    
    def __init__(self):
        # CEEB codes are typically 6-digit numbers
        self.ceeb_pattern = re.compile(
            r'\b(?:CEEB|ACT)[\s:]*(\d{6})\b', 
            re.IGNORECASE
        )
        
        # Common school name patterns
        self.school_patterns = [
            # Explicit labeling (e.g., "High School: Lincoln High School")
            re.compile(
                r'(?:HIGH SCHOOL|UNIVERSITY|COLLEGE)[\s:]*([A-Z][A-Za-z\s&.]+(?:HIGH SCHOOL|UNIVERSITY|COLLEGE))',
                re.IGNORECASE
            ),
            # Direct mention (e.g., "Lincoln High School")
            re.compile(
                r'([A-Z][A-Za-z\s&.]+(?:High School|University|College))',
                re.IGNORECASE
            ),
        ]
        
        # Student ID pattern (non-SSN)
        self.student_id_pattern = re.compile(
            r'(?:Student\s+ID|Student\s+Number)[\s:]*(\d{6,10})',
            re.IGNORECASE
        )
        
    def extract_from_pdf(self, pdf_path: str) -> TranscriptInfo:
        """Extract information from a PDF transcript
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            TranscriptInfo object containing extracted data
        """
        info = TranscriptInfo(file_path=pdf_path)
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Extract text from all pages
                full_text = ""
                for page in reader.pages:
                    full_text += page.extract_text()
                
                # Extract data
                info.ceeb_code = self._extract_ceeb(full_text)
                info.school_name = self._extract_school_name(full_text)
                info.student_id = self._extract_student_id(full_text)
                
                logger.info(f"Successfully processed {pdf_path}")
                
        except FileNotFoundError:
            logger.error(f"File not found: {pdf_path}")
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
        
        return info
    
    def extract_from_text(self, text: str, file_path: str = "") -> TranscriptInfo:
        """Extract information from plain text
        
        Args:
            text: Text content to process
            file_path: Optional path identifier
            
        Returns:
            TranscriptInfo object containing extracted data
        """
        info = TranscriptInfo(file_path=file_path)
        
        info.ceeb_code = self._extract_ceeb(text)
        info.school_name = self._extract_school_name(text)
        info.student_id = self._extract_student_id(text)
        
        return info
    
    def _extract_ceeb(self, text: str) -> Optional[str]:
        """Extract CEEB code from text"""
        match = self.ceeb_pattern.search(text)
        if match:
            return match.group(1)
        return None
    
    def _extract_school_name(self, text: str) -> Optional[str]:
        """Extract school name from text"""
        # Try each pattern
        for pattern in self.school_patterns:
            match = pattern.search(text)
            if match:
                school_name = match.group(1).strip()
                # Clean up the name
                school_name = ' '.join(school_name.split())
                return school_name
        return None
    
    def _extract_student_id(self, text: str) -> Optional[str]:
        """Extract student ID from text (non-SSN identifiers only)"""
        match = self.student_id_pattern.search(text)
        if match:
            return match.group(1)
        return None
    
    def process_directory(self, directory_path: str, pattern: str = "*.pdf") -> List[TranscriptInfo]:
        """Process all matching files in a directory
        
        Args:
            directory_path: Path to directory containing transcripts
            pattern: Glob pattern for file matching (default: *.pdf)
            
        Returns:
            List of TranscriptInfo objects
        """
        results = []
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory_path}")
            return results
        
        files = list(directory.glob(pattern))
        logger.info(f"Found {len(files)} files to process")
        
        for file_path in files:
            logger.info(f"Processing: {file_path.name}")
            info = self.extract_from_pdf(str(file_path))
            results.append(info)
        
        return results
    
    def export_to_csv(self, results: List[TranscriptInfo], output_path: str):
        """Export results to CSV
        
        Args:
            results: List of TranscriptInfo objects
            output_path: Path for output CSV file
        """
        import csv
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['file_path', 'school_name', 'ceeb_code', 'student_id']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for info in results:
                    writer.writerow({
                        'file_path': info.file_path,
                        'school_name': info.school_name or '',
                        'ceeb_code': info.ceeb_code or '',
                        'student_id': info.student_id or ''
                    })
            
            logger.info(f"Results exported to {output_path}")
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
    
    def print_summary(self, results: List[TranscriptInfo]):
        """Print summary statistics of extraction results"""
        total = len(results)
        with_school = sum(1 for r in results if r.school_name)
        with_ceeb = sum(1 for r in results if r.ceeb_code)
        with_student_id = sum(1 for r in results if r.student_id)
        
        print("\n" + "="*50)
        print("EXTRACTION SUMMARY")
        print("="*50)
        print(f"Total transcripts processed: {total}")
        print(f"School names found: {with_school} ({with_school/total*100:.1f}%)")
        print(f"CEEB codes found: {with_ceeb} ({with_ceeb/total*100:.1f}%)")
        print(f"Student IDs found: {with_student_id} ({with_student_id/total*100:.1f}%)")
        print("="*50 + "\n")


def main():
    """Main execution function with example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Extract school information from transcript PDFs'
    )
    parser.add_argument(
        'input',
        help='Input PDF file or directory containing PDFs'
    )
    parser.add_argument(
        '-o', '--output',
        default='extracted_data.csv',
        help='Output CSV file path (default: extracted_data.csv)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    extractor = TranscriptExtractor()
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Process single file
        logger.info(f"Processing single file: {input_path}")
        info = extractor.extract_from_pdf(str(input_path))
        results = [info]
    elif input_path.is_dir():
        # Process directory
        logger.info(f"Processing directory: {input_path}")
        results = extractor.process_directory(str(input_path))
    else:
        logger.error(f"Invalid input path: {input_path}")
        return
    
    # Export results
    extractor.export_to_csv(results, args.output)
    
    # Print summary
    extractor.print_summary(results)


if __name__ == "__main__":
    main()
