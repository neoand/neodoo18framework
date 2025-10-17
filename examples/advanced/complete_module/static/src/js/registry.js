/** @odoo-module **/

/**
 * REGISTRY - Registro de Componentes OWL no Odoo 18
 *
 * Este arquivo demonstra como registrar componentes OWL nos diferentes
 * registries do Odoo para que possam ser usados em todo o sistema.
 *
 * IMPORTANTE: Este arquivo deve ser carregado em web.assets_backend
 * ANTES dos templates XML dos componentes.
 */

import { registry } from "@web/core/registry";
import { ComponentBasicExample } from "./component_basic_example";
import { ComponentAdvancedExample } from "./component_advanced_example";
import { ComponentListDashboard } from "./component_list_dashboard";

// ================================================================
// 1. CLIENT ACTIONS REGISTRY
// ================================================================
/**
 * Client Actions são componentes que podem ser abertos como "actions"
 * no Odoo, seja via menu, botão, ou programaticamente.
 *
 * Uso:
 * - Podem ser referenciados em ir.actions.client pelo campo "tag"
 * - Podem ser chamados via action.doAction()
 * - Aparecem como views principais no Odoo
 */
const actionRegistry = registry.category("actions");

// Registra componente básico
actionRegistry.add("odoo_examples.ComponentBasicExample", ComponentBasicExample);

// Registra componente avançado
actionRegistry.add("odoo_examples.ComponentAdvancedExample", ComponentAdvancedExample);

// Registra dashboard
actionRegistry.add("odoo_examples.ComponentListDashboard", ComponentListDashboard);

console.log("[Registry] Client Actions registered:", [
    "odoo_examples.ComponentBasicExample",
    "odoo_examples.ComponentAdvancedExample",
    "odoo_examples.ComponentListDashboard",
]);

// ================================================================
// 2. COMO USAR AS CLIENT ACTIONS
// ================================================================

/**
 * Exemplo 1: Via XML (ir.actions.client)
 *
 * <record id="action_basic_example" model="ir.actions.client">
 *     <field name="name">Exemplo Básico</field>
 *     <field name="tag">odoo_examples.ComponentBasicExample</field>
 *     <field name="params" eval="{'title': 'Meu Título'}"/>
 * </record>
 */

/**
 * Exemplo 2: Via JavaScript (doAction)
 *
 * import { useService } from "@web/core/utils/hooks";
 *
 * setup() {
 *     this.action = useService("action");
 * }
 *
 * async openBasicExample() {
 *     await this.action.doAction("odoo_examples.ComponentBasicExample", {
 *         additionalContext: {
 *             // context adicional
 *         },
 *         props: {
 *             title: "Meu Título",
 *             maxCount: 100,
 *         },
 *     });
 * }
 */

/**
 * Exemplo 3: Via doAction com objeto
 *
 * await this.action.doAction({
 *     type: "ir.actions.client",
 *     tag: "odoo_examples.ComponentBasicExample",
 *     name: "Exemplo Básico",
 *     target: "current", // "current", "new", "fullscreen", "main"
 *     params: {
 *         title: "Meu Título",
 *         maxCount: 100,
 *     },
 * });
 */

// ================================================================
// 3. FIELD WIDGETS REGISTRY
// ================================================================
/**
 * Field Widgets são componentes usados para renderizar campos em forms/lists.
 *
 * Exemplo de Field Widget customizado:
 */

// import { Component } from "@odoo/owl";
// import { _t } from "@web/core/l10n/translation";
// import { standardFieldProps } from "@web/views/fields/standard_field_props";

// class CustomFieldWidget extends Component {
//     static template = "odoo_examples.CustomFieldWidget";
//     static props = {
//         ...standardFieldProps,
//     };

//     get formattedValue() {
//         return `Custom: ${this.props.record.data[this.props.name]}`;
//     }

//     async onValueChange(newValue) {
//         await this.props.record.update({
//             [this.props.name]: newValue,
//         });
//     }
// }

// // Registra o field widget
// const fieldRegistry = registry.category("fields");
// fieldRegistry.add("custom_widget", {
//     component: CustomFieldWidget,
//     supportedTypes: ["char", "text"], // tipos de campo suportados
// });

