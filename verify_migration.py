"""
Verify that the migration was successful
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

with app.app_context():
    with db.engine.connect() as conn:
        result = conn.execute(db.text("PRAGMA table_info(appointments)"))
        columns = [(row[1], row[2]) for row in result]
        
        print("\n" + "=" * 60)
        print("Appointments Table Schema")
        print("=" * 60)
        for col_name, col_type in columns:
            marker = "✓" if col_name in ['rejection_reason', 'updated_at'] else " "
            print(f"{marker} {col_name:<25} {col_type}")
        print("=" * 60)
        
        # Check if new columns exist
        col_names = [c[0] for c in columns]
        if 'rejection_reason' in col_names and 'updated_at' in col_names:
            print("✅ Migration successful! All required columns present.")
        else:
            print("❌ Migration incomplete. Missing columns:")
            if 'rejection_reason' not in col_names:
                print("  - rejection_reason")
            if 'updated_at' not in col_names:
                print("  - updated_at")
        print("=" * 60 + "\n")
