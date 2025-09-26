#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neodoo18Framework Project Generator
Creates new Odoo 18+ projects with all best practices built-in
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import Dict, Any
import re

class ProjectGenerator:
    """Generates new Odoo 18+ projects from templates"""
    
    def __init__(self):
        self.framework_path = Path(__file__).parent.parent
        self.templates_path = self.framework_path / 'templates'
    
    def create_project(self, name: str, project_type: str = 'minimal', 
                      output_path: str = None, **kwargs) -> bool:
        """Create a new project from template"""
        
        # Validate inputs
        if not self._validate_name(name):
            print(f"❌ Invalid project name: {name}")
            print("Name should contain only letters, numbers, and underscores")
            return False
        
        template_path = self.templates_path / f'{project_type}-project'
        if not template_path.exists():
            print(f"❌ Template not found: {project_type}")
            self._list_available_templates()
            return False
        
        # Determine output path
        if output_path is None:
            output_path = Path.cwd() / name
        else:
            output_path = Path(output_path) / name
        
        if output_path.exists():
            print(f"❌ Directory already exists: {output_path}")
            return False
        
        # Generate template variables
        variables = self._generate_variables(name, **kwargs)
        
        print(f"🚀 Creating {project_type} project: {name}")
        print(f"📁 Output path: {output_path}")
        
        # Copy and process template
        try:
            self._copy_template(template_path, output_path, variables)
            self._post_process_project(output_path, variables)
            
            print("✅ Project created successfully!")
            print(f"\n📋 Next steps:")
            print(f"   cd {output_path}")
            print(f"   # Review and customize the generated files")
            print(f"   # Initialize your Odoo development environment")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating project: {e}")
            if output_path.exists():
                shutil.rmtree(output_path)
            return False
    
    def _validate_name(self, name: str) -> bool:
        """Validate project name"""
        return re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name) is not None
    
    def _generate_variables(self, name: str, **kwargs) -> Dict[str, str]:
        """Generate template variables"""
        
        # Convert name to different formats
        technical_name = name.lower()
        class_name = ''.join(word.capitalize() for word in name.split('_'))
        display_name = name.replace('_', ' ').title()
        
        variables = {
            'MODULE_NAME': kwargs.get('display_name', display_name),
            'MODULE_TECHNICAL_NAME': technical_name,
            'MODULE_CLASS': class_name,
            'MODEL_NAME': kwargs.get('model_name', 'item'),
            'MODEL_DESCRIPTION': kwargs.get('model_description', f'{display_name} Item'),
            'CATEGORY': kwargs.get('category', 'Operations'),
            'SUMMARY': kwargs.get('summary', f'{display_name} management module'),
            'DESCRIPTION': kwargs.get('description', f'Module for managing {display_name.lower()}'),
            'AUTHOR': kwargs.get('author', 'Your Name'),
            'WEBSITE': kwargs.get('website', 'https://yourwebsite.com'),
            'IS_APPLICATION': str(kwargs.get('is_application', False)).lower(),
        }
        
        return variables
    
    def _copy_template(self, template_path: Path, output_path: Path, variables: Dict[str, str]):
        """Copy template files and process variables"""
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Copy all files and directories
        for item in template_path.rglob('*'):
            if item.is_file():
                # Calculate relative path
                rel_path = item.relative_to(template_path)
                
                # Process filename variables
                processed_name = self._process_variables(str(rel_path), variables)
                target_file = output_path / processed_name
                
                # Create parent directories
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Read, process, and write file content
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Process content variables
                    processed_content = self._process_variables(content, variables)
                    
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(processed_content)
                    
                    print(f"   📄 {processed_name}")
                    
                except Exception as e:
                    print(f"   ❌ Error processing {rel_path}: {e}")
                    raise
    
    def _process_variables(self, text: str, variables: Dict[str, str]) -> str:
        """Replace template variables in text"""
        for key, value in variables.items():
            text = text.replace(f'{{{{{key}}}}}', value)
        return text
    
    def _post_process_project(self, output_path: Path, variables: Dict[str, str]):
        """Post-process the generated project"""
        
        # Create additional directories if needed
        dirs_to_create = [
            'static/description',
            'static/img',
            'demo',
            'tests',
            'wizard',
            'report',
        ]
        
        for dir_name in dirs_to_create:
            dir_path = output_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py for Python directories
            if dir_name in ['wizard', 'tests']:
                init_file = dir_path / '__init__.py'
                init_file.write_text('# -*- coding: utf-8 -*-\n')
        
        # Create icon if it doesn't exist
        icon_path = output_path / 'static' / 'description' / 'icon.png'
        if not icon_path.exists():
            # Create a simple placeholder text file
            placeholder = output_path / 'static' / 'description' / 'icon_placeholder.txt'
            placeholder.write_text('Add your module icon here (icon.png)')
        
        # Create README
        readme_path = output_path / 'README.md'
        readme_content = f"""# {variables['MODULE_NAME']}

{variables['DESCRIPTION']}

## Installation

1. Copy this module to your Odoo addons directory
2. Update the app list in Odoo
3. Install the module

## Configuration

Configure the module through Odoo settings.

## Usage

Access the module through the main menu.

## Changelog

### 18.0.1.0.0
- Initial version
"""
        readme_path.write_text(readme_content)
    
    def _list_available_templates(self):
        """List available project templates"""
        print("\n📦 Available templates:")
        for template_dir in self.templates_path.glob('*-project'):
            if template_dir.is_dir():
                template_name = template_dir.name.replace('-project', '')
                print(f"   • {template_name}")

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Neodoo18Framework Project Generator')
    parser.add_argument('name', help='Project name (technical name)')
    parser.add_argument('--type', default='minimal', help='Project type (default: minimal)')
    parser.add_argument('--output', help='Output directory (default: current directory)')
    parser.add_argument('--display-name', help='Display name for the module')
    parser.add_argument('--category', help='Module category')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--website', help='Author website')
    parser.add_argument('--summary', help='Module summary')
    parser.add_argument('--description', help='Module description')
    parser.add_argument('--application', action='store_true', help='Mark as application')
    parser.add_argument('--list-templates', action='store_true', help='List available templates')
    
    args = parser.parse_args()
    
    generator = ProjectGenerator()
    
    if args.list_templates:
        generator._list_available_templates()
        return 0
    
    # Prepare kwargs
    kwargs = {}
    if args.display_name:
        kwargs['display_name'] = args.display_name
    if args.category:
        kwargs['category'] = args.category
    if args.author:
        kwargs['author'] = args.author
    if args.website:
        kwargs['website'] = args.website
    if args.summary:
        kwargs['summary'] = args.summary
    if args.description:
        kwargs['description'] = args.description
    if args.application:
        kwargs['is_application'] = True
    
    success = generator.create_project(
        name=args.name,
        project_type=args.type,
        output_path=args.output,
        **kwargs
    )
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())