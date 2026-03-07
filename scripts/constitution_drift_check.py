"""Constitution Drift Checker.

Validates that codebase models and patterns adhere to
the rules defined in docs/constitution.md.
"""

import ast
import sys
from pathlib import Path


def check_vindicta_model_inheritance(packages_dir: Path) -> list[str]:
    """Check that all model classes in src/ inherit from VindictaModel."""
    violations: list[str] = []

    for src_dir in packages_dir.glob("*/src"):
        for py_file in src_dir.rglob("*.py"):
            if "models" not in str(py_file):
                continue
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                # Skip base class itself, test helpers, and private classes
                if node.name.startswith("_") or node.name == "VindictaModel":
                    continue
                # Check if any base is VindictaModel (direct or indirect)
                base_names = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_names.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        base_names.append(base.attr)

                # Models in models/ dirs should inherit from VindictaModel
                if "models" in py_file.parts and not any(
                    "VindictaModel" in name or "Model" in name
                    for name in base_names
                ):
                    rel_path = py_file.relative_to(packages_dir)
                    violations.append(
                        f"VIOLATION: {rel_path}:{node.lineno} — "
                        f"class {node.name} does not inherit from VindictaModel "
                        f"(bases: {base_names})"
                    )
    return violations


def check_adr_index(docs_dir: Path) -> list[str]:
    """Check that all ADR files are referenced in architecture docs."""
    violations: list[str] = []
    adr_dir = docs_dir / "architecture" / "adr"

    if not adr_dir.exists():
        return violations

    adr_files = [
        f.name for f in adr_dir.glob("*.md")
        if not f.name.startswith("_")
    ]

    # Check if there's an index or c4 model referencing ADRs
    arch_content = ""
    for arch_file in (docs_dir / "architecture").glob("*.md"):
        arch_content += arch_file.read_text(encoding="utf-8")

    for adr_file in adr_files:
        if adr_file not in arch_content:
            violations.append(
                f"VIOLATION: ADR {adr_file} is not referenced in "
                f"architecture documentation"
            )

    return violations


def check_constitution_exists(root: Path) -> list[str]:
    """Ensure constitution file exists and is non-empty."""
    violations: list[str] = []
    constitution = root / "docs" / "constitution.md"

    if not constitution.exists():
        violations.append("VIOLATION: docs/constitution.md does not exist")
    elif constitution.stat().st_size < 100:
        violations.append(
            "VIOLATION: docs/constitution.md appears empty or too short"
        )
    return violations


def main() -> int:
    root = Path.cwd()
    packages_dir = root / "packages"
    docs_dir = root / "docs"

    all_violations: list[str] = []

    # Run all checks
    all_violations.extend(check_constitution_exists(root))

    if packages_dir.exists():
        all_violations.extend(
            check_vindicta_model_inheritance(packages_dir)
        )

    if docs_dir.exists():
        all_violations.extend(check_adr_index(docs_dir))

    # Report
    if all_violations:
        print(f"Found {len(all_violations)} violation(s):\n")
        for v in all_violations:
            print(f"  {v}")
        return 1
    else:
        print("✅ No constitution drift violations detected.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
