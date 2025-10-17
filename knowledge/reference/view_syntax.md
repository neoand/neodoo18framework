# Sintaxe de Views (XML) no Odoo 18

## Mudancas Principais no Odoo 18

### 1. `list` vs `tree`

No Odoo 18, a tag `<tree>` foi oficialmente substituida por `<list>` para views de lista. Embora `<tree>` ainda funcione por compatibilidade, o uso de `<list>` e recomendado.

**Antes (Odoo 17 e anteriores):**
```xml
<record id="view_partner_tree" model="ir.ui.view">
    <field name="name">res.partner.tree</field>
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <tree string="Contacts">
            <field name="name"/>
            <field name="email"/>
            <field name="phone"/>
        </tree>
    </field>
</record>
```

**Agora (Odoo 18):**
```xml
<record id="view_partner_list" model="ir.ui.view">
    <field name="name">res.partner.list</field>
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <list string="Contacts">
            <field name="name"/>
            <field name="email"/>
            <field name="phone"/>
        </list>
    </field>
</record>
```

#### Novos Atributos em List Views

**`multi_edit`** - Permite edicao em massa de registros:
```xml
<list multi_edit="1">
    <field name="name"/>
    <field name="date"/>
    <field name="state"/>
</list>
```

**`editable`** - Define se a lista e editavel inline (top/bottom):
```xml
<list editable="bottom">
    <field name="product_id"/>
    <field name="quantity"/>
    <field name="price_unit"/>
</list>
```

**`expand`** - Expande automaticamente grupos:
```xml
<list expand="1">
    <field name="name"/>
    <field name="category_id"/>
</list>
```

**`limit`** - Define numero padrao de registros por pagina:
```xml
<list limit="80">
    <field name="name"/>
</list>
```

**`groups_limit`** - Limite de registros quando agrupado:
```xml
<list groups_limit="10">
    <field name="name"/>
</list>
```

**`open_form_view`** - Controla abertura do form ao clicar:
```xml
<list open_form_view="1">
    <field name="name"/>
</list>
```

**Exemplo Completo de List View Moderna:**
```xml
<record id="view_sale_order_list" model="ir.ui.view">
    <field name="name">sale.order.list</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <list string="Sales Orders"
              multi_edit="1"
              sample="1"
              expand="1"
              decoration-info="state == 'draft'"
              decoration-success="state == 'sale'">

            <header>
                <button name="action_confirm"
                        string="Confirm"
                        type="object"
                        class="btn-primary"/>
            </header>

            <field name="name" string="Order Reference"/>
            <field name="date_order" string="Order Date"/>
            <field name="partner_id"/>
            <field name="user_id" widget="many2one_avatar_user"/>
            <field name="amount_total" sum="Total"/>
            <field name="state"
                   widget="badge"
                   decoration-success="state == 'sale'"
                   decoration-info="state == 'draft'"/>

            <button name="action_view_invoice"
                    type="object"
                    string="View Invoice"
                    icon="fa-file-text-o"
                    invisible="invoice_count == 0"/>
        </list>
    </field>
</record>
```

---

## 2. Form Views

### Novos Atributos e Comportamentos

**`js_class`** - Define classe JavaScript customizada:
```xml
<form js_class="custom_form_controller">
    <sheet>
        <field name="name"/>
    </sheet>
</form>
```

**`disable_autofocus`** - Desabilita autofocus no primeiro campo:
```xml
<form disable_autofocus="1">
    <sheet>
        <field name="name"/>
    </sheet>
</form>
```

