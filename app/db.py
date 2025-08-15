import mysql.connector
import os
from datetime import datetime
import logging

# Set up logging for database operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection():
    """Create and return a MySQL database connection"""
    try:
        return mysql.connector.connect(
            host="db",
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            autocommit=False
        )
    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}")
        raise

def init_database():
    """Initialize the database and create tables if they don't exist"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create notes table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        logger.info("Database initialized successfully")
        
    except mysql.connector.Error as err:
        logger.error(f"Error initializing database: {err}")
        raise
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_notes():
    """Retrieve all notes ordered by creation date (newest first)"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT id, content, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as formatted_date 
        FROM notes 
        ORDER BY created_at DESC
        """
        
        cursor.execute(query)
        notes = cursor.fetchall()
        logger.info(f"Retrieved {len(notes)} notes")
        return notes
        
    except mysql.connector.Error as err:
        logger.error(f"Error retrieving notes: {err}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_note(content):
    """Add a new note to the database"""
    if not content or not content.strip():
        logger.warning("Attempted to add empty note")
        return False
        
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Trim whitespace from content
        content = content.strip()
        
        query = "INSERT INTO notes (content) VALUES (%s)"
        cursor.execute(query, (content,))
        conn.commit()
        
        note_id = cursor.lastrowid
        logger.info(f"Added new note with ID: {note_id}")
        return True
        
    except mysql.connector.Error as err:
        logger.error(f"Error adding note: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def delete_note(note_id):
    """Delete a note by its ID"""
    if not note_id or note_id <= 0:
        logger.warning(f"Invalid note ID for deletion: {note_id}")
        return False
        
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if note exists first
        cursor.execute("SELECT id FROM notes WHERE id = %s", (note_id,))
        if not cursor.fetchone():
            logger.warning(f"Note with ID {note_id} not found")
            return False
        
        # Delete the note
        query = "DELETE FROM notes WHERE id = %s"
        cursor.execute(query, (note_id,))
        conn.commit()
        
        deleted_rows = cursor.rowcount
        if deleted_rows > 0:
            logger.info(f"Deleted note with ID: {note_id}")
            return True
        else:
            logger.warning(f"No note deleted with ID: {note_id}")
            return False
            
    except mysql.connector.Error as err:
        logger.error(f"Error deleting note {note_id}: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def update_note(note_id, new_content):
    """Update a note's content by its ID"""
    if not note_id or note_id <= 0:
        logger.warning(f"Invalid note ID for update: {note_id}")
        return False
        
    if not new_content or not new_content.strip():
        logger.warning("Attempted to update note with empty content")
        return False
        
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if note exists first
        cursor.execute("SELECT id FROM notes WHERE id = %s", (note_id,))
        if not cursor.fetchone():
            logger.warning(f"Note with ID {note_id} not found")
            return False
        
        # Trim whitespace from content
        new_content = new_content.strip()
        
        # Update the note (updated_at will be automatically set by MySQL)
        query = "UPDATE notes SET content = %s WHERE id = %s"
        cursor.execute(query, (new_content, note_id))
        conn.commit()
        
        updated_rows = cursor.rowcount
        if updated_rows > 0:
            logger.info(f"Updated note with ID: {note_id}")
            return True
        else:
            logger.warning(f"No note updated with ID: {note_id}")
            return False
            
    except mysql.connector.Error as err:
        logger.error(f"Error updating note {note_id}: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_note_by_id(note_id):
    """Get a single note by its ID"""
    if not note_id or note_id <= 0:
        logger.warning(f"Invalid note ID: {note_id}")
        return None
        
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT id, content, created_at, updated_at 
        FROM notes 
        WHERE id = %s
        """
        
        cursor.execute(query, (note_id,))
        note = cursor.fetchone()
        
        if note:
            logger.info(f"Retrieved note with ID: {note_id}")
        else:
            logger.warning(f"Note with ID {note_id} not found")
            
        return note
        
    except mysql.connector.Error as err:
        logger.error(f"Error retrieving note {note_id}: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_notes_count():
    """Get the total number of notes"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM notes")
        count = cursor.fetchone()[0]
        logger.info(f"Total notes count: {count}")
        return count
        
    except mysql.connector.Error as err:
        logger.error(f"Error getting notes count: {err}")
        return 0
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Initialize database when module is imported
if __name__ != '__main__':
    try:
        init_database()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
