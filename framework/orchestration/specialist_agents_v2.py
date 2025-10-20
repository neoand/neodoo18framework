"""
🤖 SPECIALIST AGENTS V2 - SEM LOCK-IN

Agents que usam a abstração LLM - pode trocar de backend facilmente!

Uso:
    backend_config = {
        "provider": "claude",  # ou "openai"
        "api_key": "sk-ant-...",  # opcional (lê de env)
    }

    agent = BackendDeveloperAgent(backend_config)
    result = agent.generate_model(spec)
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from .llm_abstraction import LLMFactory, LLMResponse


class BaseSpecialistAgent(ABC):
    """Classe base para todos os specialists"""

    def __init__(self, backend_config: Dict):
        """
        Inicializa agent com backend LLM.

        Args:
            backend_config: {
                "provider": "claude" ou "openai",
                "api_key": "...",  # opcional
                "model": "..."  # opcional
            }
        """
        provider = backend_config.get("provider", "claude")
        api_key = backend_config.get("api_key")
        model = backend_config.get("model")

        # Cria backend usando factory (SEM LOCK-IN!)
        kwargs = {}
        if api_key:
            kwargs["api_key"] = api_key
        if model:
            kwargs["model"] = model

        self.llm = LLMFactory.create(provider, **kwargs)
        self.provider = provider
        self.backend_config = backend_config

    @abstractmethod
    def execute_task(self, task_spec: Dict) -> Dict:
        """Executa tarefa específica do agent"""
        pass

    def estimate_cost(self) -> str:
        """Retorna custo da última chamada"""
        return self.llm.estimate_cost()


class BackendDeveloperAgent(BaseSpecialistAgent):
    """
    ✅ Backend Developer - Gera modelos Odoo, controllers, workflows
    Agora com execução REAL (não simulação!)
    """

    def execute_task(self, task_spec: Dict) -> Dict:
        """
        Executa tarefa de desenvolvimento backend.

        Args:
            task_spec: {
                'type': 'model' | 'controller' | 'workflow',
                'model_name': 'sale.contract',
                'description': '...',
                'fields': [...]
            }

        Returns:
            Dict com código gerado
        """

        task_type = task_spec.get("type", "model")

        if task_type == "model":
            return self._generate_model(task_spec)
        elif task_type == "controller":
            return self._generate_controller(task_spec)
        elif task_type == "workflow":
            return self._generate_workflow(task_spec)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def _generate_model(self, spec: Dict) -> Dict:
        """Gera modelo Odoo de VERDADE (não simulação!)"""

        response = self.llm.generate_model(
            {
                "name": spec.get("model_name", "my.model"),
                "description": spec.get("description", "Custom model"),
                "fields": spec.get("fields", []),
            }
        )

        return {
            "type": "model",
            "status": "generated",  # ✅ REAL, não 'simulated'!
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "model": response.model,
            "provider": self.provider,
        }

    def _generate_controller(self, spec: Dict) -> Dict:
        """Gera controller Odoo"""

        prompt = f"""
Gere um controller Odoo 18 com:
- Rotas: {spec.get('routes', [])}
- Métodos: {spec.get('methods', [])}

Requisitos:
1. Python válido
2. Type hints
3. Error handling
4. Pronto para produção

Retorne APENAS código Python:
        """

        response = self.llm.generate(prompt, max_tokens=1024)

        return {
            "type": "controller",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }

    def _generate_workflow(self, spec: Dict) -> Dict:
        """Gera workflow Odoo"""

        prompt = f"""
Gere um workflow Odoo 18 com:
- Estados: {spec.get('states', [])}
- Transições: {spec.get('transitions', [])}

Requisitos:
1. XML válido
2. Estados bem definidos
3. Pronto para produção

