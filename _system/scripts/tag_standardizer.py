#!/usr/bin/env python3
"""
Tag Standardization Script for Project Vault
Normalizes tags according to TAG_TAXONOMY.md
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

# Tag standardization mapping
TAG_MAPPING = {
    # Flatten tags to hierarchical
    'documentation': 'documentation/guide',
    'index': 'navigation/index',
    'moc': 'navigation/moc',
    'navigation': 'navigation/moc',
    'standardization': 'metadata/standardization',
    'optimization': 'metadata/optimization',
    'performance': 'metadata/performance',
    'vault-health': 'metadata/vault-health',
    'sales-automation': 'workflow/sales-report',
    'metadata': 'metadata/standards',
    
    # Category consolidation
    'setup/general': 'setup/configuration',
    'setup/api': 'integration/api',
    'setup/api/serpstack': 'integration/api/serpstack',
    
    # Case normalization (if needed)
    'Setup': 'setup/configuration',
    'Documentation': 'documentation/guide',
}

# Project name normalization
PROJECT_MAPPING = {
    'suno_auto': 'suno-auto',
    'dify_note': 'dify-note',
    'Airregi-Analytics': 'airregi-analytics',
    'Dify-n8n-workflow': 'dify-n8n-workflow',
}


def extract_frontmatter(content):
    """Extract frontmatter and body from markdown content"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        return match.group(1), match.group(2)
    return None, content


def extract_tags_from_frontmatter_text(frontmatter_text):
    """Extract tags from frontmatter text"""
    tags = []
    in_tags = False
    
    for line in frontmatter_text.split('\n'):
        line_stripped = line.strip()
        
        if line_stripped.startswith('tags:'):
            in_tags = True
            # Check for inline array format
            inline_match = re.search(r'tags:\s*\[(.*?)\]', line_stripped)
            if inline_match:
                tag_str = inline_match.group(1)
                tags.extend([t.strip(' "\'') for t in tag_str.split(',')])
                in_tags = False
            continue
        
        if in_tags:
            if line_stripped.startswith('- '):
                tag = line_stripped[2:].strip(' "\'')
                tags.append(tag)
            elif line_stripped and not line_stripped.endswith(':'):
                in_tags = False
    
    return tags


def standardize_tag(tag):
    """Standardize a single tag according to mapping"""
    # Direct mapping
    if tag in TAG_MAPPING:
        return TAG_MAPPING[tag]
    
    # Project name normalization
    if tag.startswith('project/'):
        project_name = tag.split('/', 1)[1]
        if project_name in PROJECT_MAPPING:
            return f"project/{PROJECT_MAPPING[project_name]}"
    
    # No change needed
    return tag


def standardize_tags(tags):
    """Standardize a list of tags"""
    standardized = []
    seen = set()
    
    for tag in tags:
        new_tag = standardize_tag(tag)
        
        # Avoid duplicates
        if new_tag not in seen:
            standardized.append(new_tag)
            seen.add(new_tag)
    
    return standardized


def update_frontmatter_tags(frontmatter_text, new_tags):
    """Update tags in frontmatter text"""
    lines = frontmatter_text.split('\n')
    new_lines = []
    in_tags = False
    tags_updated = False
    
    for line in lines:
        line_stripped = line.strip()
        
        if line_stripped.startswith('tags:'):
            # Replace tags section
            new_lines.append('tags:')
            for tag in new_tags:
                new_lines.append(f'  - "{tag}"')
            in_tags = True
            tags_updated = True
            
            # Check if inline format (skip it)
            if '[' in line:
                in_tags = False
            continue
        
        if in_tags:
            # Skip old tag lines
            if line_stripped.startswith('- '):
                continue
            elif line_stripped and not line_stripped.endswith(':'):
                # End of tags section
                in_tags = False
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # If tags weren't found, add them
    if not tags_updated:
        new_lines.append('tags:')
        for tag in new_tags:
            new_lines.append(f'  - "{tag}"')
    
    return '\n'.join(new_lines)


