/** @odoo-module **/

import { Component, useState, useRef, useEffect, onWillStart, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Domain } from "@web/core/domain";

/**
 * ComponentListDashboard
 *
 * Dashboard completo demonstrando:
 * - Busca de dados via ORM com múltiplos models
 * - Filtros avançados e search
 * - Lista de cards interativos
 * - Gráficos e estatísticas
 * - Actions (doAction)
 * - Refresh automático
 * - Export de dados
 * - Drill-down navigation
 *
 * @extends Component
 */
export class ComponentListDashboard extends Component {
    setup() {
        // ===== SERVICES =====
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.user = useService("user");

        // ===== STATE =====
        this.state = useState({
            // Dados principais
            records: [],
            categories: [],
            partners: [],

            // Estatísticas do dashboard
            statistics: {
                total: 0,
                thisMonth: 0,
                thisWeek: 0,
                today: 0,
                totalAmount: 0,
                averageAmount: 0,
            },

            // Dados para gráficos
            chartData: {
                byCategory: [],
                byMonth: [],
                byStatus: [],
            },

            // UI State
            loading: false,
            loadingStats: false,
            selectedView: "cards", // "cards", "list", "kanban"
            selectedRecord: null,

            // Filtros
            filters: {
                searchTerm: "",
                category_id: null,
                partner_id: null,
                state: "all", // "all", "draft", "done", "cancelled"
                date_from: null,
                date_to: null,
                active: true,
            },

            // Ordenação
            sortBy: "date",
            sortOrder: "desc", // "asc" ou "desc"

            // Paginação
            page: 1,
            pageSize: 12,
            totalRecords: 0,

            // Auto-refresh
            autoRefresh: false,
            refreshInterval: 30000, // 30 segundos
        });

        // ===== REFS =====
        this.searchInputRef = useRef("searchInput");
        this.chartCategoryRef = useRef("chartCategory");
        this.chartMonthRef = useRef("chartMonth");
        this.chartStatusRef = useRef("chartStatus");

        // ===== EFFECTS =====

        // Effect: Recarrega dados quando filtros mudam
        useEffect(
            () => {
                console.log("[Dashboard] Filters changed, reloading...");
                this.state.page = 1; // Reset page
                this._loadAllData();
            },
            () => [
                this.state.filters.category_id,
                this.state.filters.partner_id,
                this.state.filters.state,
                this.state.filters.date_from,
                this.state.filters.date_to,
                this.state.filters.active,
                this.state.sortBy,
                this.state.sortOrder,
            ]
        );

        // Effect: Search com debounce
        useEffect(
            () => {
                const timeoutId = setTimeout(() => {
                    if (this.state.filters.searchTerm) {
                        console.log("[Dashboard] Searching:", this.state.filters.searchTerm);
                        this.state.page = 1;
                        this._loadRecords();
                    }
                }, 500);

                return () => clearTimeout(timeoutId);
            },
            () => [this.state.filters.searchTerm]
        );

        // Effect: Auto-refresh
        useEffect(
            () => {
                if (this.state.autoRefresh) {
                    console.log("[Dashboard] Auto-refresh enabled");

                    const intervalId = setInterval(() => {
                        console.log("[Dashboard] Auto-refreshing data...");
                        this._loadAllData();
                    }, this.state.refreshInterval);

                    return () => {
                        console.log("[Dashboard] Auto-refresh disabled");
                        clearInterval(intervalId);
                    };
                }
            },
            () => [this.state.autoRefresh, this.state.refreshInterval]
        );

        // Effect: Atualiza paginação
        useEffect(
            () => {
                this._loadRecords();
            },
            () => [this.state.page]
        );

        // ===== LIFECYCLE =====
        onWillStart(async () => {
            console.log("[Dashboard] Component starting...");
            await this._loadAllData();
        });

        onMounted(() => {
            console.log("[Dashboard] Component mounted");
            this._initializeCharts();
        });

        // Variáveis de instância
        this._chartInstances = {};
    }

    // ===== PROPS =====
    static props = {
        // Model principal
        resModel: { type: String },

        // Título do dashboard
        title: { type: String, optional: true },

        // Domain base
        domain: { type: Array, optional: true },

        // Context
        context: { type: Object, optional: true },

        // Campos a serem buscados
        fields: { type: Array, optional: true },

        // Configurações de visualização
        showStatistics: { type: Boolean, optional: true },
        showCharts: { type: Boolean, optional: true },
        showFilters: { type: Boolean, optional: true },

        // Callbacks
        onRecordClick: { type: Function, optional: true },
        onActionExecuted: { type: Function, optional: true },
    };

