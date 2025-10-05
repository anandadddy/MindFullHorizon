"""
Migration script to add rejection_reason and updated_at fields to appointments table.
Run this script once to update your database schema.

Usage:
    python add_appointment_fields_migration.py
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Appointment

def migrate_database():
    """Add new fields to the appointments table"""
    with app.app_context():
        try:
            # Check if we're using SQLite
            if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
                print("Detected SQLite database. Performing migration...")
                
                # For SQLite, we need to use raw SQL
                with db.engine.connect() as conn:
                    # Check if columns already exist
                    result = conn.execute(db.text("PRAGMA table_info(appointments)"))
                    columns = [row[1] for row in result]
                    
                    if 'rejection_reason' not in columns:
                        print("Adding 'rejection_reason' column...")
                        conn.execute(db.text("ALTER TABLE appointments ADD COLUMN rejection_reason TEXT"))
                        conn.commit()
                        print("✓ Added 'rejection_reason' column")
                    else:
                        print("✓ 'rejection_reason' column already exists")
                    
                    if 'updated_at' not in columns:
                        print("Adding 'updated_at' column...")
                        conn.execute(db.text("ALTER TABLE appointments ADD COLUMN updated_at DATETIME"))
                        # Set default value for existing rows
                        conn.execute(db.text("UPDATE appointments SET updated_at = created_at WHERE updated_at IS NULL"))
                        conn.commit()
                        print("✓ Added 'updated_at' column")
                    else:
                        print("✓ 'updated_at' column already exists")
                
                print("\n✅ Migration completed successfully!")
                print("Your database is now ready to use the enhanced appointment system.")
                
            else:
                print("Non-SQLite database detected.")
                print("Please use Flask-Migrate (Alembic) for schema changes:")
                print("  flask db migrate -m 'Add rejection_reason and updated_at to appointments'")
                print("  flask db upgrade")
                
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            print("\nAlternative: You can recreate the database by:")
            print("  1. Backup your data")
            print("  2. Delete the database file")
            print("  3. Run: flask db upgrade")
            sys.exit(1)

if __name__ == '__main__':
    print("=" * 60)
    print("Appointment System Database Migration")
    print("=" * 60)
    print("\nThis will add the following fields to the appointments table:")
    print("  - rejection_reason (TEXT)")
    print("  - updated_at (DATETIME)")
    print("\n" + "=" * 60)
    
    response = input("\nProceed with migration? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        migrate_database()
    else:
        print("Migration cancelled.")
