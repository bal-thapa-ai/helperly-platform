"""
Database initialization script.

Creates initial organization and sets up database schema.
Run this after setting up your database.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import init_db, AsyncSessionLocal
from app.models.organization import Organization


async def create_initial_org():
    """Create initial organization for testing."""
    if not AsyncSessionLocal:
        print("Database not configured. Skipping organization creation.")
        return
    
    async with AsyncSessionLocal() as session:
        # Check if org already exists
        from sqlalchemy import select
        result = await session.execute(select(Organization).where(Organization.id == 1))
        existing = result.scalar_one_or_none()
        
        if existing:
            print(f"Organization already exists: {existing.name}")
            return
        
        # Create initial org
        org = Organization(
            id=1,
            name="Default Organization",
            plan="free",
            api_key="dev-api-key-12345",  # Change this in production!
        )
        session.add(org)
        await session.commit()
        print(f"Created organization: {org.name} (ID: {org.id})")
        print(f"API Key: {org.api_key}")


async def main():
    """Initialize database and create initial data."""
    print("Initializing database...")
    
    try:
        await init_db()
        print("✓ Database schema created/verified")
        
        await create_initial_org()
        print("✓ Initial organization created")
        
        print("\n✅ Database initialization complete!")
        print("\nYou can now start the server with:")
        print("  uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