    static template = "odoo_examples.ComponentListDashboard";

    // ===== COMPUTED PROPERTIES =====

    get dashboardTitle() {
        return this.props.title || "Dashboard";
    }

    get filteredRecords() {
        let records = [...this.state.records];

        // Busca por texto (já aplicada no backend, mas podemos refinar aqui)
        if (this.state.filters.searchTerm) {
            const term = this.state.filters.searchTerm.toLowerCase();
            records = records.filter(r =>
                (r.name && r.name.toLowerCase().includes(term)) ||
                (r.description && r.description.toLowerCase().includes(term))
            );
        }

        return records;
    }

    get sortedRecords() {
        const records = [...this.filteredRecords];
        const sortBy = this.state.sortBy;
        const order = this.state.sortOrder;

        records.sort((a, b) => {
            let aVal = a[sortBy];
            let bVal = b[sortBy];

            // Handle null/undefined
            if (aVal == null) return order === "asc" ? -1 : 1;
            if (bVal == null) return order === "asc" ? 1 : -1;

            // Handle dates
            if (sortBy.includes("date")) {
                aVal = new Date(aVal);
                bVal = new Date(bVal);
            }

            // Compare
            if (aVal < bVal) return order === "asc" ? -1 : 1;
            if (aVal > bVal) return order === "asc" ? 1 : -1;
            return 0;
        });

        return records;
    }

    get paginatedRecords() {
        const start = (this.state.page - 1) * this.state.pageSize;
        const end = start + this.state.pageSize;
        return this.sortedRecords.slice(start, end);
    }

    get totalPages() {
        return Math.ceil(this.filteredRecords.length / this.state.pageSize);
    }

    get showStatistics() {
        return this.props.showStatistics !== false;
    }

    get showCharts() {
        return this.props.showCharts !== false;
    }

    get showFilters() {
        return this.props.showFilters !== false;
    }

    // ===== DATA LOADING =====

    /**
     * Carrega todos os dados do dashboard
     *
     * @private
     */
    async _loadAllData() {
        await Promise.all([
            this._loadRecords(),
            this._loadStatistics(),
            this._loadChartData(),
            this._loadFilterOptions(),
        ]);
    }

    /**
     * Carrega registros principais
     *
     * @private
     */
    async _loadRecords() {
        this.state.loading = true;

        try {
            const domain = this._buildDomain();
            const fields = this.props.fields || [
                "name",
                "description",
                "partner_id",
                "category_id",
                "date",
                "state",
                "amount",
                "active",
            ];

            console.log("[Dashboard] Loading records with domain:", domain);

            // Carrega registros
            const records = await this.orm.searchRead(
                this.props.resModel,
                domain,
                fields,
                {
                    order: this._buildOrder(),
                    context: this._getContext(),
                }
            );

            // Conta total
            const count = await this.orm.searchCount(
                this.props.resModel,
                domain,
                { context: this._getContext() }
            );

            console.log(`[Dashboard] Loaded ${records.length} of ${count} records`);

            this.state.records = records;
            this.state.totalRecords = count;

        } catch (error) {
            console.error("[Dashboard] Error loading records:", error);
            this.notification.add("Erro ao carregar dados: " + error.message, {
                type: "danger",
            });
        } finally {
            this.state.loading = false;
        }
    }

