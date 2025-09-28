# ai_api_module/core/memory.py
"""
Memory and context management
"""
import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Message:
    """Individual message in conversation"""
    role: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Memory:
    """Manages long-term memory and usage tracking"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Path.home() / ".ai_api_module" / "memory.db"
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        self._init_db()
        
        # In-memory caches
        self._facts_cache = {}
        self._usage_cache = []
    
    def _init_db(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    category TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    model TEXT,
                    provider TEXT,
                    cost REAL,
                    tokens INTEGER,
                    request_type TEXT,
                    metadata TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    total_cost REAL,
                    message_count INTEGER,
                    metadata TEXT
                )
            """)
    
    def add_fact(self, key: str, value: str, category: str = "general"):
        """Add or update a fact in memory"""
        now = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO facts (key, value, category, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (key, value, category, now, now))
        
        self._facts_cache[key] = value
    
    def get_fact(self, key: str) -> Optional[str]:
        """Get a fact from memory"""
        if key in self._facts_cache:
            return self._facts_cache[key]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT value FROM facts WHERE key = ?", (key,))
            result = cursor.fetchone()
            
            if result:
                value = result[0]
                self._facts_cache[key] = value
                return value
        
        return None
    
    def get_facts_by_category(self, category: str) -> Dict[str, str]:
        """Get all facts in a category"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT key, value FROM facts WHERE category = ?", 
                (category,)
            )
            return dict(cursor.fetchall())

    def get_all_facts(self) -> Dict[str, str]:
        """Return all stored facts regardless of category."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT key, value FROM facts")
            results = cursor.fetchall()

        facts = {key: value for key, value in results}
        self._facts_cache.update(facts)
        return facts
    
    def remove_fact(self, key: str):
        """Remove a fact from memory"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM facts WHERE key = ?", (key,))
        
        if key in self._facts_cache:
            del self._facts_cache[key]
    
    def add_usage_record(self, record: Dict[str, Any]):
        """Add usage record for cost tracking"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO usage_records 
                (timestamp, model, provider, cost, tokens, request_type, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                record.get("timestamp", datetime.now()),
                record.get("model", ""),
                record.get("provider", ""),
                record.get("cost", 0.0),
                record.get("tokens", 0),
                record.get("request_type", "chat"),
                json.dumps(record.get("metadata", {}))
            ))
        
        self._usage_cache.append(record)
    
    def get_daily_cost(self, date: Optional[datetime] = None) -> float:
        """Get total cost for a specific day"""
        if not date:
            date = datetime.now()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT SUM(cost) FROM usage_records 
                WHERE timestamp >= ? AND timestamp < ?
            """, (start_of_day, end_of_day))
            
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0.0
    
    def get_monthly_cost(self, year: int = None, month: int = None) -> float:
        """Get total cost for a specific month"""
        now = datetime.now()
        year = year or now.year
        month = month or now.month
        
        start_of_month = datetime(year, month, 1)
        if month == 12:
            end_of_month = datetime(year + 1, 1, 1)
        else:
            end_of_month = datetime(year, month + 1, 1)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT SUM(cost) FROM usage_records 
                WHERE timestamp >= ? AND timestamp < ?
            """, (start_of_month, end_of_month))
            
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0.0
    
    def get_most_used_model(self, days: int = 30) -> str:
        """Get most frequently used model in recent days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT model, COUNT(*) as usage_count 
                FROM usage_records 
                WHERE timestamp >= ? 
                GROUP BY model 
                ORDER BY usage_count DESC 
                LIMIT 1
            """, (cutoff_date,))
            
            result = cursor.fetchone()
            return result[0] if result else "unknown"
    
    def get_usage_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive usage statistics"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            # Total cost and requests
            cursor = conn.execute("""
                SELECT 
                    SUM(cost) as total_cost,
                    COUNT(*) as total_requests,
                    AVG(cost) as avg_cost_per_request,
                    SUM(tokens) as total_tokens
                FROM usage_records 
                WHERE timestamp >= ?
            """, (cutoff_date,))
            
            totals = cursor.fetchone()
            
            # Usage by model
            cursor = conn.execute("""
                SELECT model, COUNT(*) as count, SUM(cost) as cost
                FROM usage_records 
                WHERE timestamp >= ?
                GROUP BY model
                ORDER BY count DESC
            """, (cutoff_date,))
            
            model_usage = cursor.fetchall()
            
            # Usage by provider
            cursor = conn.execute("""
                SELECT provider, COUNT(*) as count, SUM(cost) as cost
                FROM usage_records 
                WHERE timestamp >= ?
                GROUP BY provider
                ORDER BY count DESC
            """, (cutoff_date,))
            
            provider_usage = cursor.fetchall()
        
        return {
            "period_days": days,
            "total_cost": totals[0] if totals[0] else 0.0,
            "total_requests": totals[1] if totals[1] else 0,
            "avg_cost_per_request": totals[2] if totals[2] else 0.0,
            "total_tokens": totals[3] if totals[3] else 0,
            "model_usage": [
                {"model": m[0], "requests": m[1], "cost": m[2]}
                for m in model_usage
            ],
            "provider_usage": [
                {"provider": p[0], "requests": p[1], "cost": p[2]}
                for p in provider_usage
            ]
        }
    
    def clean_old_records(self, days_to_keep: int = 90):
        """Clean old usage records to prevent database bloat"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM usage_records WHERE timestamp < ?
            """, (cutoff_date,))
            
            deleted_count = cursor.rowcount
        
        return deleted_count
