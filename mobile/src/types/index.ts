/**
 * Types for Kenkoumon
 */

export interface Session {
  id: string;
  patient_id: string;
  date: string;
  transcript_ja: string | null;
  report_ja: string | null;
  patient_notes: string | null;
  status: SessionStatus;
  created_at: string;
  updated_at: string;
}

export enum SessionStatus {
  UPLOADING = 'uploading',
  UPLOADED = 'uploaded',
  TRANSCRIBING = 'transcribing',
  TRANSCRIBED = 'transcribed',
  GENERATING = 'generating',
  COMPLETE = 'complete',
  FAILED = 'failed',
  TRANSCRIPTION_FAILED = 'transcription_failed',
  GENERATION_FAILED = 'generation_failed',
}

export interface Report {
  id: string;
  date: string;
  status: SessionStatus;
  transcript_ja: string | null;
  report_ja: string | null;
  patient_notes: string | null;
  entities: ReportEntities;
}

export interface ReportEntities {
  medications: Medication[];
  conditions: Condition[];
  instructions: Instruction[];
  providers: Provider[];
}

export interface Medication {
  id: string;
  name_ja: string;
  name_en: string | null;
  dosage: string | null;
  status: string;
  confidence: string | null;
  patient_confirmed: boolean;
}

export interface Condition {
  id: string;
  name_ja: string;
  name_en: string | null;
  icd_code: string | null;
  status: string;
  confidence: string | null;
  patient_confirmed: boolean;
}

export interface Instruction {
  id: string;
  content_ja: string;
  category: string;
  due_date: string | null;
  confidence: string | null;
  patient_confirmed: boolean;
}

export interface Provider {
  id: string;
  name_ja: string;
  name_en: string | null;
  specialty: string | null;
  clinic_name: string | null;
  first_seen: string | null;
  last_seen: string | null;
}

export interface HealthDocument {
  id: string;
  patient_id: string;
  file_name: string;
  file_type: string;
  upload_date: string;
  document_date: string | null;
  category: DocumentCategory;
  summary: string | null;
  tags: string[];
  extracted_data: ExtractedHealthData | null;
}

export enum DocumentCategory {
  HEALTH_CHECKUP = 'health_checkup',
  MEDICATION = 'medication',
  VACCINATION = 'vaccination',
  LAB_RESULTS = 'lab_results',
  MEDICAL_CERTIFICATE = 'medical_certificate',
  OTHER = 'other',
}

export interface ExtractedHealthData {
  checkup_date?: string;
  height?: number;
  weight?: number;
  bmi?: number;
  blood_pressure_systolic?: number;
  blood_pressure_diastolic?: number;
  blood_sugar?: number;
  hba1c?: number;
  ldl_cholesterol?: number;
  hdl_cholesterol?: number;
  triglycerides?: number;
  ast?: number;
  alt?: number;
  gamma_gtp?: number;
}

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  created_at: string;
}

export interface ShareLink {
  id: string;
  token: string;
  expires_at: string;
  url: string;
}
