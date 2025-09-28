# 🚀 Guía Completa: Neodoo18Framework

> **Framework Universal para Desarrollo Odoo 18+ con Sistema SOIL**Gestionar
```bash
./neodoo list
./neodoo delete
./neodoo run                            # ejecutar proyecto en directorio actual
./neodoo run --path /ruta/del/proyecto  # ejecutar proyecto especifico
./neodoo doctor                         # revisar env (python, git, puertos)
./neodoo doctor --path /ruta/del/proyecto **ÍNDICE**

1. [Instalación Rápida](#instalación-rápida)
2. [Primer Proyecto](#primer-proyecto)  
3. [Desarrollo con IA](#desarrollo-con-ia)
4. [Estándares Obligatorios](#estándares-obligatorios)
5. [Validación Automática](#validación-automática)
6. [Ejemplos Prácticos](#ejemplos-prácticos)
7. [Integración con Odoo](#integración-con-odoo)
8. [Solución de Problemas](#solución-de-problemas)
# 🚀 Guía Completa: Neodoo18Framework

> Framework universal para Odoo 18+ con SOIL y un CLI de un solo comando.

## 📚 Índice

1. Inicio Rápido (recomendado)
2. Anatomía del Proyecto
3. Flujos Clave (crear, gestionar, validar)
4. Estándares Odoo 18+ obligatorios
5. Modos del Validador: strict y template-mode
6. Desarrollo con IA (LLM)
7. Update y Doctor
8. Troubleshooting y Checklist

---

## ⚡ Inicio Rápido (30s)

> [!tip]
> El nuevo CLI es el camino más rápido. Los scripts heredados existen, pero el CLI ofrece la mejor DX.

```bash
# 1) Clonar
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# 2) Crear un proyecto Odoo 18+ completo (asistente)
./neodoo create

# 3) Ejecutar
cd ~/odoo_projects/<tu_proyecto>
./run.sh
```

No interactivo (reproducible) desde config:
```bash
./neodoo create --from-config /ruta/a/.neodoo.yml
```

Ejemplo mínimo de .neodoo.yml
```yaml
version: 1
name: mi_proyecto_odoo18
base_dir: ~/odoo_projects
module: mi_modulo
template: minimal
venv: true
odoo_branch: 18.0
```

También puedes usar el ejemplo compartido directamente:
```bash
./neodoo create --from-config ./docs/.neodoo.yml
```

> [!note]
> El CLI genera: Odoo source, OCA/web, custom_addons, venv (opcional), odoo.conf y run.sh.

---

## 🏗 Anatomía del Proyecto

```
~/odoo_projects/tu_proyecto/
├── odoo_source/           # Código fuente de Odoo 18+ (git clone)
├── community_addons/      # Módulos OCA (incluye web)
│   └── web/
├── custom_addons/         # Tus módulos
├── .venv/                 # Entorno Python aislado (opcional)
├── odoo.conf              # Preconfigurado para dev
├── run.sh                 # Inicia Odoo
└── .neodoo.yml            # Config del proyecto (para create reproducible)
```

> [!example]
> Ejecuta el validador sobre tu carpeta de módulos custom:
> 
> ```bash
> python framework/validator/validate.py ~/odoo_projects/tu_proyecto/custom_addons --strict --auto-fix
> ```

---

## 🔁 Flujos Clave

Crear
```bash
./neodoo create                         # asistente
./neodoo create --from-config .neodoo.yml  # reproducible
```

Gestionar
```bash
./neodoo list
./neodoo delete
./neodoo doctor                         # verifica entorno (python, git, puertos)
./neodoo doctor --path /ruta/al/proyecto
./neodoo update --path /ruta/al/proyecto  # pull repos + actualizar deps
```

Validar (cumplimiento Odoo 18+)
```bash
# Desde la raíz del repo
python framework/validator/validate.py ruta/al/modulo --strict --auto-fix
python framework/validator/validate.py templates/minimal --template-mode --auto-fix
```

---

## � OCA Watch y Rollups Semanales

Mantente al día con el ecosistema OCA directamente desde este repo:

- Digests diarios: el workflow “OCA Watch” monitorea repos OCA seleccionados y escribe resúmenes en `docs/oca-digests/`. Cuando hay novedades, abre un PR con etiquetas/asignación automáticas y auto‑merge habilitado.
- Rollups semanales: cada lunes (03:00 UTC), el workflow “OCA Weekly Rollup” agrega los últimos 7 días en `docs/oca-digests/rollups/YYYY-Www.md`.

Ejecución manual:
- En la pestaña Actions de GitHub, ejecuta “OCA Watch” (opcionalmente con bootstrap en la primera ejecución) o “OCA Weekly Rollup”.

Más info: ver `docs/oca-digests/README.md`.

---

## �📏 Estándares Odoo 18+ obligatorios

> [!warning]
> Nunca uses <tree>. Usa siempre <list>. Las acciones deben declarar view_mode="list,form".

XML (correcto)
```xml
<record id="book_view_list" model="ir.ui.view">
  <field name="name">book.view.list</field>
  <field name="model">bjj.book</field>
  <field name="arch" type="xml">
    <list string="Libros">
      <field name="title"/>
      <field name="author"/>
    </list>
  </field>