Retorne APENAS XML:
        """

        response = self.llm.generate(prompt, max_tokens=1024)

        return {
            "type": "workflow",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }


class OWLSpecialistAgent(BaseSpecialistAgent):
    """
    🎨 OWL Specialist - Gera componentes OWL 2.0
    """

    def execute_task(self, task_spec: Dict) -> Dict:
        """
        Executa tarefa de frontend OWL.

        Args:
            task_spec: {
                'type': 'component' | 'template',
                'component_name': '...',
                'props': [...]
            }
        """

        task_type = task_spec.get("type", "component")

        if task_type == "component":
            return self._generate_component(task_spec)
        elif task_type == "template":
            return self._generate_template(task_spec)
        else:
            raise ValueError(f"Unknown OWL task: {task_type}")

    def _generate_component(self, spec: Dict) -> Dict:
        """Gera componente OWL 2.0"""

        prompt = f"""
Gere um componente OWL 2.0 com:
- Nome: {spec.get('component_name', 'MyComponent')}
- Props: {spec.get('props', [])}

Requisitos:
1. JavaScript válido
2. Segue padrões OWL 2.0
3. Type hints JSDoc
4. Pronto para produção

Retorne APENAS código JavaScript:
        """

        response = self.llm.generate(prompt, max_tokens=1500)

        return {
            "type": "component",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }

    def _generate_template(self, spec: Dict) -> Dict:
        """Gera template OWL"""

        prompt = f"""
Gere um template OWL (XML):
- Nome: {spec.get('template_name', 'my-template')}
- Elementos: {spec.get('elements', [])}

Requisitos:
1. XML válido
2. OWL syntax correto
3. Pronto para produção

Retorne APENAS XML:
        """

        response = self.llm.generate(prompt, max_tokens=1024)

        return {
            "type": "template",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }


class SecurityExpertAgent(BaseSpecialistAgent):
    """
    🔐 Security Expert - Gera regras de acesso e segurança
    """

    def execute_task(self, task_spec: Dict) -> Dict:
        """
        Executa tarefa de segurança.

        Args:
            task_spec: {
                'type': 'access_rules' | 'record_rules',
                'model': 'sale.order',
                'groups': ['group_user', 'group_manager']
            }
        """

        task_type = task_spec.get("type", "access_rules")

        if task_type == "access_rules":
            return self._generate_access_rules(task_spec)
        elif task_type == "record_rules":
            return self._generate_record_rules(task_spec)
        else:
            raise ValueError(f"Unknown security task: {task_type}")

    def _generate_access_rules(self, spec: Dict) -> Dict:
        """Gera regras de acesso"""

        prompt = f"""
Gere regras de acesso (ir.model.access) para:
- Modelo: {spec.get('model', 'model')}
- Grupos: {spec.get('groups', [])}

Formato CSV:
id,name,model_id,group_id,perm_read,perm_write,perm_create,perm_unlink

Requisitos:
1. CSV válido
2. Segurança adequada por grupo
3. Pronto para produção

Retorne APENAS CSV:
        """

        response = self.llm.generate(prompt, max_tokens=512)

        return {
            "type": "access_rules",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }

    def _generate_record_rules(self, spec: Dict) -> Dict:
        """Gera regras de registro"""

        prompt = f"""
Gere regras de registro XML (ir.rule) para:
- Modelo: {spec.get('model', 'model')}
- Domínio: {spec.get('domain', [])}

Requisitos:
1. XML válido Odoo
2. Filtros corretos
3. Pronto para produção

Retorne APENAS XML:
        """

        response = self.llm.generate(prompt, max_tokens=512)

        return {
            "type": "record_rules",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }


class DevOpsAgent(BaseSpecialistAgent):
    """
    🚀 DevOps - Deployment, configuração, testes
    """

    def execute_task(self, task_spec: Dict) -> Dict:
        """
        Executa tarefa DevOps.

        Args:
            task_spec: {
                'type': 'dockerfile' | 'tests' | 'deployment',
                'framework': 'Odoo 18',
                'env': 'production'
            }
        """

        task_type = task_spec.get("type", "dockerfile")

        if task_type == "dockerfile":
            return self._generate_dockerfile(task_spec)
        elif task_type == "tests":
            return self._generate_tests(task_spec)
        elif task_type == "deployment":
            return self._generate_deployment(task_spec)
        else:
            raise ValueError(f"Unknown DevOps task: {task_type}")

    def _generate_dockerfile(self, spec: Dict) -> Dict:
        """Gera Dockerfile"""

        prompt = f"""