**Estrutura Moderna de Form View:**
```xml
<record id="view_partner_form" model="ir.ui.view">
    <field name="name">res.partner.form</field>
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <form string="Contact">
            <!-- Header com botoes de acao e status -->
            <header>
                <button name="action_archive"
                        string="Archive"
                        type="object"
                        invisible="active == False"/>
                <field name="state" widget="statusbar"
                       statusbar_visible="draft,open,done"/>
            </header>

            <!-- Widget de imagem/avatar -->
            <sheet>
                <widget name="web_ribbon"
                        title="Archived"
                        bg_color="text-bg-danger"
                        invisible="active == True"/>

                <field name="avatar_128"
                       widget="image"
                       class="oe_avatar"/>

                <div class="oe_title">
                    <label for="name" class="oe_edit_only"/>
                    <h1><field name="name" placeholder="Name"/></h1>
                    <field name="category_id"
                           widget="many2many_tags"
                           options="{'color_field': 'color'}"/>
                </div>

                <!-- Notebook com abas -->
                <notebook>
                    <page string="Contact Information" name="contact">
                        <group>
                            <group string="Address">
                                <field name="street"/>
                                <field name="street2"/>
                                <div class="o_address_format">
                                    <field name="city"
                                           placeholder="City"
                                           class="o_address_city"/>
                                    <field name="state_id"
                                           placeholder="State"
                                           class="o_address_state"/>
                                    <field name="zip"
                                           placeholder="ZIP"
                                           class="o_address_zip"/>
                                </div>
                                <field name="country_id"
                                       placeholder="Country"/>
                            </group>
                            <group string="Communication">
                                <field name="email"
                                       widget="email"/>
                                <field name="phone"
                                       widget="phone"/>
                                <field name="mobile"
                                       widget="phone"/>
                                <field name="website"
                                       widget="url"/>
                            </group>
                        </group>
                    </page>

                    <page string="Sales &amp; Purchase" name="sales_purchase">
                        <group>
                            <group string="Sales">
                                <field name="user_id"
                                       widget="many2one_avatar_user"/>
                                <field name="team_id"/>
                            </group>
                            <group string="Purchase">
                                <field name="property_payment_term_id"/>
                                <field name="property_supplier_payment_term_id"/>
                            </group>
                        </group>
                    </page>

                    <page string="Internal Notes" name="internal_notes">
                        <field name="comment"
                               placeholder="Internal notes..."/>
                    </page>
                </notebook>
            </sheet>

            <!-- Chatter para mensagens e atividades -->
            <chatter/>
        </form>
    </field>
</record>
```

### Widgets Modernos em Form Views

**`many2one_avatar`** - Exibe avatar em relacao many2one:
```xml
<field name="user_id" widget="many2one_avatar"/>
```

**`many2one_avatar_user`** - Especifico para usuarios:
```xml
<field name="user_id" widget="many2one_avatar_user"/>
```

**`statusbar`** - Barra de status com cliques:
```xml
<field name="state" widget="statusbar"
       statusbar_visible="draft,confirmed,done"
       clickable="1"/>
```

**`badge`** - Badge colorido para status:
```xml
<field name="priority" widget="badge"/>
```

**`percentage`** - Exibe como percentual:
```xml
<field name="completion_rate" widget="percentage"/>
```

**`monetary`** - Campo monetario com moeda:
```xml
<field name="currency_id" invisible="1"/>
<field name="amount" widget="monetary" options="{'currency_field': 'currency_id'}"/>
```

**`image`** - Exibe e permite upload de imagens:
```xml
<field name="image_1920" widget="image" class="oe_avatar" options="{'preview_image': 'image_128'}"/>
```

**`pdf_viewer`** - Visualizador de PDF inline:
```xml
<field name="pdf_file" widget="pdf_viewer"/>
```

---

## 3. Kanban Views

### Estrutura Completa de Kanban View