/**
 * Uso no XML:
 *
 * <field name="my_field" widget="custom_widget"/>
 */

// ================================================================
// 4. SYSTRAY ITEMS REGISTRY
// ================================================================
/**
 * Systray Items são componentes que aparecem na barra superior do Odoo.
 *
 * Exemplo de Systray Item:
 */

// import { Component } from "@odoo/owl";

// class CustomSystrayItem extends Component {
//     static template = "odoo_examples.CustomSystrayItem";
//     static props = {};

//     onClick() {
//         console.log("Systray item clicked!");
//     }
// }

// // Registra no systray
// const systrayRegistry = registry.category("systray");
// systrayRegistry.add(
//     "CustomSystray",
//     {
//         Component: CustomSystrayItem,
//     },
//     {
//         sequence: 100, // ordem de exibição (menor = mais à esquerda)
//     }
// );

/**
 * Template XML para Systray:
 *
 * <t t-name="odoo_examples.CustomSystrayItem">
 *     <div class="o_systray_item" t-on-click="onClick">
 *         <i class="fa fa-bell"/>
 *         <span class="badge">3</span>
 *     </div>
 * </t>
 */

// ================================================================
// 5. SERVICES REGISTRY
// ================================================================
/**
 * Services são singletons que fornecem funcionalidades globais.
 *
 * Exemplo de Service customizado:
 */

// export const customService = {
//     dependencies: ["notification", "orm"],

//     start(env, { notification, orm }) {
//         console.log("[CustomService] Starting...");

//         return {
//             // Método 1: Função simples
//             async fetchData(model, domain = []) {
//                 console.log("[CustomService] Fetching data:", model);
//                 try {
//                     const records = await orm.searchRead(model, domain, ["name"]);
//                     notification.add("Dados carregados com sucesso!", {
//                         type: "success",
//                     });
//                     return records;
//                 } catch (error) {
//                     notification.add("Erro ao carregar dados: " + error.message, {
//                         type: "danger",
//                     });
//                     throw error;
//                 }
//             },

//             // Método 2: Função com estado
//             cache: new Map(),

//             async getCached(key, fetcher) {
//                 if (this.cache.has(key)) {
//                     console.log("[CustomService] Cache hit:", key);
//                     return this.cache.get(key);
//                 }

//                 console.log("[CustomService] Cache miss:", key);
//                 const value = await fetcher();
//                 this.cache.set(key, value);
//                 return value;
//             },

//             clearCache() {
//                 this.cache.clear();
//             },
//         };
//     },
// };

// // Registra o service
// const serviceRegistry = registry.category("services");
// serviceRegistry.add("customService", customService);

/**
 * Uso em componentes:
 *
 * import { useService } from "@web/core/utils/hooks";
 *
 * setup() {
 *     const customService = useService("customService");
 *
 *     onWillStart(async () => {
 *         const data = await customService.fetchData("res.partner");
 *         console.log("Data:", data);
 *     });
 * }
 */

// ================================================================
// 6. MAIN COMPONENTS REGISTRY
// ================================================================
/**
 * Main Components são componentes estruturais que compõem o layout do Odoo.
 *
 * Exemplo: Customizar o WebClient
 */

// import { WebClient } from "@web/webclient/webclient";
// import { patch } from "@web/core/utils/patch";

// // Patch do WebClient para adicionar funcionalidade
// patch(WebClient.prototype, {
//     setup() {
//         super.setup();
//         console.log("[CustomWebClient] WebClient patched!");

//         // Adicionar lógica customizada aqui
//     },
// });

// ================================================================
// 7. VIEW REGISTRY
// ================================================================
/**
 * Views customizadas podem ser registradas para criar novos tipos de view.
 *
 * Exemplo de view customizada (Calendar, Gantt, etc):
 */

// import { registry } from "@web/core/registry";

// const customView = {
//     type: "custom_view",
//     display_name: "Custom View",
//     icon: "fa fa-th",
//     multiRecord: true,
//     Controller: CustomViewController,
//     Renderer: CustomViewRenderer,
//     Model: CustomViewModel,
//     props: (genericProps, view) => {
//         return {
//             ...genericProps,
//             // props específicas
//         };
//     },
// };

