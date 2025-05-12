# Obsidian Export Tool

A Python utility for exporting Obsidian markdown files along with their linked files and assets to a specified output directory with a flattened folder structure.

## Description

This tool helps Obsidian users export their notes and related assets to a simplified directory structure. It processes a target markdown file, identifies all linked files using Obsidian's `[[link]]` syntax, finds referenced assets (images, PDFs, etc.), and copies everything to a specified output directory.

Key features:
- Exports a target markdown file and all its directly linked files
- Includes all referenced assets (images, documents, etc.)
- Handles filename conflicts by adding parent directory names as prefixes
- Creates a flat directory structure for easy access to all exported files

## Installation

This project uses Poetry for dependency management.

```bash
# Clone the repository
git clone https://github.com/yourusername/export-obsidian.git
cd export-obsidian

# Install dependencies using Poetry
poetry install
```

## Usage

```bash
# Basic usage
python src/export-obsidian/export-obsidian.py <target_file> <output_directory>

# Example
python src/export-obsidian/export-obsidian.py test_notes/main_note.md output_notes/
```

### Arguments

- `target_file`: Path to the target markdown file you want to export
- `output_directory`: Path to the output directory where files will be copied

## How It Works

1. The script parses the target markdown file to find:
   - Links to other markdown files using Obsidian's `[[link]]` syntax
   - References to assets using standard markdown image/link syntax `![alt](path)` or `[text](path)`

2. It copies the target file, all linked files, and all referenced assets to the output directory

3. If filename conflicts occur, it resolves them by adding the parent directory name as a prefix

## Project Structure

```
export-obsidian/
├── poetry.lock              # Poetry lock file with exact dependency versions
├── pyproject.toml           # Project configuration and dependencies
├── output_notes/            # Example output directory
├── src/
│   └── export-obsidian/     # Source code
│       ├── __init__.py
│       └── export-obsidian.py  # Main script
└── test_notes/              # Example notes for testing
    ├── main_note.md
    ├── second_note.md
    ├── third_note.md
    ├── documents/
    │   └── sample.txt
    ├── folder/
    │   └── nested_note.md
    └── images/
        ├── sample.png
        └── sample.txt
```

## Dependencies

- Python 3.12 or higher
- Poetry for dependency management

## License

[Add license information here]

## Contributing

[Add contribution guidelines here]
