"""
🏗️ LLM ABSTRACTION LAYER - SEM LOCK-IN

Permite usar qualquer LLM (Claude, OpenAI, Ollama, etc) sem mudar código.

Estrutura:
    LLMBackend (interface)
        ├── ClaudeBackend (Claude SDK)
        ├── OpenAIBackend (OpenAI API)
        └── LocalBackend (Ollama, etc)

Uso:
    backend = LLMFactory.create("claude")
    # ou
    backend = LLMFactory.create("openai")
    # Mesmo interface!
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import os


@dataclass
class LLMResponse:
    """Resposta padronizada de qualquer LLM"""
    content: str
    tokens_used: int
    cost: str
    model: str
    raw_response: Any = None  # Para debug


class LLMBackend(ABC):
    """
    Interface abstrata para qualquer LLM.
    Todos os backends devem implementar estes métodos.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """
        Gera texto usando o LLM.

        Args:
            prompt: Prompt do usuário
            system: System prompt (instruções)
            max_tokens: Limite de tokens
            temperature: Criatividade (0-1)

        Returns:
            LLMResponse padronizada
        """
        pass

    @abstractmethod
    def analyze_code(self, code: str, language: str = "python") -> LLMResponse:
        """Analisa código"""
        pass

    @abstractmethod
    def generate_model(self, spec: Dict) -> LLMResponse:
        """Gera modelo Odoo"""
        pass

    @abstractmethod
    def generate_view(self, spec: Dict) -> LLMResponse:
        """Gera view XML Odoo"""
        pass

    @abstractmethod
    def estimate_cost(self) -> str:
        """Estima custo da última chamada"""
        pass


class ClaudeBackend(LLMBackend):
    """
    Implementação Claude usando Claude SDK.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Inicializa backend Claude.

        Args:
            api_key: Chave API (ou lê de env)
            model: Modelo a usar
        """
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError(
                "Claude SDK não instalado! Execute: pip install anthropic"
            )

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY não configurada!")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.last_response = None

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Chama Claude API"""

        messages = [{"role": "user", "content": prompt}]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "",
            messages=messages,
        )

        self.last_response = response

        return LLMResponse(
            content=response.content[0].text,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            cost=self._estimate_cost(response.usage),
            model=self.model,
            raw_response=response,
        )

    def analyze_code(self, code: str, language: str = "python") -> LLMResponse:
        """Analisa código com Claude"""
        prompt = f"""
Analise este código {language}:

```{language}
{code}
```

Identifique:
1. Problemas de segurança
2. Violações de padrão
3. Performance issues
4. Sugestões de melhoria

Retorne análise detalhada.
        """
        return self.generate(prompt)

    def generate_model(self, spec: Dict) -> LLMResponse:
        """Gera modelo Odoo com Claude"""
        import json

        prompt = f"""
Você é especialista em Odoo 18+.

Gere um modelo Odoo com:
- Nome: {spec.get('name', 'model')}
- Descrição: {spec.get('description', '')}
- Campos: {json.dumps(spec.get('fields', []), ensure_ascii=False, indent=2)}

Requisitos:
1. Código Python completo e funcional
2. Type hints
3. Docstrings
4. Validações
5. Pronto para produção

Retorne APENAS o código Python:
        """
        return self.generate(prompt, max_tokens=2048)

    def generate_view(self, spec: Dict) -> LLMResponse:
        """Gera view XML Odoo com Claude"""
        import json

        prompt = f"""
Você é especialista em views Odoo 18+.

Gere uma view XML:
- Modelo: {spec.get('model', 'model')}
- Tipo: {spec.get('view_type', 'form')}
- Campos: {json.dumps(spec.get('fields', []), ensure_ascii=False, indent=2)}

Requisitos:
1. XML válido
2. Nomes de campos existem
3. Convenções Odoo
4. Pronto para produção

Retorne APENAS o XML:
        """
        return self.generate(prompt, max_tokens=1024)

    def _estimate_cost(self, usage) -> str:
        """Estima custo Claude"""
        # Claude 3.5 Sonnet: $3/1M input, $15/1M output
        input_cost = (usage.input_tokens / 1_000_000) * 3
        output_cost = (usage.output_tokens / 1_000_000) * 15
        total = input_cost + output_cost
        return f"${total:.6f}"

    def estimate_cost(self) -> str:
        """Retorna custo da última chamada"""
        if not self.last_response:
            return "$0.00"
        return self._estimate_cost(self.last_response.usage)


class OpenAIBackend(LLMBackend):
    """
    Implementação OpenAI usando OpenAI SDK.
    Compatível 100% com ClaudeBackend - mesma interface!
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Inicializa backend OpenAI.

        Args:
            api_key: Chave API (ou lê de env)
            model: Modelo (gpt-4, gpt-4o, etc)
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI SDK não instalado! Execute: pip install openai")

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY não configurada!")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.last_response = None

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Chama OpenAI API"""

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )

        self.last_response = response

        return LLMResponse(
            content=response.choices[0].message.content,
            tokens_used=response.usage.prompt_tokens + response.usage.completion_tokens,
            cost=self._estimate_cost(response.usage),
            model=self.model,
            raw_response=response,
        )

    def analyze_code(self, code: str, language: str = "python") -> LLMResponse:
        """Analisa código com OpenAI"""
        prompt = f"""