```xml
<record id="view_task_kanban" model="ir.ui.view">
    <field name="name">project.task.kanban</field>
    <field name="model">project.task</field>
    <field name="arch" type="xml">
        <kanban default_group_by="stage_id"
                class="o_kanban_small_column"
                on_create="quick_create"
                quick_create_view="project.quick_create_task_form"
                sample="1">

            <!-- Campos carregados para performance -->
            <field name="stage_id"/>
            <field name="user_id"/>
            <field name="priority"/>
            <field name="color"/>
            <field name="kanban_state"/>
            <field name="activity_ids"/>
            <field name="activity_state"/>

            <!-- Templates progressbar -->
            <progressbar field="kanban_state"
                        colors='{"done": "success", "blocked": "danger"}'
                        sum_field="planned_hours"/>

            <!-- Template do card -->
            <templates>
                <t t-name="kanban-box">
                    <div t-attf-class="{{!selection_mode ? 'oe_kanban_color_' + kanban_color : ''}}
                                       oe_kanban_card oe_kanban_global_click">

                        <!-- Menu dropdown do card -->
                        <div class="oe_kanban_content">
                            <div class="o_kanban_record_top">
                                <div class="o_kanban_record_headings">
                                    <strong class="o_kanban_record_title">
                                        <field name="name"/>
                                    </strong>
                                    <div class="o_kanban_record_subtitle text-muted">
                                        <field name="partner_id"/>
                                    </div>
                                </div>

                                <div class="o_dropdown_kanban dropdown">
                                    <a class="dropdown-toggle o-no-caret btn"
                                       role="button"
                                       data-bs-toggle="dropdown"
                                       href="#"
                                       aria-label="Dropdown menu"
                                       title="Dropdown menu">
                                        <span class="fa fa-ellipsis-v"/>
                                    </a>
                                    <div class="dropdown-menu" role="menu">
                                        <a role="menuitem"
                                           type="edit"
                                           class="dropdown-item">Edit</a>
                                        <a role="menuitem"
                                           type="delete"
                                           class="dropdown-item">Delete</a>
                                        <ul class="oe_kanban_colorpicker"
                                            data-field="color"/>
                                    </div>
                                </div>
                            </div>

                            <!-- Corpo do card -->
                            <div class="o_kanban_record_body">
                                <field name="tag_ids" widget="many2many_tags"
                                       options="{'color_field': 'color'}"/>

                                <div class="text-muted">
                                    <i class="fa fa-clock-o" role="img"
                                       aria-label="Deadline" title="Deadline"/>
                                    <field name="date_deadline"/>
                                </div>
                            </div>

                            <!-- Rodape do card -->
                            <div class="o_kanban_record_bottom">
                                <div class="oe_kanban_bottom_left">
                                    <field name="priority" widget="priority"/>
                                    <field name="activity_ids" widget="kanban_activity"/>
                                </div>
                                <div class="oe_kanban_bottom_right">
                                    <field name="user_id" widget="many2one_avatar_user"/>
                                </div>
                            </div>
                        </div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

### Novos Atributos em Kanban Views

**`quick_create_view`** - Define view customizada para criacao rapida:
```xml
<kanban quick_create_view="module.view_quick_create_form">
```

**`on_create`** - Comportamento ao criar (quick_create ou form):
```xml
<kanban on_create="quick_create">
```

**`sample`** - Exibe dados de exemplo quando vazio:
```xml
<kanban sample="1">
```

**`records_draggable`** - Permite arrastar cards:
```xml
<kanban records_draggable="1">
```

---

## 4. Pivot Views

### Estrutura Completa de Pivot View

```xml
<record id="view_sales_pivot" model="ir.ui.view">
    <field name="name">sale.report.pivot</field>
    <field name="model">sale.report</field>
    <field name="arch" type="xml">
        <pivot string="Sales Analysis"
               display_quantity="1"
               sample="1">

            <!-- Dimensoes (linhas e colunas) -->
            <field name="date" type="row" interval="month"/>
            <field name="product_id" type="row"/>
            <field name="user_id" type="col"/>

            <!-- Medidas (valores agregados) -->
            <field name="product_uom_qty" type="measure"/>
            <field name="price_total" type="measure"/>
            <field name="margin" type="measure"/>
        </pivot>
    </field>
</record>
```

### Atributos de Pivot Views

**`display_quantity`** - Mostra quantidade por padrao:
```xml
<pivot display_quantity="1">
```

**`disable_linking`** - Desabilita links para registros:
```xml
<pivot disable_linking="1">
```

**`sample`** - Dados de exemplo quando vazio:
```xml
<pivot sample="1">
```

### Tipos de Campos em Pivot

**`type="row"`** - Campo como linha:
```xml
<field name="category_id" type="row"/>
```

**`type="col"`** - Campo como coluna:
```xml
<field name="user_id" type="col"/>
```

**`type="measure"`** - Campo como medida agregada:
```xml
<field name="amount_total" type="measure"/>
```

**`interval`** - Intervalo para campos de data:
```xml
<field name="date_order" type="row" interval="month"/>
<!-- Opcoes: day, week, month, quarter, year -->
```

---

## 5. Graph Views

### Estrutura Completa de Graph View

```xml
<record id="view_sales_graph" model="ir.ui.view">
    <field name="name">sale.order.graph</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <graph string="Sales Dashboard"
               type="bar"
               stacked="1"
               sample="1"
               order="desc">

            <field name="date_order" interval="month"/>
            <field name="amount_total" type="measure"/>
            <field name="state" group="1"/>
        </graph>
    </field>
</record>
```

### Tipos de Graficos

**`type="bar"`** - Grafico de barras:
```xml
<graph type="bar">
    <field name="date" interval="month"/>
    <field name="amount" type="measure"/>
</graph>
```

**`type="line"`** - Grafico de linhas:
```xml
<graph type="line">
    <field name="date" interval="day"/>
    <field name="count" type="measure"/>
