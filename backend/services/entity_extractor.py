"""
Entity extraction from medical transcripts.

Extracts medications, conditions, instructions, and providers
from AI-generated reports.
"""

import re
import json
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from models import Medication, Condition, Instruction, Provider


# =============================================================================
# Entity Extraction Patterns
# =============================================================================

class EntityExtractor:
    """
    Extract medical entities from AI-generated reports.

    The AI is prompted to include structured entity information
    in the report, which we then parse and store.
    """

    # Patterns for extracting entities from AI-generated text
    MEDICATION_PATTERN = re.compile(
        r'(?:薬|薬剤|Medication)[：:]\s*([^\n]+)',
        re.MULTILINE
    )
    CONDITION_PATTERN = re.compile(
        r'(?:病名|疾患|Condition|Diagnosis)[：:]\s*([^\n]+)',
        re.MULTILINE
    )
    INSTRUCTION_PATTERN = re.compile(
        r'(?:指示|指導|Instruction)[：:]\s*([^\n]+)',
        re.MULTILINE
    )
    PROVIDER_PATTERN = re.compile(
        r'(?:医師|Doctor|Provider)[：:]\s*([^\n]+)',
        re.MULTILINE
    )

    @classmethod
    def extract_from_report(
        cls,
        session_id: str,
        patient_id: str,
        report_text: str,
        db: Session
    ) -> Dict[str, List]:
        """
        Extract entities from AI-generated report and store in database.

        Returns a dictionary with extracted entities.
        """
        result = {
            "medications": [],
            "conditions": [],
            "instructions": [],
            "providers": [],
        }

        # Try JSON extraction first (AI should include structured data)
        json_entities = cls._extract_json_entities(report_text)
        if json_entities:
            result = cls._store_json_entities(
                json_entities, session_id, patient_id, db
            )
            return result

        # Fallback to pattern-based extraction
        result["medications"] = cls._extract_medications(
            report_text, session_id, patient_id, db
        )
        result["conditions"] = cls._extract_conditions(
            report_text, session_id, patient_id, db
        )
        result["instructions"] = cls._extract_instructions(
            report_text, session_id, patient_id, db
        )
        result["providers"] = cls._extract_providers(
            report_text, session_id, patient_id, db
        )

        return result

    @staticmethod
    def _extract_json_entities(report_text: str) -> Optional[Dict]:
        """
        Try to extract JSON entities from report.

        AI is prompted to include structured data like:
        ```json
        {"medications": [...], "conditions": [...]}
        ```
        """
        # Look for JSON blocks
        json_pattern = re.compile(r'```json\s*([\s\S]*?)\s*```')
        matches = json_pattern.findall(report_text)

        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue

        return None

    @staticmethod
    def _store_json_entities(
        entities: Dict,
        session_id: str,
        patient_id: str,
        db: Session
    ) -> Dict[str, List]:
        """Store entities extracted from JSON."""
        import uuid

        result = {
            "medications": [],
            "conditions": [],
            "instructions": [],
            "providers": [],
        }

        for med_data in entities.get("medications", []):
            medication = Medication(
                id=str(uuid.uuid4()),
                patient_id=patient_id,
                source_session_id=session_id,
                name_ja=med_data.get("name_ja", ""),
                name_en=med_data.get("name_en"),
                dosage=med_data.get("dosage"),
                status=med_data.get("status", "discussed"),
                confidence=med_data.get("confidence", "medium"),
            )
            db.add(medication)
            result["medications"].append(medication)

        for cond_data in entities.get("conditions", []):
            condition = Condition(
                id=str(uuid.uuid4()),
                patient_id=patient_id,
                source_session_id=session_id,
                name_ja=cond_data.get("name_ja", ""),
                name_en=cond_data.get("name_en"),
                icd_code=cond_data.get("icd_code"),
                status=cond_data.get("status", "discussed"),
                confidence=cond_data.get("confidence", "medium"),
            )
            db.add(condition)
            result["conditions"].append(condition)

        for instr_data in entities.get("instructions", []):
            instruction = Instruction(
                id=str(uuid.uuid4()),
                patient_id=patient_id,
                source_session_id=session_id,
                content_ja=instr_data.get("content_ja", ""),
                category=instr_data.get("category", "lifestyle"),
                confidence=instr_data.get("confidence", "medium"),
            )
            db.add(instruction)
            result["instructions"].append(instruction)

        for prov_data in entities.get("providers", []):
            provider = Provider(
                id=str(uuid.uuid4()),
                patient_id=patient_id,
                source_session_id=session_id,
                name_ja=prov_data.get("name_ja", ""),
                name_en=prov_data.get("name_en"),
                specialty=prov_data.get("specialty"),
                clinic_name=prov_data.get("clinic_name"),
            )
            db.add(provider)
            result["providers"].append(provider)

        db.commit()
        return result

    @staticmethod
    def _extract_medications(
        report_text: str,
        session_id: str,
        patient_id: str,
        db: Session
    ) -> List[Medication]:
        """Extract medications from report text."""
        medications = []
        import uuid

        # Look for medication section
        med_match = re.search(
            r'(?:薬剤処方|Medications?)[：:].*?(?=\n\n|\n[０-９０-９\.]|$)',
            report_text,
            re.MULTILINE | re.DOTALL
        )

        if med_match:
            med_text = med_match.group(0)
            # Split by common delimiters
            med_names = re.split(r'[、\n•\-\*]|（', med_text)

            for name in med_names:
                name = name.strip()
                if name and len(name) > 1:
                    medication = Medication(
                        id=str(uuid.uuid4()),
                        patient_id=patient_id,
                        source_session_id=session_id,
                        name_ja=name,
                        status="discussed",
                        confidence="medium",
                    )
                    db.add(medication)
                    medications.append(medication)

        db.commit()
        return medications

    @staticmethod
    def _extract_conditions(
        report_text: str,
        session_id: str,
        patient_id: str,
        db: Session
    ) -> List[Condition]:
        """Extract conditions from report text."""
        conditions = []
        import uuid

        cond_match = re.search(
            r'(?:病名|疾患|Conditions?|Diagnosis)[：:].*?(?=\n\n|\n[０-９０-９\.]|$)',
            report_text,
            re.MULTILINE | re.DOTALL
        )

        if cond_match:
            cond_text = cond_match.group(0)
            cond_names = re.split(r'[、\n•\-\*]|（', cond_text)

            for name in cond_names:
                name = name.strip()
                if name and len(name) > 1:
                    condition = Condition(
                        id=str(uuid.uuid4()),
                        patient_id=patient_id,
                        source_session_id=session_id,
                        name_ja=name,
                        status="discussed",
                        confidence="medium",
                    )
                    db.add(condition)
                    conditions.append(condition)

        db.commit()
        return conditions

    @staticmethod
    def _extract_instructions(
        report_text: str,
        session_id: str,
        patient_id: str,
        db: Session
    ) -> List[Instruction]:
        """Extract instructions from report text."""
        instructions = []
        import uuid

        instr_match = re.search(
            r'(?:指示|指導| Instructions?)[：:].*?(?=\n\n|\n[０-９０-９\.]|$)',
            report_text,
            re.MULTILINE | re.DOTALL
        )

        if instr_match:
            instr_text = instr_match.group(0)
            instr_items = re.split(r'[、\n•\-\*]|（', instr_text)

            for content in instr_items:
                content = content.strip()
                if content and len(content) > 2:
                    instruction = Instruction(
                        id=str(uuid.uuid4()),
                        patient_id=patient_id,
                        source_session_id=session_id,
                        content_ja=content,
                        category="lifestyle",
                        confidence="medium",
                    )
                    db.add(instruction)
                    instructions.append(instruction)

        db.commit()
        return instructions

    @staticmethod
    def _extract_providers(
        report_text: str,
        session_id: str,
        patient_id: str,
        db: Session
    ) -> List[Provider]:
        """Extract providers from report text."""
        providers = []
        import uuid

        prov_match = re.search(
            r'(?:医師|Doctor|Provider)[：:]\s*([^\n]+)',
            report_text
        )

        if prov_match:
            name = prov_match.group(1).strip()
            if name:
                provider = Provider(
                    id=str(uuid.uuid4()),
                    patient_id=patient_id,
                    source_session_id=session_id,
                    name_ja=name,
                )
                db.add(provider)
                providers.append(provider)

        db.commit()
        return providers
