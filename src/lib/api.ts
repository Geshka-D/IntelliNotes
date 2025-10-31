import type { NoteDetail, NoteListItem, RecordingStatus } from "../types";

interface RecordingResponsePayload {
  status: string;
  message: string;
  filename?: string;
  device_name?: string;
}

const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? "/api").replace(/\/$/, "");

class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      Accept: "application/json",
      ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...options.headers,
    },
  });

  if (response.status === 204) {
    return {} as T;
  }

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const payload = await response.json();
      detail = payload.detail ?? detail;
    } catch {
      // ignore parse errors
    }
    throw new ApiError(response.status, detail);
  }

  return (await response.json()) as T;
}

export async function listNotes(): Promise<NoteListItem[]> {
  const data = await request<{ items: NoteListItem[] }>(`/notes`);
  return data.items ?? [];
}

export async function getNoteDetail(id: number): Promise<NoteDetail> {
  return request<NoteDetail>(`/notes/${id}`);
}

export async function deleteNote(id: number): Promise<void> {
  await request(`/notes/${id}`, { method: "DELETE" });
}

export async function createNoteFromUpload(file: File, title?: string): Promise<NoteDetail> {
  const form = new FormData();
  form.append("file", file);
  if (title) {
    form.append("title", title);
  }
  return request<NoteDetail>(`/lectures/upload`, {
    method: "POST",
    body: form,
  });
}

export async function createNoteFromRecording(filename: string, title?: string): Promise<NoteDetail> {
  return request<NoteDetail>(`/lectures/process-recording`, {
    method: "POST",
    body: JSON.stringify({ filename, title }),
  });
}

export async function createNoteFromText(text: string, title?: string): Promise<NoteDetail> {
  return request<NoteDetail>(`/lectures/text`, {
    method: "POST",
    body: JSON.stringify({ text, title }),
  });
}

export async function startRecording(): Promise<RecordingResponsePayload> {
  const response = await request<RecordingResponsePayload>(`/recording/start`, { method: "POST" });
  if (response.status !== "success") {
    throw new ApiError(400, response.message);
  }
  return response;
}

export async function stopRecording(): Promise<RecordingResponsePayload> {
  const response = await request<RecordingResponsePayload>(`/recording/stop`, { method: "POST" });
  if (response.status !== "success") {
    throw new ApiError(400, response.message);
  }
  return response;
}

export async function getRecordingStatus(): Promise<RecordingStatus> {
  return request<RecordingStatus>(`/recording/status`);
}

export { ApiError };
