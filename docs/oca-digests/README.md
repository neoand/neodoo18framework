Este diretório guarda resumos práticos da OCA (por repositório/tema): padrões úteis, pitfalls e referências para o neodoo.

Atualização automática
- Um workflow do GitHub (OCA Watch) roda o script `scripts/oca_watch.py --update` e cria PRs com alterações em:
	- `docs/oca-digests/` (novos itens por repositório)
	- `.neodoo/oca_state.json` (ponteiros de última versão/commit processado)
- Revisões humanas podem editar e consolidar os digests. O merge do PR mantém o histórico.

Sugestão de arquivos:
- server-tools.md
- connector.md
- web.md
- sale-workflow.md
- project.md
