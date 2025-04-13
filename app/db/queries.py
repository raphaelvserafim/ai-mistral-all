from .connection import get_connection

def save_message(conversation_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO conversations (id) VALUES (?)", (conversation_id,))
    cursor.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                   (conversation_id, role, content))
    conn.commit()
    conn.close()

def load_history(conversation_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
                   (conversation_id,))
    results = cursor.fetchall()
    conn.close()
    
    return [{"role": row["role"], "content": row["content"]} for row in results]



def list_conversations():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, created_at FROM conversations ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]