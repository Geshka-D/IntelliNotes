from .database import get_connection

def create_note(title: str, content: str, summary: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (title, content, summary) VALUES (?, ?, ?)", (title, content, summary))
    conn.commit()
    nid = cur.lastrowid
    conn.close()
    return nid

def list_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, summary, created_at FROM notes ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_note(note_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None
