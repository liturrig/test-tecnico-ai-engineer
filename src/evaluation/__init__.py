from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAPPINGS_DIR = PROJECT_ROOT / "src" / "experiments" / "artifacts"

print(f"MAPPINGS_DIR is set to: {MAPPINGS_DIR}")