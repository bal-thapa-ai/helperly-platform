"""
Quick verification script to check if the backend is properly set up.
Run this before starting the server to catch any issues early.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("Helperly Backend - Installation Verification")
print("=" * 60)

checks_passed = 0
checks_total = 0

# Check 1: Import core modules
checks_total += 1
try:
    from app.core.config import settings
    print(f"\n✓ Config loaded: {settings.app_name}")
    print(f"  Environment: {settings.env}")
    print(f"  Log level: {settings.log_level}")
    checks_passed += 1
except Exception as e:
    print(f"\n✗ Failed to load config: {e}")

# Check 2: Import database module
checks_total += 1
try:
    from app.core.database import Base
    print("\n✓ Database module imported")
    checks_passed += 1
except Exception as e:
    print(f"\n✗ Failed to import database: {e}")

# Check 3: Import models
checks_total += 1
try:
    from app.models import Organization, Chatbox, Document, Chunk
    print("\n✓ Models imported successfully")
    checks_passed += 1
except Exception as e:
    print(f"\n✗ Failed to import models: {e}")

# Check 4: Import services
checks_total += 1
try:
    from app.services import (
        EmbeddingService,
        LLMService,
        ChunkingService,
        IngestionService,
        QueryService,
    )
    print("\n✓ Services imported successfully")
    checks_passed += 1
except Exception as e:
    print(f"\n✗ Failed to import services: {e}")

# Check 5: Import API routes
checks_total += 1
try:
    from app.api.routes import health, chatboxes, ingest, query
    print("\n✓ API routes imported successfully")
    checks_passed += 1
except Exception as e:
    print(f"\n✗ Failed to import routes: {e}")

# Check 6: Import main app
checks_total += 1
try:
    from app.main import app
    print("\n✓ FastAPI app created successfully")
    checks_passed += 1
except Exception as e:
    print(f"\n✗ Failed to create app: {e}")

# Check 7: Verify dependencies
checks_total += 1
try:
    import fastapi
    import sqlalchemy
    import pydantic
    print("\n✓ Core dependencies installed")
    print(f"  FastAPI: {fastapi.__version__}")
    print(f"  SQLAlchemy: {sqlalchemy.__version__}")
    print(f"  Pydantic: {pydantic.__version__}")
    checks_passed += 1
except Exception as e:
    print(f"\n✗ Missing dependencies: {e}")

# Check 8: Optional dependencies
print("\n📦 Optional dependencies:")
try:
    import openai
    print(f"  ✓ OpenAI: {openai.__version__}")
except ImportError:
    print("  ℹ OpenAI: Not installed (will use stubs)")

try:
    import pgvector
    print(f"  ✓ pgvector: {pgvector.__version__}")
except ImportError:
    print("  ℹ pgvector: Not installed (needed for vector search)")

# Check 9: Configuration warnings
print("\n⚙️  Configuration:")
if not settings.database_url:
    print("  ⚠ DATABASE_URL not set (running without database)")
else:
    print(f"  ✓ DATABASE_URL configured")

if not settings.openai_api_key:
    print("  ⚠ OPENAI_API_KEY not set (using stub implementations)")
else:
    print(f"  ✓ OPENAI_API_KEY configured")

if not settings.api_key:
    print("  ⚠ API_KEY not set (authentication disabled)")
else:
    print(f"  ✓ API_KEY configured")

# Summary
print("\n" + "=" * 60)
print(f"Verification Results: {checks_passed}/{checks_total} checks passed")
print("=" * 60)

if checks_passed == checks_total:
    print("\n✅ All checks passed! You're ready to start the server:")
    print("   uvicorn app.main:app --reload")
    sys.exit(0)
else:
    print(f"\n❌ {checks_total - checks_passed} check(s) failed.")
    print("   Please install dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