    /**
     * Carrega estatísticas
     *
     * @private
     */
    async _loadStatistics() {
        if (!this.showStatistics) return;

        this.state.loadingStats = true;

        try {
            console.log("[Dashboard] Loading statistics...");

            // Opção 1: Calcular no frontend (para dados já carregados)
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const thisWeekStart = new Date(today);
            thisWeekStart.setDate(today.getDate() - today.getDay());

            const thisMonthStart = new Date(today.getFullYear(), today.getMonth(), 1);

            // Filtra records por data
            const allRecords = this.state.records;
            const todayRecords = allRecords.filter(r => {
                const recordDate = new Date(r.date);
                return recordDate >= today;
            });
            const weekRecords = allRecords.filter(r => {
                const recordDate = new Date(r.date);
                return recordDate >= thisWeekStart;
            });
            const monthRecords = allRecords.filter(r => {
                const recordDate = new Date(r.date);
                return recordDate >= thisMonthStart;
            });

            // Calcula totais
            const totalAmount = allRecords.reduce((sum, r) => sum + (r.amount || 0), 0);
            const averageAmount = allRecords.length > 0 ? totalAmount / allRecords.length : 0;

            this.state.statistics = {
                total: allRecords.length,
                today: todayRecords.length,
                thisWeek: weekRecords.length,
                thisMonth: monthRecords.length,
                totalAmount: totalAmount,
                averageAmount: averageAmount,
            };

            // Opção 2: Buscar do backend (para estatísticas mais complexas)
            // const stats = await this.orm.call(
            //     this.props.resModel,
            //     "get_dashboard_statistics",
            //     [],
            //     { domain: this._buildDomain() }
            // );
            // this.state.statistics = stats;

        } catch (error) {
            console.error("[Dashboard] Error loading statistics:", error);
        } finally {
            this.state.loadingStats = false;
        }
    }

    /**
     * Carrega dados para gráficos
     *
     * @private
     */
    async _loadChartData() {
        if (!this.showCharts) return;

        try {
            console.log("[Dashboard] Loading chart data...");

            const domain = this._buildDomain();

            // Opção 1: read_group para agrupar dados
            const byCategory = await this.orm.readGroup(
                this.props.resModel,
                domain,
                ["category_id", "amount:sum"],
                ["category_id"],
                { context: this._getContext() }
            );

            const byStatus = await this.orm.readGroup(
                this.props.resModel,
                domain,
                ["state", "id:count"],
                ["state"],
                { context: this._getContext() }
            );

            // Dados por mês (últimos 6 meses)
            const byMonth = await this._getMonthlyData();

            this.state.chartData = {
                byCategory: byCategory,
                byMonth: byMonth,
                byStatus: byStatus,
            };

            // Atualiza gráficos se já estiverem montados
            this._updateCharts();

        } catch (error) {
            console.error("[Dashboard] Error loading chart data:", error);
        }
    }

    /**
     * Carrega opções para filtros (categorias, parceiros, etc)
     *
     * @private
     */
    async _loadFilterOptions() {
        try {
            console.log("[Dashboard] Loading filter options...");

            // Carrega categorias
            const categories = await this.orm.searchRead(
                "product.category", // ou o model de categoria apropriado
                [],
                ["name"],
                {
                    order: "name",
                    context: this._getContext(),
                }
            );

            // Carrega parceiros (top 100)
            const partners = await this.orm.searchRead(
                "res.partner",
                [],
                ["name"],
                {
                    limit: 100,
                    order: "name",
                    context: this._getContext(),
                }
            );

            this.state.categories = categories;
            this.state.partners = partners;

        } catch (error) {
            console.error("[Dashboard] Error loading filter options:", error);
        }
    }

    /**
     * Obtém dados agrupados por mês
     *
     * @private
     * @returns {Array}
     */
    async _getMonthlyData() {
        const months = [];
        const today = new Date();

        for (let i = 5; i >= 0; i--) {
            const date = new Date(today.getFullYear(), today.getMonth() - i, 1);
            const nextDate = new Date(date.getFullYear(), date.getMonth() + 1, 1);

            const domain = [
                ...this._buildDomain(),
                ["date", ">=", date.toISOString().split("T")[0]],
                ["date", "<", nextDate.toISOString().split("T")[0]],
            ];

            const count = await this.orm.searchCount(
                this.props.resModel,
                domain,
                { context: this._getContext() }
            );

            months.push({
                month: date.toLocaleDateString("pt-BR", { month: "short" }),
                count: count,
            });
        }

        return months;
    }

    // ===== DOMAIN & ORDER BUILDERS =====

    /**
     * Constrói domain baseado nos filtros
     *
     * @private
     * @returns {Array}
     */
    _buildDomain() {
        const domain = [...(this.props.domain || [])];

        // Filtro de categoria
        if (this.state.filters.category_id) {
            domain.push(["category_id", "=", this.state.filters.category_id]);
        }

        // Filtro de parceiro
        if (this.state.filters.partner_id) {
            domain.push(["partner_id", "=", this.state.filters.partner_id]);
        }

        // Filtro de estado
        if (this.state.filters.state !== "all") {
            domain.push(["state", "=", this.state.filters.state]);
        }

        // Filtro de data
        if (this.state.filters.date_from) {
            domain.push(["date", ">=", this.state.filters.date_from]);
        }
        if (this.state.filters.date_to) {
            domain.push(["date", "<=", this.state.filters.date_to]);
        }

        // Filtro de active
        if (this.state.filters.active !== null) {
            domain.push(["active", "=", this.state.filters.active]);
        }

        // Busca textual
        if (this.state.filters.searchTerm) {
            const term = this.state.filters.searchTerm;
            domain.push("|", ["name", "ilike", term], ["description", "ilike", term]);
        }

        return domain;
    }

