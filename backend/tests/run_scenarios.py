#!/usr/bin/env python3
"""
Run mock recording scenarios through the Kenkoumon system and evaluate outputs.

This script:
1. Loads each mock scenario
2. Processes the transcript through the report generation system
3. Compares output with expected results
4. Generates a comprehensive evaluation report
"""

import json
import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import difflib

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ai_service import AIServiceConfig, ReportGenerationService
from core.config import settings


class ScenarioEvaluator:
    """Evaluate mock scenarios against system output."""

    def __init__(self):
        self.scenarios_dir = Path(__file__).parent / "mock_recordings"
        self.results = []
        self.scenarios = []

    def load_scenarios(self) -> List[Dict]:
        """Load all scenario JSON files."""
        scenarios = []
        index_path = self.scenarios_dir / "index.json"

        # Load index if exists
        index_data = {}
        if index_path.exists():
            with open(index_path) as f:
                index_data = json.load(f)

        for json_file in sorted(self.scenarios_dir.glob("scenario_*.json")):
            with open(json_file) as f:
                scenario = json.load(f)
                scenarios.append(scenario)

        self.scenarios = scenarios
        print(f"Loaded {len(scenarios)} scenarios")
        return scenarios

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity ratio between two strings."""
        return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def evaluate_summary(
        self, expected: Dict[str, Any], actual: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare expected vs actual summary."""
        scores = {
            "chief_complaint_match": 0.0,
            "findings_recall": 0.0,
            "recommendations_recall": 0.0,
            "follow_up_match": 0.0,
            "overall_score": 0.0,
            "missing_findings": [],
            "missing_recommendations": [],
            "extra_findings": [],
            "extra_recommendations": [],
        }

        # Chief complaint similarity
        if "chief_complaint" in expected and "chief_complaint" in actual:
            scores["chief_complaint_match"] = self.calculate_similarity(
                expected["chief_complaint"], actual.get("chief_complaint", "")
            )

        # Findings recall
        expected_findings = set(expected.get("findings", []))
        actual_findings = set(actual.get("findings", []))

        if expected_findings:
            found = expected_findings & actual_findings
            scores["findings_recall"] = len(found) / len(expected_findings)
            scores["missing_findings"] = list(expected_findings - actual_findings)
            scores["extra_findings"] = list(actual_findings - expected_findings)

        # Recommendations recall
        expected_recs = set(expected.get("recommendations", []))
        actual_recs = set(actual.get("recommendations", []))

        if expected_recs:
            found = expected_recs & actual_recs
            scores["recommendations_recall"] = len(found) / len(expected_recs)
            scores["missing_recommendations"] = list(expected_recs - actual_recs)
            scores["extra_recommendations"] = list(actual_recs - expected_recs)

        # Follow up match
        if "follow_up" in expected and "follow_up" in actual:
            scores["follow_up_match"] = self.calculate_similarity(
                expected["follow_up"], actual.get("follow_up", "")
            )

        # Overall score (weighted average)
        weights = {
            "chief_complaint_match": 0.25,
            "findings_recall": 0.30,
            "recommendations_recall": 0.30,
            "follow_up_match": 0.15,
        }
        scores["overall_score"] = sum(
            scores[k] * weights[k] for k in weights if k in scores
        )

        return scores

    def print_scenario_report(self, scenario: Dict, scores: Dict, actual: Dict = None):
        """Print evaluation report for a single scenario."""
        print(f"\n{'='*70}")
        print(f"Scenario: {scenario.get('title', scenario.get('scenario', 'Unknown'))}")
        print(f"ID: {scenario.get('id', 'N/A')}")
        print(f"Duration: {scenario.get('duration_seconds', 0)}s")
        print(f"{'='*70}")

        if actual:
            print(f"\nExpected Chief Complaint: {scenario['expected_summary'].get('chief_complaint', 'N/A')}")
            print(f"Actual Chief Complaint: {actual.get('chief_complaint', 'N/A')}")
            print(f"Match Score: {scores['chief_complaint_match']:.2%}")

            print(f"\nExpected Findings: {scenario['expected_summary'].get('findings', [])}")
            print(f"Actual Findings: {actual.get('findings', [])}")
            print(f"Recall: {scores['findings_recall']:.2%}")
            if scores['missing_findings']:
                print(f"  Missing: {scores['missing_findings']}")
            if scores['extra_findings']:
                print(f"  Extra: {scores['extra_findings']}")

            print(f"\nExpected Recommendations: {scenario['expected_summary'].get('recommendations', [])}")
            print(f"Actual Recommendations: {actual.get('recommendations', [])}")
            print(f"Recall: {scores['recommendations_recall']:.2%}")
            if scores['missing_recommendations']:
                print(f"  Missing: {scores['missing_recommendations']}")
            if scores['extra_recommendations']:
                print(f"  Extra: {scores['extra_recommendations']}")
        else:
            print("\nNo actual output to compare (system not available)")

        print(f"\nOverall Score: {scores['overall_score']:.2%}")

    def generate_final_report(self):
        """Generate final evaluation report."""
        if not self.results:
            print("\nNo results to report.")
            return

        print(f"\n\n{'='*70}")
        print("FINAL EVALUATION REPORT")
        print(f"{'='*70}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Scenarios: {len(self.results)}")

        # Calculate statistics
        overall_scores = [r["overall_score"] for r in self.results]
        avg_score = sum(overall_scores) / len(overall_scores)

        print(f"\nAverage Overall Score: {avg_score:.2%}")

        # Category averages
        categories = [
            "chief_complaint_match",
            "findings_recall",
            "recommendations_recall",
            "follow_up_match",
        ]
        print("\nCategory Averages:")
        for cat in categories:
            values = [r.get(cat, 0) for r in self.results]
            avg = sum(values) / len(values) if values else 0
            print(f"  {cat}: {avg:.2%}")

        # Worst performing scenarios
        print("\nLowest Scoring Scenarios:")
        for result in sorted(self.results, key=lambda x: x["overall_score"])[:3]:
            print(f"  {result['scenario']}: {result['overall_score']:.2%}")

        # Best performing scenarios
        print("\nHighest Scoring Scenarios:")
        for result in sorted(self.results, key=lambda x: -x["overall_score"])[:3]:
            print(f"  {result['scenario']}: {result['overall_score']:.2%}")

        # Common issues
        all_missing_findings = []
        all_missing_recommendations = []
        for result in self.results:
            all_missing_findings.extend(result.get("missing_findings", []))
            all_missing_recommendations.extend(result.get("missing_recommendations", []))

        print("\nMost Common Missing Findings:")
        from collections import Counter
        for item, count in Counter(all_missing_findings).most_common(5):
            print(f"  - {item} ({count} scenarios)")

        print("\nMost Common Missing Recommendations:")
        for item, count in Counter(all_missing_recommendations).most_common(5):
            print(f"  - {item} ({count} scenarios)")

    def generate_recommendations(self) -> List[Dict]:
        """Generate recommendations for new scenarios based on gaps."""
        recommendations = []

        # Analyze current coverage
        complexities = [s.get("complexity", "unknown") for s in self.scenarios]
        topics = []
        for s in self.scenarios:
            topics.extend(s.get("topics", []))

        from collections import Counter
        topic_counts = Counter(topics)

        # Identify gaps
        recommended_scenarios = [
            {
                "scenario": "drug_prescription_new",
                "title": "新薬処方説明 - New Medication Prescription",
                "priority": "high",
                "reason": "Critical for patient safety - understanding side effects and usage",
                "topics": ["prescription", "side_effects", "medication_instructions"],
                "complexity": "medium",
                "edge_cases": ["new_medication", "detailed_instructions"],
            },
            {
                "scenario": "surgery_consent",
                "title": "手術同意説明 - Surgical Consent Discussion",
                "priority": "high",
                "reason": "Legal and safety critical - requires accurate documentation",
                "topics": ["surgery", "informed_consent", "risks", "recovery_time"],
                "complexity": "high",
                "edge_cases": ["legal_discussion", "risk_assessment"],
            },
            {
                "scenario": "lab_results_abnormal",
                "title": "検査結果異常 - Abnormal Lab Results",
                "priority": "high",
                "reason": "High anxiety situations require accurate summaries",
                "topics": ["lab_results", "abnormal_values", "further_testing"],
                "complexity": "medium",
                "edge_cases": ["anxiety_patient", "uncertain_diagnosis"],
            },
            {
                "scenario": "telephone_consultation",
                "title": "電話相談 - Telephone Consultation",
                "priority": "medium",
                "reason": "Common modality with unique challenges (no visual)",
                "topics": ["telephone", "triage", "home_care_advice"],
                "complexity": "low",
                "edge_cases": ["audio_only", "remote_assessment"],
            },
            {
                "scenario": "dietary_counseling",
                "title": "食事指導 - Dietary Counseling",
                "priority": "medium",
                "reason": "Lifestyle medicine is increasingly important",
                "topics": ["nutrition", "diet", "lifestyle_changes", "diabetes_diet"],
                "complexity": "medium",
                "edge_cases": ["detailed_instructions", "behavior_change"],
            },
            {
                "scenario": "vaccination_discussion",
                "title": "ワクチン相談 - Vaccination Consultation",
                "priority": "medium",
                "reason": "Important public health topic",
                "topics": ["vaccination", "side_effects", "schedule"],
                "complexity": "low",
                "edge_cases": ["patient_concerns", "vaccine_hesitancy"],
            },
            {
                "scenario": "chronic_pain_management",
                "title": "慢性疼痛管理 - Chronic Pain Management",
                "priority": "high",
                "reason": "Complex condition requiring careful documentation",
                "topics": ["chronic_pain", "pain_scale", "medication", "physical_therapy"],
                "complexity": "high",
                "edge_cases": ["subjective_symptoms", "long_term_care"],
            },
            {
                "scenario": "family_present_interpreter",
                "title": "家族同席・通訳 - Family Present with Interpreter",
                "priority": "high",
                "reason": "Multi-speaker scenario with translation layer",
                "topics": ["family", "interpreter", "communication_barrier"],
                "complexity": "critical",
                "edge_cases": ["multi_speaker", "third_party_translation", "family_dynamics"],
            },
            {
                "scenario": "allergy_consultation",
                "title": "アレルギー相談 - Allergy Consultation",
                "priority": "medium",
                "reason": "Safety critical - requires accurate allergen identification",
                "topics": ["allergy", "anaphylaxis", "testing", "epipen"],
                "complexity": "medium",
                "edge_cases": ["safety_critical", "emergency_medication"],
            },
            {
                "scenario": "pregnancy_care",
                "title": "妊婦健診 - Pregnancy Checkup",
                "priority": "medium",
                "reason": "Common specialized care scenario",
                "topics": ["pregnancy", "prenatal_care", "due_date", "symptoms"],
                "complexity": "medium",
                "edge_cases": ["obstetrics", "fetal_health"],
            },
            {
                "scenario": "dementia_care_planning",
                "title": "認知症ケア計画 - Dementia Care Planning",
                "priority": "high",
                "reason": "Complex family discussion with legal implications",
                "topics": ["dementia", "care_planning", "family_discussion", "legal"],
                "complexity": "high",
                "edge_cases": ["cognitive_decline", "family_caregiver", "future_planning"],
            },
            {
                "scenario": "discharge_planning",
                "title": "退院説明 - Hospital Discharge Planning",
                "priority": "high",
                "reason": "Critical transition point - high error risk",
                "topics": ["discharge", "medications", "follow_up", "warning_signs"],
                "complexity": "high",
                "edge_cases": ["care_transition", "multiple_medications", "red_flags"],
            },
            {
                "scenario": "cancer_diagnosis",
                "title": "がん告知 - Cancer Diagnosis Disclosure",
                "priority": "high",
                "reason": "High-stakes emotional conversation",
                "topics": ["cancer", "diagnosis", "treatment_options", "prognosis"],
                "complexity": "critical",
                "edge_cases": ["breaking_bad_news", "emotional_support", "treatment_planning"],
            },
            {
                "scenario": "medication_side_effect",
                "title": "副作用相談 - Medication Side Effect Consultation",
                "priority": "high",
                "reason": "Safety critical - requires accurate assessment",
                "topics": ["side_effects", "adverse_reaction", "medication_change"],
                "complexity": "medium",
                "edge_cases": ["adverse_event", "medication_adjustment"],
            },
            {
                "scenario": "physical_examination",
                "title": "身体診察 - Physical Examination",
                "priority": "medium",
                "reason": "Common consultation with specific procedural language",
                "topics": ["physical_exam", "symptoms", "diagnosis"],
                "complexity": "low",
                "edge_cases": ["procedural_language", "patient_instructions"],
            },
        ]

        return recommended_scenarios

    async def run_scenario(self, scenario: Dict, ai_service: ReportGenerationService) -> Dict:
        """Run a single scenario through the AI service."""
        print(f"\nProcessing: {scenario.get('title', scenario.get('scenario'))}")

        # Create transcript text
        transcript_parts = []
        for turn in scenario.get("transcript", []):
            speaker = "医師" if turn["speaker"] == "doctor" else "患者"
            transcript_parts.append(f"{speaker}: {turn['text']}")

        transcript = "\n".join(transcript_parts)

        try:
            # Generate report
            actual_summary = await ai_service.generate_summary(transcript)

            # Evaluate
            scores = self.evaluate_summary(
                scenario["expected_summary"], actual_summary
            )

            result = {
                "scenario": scenario.get("scenario", "unknown"),
                "title": scenario.get("title", "Unknown"),
                "complexity": scenario.get("complexity", "unknown"),
                "scores": scores,
                "actual": actual_summary,
                "expected": scenario["expected_summary"],
            }

            # Flatten scores for results
            result.update(scores)

            self.print_scenario_report(scenario, scores, actual_summary)
            self.results.append(result)

            return result

        except Exception as e:
            print(f"  Error: {e}")
            # Still evaluate with zero scores
            scores = {k: 0.0 for k in ["chief_complaint_match", "findings_recall",
                                        "recommendations_recall", "follow_up_match", "overall_score"]}
            self.print_scenario_report(scenario, scores, None)

            result = {
                "scenario": scenario.get("scenario", "unknown"),
                "title": scenario.get("title", "Unknown"),
                "complexity": scenario.get("complexity", "unknown"),
                "error": str(e),
                **scores,
            }
            self.results.append(result)
            return result

    async def run_all(self):
        """Run all scenarios."""
        scenarios = self.load_scenarios()

        # Try to initialize AI service
        ai_service = None
        try:
            config = AIServiceConfig()
            ai_service = ReportGenerationService(config)
            print("\nAI Service initialized successfully")
        except Exception as e:
            print(f"\nWarning: Could not initialize AI service: {e}")
            print("Running in dry-run mode (comparing expected summaries only)")

        for scenario in scenarios:
            if ai_service:
                await self.run_scenario(scenario, ai_service)
            else:
                # Dry run - just print what we expect
                self.print_scenario_report(
                    scenario,
                    {
                        "overall_score": 0.0,
                        "chief_complaint_match": 0.0,
                        "findings_recall": 0.0,
                        "recommendations_recall": 0.0,
                        "follow_up_match": 0.0,
                    },
                    None
                )
                self.results.append({
                    "scenario": scenario.get("scenario", "unknown"),
                    "title": scenario.get("title", "Unknown"),
                    "overall_score": 0.0,
                })

        self.generate_final_report()

        # Generate recommendations
        print(f"\n\n{'='*70}")
        print("RECOMMENDED NEW SCENARIOS")
        print(f"{'='*70}")

        recommendations = self.generate_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['title']} ({rec['scenario']})")
            print(f"   Priority: {rec['priority']}")
            print(f"   Complexity: {rec['complexity']}")
            print(f"   Reason: {rec['reason']}")
            print(f"   Topics: {', '.join(rec['topics'])}")
            if rec.get('edge_cases'):
                print(f"   Edge Cases: {', '.join(rec['edge_cases'])}")


async def main():
    """Main entry point."""
    evaluator = ScenarioEvaluator()
    await evaluator.run_all()


if __name__ == "__main__":
    asyncio.run(main())
