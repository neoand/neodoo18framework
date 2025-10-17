/** @odoo-module **/

import { Component, useState, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";

/**
 * ComponentBasicExample
 *
 * Componente básico demonstrando conceitos fundamentais do OWL 2.0:
 * - Props validation (static props)
 * - State management (useState)
 * - Lifecycle hooks
 * - Event handling
 * - Template binding
 *
 * @extends Component
 */
export class ComponentBasicExample extends Component {
    /**
     * setup()
     *
     * Método especial do OWL 2.0 que é chamado ANTES do componente ser renderizado.
     * É aqui que você deve:
     * - Inicializar state com useState
     * - Configurar hooks (onWillStart, onMounted, etc)
     * - Usar services (useService)
     * - Configurar refs (useRef)
     */
    setup() {
        // ===== STATE MANAGEMENT =====
        // useState retorna um proxy reativo. Qualquer mudança no state
        // automaticamente dispara um re-render do componente
        this.state = useState({
            counter: 0,
            isActive: false,
            userName: "",
            items: [],
            loading: false,
        });

        // ===== LIFECYCLE HOOKS =====

        /**
         * onWillStart
         * Executa ANTES do primeiro render, ideal para:
         * - Carregar dados assíncronos
         * - Inicializar state baseado em dados externos
         * - Validar props
         */
        onWillStart(async () => {
            console.log("[BasicExample] Component will start");
            this.state.loading = true;

            // Simula carregamento de dados
            await this._loadInitialData();

            this.state.loading = false;
        });

        /**
         * onMounted
         * Executa DEPOIS do componente ser montado no DOM
         * Ideal para:
         * - Manipulação direta do DOM
         * - Inicializar bibliotecas de terceiros
         * - Focus em elementos
         * - Iniciar timers/intervals
         */
        onMounted(() => {
            console.log("[BasicExample] Component mounted");

            // Exemplo: focar no input quando o componente monta
            const inputElement = this.el.querySelector('input[name="userName"]');
            if (inputElement) {
                inputElement.focus();
            }
        });

        /**
         * onWillUnmount
         * Executa ANTES do componente ser removido do DOM
         * Ideal para:
         * - Cleanup de timers/intervals
         * - Remover event listeners
         * - Cancelar requisições pendentes
         */
        onWillUnmount(() => {
            console.log("[BasicExample] Component will unmount - cleanup time!");

            // Exemplo: limpar um interval se existir
            if (this._intervalId) {
                clearInterval(this._intervalId);
            }
        });
    }

    // ===== PROPS VALIDATION =====
    /**
     * static props
     *
     * No OWL 2.0, props são validadas usando esta propriedade estática.
     * Tipos disponíveis: String, Number, Boolean, Object, Array, Date, Function
     *
     * Configurações:
     * - type: tipo esperado da prop
     * - optional: true/false (padrão: false)
     * - element: true se espera um elemento HTML/Component
     */
    static props = {
        // Props obrigatórias
        title: { type: String },

        // Props opcionais
        subtitle: { type: String, optional: true },
        maxCount: { type: Number, optional: true },
        onSave: { type: Function, optional: true },

        // Props com valores padrão (tratados no getter)
        initialCounter: { type: Number, optional: true },

        // Props complexas
        config: {
            type: Object,
            optional: true,
            // Você pode adicionar shape para validação mais específica
        },

        // Props que podem receber componentes filhos
        slots: { type: Object, optional: true },
    };

    /**
     * static template
     *
     * Define qual template XML será usado para renderizar este componente.
     * O nome deve corresponder ao atributo t-name no arquivo XML.
     */
    static template = "odoo_examples.ComponentBasicExample";

    // ===== GETTERS =====
    /**
     * Getters são úteis para:
     * - Computar valores derivados do state
     * - Aplicar valores padrão a props
     * - Formatar dados para exibição
     */
    get currentCount() {
        return this.state.counter || this.props.initialCounter || 0;
    }

    get displayTitle() {
        return this.props.subtitle
            ? `${this.props.title} - ${this.props.subtitle}`
            : this.props.title;
    }

    get canIncrement() {
        const max = this.props.maxCount || 100;
        return this.state.counter < max;
    }

    get progressPercentage() {
        const max = this.props.maxCount || 100;
        return Math.min((this.state.counter / max) * 100, 100);
    }

    // ===== EVENT HANDLERS =====
    /**
     * Event handlers devem ser arrow functions ou bound functions
     * para manter o contexto correto de 'this'
     */

    /**
     * Incrementa o contador
     * Demonstra atualização simples de state
     */
    onIncrement() {
        if (this.canIncrement) {
            this.state.counter++;
        }
    }

    /**
     * Decrementa o contador
     * Demonstra validação antes de atualizar state
     */
    onDecrement() {
        if (this.state.counter > 0) {
            this.state.counter--;
        }
    }

    /**
     * Reset do contador
     * Demonstra atualização múltipla de state
     */
    onReset() {
        this.state.counter = this.props.initialCounter || 0;
        this.state.isActive = false;
    }

    /**
     * Toggle de estado
     * Demonstra uso de boolean no state
     */
    onToggleActive() {
        this.state.isActive = !this.state.isActive;
    }

    /**
     * Handler de input
     * Demonstra two-way binding manual
     *
     * @param {Event} ev - evento do input
     */
    onInputChange(ev) {
        this.state.userName = ev.target.value;
    }

    /**
     * Handler de submit do form
     * Demonstra:
     * - Prevenção de comportamento padrão
     * - Validação de dados
     * - Chamada de callback (prop)
     *
     * @param {Event} ev - evento do form
     */
    async onSubmit(ev) {
        ev.preventDefault();

        // Validação básica
        if (!this.state.userName.trim()) {
            alert("Por favor, insira um nome");
            return;
        }

        // Prepara os dados para salvar
        const formData = {
            userName: this.state.userName,
            counter: this.state.counter,
            isActive: this.state.isActive,
        };

        console.log("[BasicExample] Submitting form data:", formData);

        // Chama callback se fornecido
        if (this.props.onSave) {
            try {
                await this.props.onSave(formData);
                console.log("[BasicExample] Save successful");

                // Limpa o form após salvar
                this.onReset();
                this.state.userName = "";
            } catch (error) {
                console.error("[BasicExample] Save failed:", error);
                alert("Erro ao salvar: " + error.message);
            }
        }
    }

    /**
     * Adiciona item à lista
     * Demonstra manipulação de arrays no state
     */
    onAddItem() {
        if (!this.state.userName.trim()) {
            alert("Digite um nome antes de adicionar");
            return;
        }

        const newItem = {
            id: Date.now(),
            name: this.state.userName,
            count: this.state.counter,
            timestamp: new Date().toLocaleString(),
        };

        // IMPORTANTE: Para arrays e objects, você deve atualizar o state
        // criando uma nova referência para o OWL detectar a mudança
        this.state.items = [...this.state.items, newItem];

        // Limpa o input
        this.state.userName = "";
    }

    /**
     * Remove item da lista
     * Demonstra filtro e atualização de array
     *
     * @param {number} itemId - ID do item a ser removido
     */
    onRemoveItem(itemId) {
        this.state.items = this.state.items.filter(item => item.id !== itemId);
    }

    // ===== MÉTODOS AUXILIARES =====

    /**
     * Carrega dados iniciais (simulado)
     * Demonstra método assíncrono privado
     *
     * @private
     * @returns {Promise<void>}
     */
    async _loadInitialData() {
        // Simula delay de rede
        await new Promise(resolve => setTimeout(resolve, 500));

        // Inicializa state com dados "carregados"
        this.state.items = [
            {
                id: 1,
                name: "Item de Exemplo",
                count: 5,
                timestamp: new Date().toLocaleString()
            },
        ];
    }

    /**
     * Valida dados do formulário
     *
     * @private
     * @returns {boolean}
     */
    _validateForm() {
        if (!this.state.userName.trim()) {
            return false;
        }
        if (this.state.counter < 0) {
            return false;
        }
        return true;
    }
}

/**
 * COMO USAR ESTE COMPONENTE:
 *
 * 1. No template XML:
 *
 * <t t-component="ComponentBasicExample"
 *    title="'Meu Título'"
 *    subtitle="'Subtítulo Opcional'"
 *    maxCount="50"
 *    initialCounter="10"
 *    onSave="onSaveHandler" />
 *
 * 2. Em outro componente JS:
 *
 * import { ComponentBasicExample } from "./component_basic_example";
 *
 * export class ParentComponent extends Component {
 *     static components = { ComponentBasicExample };
 *     static template = xml`
 *         <ComponentBasicExample
 *             title="'Hello World'"
 *             maxCount="100"
 *             onSave="onSave" />
 *     `;
 *
 *     setup() {
 *         this.onSave = async (data) => {
 *             console.log("Dados salvos:", data);
 *         };
 *     }
 * }
 *
 * 3. Registrar no registry (para usar em views XML):
 *
 * import { registry } from "@web/core/registry";
 *
 * registry.category("actions").add("basic_example_action", ComponentBasicExample);
 */