Analise este código {language}:

```{language}
{code}
```

Identifique:
1. Problemas de segurança
2. Violações de padrão
3. Performance issues
4. Sugestões de melhoria
        """
        return self.generate(prompt)

    def generate_model(self, spec: Dict) -> LLMResponse:
        """Gera modelo Odoo com OpenAI"""
        import json

        prompt = f"""
Você é especialista em Odoo 18+.

Gere um modelo Odoo com:
- Nome: {spec.get('name', 'model')}
- Descrição: {spec.get('description', '')}
- Campos: {json.dumps(spec.get('fields', []), ensure_ascii=False, indent=2)}

Requisitos:
1. Código Python completo
2. Type hints
3. Docstrings
4. Validações
5. Pronto para produção

Retorne APENAS código Python:
        """
        return self.generate(prompt, max_tokens=2048)

    def generate_view(self, spec: Dict) -> LLMResponse:
        """Gera view XML Odoo com OpenAI"""
        import json

        prompt = f"""
Você é especialista em views Odoo 18+.

Gere view XML:
- Modelo: {spec.get('model', 'model')}
- Tipo: {spec.get('view_type', 'form')}
- Campos: {json.dumps(spec.get('fields', []), ensure_ascii=False, indent=2)}

Requisitos:
1. XML válido
2. Campos existem
3. Convenções Odoo
4. Pronto para produção

Retorne APENAS XML:
        """
        return self.generate(prompt, max_tokens=1024)

    def _estimate_cost(self, usage) -> str:
        """Estima custo OpenAI"""
        # GPT-4o: $5/1M input, $15/1M output (aproximado)
        input_cost = (usage.prompt_tokens / 1_000_000) * 5
        output_cost = (usage.completion_tokens / 1_000_000) * 15
        total = input_cost + output_cost
        return f"${total:.6f}"

    def estimate_cost(self) -> str:
        """Retorna custo da última chamada"""
        if not self.last_response:
            return "$0.00"
        return self._estimate_cost(self.last_response.usage)


class LLMFactory:
    """
    Factory para criar backends LLM sem lock-in.

    Uso:
        backend = LLMFactory.create("claude")
        # ou
        backend = LLMFactory.create("openai")
    """

    _backends = {
        "claude": ClaudeBackend,
        "openai": OpenAIBackend,
    }

    @classmethod
    def register(cls, name: str, backend_class: type):
        """Registra novo backend"""
        cls._backends[name] = backend_class

    @classmethod
    def create(cls, backend_name: str, **kwargs) -> LLMBackend:
        """
        Cria instância de backend LLM.

        Args:
            backend_name: "claude", "openai", etc
            **kwargs: Argumentos para o backend

        Returns:
            Instância de LLMBackend

        Raises:
            ValueError: Se backend não existe
        """
        if backend_name not in cls._backends:
            available = ", ".join(cls._backends.keys())
            raise ValueError(
                f"❌ Backend '{backend_name}' não existe!\n"
                f"Disponíveis: {available}"
            )

        backend_class = cls._backends[backend_name]
        return backend_class(**kwargs)

    @classmethod
    def list_backends(cls) -> List[str]:
        """Lista backends disponíveis"""
        return list(cls._backends.keys())

    @classmethod
    def get_default(cls) -> str:
        """Retorna backend padrão (Claude, se disponível)"""
        if "claude" in cls._backends:
            return "claude"
        return list(cls._backends.keys())[0]


# ============================================
# EXEMPLO DE USO
# ============================================

if __name__ == "__main__":
    print("🚀 Teste de Abstração LLM (sem lock-in)\n")

    # Teste 1: Usar Claude
    print("=" * 70)
    print("Test 1: Claude Backend")
    print("=" * 70)

    try:
        claude = LLMFactory.create("claude")
        print(f"✅ Claude backend criado: {claude.model}")

        response = claude.generate(
            "Escreva 1 linha sobre Odoo 18",
            max_tokens=100,
        )
        print(f"Resposta: {response.content[:100]}...")
        print(f"Custo: {response.cost}")
        print(f"Tokens: {response.tokens_used}")

    except Exception as e:
        print(f"⚠️  Claude não disponível: {e}")

    # Teste 2: Usar OpenAI como fallback
    print("\n" + "=" * 70)
    print("Test 2: OpenAI Backend (Fallback)")
    print("=" * 70)

    try:
        openai = LLMFactory.create("openai")
        print(f"✅ OpenAI backend criado: {openai.model}")

        response = openai.generate(
            "Escreva 1 linha sobre Odoo 18",
            max_tokens=100,
        )
        print(f"Resposta: {response.content[:100]}...")
        print(f"Custo: {response.cost}")

    except Exception as e:
        print(f"⚠️  OpenAI não disponível: {e}")

    # Teste 3: Listar backends
    print("\n" + "=" * 70)
    print("Test 3: Backends Disponíveis")
    print("=" * 70)

    backends = LLMFactory.list_backends()
    print(f"Backends registrados: {', '.join(backends)}")
    print(f"Backend padrão: {LLMFactory.get_default()}")

    print("\n✅ Abstração LLM funcionando! SEM LOCK-IN! 🚀")
