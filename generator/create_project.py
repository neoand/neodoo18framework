#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neodoo18Framework Project Generator
Creates new Odoo 18+ projects with proper structure and compliance
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

class ProjectGenerator:
    """Generate new Odoo 18+ projects from templates"""
    
    def __init__(self):
        self.framework_root = Path(__file__).parent.parent
        self.templates_dir = self.framework_root / 'templates'
        
    def create_project(self, name: str, project_type: str = 'minimal', output_dir: str = None):
        """Create a new project from template"""
        
        # Validate inputs
        if not name.isidentifier():
            raise ValueError(f"Invalid project name: {name}")
            
        template_path = self.templates_dir / f"{project_type}-project"
        
        if not template_path.exists():
            available = [d.name.replace('-project', '') for d in self.templates_dir.glob('*-project')]
            raise ValueError(f"Template '{project_type}' not found. Available: {', '.join(available)}")
        
        # Determine output directory
        if output_dir is None:
            output_dir = Path.cwd() / name
        else:
            output_dir = Path(output_dir) / name
            
        if output_dir.exists():
            raise ValueError(f"Directory already exists: {output_dir}")
        
        print(f"🚀 Creating project '{name}' using '{project_type}' template...")
        
        # Copy template
        shutil.copytree(template_path, output_dir)
        
        # Customize project
        self._customize_project(output_dir, name, project_type)
        
        print(f"✅ Project created successfully!")
        print(f"📁 Location: {output_dir}")
        print(f"\n🔄 Next steps:")
        print(f"   cd {output_dir}")
        print(f"   ./init_project.sh")
        print(f"   python -m framework.validator .")
        
        return output_dir
    
    def _customize_project(self, project_dir: Path, name: str, project_type: str):
        """Customize the copied template with project-specific values"""
        
        replacements = {
            '{{PROJECT_NAME}}': name,
            '{{PROJECT_TYPE}}': project_type,
            '{{CREATION_DATE}}': datetime.now().strftime('%Y-%m-%d'),
            '{{FRAMEWORK_VERSION}}': '1.0.0'
        }
        
        # Files to process
        files_to_process = [
            'README.md',
            '__manifest__.py',
            'models/__init__.py'
        ]
        
        for file_rel_path in files_to_process:
            file_path = project_dir / file_rel_path
            
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                
                for placeholder, replacement in replacements.items():
                    content = content.replace(placeholder, replacement)
                
                file_path.write_text(content, encoding='utf-8')
        
        # Make scripts executable
        for script in ['init_project.sh', 'validate_odoo18.sh']:
            script_path = project_dir / script
            if script_path.exists():
                os.chmod(script_path, 0o755)
    
    def list_templates(self):
        """List available project templates"""
        templates = []
        
        for template_dir in self.templates_dir.glob('*-project'):
            template_name = template_dir.name.replace('-project', '')
            
            # Read template info if available
            info_file = template_dir / 'TEMPLATE_INFO.md'
            description = "No description available"
            
            if info_file.exists():
                content = info_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                if lines and lines[0].startswith('# '):
                    description = lines[0][2:].strip()
            
            templates.append({
                'name': template_name,
                'description': description,
                'path': template_dir
            })
        
        return templates

def main():
    """CLI interface for project generator"""
    parser = argparse.ArgumentParser(
        description="Neodoo18Framework Project Generator",
        epilog="Example: python create_project.py --name=my_crm --type=minimal"
    )
    
    parser.add_argument('--name', required=True, help='Project name (must be valid Python identifier)')
    parser.add_argument('--type', default='minimal', help='Project template type (default: minimal)')
    parser.add_argument('--output', help='Output directory (default: current directory)')
    parser.add_argument('--list-templates', action='store_true', help='List available templates')
    
    args = parser.parse_args()
    
    generator = ProjectGenerator()
    
    if args.list_templates:
        print("📦 Available Project Templates:")
        print("=" * 50)
        
        templates = generator.list_templates()
        
        for template in templates:
            print(f"• {template['name']}: {template['description']}")
        
        return
    
    try:
        project_dir = generator.create_project(
            name=args.name,
            project_type=args.type,
            output_dir=args.output
        )
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()