    /**
     * Constrói string de ordenação
     *
     * @private
     * @returns {string}
     */
    _buildOrder() {
        const direction = this.state.sortOrder === "asc" ? "asc" : "desc";
        return `${this.state.sortBy} ${direction}`;
    }

    // ===== EVENT HANDLERS - FILTROS =====

    onSearchInput(ev) {
        this.state.filters.searchTerm = ev.target.value;
    }

    onClearSearch() {
        this.state.filters.searchTerm = "";
    }

    onCategoryChange(ev) {
        const value = ev.target.value;
        this.state.filters.category_id = value ? parseInt(value) : null;
    }

    onPartnerChange(ev) {
        const value = ev.target.value;
        this.state.filters.partner_id = value ? parseInt(value) : null;
    }

    onStateChange(state) {
        this.state.filters.state = state;
    }

    onDateFromChange(ev) {
        this.state.filters.date_from = ev.target.value;
    }

    onDateToChange(ev) {
        this.state.filters.date_to = ev.target.value;
    }

    onClearFilters() {
        this.state.filters = {
            searchTerm: "",
            category_id: null,
            partner_id: null,
            state: "all",
            date_from: null,
            date_to: null,
            active: true,
        };
    }

    // ===== EVENT HANDLERS - SORTING =====

    onSortChange(field) {
        if (this.state.sortBy === field) {
            // Toggle order
            this.state.sortOrder = this.state.sortOrder === "asc" ? "desc" : "asc";
        } else {
            this.state.sortBy = field;
            this.state.sortOrder = "desc";
        }
    }

    // ===== EVENT HANDLERS - VIEW =====

    onViewChange(view) {
        this.state.selectedView = view;
    }

    onRefresh() {
        console.log("[Dashboard] Manual refresh");
        this._loadAllData();
    }

    onToggleAutoRefresh() {
        this.state.autoRefresh = !this.state.autoRefresh;

        this.notification.add(
            this.state.autoRefresh
                ? "Auto-refresh ativado"
                : "Auto-refresh desativado",
            { type: "info" }
        );
    }

    // ===== EVENT HANDLERS - RECORDS =====

    onRecordClick(record) {
        console.log("[Dashboard] Record clicked:", record);

        this.state.selectedRecord = record;

        if (this.props.onRecordClick) {
            this.props.onRecordClick(record);
        } else {
            // Comportamento padrão: abrir form view
            this.openRecordForm(record.id);
        }
    }