</record>

<record id="book_action" model="ir.actions.act_window">
  <field name="name">Libros</field>
  <field name="res_model">bjj.book</field>
  <field name="view_mode">list,form</field>
</record>
```

Python (modelo básico)
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Book(models.Model):
    _name = 'bjj.book'
    _description = 'Libro de Biblioteca'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(required=True, tracking=True)
    author = fields.Char(required=True)
    isbn = fields.Char(size=13)

    @api.constrains('isbn')
    def _check_isbn(self):
        for rec in self:
            if rec.isbn and len(rec.isbn) != 13:
                raise ValidationError(_('El ISBN debe tener 13 dígitos'))
```

---

## 🧪 Modos del Validador

> [!info]
> strict: promueve algunos avisos a errores para proyectos de usuario.
> 
> template-mode: mantiene placeholders/cosméticos como avisos en plantillas, manteniendo las reglas críticas de Odoo 18+ como errores.

Ejemplos
```bash
# Strict (recomendado para módulos reales)
python framework/validator/validate.py mi_modulo --strict --auto-fix

# Template (permisivo para placeholders)
python framework/validator/validate.py templates/advanced --template-mode --auto-fix
```

---

## 🤖 Desarrollo con IA

> [!tip]
> Empieza por: framework/standards/ODOO18_CORE_STANDARDS.md y framework/standards/SOIL_CORE.md.

Contexto
```bash
cat framework/standards/ODOO18_CORE_STANDARDS.md
cat framework/standards/SOIL_CORE.md
```

Prompt inicial
```
Crea un módulo Biblioteca siguiendo Odoo 18+:
- Modelo: bjj.book (title, author, isbn, category)
- Vistas: list + form (sin tree)
- Acción: view_mode="list,form"
- Seguridad: access.csv básico
Luego ejecuta: python framework/validator/validate.py <path> --strict --auto-fix
```

---

## 🔄 Update y 🩺 Doctor

```bash
./neodoo doctor                         # verifica python3, git, docker/psql y puertos 8069/8072
./neodoo doctor --path /proyecto        # también verifica odoo_source, addons y venv

./neodoo update --path /proyecto        # git pull Odoo + OCA/web y actualizar deps del venv
```

> [!success]
> Usa doctor antes de iniciar y después de updates para detectar conflictos de puertos y herramientas faltantes.

---

## � CI & Sanity Checks

Este repositorio incluye verificaciones automáticas para mantener sólida la experiencia del desarrollador:

- Verificaciones rápidas (CI, en push/PR):
  - Lista plantillas del generador
  - Genera un módulo minimal (offline)
  - Valida el módulo generado con el validador en modo strict

- Prueba smoke (manual):
  - Activa el workflow "CI" con "Run workflow" (workflow_dispatch)
  - Ejecuta `scripts/dev/quick_sanity.sh` que realiza un flujo completo end-to-end (clona Odoo y OCA/web)

Ejecución local del sanity:

```bash
# Desde la raíz del repo
bash scripts/dev/quick_sanity.sh

# O paso a paso
python3 framework/generator/create_project.py --name tmp --list-templates
./neodoo create --name sanity_proj --base-dir /tmp/neodoo_sanity --module sanity_mod --template minimal --no-venv
./neodoo doctor --path /tmp/neodoo_sanity/sanity_proj
python3 framework/validator/validate.py /tmp/neodoo_sanity/sanity_proj/custom_addons/sanity_mod --strict --auto-fix
```

Notas:
- La plantilla "minimal" genera un módulo que pasa la validación strict por defecto.
- Los nombres de archivo con placeholders se renombran automáticamente durante la generación.

---

## �🧯 Troubleshooting

> [!failure] Invalid view mode 'tree'
```bash
python framework/validator/validate.py mi_modulo --auto-fix
```

> [!question] Module not found
```bash
ls mi_modulo/__init__.py
cat mi_modulo/models/__init__.py  # verifica los imports
```

> [!warning] Access rights
```bash
ls mi_modulo/security/
grep "group_" mi_modulo/security/*.xml || true
```

---

## ✅ Checklist de Calidad

- [ ] Validador pasa (strict) sin errores
- [ ] XML usa <list>, acciones usan "list,form"
- [ ] Modelos con _description y constraints básicas
- [ ] Seguridad: ir.model.access.csv presente y listado en el manifest
- [ ] README y pruebas mínimas presentes

> [!tip]
> Para plantillas, valida con --template-mode para evitar ruido de placeholders manteniendo los problemas reales visibles.
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