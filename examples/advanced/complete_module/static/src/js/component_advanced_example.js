/** @odoo-module **/

import { Component, useState, useRef, useEffect, onWillStart, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

/**
 * ComponentAdvancedExample
 *
 * Componente avançado demonstrando:
 * - useService (ORM, action, notification, rpc)
 * - useRef para DOM manipulation
 * - useEffect para side effects
 * - Communication entre componentes (props/events)
 * - Integração com backend
 * - Debouncing e throttling
 * - Error handling
 *
 * @extends Component
 */
export class ComponentAdvancedExample extends Component {
    setup() {
        // ===== SERVICES =====
        /**
         * useService permite acessar serviços do Odoo
         *
         * Serviços comuns:
         * - orm: Para operações de banco de dados (search, read, write, create, unlink)
         * - action: Para executar actions do Odoo
         * - notification: Para mostrar notificações
         * - rpc: Para chamadas RPC customizadas
         * - dialog: Para mostrar diálogos
         * - user: Informações do usuário atual
         */
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.rpc = useService("rpc");
        this.user = useService("user");

        // ===== STATE =====
        this.state = useState({
            // Dados carregados do backend
            records: [],
            selectedRecord: null,

            // UI state
            loading: false,
            searchTerm: "",
            filters: {
                active: true,
                category: "all",
            },

            // Paginação
            page: 1,
            pageSize: 10,
            totalRecords: 0,

            // Form state
            formData: {
                name: "",
                description: "",
                partner_id: null,
            },

            // Error handling
            error: null,

            // Statistics
            stats: {
                total: 0,
                active: 0,
                inactive: 0,
            },
        });

        // ===== REFS =====
        /**
         * useRef permite acessar elementos DOM diretamente
         * Útil para:
         * - Focus management
         * - Integração com bibliotecas de terceiros
         * - Animações
         * - Medições de tamanho/posição
         */
        this.searchInputRef = useRef("searchInput");
        this.modalRef = useRef("modal");
        this.chartContainerRef = useRef("chartContainer");

        // ===== EFFECTS =====
        /**
         * useEffect executa código quando dependências mudam
         * Similar ao useEffect do React
         *
         * Sintaxe: useEffect(callback, dependencies)
         * - callback: função a ser executada
         * - dependencies: array de valores que, ao mudar, disparam o callback
         *
         * IMPORTANTE: O callback pode retornar uma função de cleanup
         */

        // Effect 1: Carrega dados quando filtros ou página mudam
        useEffect(
            () => {
                console.log("[AdvancedExample] Filters or page changed, loading data...");
                this._loadRecords();
            },
            () => [
                this.state.filters.active,
                this.state.filters.category,
                this.state.page,
            ]
        );

        // Effect 2: Search com debounce
        useEffect(
            () => {
                console.log("[AdvancedExample] Search term changed:", this.state.searchTerm);

                // Debounce: espera 300ms após a última digitação
                const timeoutId = setTimeout(() => {
                    this._performSearch();
                }, 300);

                // Cleanup: cancela o timeout se o termo mudar novamente
                return () => clearTimeout(timeoutId);
            },
            () => [this.state.searchTerm]
        );

        // Effect 3: Atualiza estatísticas quando records mudam
        useEffect(
            () => {
                this._updateStatistics();
            },
            () => [this.state.records]
        );

        // ===== LIFECYCLE HOOKS =====
        onWillStart(async () => {
            console.log("[AdvancedExample] Starting component...");

            // Carrega dados iniciais em paralelo
            await Promise.all([
                this._loadRecords(),
                this._loadStatistics(),
            ]);
        });

        onMounted(() => {
            console.log("[AdvancedExample] Component mounted");

            // Inicializa biblioteca de charts (exemplo)
            this._initializeChart();

            // Auto-focus no search input
            if (this.searchInputRef.el) {
                this.searchInputRef.el.focus();
            }
        });

        // Variáveis de instância (não reativas)
        this._debounceTimeout = null;
        this._chartInstance = null;
    }

    // ===== PROPS =====
    static props = {
        // Model do Odoo a ser usado
        resModel: { type: String },

        // Domain padrão para filtrar registros
        domain: { type: Array, optional: true },

        // Context adicional
        context: { type: Object, optional: true },

        // Modo de visualização: "list", "kanban", "form"
        viewMode: { type: String, optional: true },

        // Callbacks para comunicação com componente pai
        onRecordSelected: { type: Function, optional: true },
        onRecordCreated: { type: Function, optional: true },
        onRecordDeleted: { type: Function, optional: true },

        // Configurações
        allowCreate: { type: Boolean, optional: true },
        allowEdit: { type: Boolean, optional: true },
        allowDelete: { type: Boolean, optional: true },
    };

    static template = "odoo_examples.ComponentAdvancedExample";

    // ===== COMPUTED PROPERTIES =====

    get filteredRecords() {
        let records = this.state.records;

        // Aplica filtro de busca
        if (this.state.searchTerm) {
            const term = this.state.searchTerm.toLowerCase();
            records = records.filter(r =>
                r.name.toLowerCase().includes(term) ||
                (r.description && r.description.toLowerCase().includes(term))
            );
        }

        return records;
    }

    get paginatedRecords() {
        const start = (this.state.page - 1) * this.state.pageSize;
        const end = start + this.state.pageSize;
        return this.filteredRecords.slice(start, end);
    }

    get totalPages() {
        return Math.ceil(this.filteredRecords.length / this.state.pageSize);
    }

    get hasNextPage() {
        return this.state.page < this.totalPages;
    }

    get hasPreviousPage() {
        return this.state.page > 1;
    }

    get canCreate() {
        return this.props.allowCreate !== false;
    }

    get canEdit() {
        return this.props.allowEdit !== false;
    }

    get canDelete() {
        return this.props.allowDelete !== false;
    }

    // ===== ORM OPERATIONS =====

    /**
     * Carrega registros do backend usando ORM
     * Demonstra: search_read, domain, fields, context
     *
     * @private
     */
    async _loadRecords() {
        this.state.loading = true;
        this.state.error = null;

        try {
            // Constrói o domain baseado nos filtros
            const domain = [...(this.props.domain || [])];

            // Adiciona filtro de active se aplicável
            if (this.state.filters.active) {
                domain.push(["active", "=", true]);
            }

            // Adiciona filtro de categoria
            if (this.state.filters.category !== "all") {
                domain.push(["category_id", "=", this.state.filters.category]);
            }

            console.log("[AdvancedExample] Loading records with domain:", domain);

            // search_read: busca e lê registros em uma única chamada
            const records = await this.orm.searchRead(
                this.props.resModel,
                domain,
                ["name", "description", "partner_id", "date", "state", "amount"], // fields
                {
                    limit: this.state.pageSize,
                    offset: (this.state.page - 1) * this.state.pageSize,
                    order: "id desc",
                    context: this._getContext(),
                }
            );

            console.log(`[AdvancedExample] Loaded ${records.length} records`);

            this.state.records = records;

            // Conta total de registros
            const count = await this.orm.searchCount(
                this.props.resModel,
                domain,
                { context: this._getContext() }
            );

            this.state.totalRecords = count;

        } catch (error) {
            console.error("[AdvancedExample] Error loading records:", error);
            this.state.error = error.message || "Erro ao carregar registros";

            this.notification.add(
                "Erro ao carregar registros: " + error.message,
                {
                    type: "danger",
                    title: "Erro",
                }
            );
        } finally {
            this.state.loading = false;
        }
    }

    /**
     * Cria novo registro
     * Demonstra: create, notification
     *
     * @param {Object} values - Valores do novo registro
     */
    async createRecord(values) {
        this.state.loading = true;

        try {
            console.log("[AdvancedExample] Creating record:", values);

            // create: cria um novo registro e retorna seu ID
            const recordId = await this.orm.create(
                this.props.resModel,
                [values],
                { context: this._getContext() }
            );

            console.log("[AdvancedExample] Record created with ID:", recordId);

            // Notifica sucesso
            this.notification.add("Registro criado com sucesso!", {
                type: "success",
                title: "Sucesso",
            });

            // Recarrega a lista
            await this._loadRecords();

            // Notifica componente pai
            if (this.props.onRecordCreated) {
                this.props.onRecordCreated(recordId);
            }

            // Limpa o formulário
            this._resetForm();

            return recordId;

        } catch (error) {
            console.error("[AdvancedExample] Error creating record:", error);

            this.notification.add(
                "Erro ao criar registro: " + error.message,
                {
                    type: "danger",
                    title: "Erro",
                }
            );

            throw error;
        } finally {
            this.state.loading = false;
        }
    }

    /**
     * Atualiza registro existente
     * Demonstra: write
     *
     * @param {number} recordId - ID do registro
     * @param {Object} values - Valores a atualizar
     */
    async updateRecord(recordId, values) {
        this.state.loading = true;

        try {
            console.log("[AdvancedExample] Updating record:", recordId, values);

            // write: atualiza registros existentes
            await this.orm.write(
                this.props.resModel,
                [recordId],
                values,
                { context: this._getContext() }
            );

            console.log("[AdvancedExample] Record updated successfully");

            this.notification.add("Registro atualizado com sucesso!", {
                type: "success",
            });

            // Recarrega a lista
            await this._loadRecords();

        } catch (error) {
            console.error("[AdvancedExample] Error updating record:", error);

            this.notification.add(
                "Erro ao atualizar registro: " + error.message,
                {
                    type: "danger",
                    title: "Erro",
                }
            );

            throw error;
        } finally {
            this.state.loading = false;
        }
    }

    /**
     * Deleta registro
     * Demonstra: unlink
     *
     * @param {number} recordId - ID do registro a deletar
     */
    async deleteRecord(recordId) {
        // Confirma antes de deletar
        if (!confirm("Tem certeza que deseja deletar este registro?")) {
            return;
        }

        this.state.loading = true;

        try {
            console.log("[AdvancedExample] Deleting record:", recordId);

            // unlink: deleta registros
            await this.orm.unlink(
                this.props.resModel,
                [recordId],
                { context: this._getContext() }
            );

            console.log("[AdvancedExample] Record deleted successfully");

            this.notification.add("Registro deletado com sucesso!", {
                type: "success",
            });

            // Recarrega a lista
            await this._loadRecords();

            // Notifica componente pai
            if (this.props.onRecordDeleted) {
                this.props.onRecordDeleted(recordId);
            }

        } catch (error) {
            console.error("[AdvancedExample] Error deleting record:", error);

            this.notification.add(
                "Erro ao deletar registro: " + error.message,
                {
                    type: "danger",
                    title: "Erro",
                }
            );
        } finally {
            this.state.loading = false;
        }
    }

    /**
     * Chama método customizado no backend
     * Demonstra: call
     *
     * @param {string} method - Nome do método
     * @param {Array} args - Argumentos posicionais
     * @param {Object} kwargs - Argumentos nomeados
     */
    async callMethod(method, args = [], kwargs = {}) {
        try {
            console.log("[AdvancedExample] Calling method:", method, args, kwargs);

            // call: chama método de modelo do Odoo
            const result = await this.orm.call(
                this.props.resModel,
                method,
                args,
                kwargs
            );

            console.log("[AdvancedExample] Method result:", result);

            return result;

        } catch (error) {
            console.error("[AdvancedExample] Error calling method:", error);
            throw error;
        }
    }

    // ===== ACTION SERVICE =====

    /**
     * Abre form view de um registro
     * Demonstra: doAction
     *
     * @param {number} recordId - ID do registro
     */
    async openRecord(recordId) {
        console.log("[AdvancedExample] Opening record:", recordId);

        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: this.props.resModel,
            res_id: recordId,
            views: [[false, "form"]],
            target: "current", // "current", "new", "fullscreen"
            context: this._getContext(),
        });
    }

    /**
     * Abre list view filtrada
     * Demonstra: doAction com domain
     *
     * @param {Array} domain - Domain para filtrar
     */
    async openListView(domain = []) {
        console.log("[AdvancedExample] Opening list view with domain:", domain);

        await this.action.doAction({
            type: "ir.actions.act_window",
            name: "Registros Filtrados",
            res_model: this.props.resModel,
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: domain,
            context: this._getContext(),
        });
    }

    /**
     * Executa action por XML ID
     * Demonstra: doAction com XML ID
     *
     * @param {string} xmlId - XML ID da action
     */
    async executeAction(xmlId) {
        console.log("[AdvancedExample] Executing action:", xmlId);

        try {
            await this.action.doAction(xmlId, {
                additionalContext: this._getContext(),
            });
        } catch (error) {
            console.error("[AdvancedExample] Error executing action:", error);
            this.notification.add("Erro ao executar ação", { type: "danger" });
        }
    }

    // ===== RPC SERVICE =====

    /**
     * Faz chamada RPC customizada
     * Demonstra: rpc para endpoints customizados
     */
    async _loadStatistics() {
        try {
            console.log("[AdvancedExample] Loading statistics via RPC...");

            // Opção 1: Usar rpc diretamente
            const stats = await this.rpc("/my_module/get_statistics", {
                model: this.props.resModel,
            });

            // Opção 2: Usar orm.call para método de modelo
            // const stats = await this.orm.call(
            //     this.props.resModel,
            //     "get_statistics",
            //     [],
            //     {}
            // );

            this.state.stats = stats || this.state.stats;

        } catch (error) {
            console.error("[AdvancedExample] Error loading statistics:", error);
        }
    }

    // ===== SEARCH & FILTERS =====

    /**
     * Realiza busca (chamado pelo useEffect com debounce)
     *
     * @private
     */
    async _performSearch() {
        console.log("[AdvancedExample] Performing search:", this.state.searchTerm);

        // Reset para primeira página ao buscar
        this.state.page = 1;

        // O filteredRecords getter já aplica o filtro de busca
        // Aqui você poderia fazer uma busca no backend se necessário
        // await this._loadRecords();
    }

    /**
     * Handler do input de busca
     * Demonstra: two-way binding
     *
     * @param {Event} ev - Evento do input
     */
    onSearchInput(ev) {
        this.state.searchTerm = ev.target.value;
        // O useEffect com debounce cuidará da busca
    }

    /**
     * Limpa busca
     */
    onClearSearch() {
        this.state.searchTerm = "";
        if (this.searchInputRef.el) {
            this.searchInputRef.el.focus();
        }
    }

    /**
     * Altera filtro de categoria
     *
     * @param {string} category - Nova categoria
     */
    onCategoryChange(category) {
        this.state.filters.category = category;
        this.state.page = 1; // Reset page
        // O useEffect cuidará de recarregar os dados
    }

    /**
     * Toggle filtro de active
     */
    onToggleActive() {
        this.state.filters.active = !this.state.filters.active;
        this.state.page = 1; // Reset page
        // O useEffect cuidará de recarregar os dados
    }

    // ===== PAGINATION =====

    onNextPage() {
        if (this.hasNextPage) {
            this.state.page++;
        }
    }

    onPreviousPage() {
        if (this.hasPreviousPage) {
            this.state.page--;
        }
    }

    onPageChange(page) {
        if (page >= 1 && page <= this.totalPages) {
            this.state.page = page;
        }
    }

    // ===== RECORD SELECTION =====

    /**
     * Seleciona um registro
     * Demonstra: comunicação com componente pai via props
     *
     * @param {Object} record - Registro selecionado
     */
    onSelectRecord(record) {
        console.log("[AdvancedExample] Record selected:", record);

        this.state.selectedRecord = record;

        // Notifica componente pai
        if (this.props.onRecordSelected) {
            this.props.onRecordSelected(record);
        }
    }

    /**
     * Abre form view do registro
     *
     * @param {number} recordId - ID do registro
     */
    async onOpenRecord(recordId) {
        await this.openRecord(recordId);
    }

    /**
     * Edita registro
     *
     * @param {number} recordId - ID do registro
     */
    async onEditRecord(recordId) {
        if (!this.canEdit) {
            this.notification.add("Você não tem permissão para editar", {
                type: "warning",
            });
            return;
        }

        await this.openRecord(recordId);
    }

    /**
     * Deleta registro
     *
     * @param {number} recordId - ID do registro
     */
    async onDeleteRecord(recordId) {
        if (!this.canDelete) {
            this.notification.add("Você não tem permissão para deletar", {
                type: "warning",
            });
            return;
        }

        await this.deleteRecord(recordId);
    }

    // ===== FORM HANDLING =====

    /**
     * Handler de mudança nos inputs do form
     *
     * @param {string} field - Nome do campo
     * @param {*} value - Novo valor
     */
    onFormFieldChange(field, value) {
        this.state.formData[field] = value;
    }

    /**
     * Submit do formulário
     *
     * @param {Event} ev - Evento do form
     */
    async onFormSubmit(ev) {
        ev.preventDefault();

        if (!this.canCreate) {
            this.notification.add("Você não tem permissão para criar", {
                type: "warning",
            });
            return;
        }

        // Validação básica
        if (!this.state.formData.name.trim()) {
            this.notification.add("Nome é obrigatório", {
                type: "warning",
            });
            return;
        }

        try {
            await this.createRecord(this.state.formData);
        } catch (error) {
            // Erro já tratado em createRecord
        }
    }

    /**
     * Reset do formulário
     *
     * @private
     */
    _resetForm() {
        this.state.formData = {
            name: "",
            description: "",
            partner_id: null,
        };
    }

    // ===== HELPER METHODS =====

    /**
     * Retorna context completo para operações ORM
     *
     * @private
     * @returns {Object}
     */
    _getContext() {
        return {
            ...this.user.context,
            ...this.props.context,
        };
    }

    /**
     * Atualiza estatísticas baseadas nos records
     *
     * @private
     */
    _updateStatistics() {
        const records = this.state.records;

        this.state.stats = {
            total: records.length,
            active: records.filter(r => r.active !== false).length,
            inactive: records.filter(r => r.active === false).length,
        };
    }

    /**
     * Inicializa chart (exemplo com Chart.js ou similar)
     *
     * @private
     */
    _initializeChart() {
        if (!this.chartContainerRef.el) {
            return;
        }

        console.log("[AdvancedExample] Initializing chart...");

        // Exemplo: inicializar Chart.js ou outra biblioteca
        // this._chartInstance = new Chart(this.chartContainerRef.el, {
        //     type: 'bar',
        //     data: { ... },
        //     options: { ... }
        // });
    }
}

/**
 * EXEMPLO DE USO EM VIEW XML:
 *
 * <record id="action_advanced_example" model="ir.actions.client">
 *     <field name="name">Advanced Example</field>
 *     <field name="tag">ComponentAdvancedExample</field>
 *     <field name="params" eval="{
 *         'resModel': 'res.partner',
 *         'domain': [['is_company', '=', True]],
 *         'context': {'default_customer_rank': 1},
 *     }"/>
 * </record>
 */

/**
 * EXEMPLO DE USO EM OUTRO COMPONENTE:
 *
 * import { ComponentAdvancedExample } from "./component_advanced_example";
 *
 * export class ParentComponent extends Component {
 *     static components = { ComponentAdvancedExample };
 *
 *     setup() {
 *         this.onRecordSelected = (record) => {
 *             console.log("Record selected in parent:", record);
 *         };
 *     }
 *
 *     static template = xml`
 *         <ComponentAdvancedExample
 *             resModel="'res.partner'"
 *             domain="[[['customer_rank', '>', 0]]]"
 *             onRecordSelected="onRecordSelected"
 *             allowCreate="true"
 *             allowEdit="true"
 *             allowDelete="false" />
 *     `;
 * }
 */
