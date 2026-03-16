import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "reviews"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_message(question, answer):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_history (question, answer) VALUES (%s, %s)",
        (question, answer)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT question, answer, created_at FROM chat_history ORDER BY created_at DESC LIMIT 20")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows