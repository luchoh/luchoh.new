from pathlib import Path
from typing import Dict, Optional, List
import re

# Define comment styles as a constant dictionary
COMMENT_STYLES: Dict[str, Dict[str, Optional[str]]] = {
    ".py": {"start": "#", "end": None},
    ".njk": {"start": "{#", "end": "#}"},
    ".html": {"start": "/*", "end": "*/"},
    ".css": {"start": "/*", "end": "*/"},
    ".js": {"start": "/*", "end": "*/"},
}

# Define patterns for folders to skip
SKIP_PATTERNS: List[str] = [
    r"(^|/)dist($|/)",
    r"(^|/)__pycache__($|/)",
    r"(^|/)__pycache__($|/)",
    r"(^|/)node_modules($|/)",
    r"(^|/)\.git($|/)",
    r"(^|/)\.vscode($|/)",
    r"(^|/)\.idea($|/)",
    r"(^|/)build($|/)",
    r"(^|/)tmp($|/)",
    r"(^|/)temp($|/)",
    r"(^|/)logs($|/)",
    r"(^|/)venv($|/)",
    r"(^|/)env($|/)",
    r"(^|/)alembic($|/)",
]


def get_comment_style(file_extension: str) -> Optional[Dict[str, Optional[str]]]:
    return COMMENT_STYLES.get(file_extension)


def should_skip_folder(path: Path) -> bool:
    path_str = str(path)
    return any(re.search(pattern, path_str) for pattern in SKIP_PATTERNS)


def annotate_file(file_path: Path, relative_path: Path, project: str) -> None:
    comment_style = get_comment_style(file_path.suffix)
    if not comment_style:
        return  # Skip files with unsupported extensions

    with file_path.open("r+", encoding="utf-8") as file:
        content = file.read()
        if f"File: {relative_path}" in content:
            print(f"Skipping already annotated {file_path}")
            return

        file.seek(0)

        # Check for front matter
        front_matter_match = re.match(r"^---\n(.*?\n)---\n", content, re.DOTALL)

        if front_matter_match:
            front_matter = front_matter_match.group(0)
            rest_of_content = content[len(front_matter) :]

            file.write(front_matter)
            file.write(
                f"{comment_style['start']} Project: {project} # File: {relative_path} {comment_style['end']}\n"
            )
            file.write(rest_of_content)
        else:
            # If no front matter, proceed as before
            if file_path.suffix == ".njk":
                file.write(
                    f"{comment_style['start']} Project: {project} # File: {relative_path} {comment_style['end']}\n"
                )
            elif comment_style["end"]:
                file.write(
                    f"{comment_style['start']}Project: {project}\nFile: {relative_path}{comment_style['end']}\n"
                )
            else:
                file.write(
                    f"{comment_style['start']} Project: {project}\n{comment_style['start']} File: {relative_path}\n"
                )
            file.write(content)

    print(f"Annotated {file_path}")


def annotate_files(root_dir: Path, project: str) -> None:
    root_dir = root_dir.resolve()
    script_path = Path(__file__).resolve()

    for file_path in root_dir.rglob("*"):
        if (
            file_path.is_file()
            and file_path.suffix in COMMENT_STYLES
            and file_path != script_path
        ):
            relative_path = file_path.relative_to(root_dir)
            if not any(
                part.startswith(".") for part in relative_path.parts
            ) and not should_skip_folder(relative_path):
                annotate_file(file_path, relative_path, project)


if __name__ == "__main__":
    root_directory = Path(".")
    project = "luchoh.com refactoring"
    annotate_files(root_directory, project)