    async openRecordForm(recordId) {
        console.log("[Dashboard] Opening record form:", recordId);

        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: this.props.resModel,
            res_id: recordId,
            views: [[false, "form"]],
            target: "new", // Abre em modal
            context: this._getContext(),
        });
    }

    async onCreateRecord() {
        console.log("[Dashboard] Creating new record");

        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: this.props.resModel,
            views: [[false, "form"]],
            target: "new",
            context: {
                ...this._getContext(),
                // Pode passar valores padrão aqui
                default_partner_id: this.state.filters.partner_id,
                default_category_id: this.state.filters.category_id,
            },
        });

        // Recarrega após fechar o modal (usar event bus na prática)
        // this._loadAllData();
    }

    // ===== EVENT HANDLERS - STATISTICS CARDS =====

    async onStatisticClick(statType) {
        console.log("[Dashboard] Statistic clicked:", statType);

        let domain = [...this._buildDomain()];
        let name = "Registros";

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        switch (statType) {
            case "today":
                domain.push(["date", ">=", today.toISOString().split("T")[0]]);
                name = "Registros de Hoje";
                break;

            case "thisWeek":
                const weekStart = new Date(today);
                weekStart.setDate(today.getDate() - today.getDay());
                domain.push(["date", ">=", weekStart.toISOString().split("T")[0]]);
                name = "Registros desta Semana";
                break;

            case "thisMonth":
                const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
                domain.push(["date", ">=", monthStart.toISOString().split("T")[0]]);
                name = "Registros deste Mês";
                break;
        }

        // Abre list view filtrada
        await this.action.doAction({
            type: "ir.actions.act_window",
            name: name,
            res_model: this.props.resModel,
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: domain,
            context: this._getContext(),
        });
    }

    // ===== EVENT HANDLERS - CHARTS =====

    onChartClick(chartType, dataPoint) {
        console.log("[Dashboard] Chart clicked:", chartType, dataPoint);

        // Implementar drill-down baseado no tipo de gráfico
        // Por exemplo, clicar em uma categoria no gráfico abre lista filtrada
    }

    // ===== PAGINATION =====

    onPageChange(page) {
        this.state.page = page;
    }

    onNextPage() {
        if (this.state.page < this.totalPages) {
            this.state.page++;
        }
    }

    onPreviousPage() {
        if (this.state.page > 1) {
            this.state.page--;
        }
    }

    onPageSizeChange(ev) {
        this.state.pageSize = parseInt(ev.target.value);
        this.state.page = 1;
    }

    // ===== EXPORT =====

    async onExport() {
        console.log("[Dashboard] Exporting data...");

        try {
            const domain = this._buildDomain();

            // Usar action de export do Odoo
            await this.action.doAction({
                type: "ir.actions.act_window",
                name: "Export",
                res_model: this.props.resModel,
                views: [[false, "list"]],
                domain: domain,
                context: {
                    ...this._getContext(),
                    // Força abertura do wizard de export
                },
                flags: {
                    action_buttons: false,
                },
            });

            this.notification.add("Exportação iniciada", { type: "info" });

        } catch (error) {
            console.error("[Dashboard] Export error:", error);
            this.notification.add("Erro ao exportar: " + error.message, {
                type: "danger",
            });
        }
    }

    // ===== CHARTS =====

    /**
     * Inicializa gráficos
     *
     * @private
     */
    _initializeCharts() {
        if (!this.showCharts) return;

        console.log("[Dashboard] Initializing charts...");

        // Exemplo: inicializar Chart.js
        // if (this.chartCategoryRef.el) {
        //     this._chartInstances.category = new Chart(this.chartCategoryRef.el, {
        //         type: 'bar',
        //         data: this._getCategoryChartData(),
        //         options: { ... }
        //     });
        // }

        this._updateCharts();
    }

    /**
     * Atualiza gráficos com novos dados
     *
     * @private
     */
    _updateCharts() {
        if (!this.showCharts) return;

        console.log("[Dashboard] Updating charts...");

        // Atualizar instâncias dos gráficos
        // if (this._chartInstances.category) {
        //     this._chartInstances.category.data = this._getCategoryChartData();
        //     this._chartInstances.category.update();
        // }
    }

    // ===== HELPERS =====

    _getContext() {
        return {
            ...this.user.context,
            ...this.props.context,
        };
    }

    /**
     * Formata valor monetário
     *
     * @param {number} amount - Valor a formatar
     * @returns {string}
     */
    formatCurrency(amount) {
        return new Intl.NumberFormat("pt-BR", {
            style: "currency",
            currency: "BRL",
        }).format(amount || 0);
    }

    /**
     * Formata data
     *
     * @param {string} date - Data a formatar
     * @returns {string}
     */
    formatDate(date) {
        if (!date) return "";
        return new Date(date).toLocaleDateString("pt-BR");
    }

    /**
     * Retorna classe CSS baseada no estado
     *
     * @param {string} state - Estado do registro
     * @returns {string}
     */
    getStateClass(state) {
        const classes = {
            draft: "text-muted",
            confirmed: "text-primary",
            done: "text-success",
            cancelled: "text-danger",
        };
        return classes[state] || "";
    }
}

/**
 * EXEMPLO DE USO:
 *
 * <record id="action_dashboard" model="ir.actions.client">
 *     <field name="name">Sales Dashboard</field>
 *     <field name="tag">ComponentListDashboard</field>
 *     <field name="params" eval="{
 *         'resModel': 'sale.order',
 *         'title': 'Dashboard de Vendas',
 *         'domain': [],
 *         'showStatistics': True,
 *         'showCharts': True,
 *         'showFilters': True,
 *     }"/>
 * </record>
 */
