"""
Automatic migration script to add rejection_reason and updated_at fields to appointments table.
This script runs automatically without user confirmation.

Usage:
    python migrate_appointments_auto.py
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_database():
    """Add new fields to the appointments table"""
    with app.app_context():
        try:
            print("=" * 60)
            print("Appointment System Database Migration")
            print("=" * 60)
            print("\nAdding new fields to appointments table...")
            
            # For SQLite, we need to use raw SQL
            with db.engine.connect() as conn:
                # Check if columns already exist
                result = conn.execute(db.text("PRAGMA table_info(appointments)"))
                columns = [row[1] for row in result]
                
                changes_made = False
                
                if 'rejection_reason' not in columns:
                    print("  → Adding 'rejection_reason' column...")
                    conn.execute(db.text("ALTER TABLE appointments ADD COLUMN rejection_reason TEXT"))
                    conn.commit()
                    print("  ✓ Added 'rejection_reason' column")
                    changes_made = True
                else:
                    print("  ✓ 'rejection_reason' column already exists")
                
                if 'updated_at' not in columns:
                    print("  → Adding 'updated_at' column...")
                    conn.execute(db.text("ALTER TABLE appointments ADD COLUMN updated_at DATETIME"))
                    # Set default value for existing rows
                    conn.execute(db.text("UPDATE appointments SET updated_at = created_at WHERE updated_at IS NULL"))
                    conn.commit()
                    print("  ✓ Added 'updated_at' column")
                    changes_made = True
                else:
                    print("  ✓ 'updated_at' column already exists")
            
            print("\n" + "=" * 60)
            if changes_made:
                print("✅ Migration completed successfully!")
                print("Your database is now ready to use the appointment system.")
            else:
                print("✅ Database already up to date!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            print("\nTroubleshooting:")
            print("  1. Make sure the Flask app is not running")
            print("  2. Check database file permissions")
            print("  3. Verify database path in app.py")
            sys.exit(1)

if __name__ == '__main__':
    migrate_database()