Gere Dockerfile para:
- Framework: {spec.get('framework', 'Odoo 18')}
- Ambiente: {spec.get('env', 'production')}

Requisitos:
1. Dockerfile válido
2. Best practices
3. Production-ready

Retorne APENAS Dockerfile:
        """

        response = self.llm.generate(prompt, max_tokens=512)

        return {
            "type": "dockerfile",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }

    def _generate_tests(self, spec: Dict) -> Dict:
        """Gera testes"""

        prompt = f"""
Gere testes pytest para:
- Modelo: {spec.get('model', 'model')}
- Casos de teste: {spec.get('test_cases', [])}

Requisitos:
1. Python válido
2. Pytest syntax
3. Coverage >80%
4. Production-ready

Retorne APENAS código Python:
        """

        response = self.llm.generate(prompt, max_tokens=1024)

        return {
            "type": "tests",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }

    def _generate_deployment(self, spec: Dict) -> Dict:
        """Gera guia de deployment"""

        prompt = f"""
Gere guia de deployment para:
- Framework: {spec.get('framework', 'Odoo 18')}
- Alvo: {spec.get('target', 'AWS')}

Requisitos:
1. Markdown bem formatado
2. Passo-a-passo claro
3. Production-ready

Retorne APENAS Markdown:
        """

        response = self.llm.generate(prompt, max_tokens=1024)

        return {
            "type": "deployment",
            "status": "generated",
            "code": response.content,
            "tokens": response.tokens_used,
            "cost": response.cost,
            "provider": self.provider,
        }


# ============================================
# EXEMPLO DE USO (SEM LOCK-IN!)
# ============================================

if __name__ == "__main__":
    print("🚀 Specialist Agents V2 - SEM LOCK-IN\n")

    # Configuração: Pode trocar facilmente!
    config = {
        "provider": "claude",  # ← Troque para "openai" se quiser!
        # "api_key": "sk-ant-...",  # Lê de env se não informar
    }

    print(f"Usando provider: {config['provider']}")
    print()

    # Cria agents
    backend_agent = BackendDeveloperAgent(config)
    owl_agent = OWLSpecialistAgent(config)
    security_agent = SecurityExpertAgent(config)

    # Test 1: Gera modelo
    print("=" * 70)
    print("Test 1: Gerar Modelo")
    print("=" * 70)

    try:
        result = backend_agent.execute_task(
            {
                "type": "model",
                "model_name": "sale.contract",
                "description": "Contrato de venda",
                "fields": [
                    {"name": "numero", "type": "Char"},
                    {"name": "valor", "type": "Float"},
                ],
            }
        )

        print(f"✅ Modelo gerado!")
        print(f"Provider: {result['provider']}")
        print(f"Status: {result['status']}")
        print(f"Tokens: {result['tokens']}")
        print(f"Custo: {result['cost']}")
        print(f"Código (primeiros 200 chars):\n{result['code'][:200]}...")

    except Exception as e:
        print(f"❌ Erro: {e}")

    # Test 2: Gera componente OWL
    print("\n" + "=" * 70)
    print("Test 2: Gerar Componente OWL")
    print("=" * 70)

    try:
        result = owl_agent.execute_task(
            {
                "type": "component",
                "component_name": "ContractForm",
                "props": ["contract", "onSave"],
            }
        )

        print(f"✅ Componente gerado!")
        print(f"Provider: {result['provider']}")
        print(f"Código (primeiros 200 chars):\n{result['code'][:200]}...")

    except Exception as e:
        print(f"❌ Erro: {e}")

    # Test 3: Gera regras de acesso
    print("\n" + "=" * 70)
    print("Test 3: Gerar Regras de Acesso")
    print("=" * 70)

    try:
        result = security_agent.execute_task(
            {
                "type": "access_rules",
                "model": "sale.contract",
                "groups": ["group_user", "group_sale_manager"],
            }
        )

        print(f"✅ Regras geradas!")
        print(f"Código:\n{result['code']}")

    except Exception as e:
        print(f"❌ Erro: {e}")

    print("\n" + "=" * 70)
    print("✅ Agents v2 funcionando! SEM LOCK-IN! 🚀")
    print("=" * 70)