</graph>
```

**`type="pie"`** - Grafico de pizza:
```xml
<graph type="pie">
    <field name="category_id"/>
    <field name="amount" type="measure"/>
</graph>
```

### Atributos de Graph Views

**`stacked`** - Empilha valores:
```xml
<graph type="bar" stacked="1">
```

**`order`** - Ordena por valor (asc/desc):
```xml
<graph order="desc">
```

**`sample`** - Dados de exemplo:
```xml
<graph sample="1">
```

**`disable_linking`** - Desabilita links:
```xml
<graph disable_linking="1">
```

---

## 6. Calendar Views

### Estrutura Completa de Calendar View

```xml
<record id="view_calendar_event" model="ir.ui.view">
    <field name="name">calendar.event.calendar</field>
    <field name="model">calendar.event</field>
    <field name="arch" type="xml">
        <calendar string="Meetings"
                  date_start="start"
                  date_stop="stop"
                  date_delay="duration"
                  color="partner_id"
                  event_open_popup="1"
                  quick_create="1"
                  mode="month"
                  form_view_id="%(view_calendar_event_form)d">

            <field name="name"/>
            <field name="partner_id"
                   avatar_field="avatar_128"
                   write_model="filter_partner_id"
                   write_field="partner_id"/>
            <field name="allday"/>
        </calendar>
    </field>
</record>
```

### Atributos de Calendar Views

**Campos de Data/Hora:**
- `date_start` - Campo de inicio (obrigatorio)
- `date_stop` - Campo de fim
- `date_delay` - Campo de duracao (alternativa ao date_stop)
- `all_day` - Campo booleano para eventos de dia inteiro

**Visualizacao:**
- `mode` - Modo inicial: day, week, month, year
- `color` - Campo para colorir eventos
- `event_open_popup` - Abre popup ao clicar
- `quick_create` - Permite criacao rapida
- `form_view_id` - ID da view de formulario

**Exemplo Completo:**
```xml
<calendar date_start="date_begin"
          date_stop="date_end"
          color="user_id"
          mode="week"
          quick_create="0"
          event_open_popup="1"
          create="1"
          delete="1"
          edit="1">

    <field name="name"/>
    <field name="user_id"
           avatar_field="avatar_128"
           write_model="res.users"
           write_field="user_id"/>
    <field name="partner_id"/>
    <field name="location"/>
</calendar>
```

---

## 7. Activity Views

### Estrutura de Activity View

```xml
<record id="view_lead_activity" model="ir.ui.view">
    <field name="name">crm.lead.activity</field>
    <field name="model">crm.lead</field>
    <field name="arch" type="xml">
        <activity string="Leads">
            <field name="user_id"/>
            <templates>
                <div t-name="activity-box">
                    <img t-att-src="activity_image('crm.lead', 'avatar_128', record.user_id.raw_value)"
                         role="img"
                         t-att-title="record.user_id.value"
                         t-att-alt="record.user_id.value"/>
                    <div>
                        <field name="name" display="full"/>
                        <div class="text-muted">
                            <field name="partner_id"/>
                            <field name="expected_revenue" widget="monetary"/>
                        </div>
                    </div>
                </div>
            </templates>
        </activity>
    </field>
</record>
```

### Atributos de Activity Views

- Agrupa registros por tipo de atividade
- Exibe timeline de atividades pendentes
- Permite agendar e completar atividades
- Mostra atividades atrasadas em vermelho

---

## 8. Search Views

### Estrutura Completa de Search View

```xml
<record id="view_partner_search" model="ir.ui.view">
    <field name="name">res.partner.search</field>
    <field name="model">res.partner</field>
    <field name="arch" type="xml">
        <search string="Search Contacts">
            <!-- Campos de busca -->
            <field name="name"
                   string="Contact"
                   filter_domain="['|', ('name', 'ilike', self), ('ref', 'ilike', self)]"/>
            <field name="email"/>
            <field name="phone"/>
            <field name="category_id"
                   string="Tags"
                   filter_domain="[('category_id', 'ilike', self)]"/>
            <field name="user_id"/>

            <!-- Separador -->
            <separator/>

            <!-- Filtros -->
            <filter string="My Contacts"
                    name="my_contacts"
                    domain="[('user_id', '=', uid)]"/>
            <filter string="Customers"
                    name="customer"
                    domain="[('customer_rank', '>', 0)]"/>
            <filter string="Suppliers"
                    name="supplier"
                    domain="[('supplier_rank', '>', 0)]"/>

            <separator/>

            <filter string="Companies"
                    name="companies"
                    domain="[('is_company', '=', True)]"/>
            <filter string="Individuals"
                    name="individuals"
                    domain="[('is_company', '=', False)]"/>

            <separator/>

            <filter string="Archived"
                    name="inactive"
                    domain="[('active', '=', False)]"/>

            <!-- Agrupamentos -->
            <group expand="0" string="Group By">
                <filter string="Salesperson"
                        name="salesperson"
                        context="{'group_by': 'user_id'}"/>
                <filter string="Country"
                        name="country"
                        context="{'group_by': 'country_id'}"/>
                <filter string="Tags"
                        name="tags"
                        context="{'group_by': 'category_id'}"/>
            </group>

            <!-- Busca favoritos -->
            <searchpanel>
                <field name="category_id"
                       icon="fa-users"
                       color="#875A7B"
                       select="multi"
                       enable_counters="1"/>
                <field name="country_id"
                       icon="fa-globe"
                       select="multi"
                       enable_counters="1"/>
            </searchpanel>
        </search>
    </field>
