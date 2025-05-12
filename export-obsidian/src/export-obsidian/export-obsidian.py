#!/usr/bin/env python3
"""
Obsidian Export Script

This script exports an Obsidian markdown file along with its directly linked files and assets
to a specified output directory with a flattened folder structure.

Usage:
    python export-obsidian.py <target_file> <output_directory>

Arguments:
    target_file: Path to the target markdown file
    output_directory: Path to the output directory where files will be copied
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path


def parse_arguments():
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Export an Obsidian markdown file and its linked files to a directory."
    )
    parser.add_argument(
        "target_file",
        type=str,
        help="Path to the target markdown file",
    )
    parser.add_argument(
        "output_directory",
        type=str,
        help="Path to the output directory",
    )
    
    args = parser.parse_args()
    
    # Validate target file exists and is a markdown file
    target_path = Path(args.target_file)
    if not target_path.exists():
        sys.exit(f"Error: Target file '{args.target_file}' does not exist.")
    if target_path.suffix.lower() != '.md':
        sys.exit(f"Error: Target file '{args.target_file}' is not a markdown file.")
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output_directory)
    output_path.mkdir(parents=True, exist_ok=True)
    
    return args


def find_linked_files(target_file_path):
    """
    Find all markdown files linked in the target file using [[link]] syntax.
    
    Args:
        target_file_path: Path to the target markdown file
        
    Returns:
        A list of paths to linked markdown files
    """
    target_path = Path(target_file_path)
    base_dir = target_path.parent
    
    with open(target_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find all [[link]] patterns
    # This regex matches [[link]] and [[link|display text]] patterns
    link_pattern = r'\[\[(.*?)(?:\|.*?)?\]\]'
    matches = re.findall(link_pattern, content)
    
    linked_files = []
    for match in matches:
        # Handle paths with or without .md extension
        file_path = match
        if not file_path.lower().endswith('.md'):
            file_path += '.md'
        
        # Try to resolve the file path
        # First check if it's an absolute path
        absolute_path = Path(file_path)
        if absolute_path.exists() and absolute_path.is_file():
            linked_files.append(absolute_path)
            continue
        
        # Then check if it's relative to the target file's directory
        relative_path = base_dir / file_path
        if relative_path.exists() and relative_path.is_file():
            linked_files.append(relative_path)
            continue
        
        # If we couldn't find the file, print a warning
        print(f"Warning: Linked file '{file_path}' not found.")
    
    return linked_files


def find_asset_references(target_file_path):
    """
    Find all assets referenced in the target file.
    
    Args:
        target_file_path: Path to the target markdown file
        
    Returns:
        A list of paths to referenced assets
    """
    target_path = Path(target_file_path)
    base_dir = target_path.parent
    
    with open(target_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find image references like ![alt](path/to/image.png)
    image_pattern = r'!\[.*?\]\((.*?)\)'
    image_matches = re.findall(image_pattern, content)
    
    # Find other asset references like [link](path/to/file.pdf)
    asset_pattern = r'(?<!!)\[.*?\]\((.*?)\)'
    asset_matches = re.findall(asset_pattern, content)
    
    # Combine all matches
    all_matches = image_matches + asset_matches
    
    assets = []
    for match in all_matches:
        # Skip URLs
        if match.startswith(('http://', 'https://', 'ftp://')):
            continue
        
        # Try to resolve the asset path
        # First check if it's an absolute path
        absolute_path = Path(match)
        if absolute_path.exists() and absolute_path.is_file():
            assets.append(absolute_path)
            continue
        
        # Then check if it's relative to the target file's directory
        relative_path = base_dir / match
        if relative_path.exists() and relative_path.is_file():
            assets.append(relative_path)
            continue
        
        # If we couldn't find the asset, print a warning
        print(f"Warning: Referenced asset '{match}' not found.")
    
    return assets


def copy_files_to_output(target_file_path, linked_files, assets, output_dir):
    """
    Copy all files to the output directory with a flat structure.
    
    Args:
        target_file_path: Path to the target markdown file
        linked_files: List of paths to linked markdown files
        assets: List of paths to referenced assets
        output_dir: Path to the output directory
    """
    output_path = Path(output_dir)
    target_path = Path(target_file_path)
    
    # Keep track of filenames to handle conflicts
    used_filenames = set()
    
    # Copy the target file
    target_output_path = output_path / target_path.name
    shutil.copy2(target_path, target_output_path)
    used_filenames.add(target_path.name)
    print(f"Copied target file: {target_path.name}")
    
    # Copy linked files
    for file_path in linked_files:
        output_filename = file_path.name
        
        # Handle filename conflicts
        if output_filename in used_filenames:
            # Add parent directory name as prefix to avoid conflicts
            parent_dir = file_path.parent.name
            name_parts = output_filename.split('.')
            if len(name_parts) > 1:
                # File has extension
                output_filename = f"{name_parts[0]}_{parent_dir}.{'.'.join(name_parts[1:])}"
            else:
                # File has no extension
                output_filename = f"{output_filename}_{parent_dir}"
        
        output_file_path = output_path / output_filename
        shutil.copy2(file_path, output_file_path)
        used_filenames.add(output_filename)
        print(f"Copied linked file: {file_path.name} as {output_filename}")
    
    # Copy assets
    for asset_path in assets:
        output_filename = asset_path.name
        
        # Handle filename conflicts
        if output_filename in used_filenames:
            # Add parent directory name as prefix to avoid conflicts
            parent_dir = asset_path.parent.name
            name_parts = output_filename.split('.')
            if len(name_parts) > 1:
                # File has extension
                output_filename = f"{name_parts[0]}_{parent_dir}.{'.'.join(name_parts[1:])}"
            else:
                # File has no extension
                output_filename = f"{output_filename}_{parent_dir}"
        
        output_asset_path = output_path / output_filename
        shutil.copy2(asset_path, output_asset_path)
        used_filenames.add(output_filename)
        print(f"Copied asset: {asset_path.name} as {output_filename}")


def main():
    """Main function to orchestrate the export process."""
    args = parse_arguments()
    
    print(f"Exporting '{args.target_file}' and linked files to '{args.output_directory}'...")
    
    # Find linked files and assets
    linked_files = find_linked_files(args.target_file)
    assets = find_asset_references(args.target_file)
    
    # Copy files to output directory
    copy_files_to_output(args.target_file, linked_files, assets, args.output_directory)
    
    print(f"\nExport complete!")
    print(f"- Target file: 1")
    print(f"- Linked files: {len(linked_files)}")
    print(f"- Assets: {len(assets)}")
    print(f"- Total files copied: {1 + len(linked_files) + len(assets)}")


if __name__ == "__main__":
    main()
