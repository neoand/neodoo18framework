# 🚀 Guía Completa: Neodoo18Framework

> **Framework Universal para Desarrollo Odoo 18+ con Sistema SOIL**

## 📚 **ÍNDICE**

1. [Instalación Rápida](#instalación-rápida)
2. [Primer Proyecto](#primer-proyecto)  
3. [Desarrollo con IA](#desarrollo-con-ia)
4. [Estándares Obligatorios](#estándares-obligatorios)
5. [Validación Automática](#validación-automática)
6. [Ejemplos Prácticos](#ejemplos-prácticos)
7. [Integración con Odoo](#integración-con-odoo)
8. [Solución de Problemas](#solución-de-problemas)

---

## 🚀 **INSTALACIÓN RÁPIDA**

### 🐍 Método 1: Setup Completo con Entorno Python (RECOMENDADO)
```bash
# 1. Clonar el framework
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# 2. Setup automático del entorno Python
./setup-env.sh
# ✅ Crea virtual environment (.venv/)
# ✅ Instala todas las dependencias Odoo 18+
# ✅ Configura herramientas de desarrollo

# 3. Crear primer proyecto
./activate-env.sh
./quick-start.sh mi_primer_proyecto

# 4. Validar calidad
python3 framework/validator.py mi_primer_proyecto/
# Esperado: 100% compliance ✅
```

### ⚡ Método 2: Proyecto con Entorno Automático
```bash
# Clone + proyecto + entorno en una secuencia
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
./quick-start.sh mi_proyecto --full-setup
```

### 📦 Método 3: Solo Framework (Sin Entorno)
```bash
# Setup básico sin entorno Python
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
chmod +x *.sh
./quick-start.sh mi_proyecto
```

### 🔧 Opciones de Entorno Python:
```bash
# Setup completo del entorno
./setup-env.sh

# Proyecto con virtual environment
./quick-start.sh proyecto --setup-venv

# Proyecto con dependencias Odoo
./quick-start.sh proyecto --install-deps

# Proyecto con setup completo
./quick-start.sh proyecto --full-setup
```

### Verificar Instalación:
```bash
# Framework
python3 framework/validator.py --version
# Esperado: Neodoo18Framework Validator v1.0.0

# Entorno Python (si configurado)
source .venv/bin/activate
python --version
# Esperado: Python 3.8+
```

---

## 🏗️ **PRIMER PROYECTO**

### 🚀 Crear Proyecto Básico en 10 Segundos:
```bash
./quick-start.sh mi_primer_modulo
```

### 🐍 Crear Proyecto con Entorno Python:
```bash
# Con virtual environment
./quick-start.sh mi_proyecto --setup-venv

# Con dependencias Odoo instaladas
./quick-start.sh mi_proyecto --install-deps

# Setup completo (venv + dependencias)
./quick-start.sh mi_proyecto --full-setup
```

### 🔧 Gestionar Entorno Python:
```bash
# Activar entorno
./activate-env.sh

# Verificar estado
source .venv/bin/activate && python -c "import odoo; print('✅ Odoo OK')"

# Desactivar
./deactivate-env.sh
```

### Lo que se Creó:
```
mi_primer_modulo/
├── __init__.py                 # Inicialización Python
├── __manifest__.py             # Configuración Odoo
├── models/                     # Modelos de datos
│   ├── __init__.py
│   └── template_model.py       # Modelo ejemplo
├── views/                      # Interfaces (creadas bajo demanda)
├── security/                   # Control de acceso
├── tests/                      # Pruebas unitarias
├── wizard/                     # Asistentes
├── demo/                       # Datos de demostración
└── README.md                   # Documentación
```

### Verificar Calidad:
```bash
python3 framework/validator.py mi_primer_modulo/
# Esperado: 100% compliance
```

---

## 🤖 **DESARROLLO CON IA**

### Para ChatGPT/Claude/Gemini:

#### 1. Preparar Contexto:
```bash
# Copiar contexto SOIL para la IA
cat framework/SOIL_CORE.md
```

#### 2. Prompt Ejemplo:
```
Usando Neodoo18Framework, desarrolla un módulo de gestión de biblioteca con:

📚 REQUISITOS:
- Modelo: bjj.libro (título, autor, isbn, categoría)
- Vistas: list, form, kanban siguiendo Odoo 18+
- Menú: "Biblioteca" en menú principal
- Seguridad: Reglas básicas de acceso

⚠️ CRÍTICO:
- Usa <list> NUNCA <tree> 
- Usa "list,form" NUNCA "tree,form"
- Validar con: python3 framework/validator.py

📋 BASE:
Usa las plantillas del framework como referencia
```

#### 3. Desarrollar y Validar:
```bash
# Después de que la IA genere el código
python3 framework/validator.py biblioteca/
# Si 100% = ¡listo para producción!
```

---

## ⚠️ **ESTÁNDARES OBLIGATORIOS**

### ✅ Vistas XML (Odoo 18+):
```xml
<!-- CORRECTO -->
<record id="libro_view_tree" model="ir.ui.view">
    <field name="name">libro.view.list</field>
    <field name="model">bjj.libro</field>
    <field name="arch" type="xml">
        <list string="Libros">
            <field name="titulo"/>
            <field name="autor"/>
        </list>
    </field>
</record>

<!-- CORRECTO - Acción -->
<record id="libro_action" model="ir.actions.act_window">
    <field name="name">Libros</field>
    <field name="res_model">bjj.libro</field>
    <field name="view_mode">list,form</field>
</record>
```

### ❌ XML Obsoleto (Odoo ≤17):
```xml
<!-- INCORRECTO - Ya no usar -->
<tree string="Libros">  <!-- Usa <list> -->
    <field name="titulo"/>
</tree>

<!-- INCORRECTO - Acción -->
<field name="view_mode">tree,form</field>  <!-- Usa list,form -->
```

### ✅ Modelos Python:
```python
# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Libro(models.Model):
    _name = 'bjj.libro'
    _description = 'Libro de Biblioteca'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'titulo asc'
    
    titulo = fields.Char(
        string='Título', 
        required=True, 
        tracking=True
    )
    autor = fields.Char(string='Autor', required=True)
    isbn = fields.Char(string='ISBN', size=13)
    
    @api.constrains('isbn')
    def _check_isbn(self):
        for record in self:
            if record.isbn and len(record.isbn) != 13:
                raise ValidationError(_('ISBN debe tener 13 dígitos'))
```

---

## ✅ **VALIDACIÓN AUTOMÁTICA**

### Comando Básico:
```bash
python3 framework/validator.py mi_proyecto/
```

### Salida Ejemplo:
```
🚀 Neodoo18Framework Validator
==================================================

📊 Summary:
   Files checked: 8
   Errors: 0
   Warnings: 0
   Auto-fixes applied: 0
   Average compliance: 100.0%

✅ All checks passed! Ready for production.
```

### Validación con Auto-Corrección:
```bash
python3 framework/validator.py mi_proyecto/ --auto-fix
```

### Validación Detallada:
```bash
python3 framework/validator.py mi_proyecto/ --verbose
```

---

## 💡 **EJEMPLOS PRÁCTICOS**

### Ejemplo 1: E-commerce Simple
```bash
./quick-start.sh tienda_online
cd tienda_online

# Desarrollar con IA usando contexto SOIL
# Resultado: Módulo con productos, categorías, pedidos
```

### Ejemplo 2: CRM Personalizado  
```bash
./quick-start.sh mi_crm
cd mi_crm

# Desarrollar: clientes, oportunidades, actividades
# Validar: python3 ../framework/validator.py .
```

### Ejemplo 3: Sistema Escolar
```bash
./quick-start.sh sistema_escolar
cd sistema_escolar

# Modelos: estudiantes, profesores, clases, notas
# Integración: herencia res.partner
```

---

## 🔗 **INTEGRACIÓN CON ODOO**

### Método 1: Copia Directa
```bash
# Copiar módulo a addons de Odoo
cp -r mi_proyecto /opt/odoo/addons/
sudo chown -R odoo:odoo /opt/odoo/addons/mi_proyecto
sudo systemctl restart odoo
```

### Método 2: Enlace Simbólico (Desarrollo)
```bash
# Crear enlace simbólico
ln -s $(pwd)/mi_proyecto /opt/odoo/addons/
# Reiniciar Odoo
```

### Método 3: Odoo.sh / SaaS
```bash
# Comprimir módulo
zip -r mi_proyecto.zip mi_proyecto/
# Subir vía interfaz Odoo.sh
```

### Activación en Odoo:
1. **Apps** → **Update Apps List**
2. **Buscar**: Nombre de tu módulo  
3. **Install**
4. **Verificar**: El menú aparece en la interfaz

---

## 🛠️ **SOLUCIÓN DE PROBLEMAS**

### ❌ Error: "Invalid view mode 'tree'"
**Solución:**
```bash
python3 framework/validator.py mi_proyecto/ --auto-fix
# Corrige automáticamente tree → list
```

### ❌ Error: "Module not found"  
**Verificar:**
```bash
# 1. ¿Existe __init__.py?
ls mi_proyecto/__init__.py

# 2. ¿Imports correctos?
cat mi_proyecto/models/__init__.py
# Debe contener: from . import nombre_modelo
```

### ❌ Error: "XML Syntax Error"
**Validar XML:**
```bash
python3 framework/xml_validator.py mi_proyecto/views/
```

### ❌ Error: "Access Rights"
**Verificar Seguridad:**
```bash
# 1. ¿Existe ir.model.access.csv?
ls mi_proyecto/security/

# 2. ¿Grupos definidos?
grep "group_" mi_proyecto/security/*.xml
```

---

## 📋 **CHECKLIST DE CALIDAD**

### Antes de Deploy:
- [ ] `python3 framework/validator.py proyecto/` = 100%
- [ ] XML usa `<list>` no `<tree>`  
- [ ] Acciones usan `"list,form"` no `"tree,form"`
- [ ] Modelos heredan `mail.thread`
- [ ] Reglas de seguridad definidas
- [ ] Pruebas básicas creadas
- [ ] README actualizado

### Estructura Mínima:
- [ ] `__manifest__.py` completo
- [ ] `models/__init__.py` con imports
- [ ] `security/ir.model.access.csv`
- [ ] `views/` con menús y acciones
- [ ] Documentación básica

---

## 🚀 **COMANDOS AVANZADOS**

### Análisis de Proyecto:
```bash
# Estadísticas detalladas
python3 framework/analyzer.py mi_proyecto/

# Dependencias
python3 framework/dependency_checker.py mi_proyecto/

# Documentación automática
python3 framework/doc_generator.py mi_proyecto/
```

### Generación Específica:
```bash
# Crear modelo específico
python3 generator/create_model.py --name="Producto" --fields="name:char,price:float"

# Crear vistas para modelo
python3 generator/create_views.py --model="producto" --views="list,form,kanban"

# Crear asistente
python3 generator/create_wizard.py --name="ImportProductos"
```

---

## 📚 **RECURSOS ADICIONALES**

### Documentación Técnica:
- **SOIL_CORE.md**: Guía para LLMs
- **STANDARDS.md**: Estándares Odoo 18+  
- **templates/**: Ejemplos listos
- **framework/**: Herramientas de desarrollo

### Comunidad:
- **GitHub**: https://github.com/neoand/neodoo18framework
- **Issues**: Reportar bugs y sugerencias  
- **Pull Requests**: Contribuciones siempre bienvenidas
- **Discussions**: Ayuda y consejos de la comunidad

### Soporte:
- **Wiki**: Casos de uso avanzados
- **Examples**: Proyectos ejemplo  
- **Updates**: Framework siempre actualizado

---

## 🎯 **CONCLUSIÓN**

**Neodoo18Framework** transforma el desarrollo Odoo de **semanas a minutos**:

✅ **Plantillas Battle-Tested** - Patrones validados en producción  
✅ **100% Odoo 18+ Compliance** - Sin errores de compatibilidad  
✅ **Validación Automática** - Calidad enterprise garantizada  
✅ **IA-Friendly** - Sistema SOIL optimizado para LLMs  
✅ **Open Source** - Licencia MIT, libertad total  

**🚀 ¡Empieza a programar ahora!**

```bash
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework  
./quick-start.sh proyecto_increible
python3 framework/validator.py proyecto_increible/
# 100% = ¡Listo para producción! 🎉
```

---

**¡Happy Coding! 🎯**