def process_file(filepath, dry_run=True):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, body = extract_frontmatter(content)
        
        if not frontmatter:
            return None, None, "No frontmatter"
        
        tags = extract_tags_from_frontmatter_text(frontmatter)
        
        if not tags:
            return None, None, "No tags"
        
        new_tags = standardize_tags(tags)
        
        # Check if changes needed
        if tags == new_tags:
            return None, None, "No changes"
        
        # Update frontmatter
        new_frontmatter = update_frontmatter_tags(frontmatter, new_tags)
        new_content = f"---\n{new_frontmatter}\n---\n{body}"
        
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return tags, new_tags, "Updated"
        
    except Exception as e:
        return None, None, f"Error: {str(e)}"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Standardize tags in Project Vault')
    parser.add_argument('--report', action='store_true', help='Generate report only (dry run)')
    parser.add_argument('--path', default='/Users/remma/project', help='Root directory path')
    args = parser.parse_args()
    
    root_dir = Path(args.path)
    dry_run = args.report
    
    print("🏷️  Tag Standardization Script")
    print("=" * 80)
    print(f"Mode: {'REPORT ONLY (dry run)' if dry_run else 'APPLY CHANGES'}")
    print(f"Path: {root_dir}")
    print()
    
    # Statistics
    stats = {
        'total': 0,
        'updated': 0,
        'no_changes': 0,
        'no_tags': 0,
        'no_frontmatter': 0,
        'errors': 0
    }
    
    changes = []
    exclude_dirs = {'node_modules', 'venv', '.git', 'dist', 'build', '.next'}
    
    # Process files
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if not file.endswith('.md'):
                continue
            
            filepath = Path(root) / file
            stats['total'] += 1
            
            old_tags, new_tags, status = process_file(filepath, dry_run)
            
            if status == "Updated":
                stats['updated'] += 1
                changes.append({
                    'file': str(filepath.relative_to(root_dir)),
                    'old_tags': old_tags,
                    'new_tags': new_tags
                })
            elif status == "No changes":
                stats['no_changes'] += 1
            elif status == "No tags":
                stats['no_tags'] += 1
            elif status == "No frontmatter":
                stats['no_frontmatter'] += 1
            elif status.startswith("Error"):
                stats['errors'] += 1
                print(f"❌ {filepath.relative_to(root_dir)}: {status}")
    
    # Print results
    print("\n📊 STATISTICS")
    print("-" * 80)
    print(f"Total files: {stats['total']}")
    print(f"Files updated: {stats['updated']}")
    print(f"Files unchanged: {stats['no_changes']}")
    print(f"Files without tags: {stats['no_tags']}")
    print(f"Files without frontmatter: {stats['no_frontmatter']}")
    print(f"Errors: {stats['errors']}")
    
    if changes:
        print(f"\n📝 CHANGES {'(PREVIEW - not applied)' if dry_run else '(APPLIED)'}")
        print("-" * 80)
        
        for change in changes[:20]:  # Show first 20
            print(f"\n{change['file']}")
            print(f"  Old: {', '.join(change['old_tags'])}")
            print(f"  New: {', '.join(change['new_tags'])}")
        
        if len(changes) > 20:
            print(f"\n... and {len(changes) - 20} more files changed")
    
    # Generate report
    if dry_run:
        report_path = '/Users/remma/project/TAG_STANDARDIZATION_REPORT.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write('title: "Tag Standardization Report"\n')
            f.write('type: documentation\n')
            f.write('status: active\n')
            f.write(f'created: "{datetime.now().strftime("%Y-%m-%d")}"\n')
            f.write(f'updated: "{datetime.now().strftime("%Y-%m-%d")}"\n')
            f.write('tags:\n')
            f.write('  - "metadata/standardization"\n')
            f.write('  - "documentation/report"\n')
            f.write("---\n\n")
            
            f.write("# タグ標準化レポート\n\n")
            f.write(f"**実施日**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**対象**: {root_dir}\n\n")
            
            f.write("## 統計サマリー\n\n")
            f.write(f"- 総ファイル数: {stats['total']}\n")
            f.write(f"- 更新対象: {stats['updated']}\n")
            f.write(f"- 変更不要: {stats['no_changes']}\n")
            f.write(f"- タグなし: {stats['no_tags']}\n")
            f.write(f"- フロントマターなし: {stats['no_frontmatter']}\n")
            f.write(f"- エラー: {stats['errors']}\n\n")
            
            if changes:
                f.write("## 変更詳細\n\n")
                for change in changes:
                    f.write(f"### {change['file']}\n\n")
                    f.write("**変更前**:\n```yaml\n")
                    for tag in change['old_tags']:
                        f.write(f'  - "{tag}"\n')
                    f.write("```\n\n")
                    f.write("**変更後**:\n```yaml\n")
                    for tag in change['new_tags']:
                        f.write(f'  - "{tag}"\n')
                    f.write("```\n\n")
            
            f.write("## 実行方法\n\n")
            f.write("変更を適用するには:\n```bash\n")
            f.write("python3 /Users/remma/project/scripts/tag_standardizer.py\n")
            f.write("```\n")
        
        print(f"\n✅ Report saved to: {report_path}")
    else:
        print(f"\n✅ Tag standardization complete!")
    
    print("=" * 80)


if __name__ == '__main__':
    main()
