"""
Database module for the Analyser Agent.
This module handles SQLite database operations for storing analysis results.
"""

import os
import json
import sqlite3
import logging
import datetime
from typing import Dict, Any, List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database file path
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "analysis_results.db")

class AnalysisDatabase:
    """Database handler for analysis results."""
    
    def __init__(self, db_path: str = DB_FILE):
        """Initialize the database connection."""
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create the database and tables if they don't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create the analysis_results table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                document_id TEXT PRIMARY KEY,
                document_name TEXT,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                score REAL,
                file_type TEXT,
                file_url TEXT,
                suggestions TEXT,  -- JSON array as text
                conflicts TEXT,    -- JSON array as text
                guidelines TEXT,
                summary TEXT
            )
            ''')
            
            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def store_analysis_result(self, 
                             document_id: str,
                             document_name: str,
                             status: str,
                             score: float,
                             file_type: str,
                             file_url: str,
                             suggestions: List[str],
                             conflicts: List[str],
                             guidelines: List[str],
                             summary: str) -> bool:
        """
        Store an analysis result in the database.
        
        Args:
            document_id: Unique identifier for the document
            document_name: Name of the document
            status: Status of the analysis (Reject/Approved)
            score: Score of the analysis
            file_type: Type of the file
            file_url: URL to the file
            suggestions: List of suggestions
            conflicts: List of conflicts
            guidelines: Guidelines used for analysis
            summary: Summary of the document
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert lists to JSON strings
            suggestions_json = json.dumps(suggestions)
            conflicts_json = json.dumps(conflicts)
            guidelines_json = json.dumps(guidelines)
            
            cursor.execute('''
            INSERT OR REPLACE INTO analysis_results 
            (document_id, document_name, upload_time, status, score, file_type, file_url, suggestions, conflicts, guidelines, summary)
            VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (document_id, document_name, status, score, file_type, file_url, suggestions_json, conflicts_json, guidelines_json, summary))
            
            conn.commit()
            logger.info(f"Stored analysis result for document ID: {document_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error storing analysis result: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()
    
    def get_analysis_result(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an analysis result from the database.
        
        Args:
            document_id: Unique identifier for the document
            
        Returns:
            Dict containing the analysis result or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # This enables column access by name
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM analysis_results WHERE document_id = ?', (document_id,))
            row = cursor.fetchone()
            
            if row:
                result = dict(row)
                # Parse JSON strings back to lists
                result['suggestions'] = json.loads(result['suggestions'])
                result['conflicts'] = json.loads(result['conflicts'])
                result['guidelines'] = json.loads(result['guidelines'])
                return result
            else:
                return None
        except sqlite3.Error as e:
            logger.error(f"Error retrieving analysis result: {str(e)}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_all_analysis_results(self) -> List[Dict[str, Any]]:
        """
        Retrieve all analysis results from the database.
        
        Returns:
            List of dictionaries containing all analysis results
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM analysis_results ORDER BY upload_time DESC')
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                result = dict(row)
                # Parse JSON strings back to lists
                result['suggestions'] = json.loads(result['suggestions'])
                result['conflicts'] = json.loads(result['conflicts'])
                result['guidelines'] = json.loads(result['guidelines'])
                results.append(result)
            
            return results
        except sqlite3.Error as e:
            logger.error(f"Error retrieving all analysis results: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
    
    def delete_analysis_result(self, document_id: str) -> bool:
        """
        Delete an analysis result from the database.
        
        Args:
            document_id: Unique identifier for the document
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM analysis_results WHERE document_id = ?', (document_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Deleted analysis result for document ID: {document_id}")
                return True
            else:
                logger.warning(f"No analysis result found for document ID: {document_id}")
                return False
        except sqlite3.Error as e:
            logger.error(f"Error deleting analysis result: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()
    
    def reset_database(self) -> bool:
        """
        Reset the database by dropping and recreating the analysis_results table.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Drop the table if it exists
            cursor.execute('DROP TABLE IF EXISTS analysis_results')
            
            # Recreate the table
            cursor.execute('''
            CREATE TABLE analysis_results (
                document_id TEXT PRIMARY KEY,
                document_name TEXT,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                score REAL,
                file_type TEXT,
                file_url TEXT,
                suggestions TEXT,  -- JSON array as text
                conflicts TEXT,    -- JSON array as text
                guidelines TEXT,
                summary TEXT
            )
            ''')
            
            conn.commit()
            logger.info("Database has been reset successfully")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error resetting database: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()