// const viewRegistry = registry.category("views");
// viewRegistry.add("custom_view", customView);

/**
 * Uso no arch XML:
 *
 * <record id="view_custom" model="ir.ui.view">
 *     <field name="name">custom.view</field>
 *     <field name="model">res.partner</field>
 *     <field name="arch" type="xml">
 *         <custom_view>
 *             <!-- configuração -->
 *         </custom_view>
 *     </field>
 * </record>
 */

// ================================================================
// 8. COMMAND PALETTE PROVIDERS
// ================================================================
/**
 * Providers para a paleta de comandos (Ctrl+K / Cmd+K)
 */

// import { Component } from "@odoo/owl";

// const customCommandProvider = {
//     namespace: "custom",
//     async provide(env, options) {
//         return [
//             {
//                 name: "Open Dashboard",
//                 action() {
//                     env.services.action.doAction("odoo_examples.ComponentListDashboard");
//                 },
//             },
//             {
//                 name: "Show Notification",
//                 action() {
//                     env.services.notification.add("Hello from command palette!", {
//                         type: "info",
//                     });
//                 },
//             },
//         ];
//     },
// };

// const commandProviderRegistry = registry.category("command_provider");
// commandProviderRegistry.add("custom_commands", customCommandProvider);

// ================================================================
// 9. FAVORITED MENU REGISTRY
// ================================================================
/**
 * Customiza como menus favoritos são exibidos
 */

// const favoritedMenuRegistry = registry.category("favorited_menu");

// ================================================================
// 10. UTILITY FUNCTIONS
// ================================================================

/**
 * Função helper para registrar múltiplos componentes de uma vez
 *
 * @param {Object} components - Objeto com componentes {tag: Component}
 * @param {string} category - Categoria do registry (padrão: "actions")
 */
export function registerComponents(components, category = "actions") {
    const reg = registry.category(category);

    Object.entries(components).forEach(([tag, component]) => {
        reg.add(tag, component);
        console.log(`[Registry] Registered ${tag} in ${category}`);
    });
}

/**
 * Função para verificar se um componente está registrado
 *
 * @param {string} tag - Tag do componente
 * @param {string} category - Categoria do registry
 * @returns {boolean}
 */
export function isComponentRegistered(tag, category = "actions") {
    const reg = registry.category(category);
    return reg.contains(tag);
}

/**
 * Função para obter todos os componentes registrados
 *
 * @param {string} category - Categoria do registry
 * @returns {Array}
 */
export function getRegisteredComponents(category = "actions") {
    const reg = registry.category(category);
    return reg.getEntries();
}

// ================================================================
// EXEMPLO DE USO DAS UTILITY FUNCTIONS
// ================================================================

// Registrar múltiplos componentes de uma vez
// registerComponents({
//     "custom.component1": Component1,
//     "custom.component2": Component2,
//     "custom.component3": Component3,
// });

// Verificar se está registrado
// if (isComponentRegistered("custom.component1")) {
//     console.log("Component is registered!");
// }

// Listar todos os registrados
// const allActions = getRegisteredComponents("actions");
// console.log("All registered actions:", allActions);

// ================================================================
// DEBUGGING E TROUBLESHOOTING
// ================================================================

/**
 * Para debugar registries no console do browser:
 *
 * // Acessar o registry
 * const { registry } = odoo.__DEBUG__.services;
 *
 * // Listar todas as categorias
 * console.log(registry.categories);
 *
 * // Ver items de uma categoria
 * const actions = registry.category("actions");
 * console.log(actions.getEntries());
 *
 * // Verificar se um item existe
 * console.log(actions.contains("odoo_examples.ComponentBasicExample"));
 *
 * // Obter um item específico
 * const component = actions.get("odoo_examples.ComponentBasicExample");
 * console.log(component);
 */

/**
 * Para forçar reload de assets em desenvolvimento:
 *
 * 1. Limpar cache do browser (Ctrl+Shift+Del)
 * 2. Usar modo desenvolvedor do Odoo: ?debug=assets
 * 3. Atualizar módulo: odoo-bin -u module_name --dev=all
 * 4. Usar Odoo Shell: /web/webclient/load_menus (força reload)
 */

console.log("[Registry] All components successfully registered!");