</record>
```

### Novos Recursos em Search Views

**Search Panel** - Painel lateral de filtros:
```xml
<searchpanel>
    <field name="category_id"
           icon="fa-tags"
           select="multi"
           enable_counters="1"
           expand="1"/>
</searchpanel>
```

**Filtros com Dominio Dinamico:**
```xml
<filter name="my_records"
        string="My Records"
        domain="[('user_id', '=', uid)]"/>
```

**Agrupamento por Data com Intervalo:**
```xml
<filter string="Order Month"
        name="order_month"
        context="{'group_by': 'date_order:month'}"/>
```

---

## 9. Cohort Views (Novo no Odoo 18)

### Estrutura de Cohort View

```xml
<record id="view_cohort" model="ir.ui.view">
    <field name="name">subscription.cohort</field>
    <field name="model">sale.subscription</field>
    <field name="arch" type="xml">
        <cohort string="Subscription Cohort"
                date_start="date_start"
                date_stop="date"
                interval="week"
                mode="churn"
                timeline="forward"
                measure="mrr">
        </cohort>
    </field>
</record>
```

### Atributos de Cohort Views

- `date_start` - Data de inicio da cohort
- `date_stop` - Data de medicao
- `interval` - Intervalo (day, week, month)
- `mode` - Modo (retention ou churn)
- `timeline` - Direcao (forward ou backward)
- `measure` - Campo para medir

---

## 10. Decorators e Estilos

### Decorators de Linha (List/Tree Views)

```xml
<list decoration-bf="state == 'draft'"
      decoration-it="state == 'cancel'"
      decoration-danger="date_deadline and date_deadline &lt; current_date"
      decoration-warning="date_deadline == current_date"
      decoration-success="state == 'done'"
      decoration-info="state == 'progress'"
      decoration-muted="state == 'cancel'">
    <field name="name"/>
    <field name="state" invisible="1"/>
    <field name="date_deadline" invisible="1"/>
</list>
```

**Decorators Disponiveis:**
- `decoration-bf` - Bold (negrito)
- `decoration-it` - Italic (italico)
- `decoration-danger` - Vermelho
- `decoration-warning` - Laranja/Amarelo
- `decoration-success` - Verde
- `decoration-info` - Azul
- `decoration-muted` - Cinza

---

## 11. Atributos Globais

### Atributos Comuns em Todas as Views

**`create`** - Permite criar registros:
```xml
<list create="1">
```

**`delete`** - Permite deletar registros:
```xml
<list delete="1">
```

**`edit`** - Permite editar registros:
```xml
<list edit="1">
```

**`import`** - Permite importar dados:
```xml
<list import="1">
```

**`export`** - Permite exportar dados:
```xml
<list export_xlsx="1">
```

**`sample`** - Exibe dados de exemplo:
```xml
<kanban sample="1">
```

---

## 12. Widgets Especiais

### Novos Widgets no Odoo 18

**`CopyClipboardChar`** - Copia texto para clipboard:
```xml
<field name="access_token" widget="CopyClipboardChar"/>
```

**`many2many_tags_email`** - Tags com validacao de email:
```xml
<field name="email_cc" widget="many2many_tags_email"/>
```

**`statinfo`** - Botao estatistico:
```xml
<button name="action_view_orders" type="object" class="oe_stat_button" icon="fa-shopping-cart">
    <field name="order_count" widget="statinfo" string="Orders"/>
