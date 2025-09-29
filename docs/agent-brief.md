# Agent Brief

_Gerado em 2025-09-29 11:13:38 CST_

## Projeto
- Nome: semprereal
- Caminho: /Users/andersongoliveira/odoo_projects/semprereal
- Target validator: /Users/andersongoliveira/odoo_projects/semprereal/custom_addons

## Comandos Executados
- `NEODOO_SKIP_PAUSE=1 /Users/andersongoliveira/odoo_projects/neodoo18framework/neodoo doctor --path /Users/andersongoliveira/odoo_projects/semprereal`
- `python3 /Users/andersongoliveira/odoo_projects/neodoo18framework/framework/validator/validate.py /Users/andersongoliveira/odoo_projects/semprereal/custom_addons --strict --auto-fix`
- `python3 /Users/andersongoliveira/odoo_projects/neodoo18framework/framework/validator/validate.py /Users/andersongoliveira/odoo_projects/semprereal/custom_addons --plugins-dir /Users/andersongoliveira/odoo_projects/neodoo18framework/corporate_plugins --strict`

## Resumo Doctor
```

╔═══════════════════════════════════════════════════════════════════════════════╗
║                          🚀 NEODOO18 FRAMEWORK                               ║
║                    Odoo 18+ Development Made Easy & Beautiful                ║
║                                                                               ║
║                        By NeoAnd for you with ❤️                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    

🔧 Verificando ambiente de desenvolvimento...

🔍 Ferramentas essenciais:
✅    python3: Encontrado
✅    git: Encontrado
✅    psql: Encontrado
✅    docker: Encontrado

🌐 Portas de rede:
✅    Porta 8069: Livre
✅    Porta 8072: Livre

📁 Verificando projeto: semprereal
✅    Código fonte do Odoo: OK
✅    Módulos customizados: OK
✅    Módulos da comunidade: OK
✅    Arquivo de configuração: OK
✅    Script de execução: OK
✅    Ambiente virtual Python: OK

──────────────────────────────────────────────────
✅ 
✅ Ambiente saudável! Tudo pronto para desenvolvimento.

By NeoAnd for you with ❤️
```

## Resumo Validator
```
WARNING: Validation passed with 18 warnings
INFO: ✅ Validation successful!
```

## Resumo Corporate Plugins
```
ERROR: Validation failed: 4 errors, 29 warnings
ERROR:   - Módulo 'custom_addons' deve ter prefixo corporativo 'acme_'
WARNING:   - Manifest deve incluir 'AcmeCorp' como autor em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/neodoo_ai/__manifest__.py
WARNING:   - Considere usar categoria corporativa 'AcmeCorp/...' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/neodoo_ai/__manifest__.py
ERROR:   - Model 'ai.generator.mixin' deve ter prefixo corporativo 'acme_' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/neodoo_ai/models/ai_generator_mixin.py
WARNING:   - XML record id 'res_config_settings_view_form_hf' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/neodoo_ai/views/hf_settings_views.xml)
WARNING:   - XML record id 'hf_api_token_param' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/neodoo_ai/views/hf_settings_views.xml)
WARNING:   - XML record id 'hf_model_param' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/neodoo_ai/views/hf_settings_views.xml)
WARNING:   - XML record id 'use_huggingface_api_param' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/neodoo_ai/views/hf_settings_views.xml)
WARNING:   - View ID 'res_config_settings_view_form_hf' deve ter prefixo corporativo 'acme_' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/neodoo_ai/views/hf_settings_views.xml
ERROR:   - Módulo 'custom_addons' deve ter prefixo corporativo 'acme_'
WARNING:   - XML record id 'template_model_demo_1' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/demo/demo_data.xml)
WARNING:   - XML record id 'template_model_demo_2' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/demo/demo_data.xml)
WARNING:   - XML record id 'template_model_demo_3' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/demo/demo_data.xml)
WARNING:   - Method action_confirm should call self.ensure_one() in /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/models/template_model.py
WARNING:   - Method action_done should call self.ensure_one() in /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/models/template_model.py
WARNING:   - Method action_draft should call self.ensure_one() in /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/models/template_model.py
ERROR:   - Model 'template.model' deve ter prefixo corporativo 'acme_' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/models/template_model.py
WARNING:   - Método 'action_confirm' deve ter docstring descritivo em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/models/template_model.py
WARNING:   - Método 'action_done' deve ter docstring descritivo em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/models/template_model.py
WARNING:   - Método 'action_draft' deve ter docstring descritivo em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/models/template_model.py
WARNING:   - Arquivo de segurança deve usar grupos corporativos 'acme_*' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/security/ir.model.access.csv
WARNING:   - XML record id 'group_template_user' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/security/security.xml)
WARNING:   - XML record id 'group_template_manager' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/security/security.xml)
WARNING:   - XML record id 'rule_template_model_user' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/security/security.xml)
WARNING:   - XML record id 'rule_template_model_manager' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/security/security.xml)
WARNING:   - XML record id 'view_template_model_list' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/views/views.xml)
WARNING:   - XML record id 'view_template_model_form' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/views/views.xml)
WARNING:   - XML record id 'view_template_model_search' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/views/views.xml)
WARNING:   - XML record id 'action_template_model' should be prefixed with 'custom_addons_' (/Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/views/views.xml)
WARNING:   - View ID 'view_template_model_list' deve ter prefixo corporativo 'acme_' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/views/views.xml
WARNING:   - View ID 'view_template_model_form' deve ter prefixo corporativo 'acme_' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/views/views.xml
WARNING:   - View ID 'view_template_model_search' deve ter prefixo corporativo 'acme_' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/views/views.xml
WARNING:   - Action ID 'action_template_model' deve ter prefixo corporativo 'acme_' em /Users/andersongoliveira/odoo_projects/semprereal/custom_addons/semprereal/views/views.xml
ERROR: ❌ Validation failed!
```

> Atualize este arquivo sempre que novos problemas ou correções forem relevantes para agentes.
