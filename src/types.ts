export interface LinkItem {
  title?: string | null;
  url?: string | null;
  summary?: string | null;
  lang?: string | null;
  source?: string | null;
  term?: string | null;
}

export interface NoteListItem {
  id: number;
  title: string;
  summary: string | null;
  language?: string | null;
  status: string;
  created_at?: string | null;
  updated_at?: string | null;
  audio_path?: string | null;
  has_transcript: boolean;
  keywords: string[];
  bullets: string[];
  decisions: string[];
  action_items: string[];
  open_questions: string[];
  links: LinkItem[];
  summarizer_provider?: string | null;
}

export interface NoteDetail extends NoteListItem {
  content?: string | null;
}

export interface RecordingStatus {
  is_recording: boolean;
  current_filename?: string | null;
  device_name?: string | null;
  started_at?: string | null;
  duration_seconds?: number | null;
  available: boolean;
}