</button>
```

**`attachment_image`** - Imagem como anexo:
```xml
<field name="image" widget="attachment_image"/>
```

**`ace`** - Editor de codigo:
```xml
<field name="code" widget="ace" options="{'mode': 'python'}"/>
```

---

## 13. Exemplo Completo de Modulo

### Arquivo views.xml Completo

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- List View -->
    <record id="view_product_list" model="ir.ui.view">
        <field name="name">product.template.list</field>
        <field name="model">product.template</field>
        <field name="arch" type="xml">
            <list string="Products"
                  multi_edit="1"
                  sample="1"
                  decoration-danger="qty_available &lt; 0"
                  decoration-warning="qty_available &lt; 10">
                <field name="default_code"/>
                <field name="name"/>
                <field name="categ_id"/>
                <field name="list_price"/>
                <field name="qty_available"/>
                <field name="active" invisible="1"/>
            </list>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_product_form" model="ir.ui.view">
        <field name="name">product.template.form</field>
        <field name="model">product.template</field>
        <field name="arch" type="xml">
            <form string="Product">
                <header>
                    <button name="action_archive"
                            string="Archive"
                            type="object"
                            invisible="active == False"/>
                </header>
                <sheet>
                    <field name="image_1920"
                           widget="image"
                           class="oe_avatar"/>
                    <div class="oe_title">
                        <label for="name"/>
                        <h1><field name="name" placeholder="Product Name"/></h1>
                    </div>
                    <notebook>
                        <page string="General Information" name="general">
                            <group>
                                <group>
                                    <field name="default_code"/>
                                    <field name="categ_id"/>
                                </group>
                                <group>
                                    <field name="list_price"/>
                                    <field name="standard_price"/>
                                </group>
                            </group>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <!-- Kanban View -->
    <record id="view_product_kanban" model="ir.ui.view">
        <field name="name">product.template.kanban</field>
        <field name="model">product.template</field>
        <field name="arch" type="xml">
            <kanban sample="1">
                <field name="id"/>
                <field name="name"/>
                <field name="list_price"/>
                <field name="image_128"/>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_card">
                            <div class="o_kanban_image">
                                <img t-att-src="kanban_image('product.template', 'image_128', record.id.raw_value)"
                                     alt="Product"/>
                            </div>
                            <div class="oe_kanban_details">
                                <strong class="o_kanban_record_title">
                                    <field name="name"/>
                                </strong>
                                <div class="o_kanban_record_subtitle">
                                    <field name="list_price" widget="monetary"/>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_product_search" model="ir.ui.view">
        <field name="name">product.template.search</field>
        <field name="model">product.template</field>
        <field name="arch" type="xml">
            <search string="Products">
                <field name="name"/>
                <field name="default_code"/>
                <field name="categ_id"/>
                <separator/>
                <filter string="Services"
                        name="services"
                        domain="[('type', '=', 'service')]"/>
                <filter string="Products"
                        name="products"
                        domain="[('type', '=', 'product')]"/>
                <group expand="0" string="Group By">
                    <filter string="Category"
                            name="category"
                            context="{'group_by': 'categ_id'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Action -->
    <record id="action_product_template" model="ir.actions.act_window">
        <field name="name">Products</field>
        <field name="res_model">product.template</field>
        <field name="view_mode">kanban,list,form</field>
        <field name="search_view_id" ref="view_product_search"/>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first product
            </p>
        </field>
    </record>
</odoo>
```

---

## Resumo das Principais Mudancas

1. **`<list>` substitui `<tree>`** - Nova nomenclatura semantica
2. **Novos atributos**: `multi_edit`, `sample`, `expand`, `groups_limit`
3. **Widgets modernos**: `many2one_avatar_user`, `badge`, `statinfo`
4. **Search Panel**: Filtros laterais interativos
5. **Cohort Views**: Nova view para analise de cohorts
6. **Melhorias em Kanban**: Quick create customizavel
7. **Graph Views**: Mais opcoes de visualizacao
8. **Calendar Views**: Melhor suporte a eventos recorrentes
9. **Decorators**: Mais opcoes de estilizacao condicional
10. **Performance**: Views otimizadas com lazy loading

---

## Referencias e Documentacao Oficial

- Odoo 18 Documentation: https://www.odoo.com/documentation/18.0/
- View Architecture: https://www.odoo.com/documentation/18.0/developer/reference/backend/views.html
- OWL Framework: https://github.com/odoo/owl
