import openpyxl
import io
import csv
from datetime import datetime
from django.conf import settings
from cryptography.fernet import InvalidToken

def get_cohort(program_term, academic_term, program):
    """
    Given a student's academic term and program term, return their cohort academic term.
    May terms (i.e., terms ending in '20') are skipped in program term progression.

    :param program_term: int from 1 to 8 indicating current term in the program.
    :param academic_term: int in form YYYYTT (e.g., 202530 = 2025 September).
    :param program: str in form AAAA indicating program.
    :return: int cohort academic term (e.g., 202430).
    """
    program_term = int(program_term)
    academic_term = int(academic_term)

    if program_term < 1 or program_term > 8:
        raise ValueError("Program term must be between 1 and 8.")

    year = academic_term // 100
    term = academic_term % 100

    while program_term > 1:
        # Move back to previous term
        if term == 10:
            term = 30
            year -= 1
        elif term == 30:
            term = 20
        elif term == 20:
            term = 10
            year -= 1

        # Only decrement program term if current term is not May (20)
        if term != 20:
            program_term -= 1

    return f"{program} {str(year * 100 + term)}"

def get_achievement_level(gai_score, question_max):
    """
    Returns the achievement level as a float formatted to 2 decimal places.
    """
    if question_max == 0:
        raise ValueError("Maximum question score cannot be zero.")
    return round(gai_score / question_max, 2)

def read_csv(uploaded_file):
    """
    Process a CSV or XLSX file and extract student data.
    Returns a list of (student_id, gai_score) tuples.
    """
    if not uploaded_file or not hasattr(uploaded_file, 'name'):
        return [], "Invalid file or no file uploaded"
        
    file_name = uploaded_file.name.lower()
    
    try:
        # Convert uploaded file to rows: list of lists
        if file_name.endswith('.csv'):
            file_content = uploaded_file.read().decode('utf-8')
            csvfile = io.StringIO(file_content)
            rows = list(csv.reader(csvfile))

        elif file_name.endswith('.xlsx'):
            wb = openpyxl.load_workbook(uploaded_file, data_only=True)
            sheet = wb.active
            rows = []
            for row in sheet.iter_rows(values_only=True):
                rows.append(list(row))
        else:
            return [], "Unsupported file type. Please upload a .csv or .xlsx file."

        # For debugging, print the first few rows
        print(f"Total rows: {len(rows)}")
        for i in range(min(5, len(rows))):
            print(f"Row {i}: {rows[i]}")

        # Extract data starting from row 4 (index 3)
        extracted_data = []
        row_count = 0
        valid_count = 0

        for row in rows[3:]:
            row_count += 1
            try:
                # Handle possible empty rows
                if not row or len(row) < 3:
                    continue
                    
                student_id = str(row[1]).strip() if row[1] is not None else None
                gai_score_raw = str(row[2]).strip() if row[2] is not None else None

                # Print for debugging
                print(f"Processing: ID={student_id}, Score={gai_score_raw}")

                if student_id and len(student_id) == 9:
                    try:
                        print("ADDING TO EXTRACTED DATA")
                        gai_score = float(gai_score_raw)
                        extracted_data.append((student_id, gai_score))
                        valid_count += 1
                    except (ValueError, TypeError):
                        print(f"Invalid score format: {gai_score_raw}")
                        continue 
                else:
                    print(f"Invalid ID format: {student_id} (length: {len(student_id) if student_id else 0})")
            except IndexError:
                print(f"Index error for row: {row}")
                continue  # Skip incomplete rows

        print(f"Processed {row_count} rows, found {valid_count} valid entries")
        
        if not extracted_data:
            return [], "No valid student data found. Check that your file has student IDs (9 digits) in column B starting from row 4, and numeric scores in column C."
            
        return extracted_data, None  # Return data and no error
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return [], f"Error processing file: {str(e)}"  # Return empty list and error message

def make_excel_safe(value):
    if isinstance(value, datetime):
        # Format datetime as string, e.g. "2025-05-19 01:02:03"
        return value.astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return value

def encrypt(value) -> str:
    """
    Encrypt a string value using FERNET.encrypt
    """
    if not value:
        return ""
    return settings.FERNET.encrypt(str(value).encode()).decode()

def decrypt(value, data_type=str) -> str:
    if not value:
        return ""
    try:
        decrypted = settings.FERNET.decrypt(value.encode()).decode()
        return data_type(decrypted)
    except (InvalidToken, ValueError):
        return "DECRYPTION FAILED"