Neodoo Rulebook (v0)

Objetivo: fixar as regras mínimas que a LLM deve seguir ao propor/gerar código para o neodoo.

- Manifestos: usar ast.literal_eval-friendly; chaves padrão, sem comentários inline.
- Python (models):
  - UTF-8, _name, _description obrigatórios; naming claro.
  - @api.depends em fields compute; evitar print/pdb/breakpoint.
  - ensure_one em ações/botões; sem side-effects em onchange.
  - Convenções de nomes e módulos conforme standards Odoo 18+.
- XML (views):
  - Usar <list> em vez de <tree>; view_mode deve incluir "list,form".
  - IDs estáveis, sem conflito; dados de segurança separados.
- Validator: sempre fazer passar o validator estrito do projeto antes de abrir PR.
- Templates: preferir templates/base do repositório; placeholders devidamente renomeados.
- Documentação: atualizar README/guides quando houver mudança de comportamento.
- Segurança/licença: respeitar licenças OCA; preferir adaptações a cópias extensas.
