"""
PDF health data extractor for MyNumber Portal documents.

Extracts health checkup data, medications, and vaccinations
from Japanese health document PDFs.
"""

import re
import json
from typing import Optional, Dict, Any
from datetime import datetime
import PyPDF2


class PDFHealthDataExtractor:
    """Extract health data from Japanese health documents."""

    def extract_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Extract health data from a PDF file.

        Returns a dictionary with extracted health metrics.
        """
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"

            return self.parse_health_data(text)
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None

    def parse_health_data(self, text: str) -> Dict[str, Any]:
        """
        Parse health checkup data from Japanese PDF text.

        MyNumber Portal PDFs contain structured health data.
        """
        data = {}

        # Height (身長)
        height_match = re.search(r'身長\s*[:：]\s*(\d+\.?\d*)\s*(cm|センチ)?', text)
        if height_match:
            data["height"] = float(height_match.group(1))

        # Weight (体重)
        weight_match = re.search(r'体重\s*[:：]\s*(\d+\.?\d*)\s*(kg|キロ)?', text)
        if weight_match:
            data["weight"] = float(weight_match.group(1))

        # BMI
        bmi_match = re.search(r'BMI\s*[:：]\s*(\d+\.?\d*)', text)
        if bmi_match:
            data["bmi"] = float(bmi_match.group(1))

        # Blood pressure (血圧) - format like "120/80" or "120 80"
        bp_match = re.search(r'血圧\s*[:：]\s*(\d+)\s*[/／\s](\d+)', text)
        if bp_match:
            data["blood_pressure_systolic"] = int(bp_match.group(1))
            data["blood_pressure_diastolic"] = int(bp_match.group(2))

        # Blood sugar (血糖値, 空腹時血糖)
        sugar_match = re.search(r'(血糖値|空腹時血糖)\s*[:：]\s*(\d+\.?\d*)\s*(mg/dL)?', text)
        if sugar_match:
            data["blood_sugar"] = float(sugar_match.group(2))

        # HbA1c
        hba1c_match = re.search(r'HbA1c|ヘモグロビンA1c\s*[:：]\s*(\d+\.?\d*)\s*%?', text)
        if hba1c_match:
            data["hba1c"] = float(hba1c_match.group(1))

        # LDL Cholesterol (LDLコレステロール, 悪玉コレステロール)
        ldl_match = re.search(r'(LDLコレステロール|悪玉コレステロール)\s*[:：]\s*(\d+\.?\d*)\s*(mg/dL)?', text)
        if ldl_match:
            data["ldl_cholesterol"] = float(ldl_match.group(2))

        # HDL Cholesterol (HDLコレステロール, 善玉コレステロール)
        hdl_match = re.search(r'(HDLコレステロール|善玉コレステロール)\s*[:：]\s*(\d+\.?\d*)\s*(mg/dL)?', text)
        if hdl_match:
            data["hdl_cholesterol"] = float(hdl_match.group(2))

        # Triglycerides (中性脂肪)
        trig_match = re.search(r'中性脂肪|トリグリセリド\s*[:：]\s*(\d+\.?\d*)\s*(mg/dL)?', text)
        if trig_match:
            data["triglycerides"] = float(trig_match.group(1))

        # AST (GOT)
        ast_match = re.search(r'(AST|GOT)\s*[:：]\s*(\d+\.?\d*)\s*(U/L|IU)?', text)
        if ast_match:
            data["ast"] = float(ast_match.group(2))

        # ALT (GPT)
        alt_match = re.search(r'(ALT|GPT)\s*[:：]\s*(\d+\.?\d*)\s*(U/L|IU)?', text)
        if alt_match:
            data["alt"] = float(alt_match.group(2))

        # Gamma-GTP
        gtp_match = re.search(r'γ-GTP|ガンマGTP\s*[:：]\s*(\d+\.?\d*)\s*(U/L|IU)?', text)
        if gtp_match:
            data["gamma_gtp"] = float(gtp_match.group(1))

        # Checkup date (健診日)
        date_match = re.search(r'健診日|受診日|検査日\s*[:：]\s*(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})日?', text)
        if date_match:
            try:
                year, month, day = date_match.groups()
                data["checkup_date"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            except ValueError:
                pass

        return data
