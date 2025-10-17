# -*- coding: utf-8 -*-
"""
================================================================================
EXEMPLO COMPLETO DE REPORT EXCEL - ODOO 18
================================================================================

Este arquivo demonstra a criação de relatórios Excel usando xlsxwriter.
Inclui: criação de worksheets, formatação de células, fórmulas, gráficos,
múltiplas abas, export de dados e comentários explicativos.

Requisitos:
    - pip install xlsxwriter

Estrutura:
    1. Controller para download do relatório
    2. Classe base para relatórios Excel
    3. Exemplos de relatórios específicos
    4. Formatações e estilos
    5. Gráficos e visualizações

================================================================================
"""

import io
import base64
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
import logging

_logger = logging.getLogger(__name__)

try:
    import xlsxwriter
except ImportError:
    _logger.warning('Cannot import xlsxwriter. Excel reports will not work.')
    xlsxwriter = None


# =============================================================================
# 1. WIZARD PARA GERAÇÃO DO RELATÓRIO
# =============================================================================
class ExcelReportWizard(models.TransientModel):
    """
    Wizard para coletar parâmetros e gerar o relatório Excel.
    Este é o ponto de entrada para o usuário.
    """
    _name = 'excel.report.wizard'
    _description = 'Excel Report Wizard'

    # -------------------------------------------------------------------------
    # CAMPOS DO WIZARD
    # -------------------------------------------------------------------------
    date_from = fields.Date(
        string='Date From',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1)
    )
    date_to = fields.Date(
        string='Date To',
        required=True,
        default=fields.Date.today
    )
    partner_ids = fields.Many2many(
        'res.partner',
        string='Customers',
        help='Leave empty to include all customers'
    )
    report_type = fields.Selection([
        ('summary', 'Summary Report'),
        ('detailed', 'Detailed Report'),
        ('comparison', 'Comparison Report'),
    ], string='Report Type', required=True, default='summary')
    include_charts = fields.Boolean(
        string='Include Charts',
        default=True,
        help='Include visual charts in the report'
    )

    # -------------------------------------------------------------------------
    # MÉTODOS DE AÇÃO
    # -------------------------------------------------------------------------
    def action_generate_report(self):
        """
        Gera o relatório Excel baseado nos parâmetros selecionados.
        Retorna uma ação para download do arquivo.
        """
        self.ensure_one()

        # Validações
        if self.date_from > self.date_to:
            raise UserError(_('Date From cannot be greater than Date To.'))

        # Determina qual relatório gerar
        if self.report_type == 'summary':
            report = SalesReportExcelSummary(self)
        elif self.report_type == 'detailed':
            report = SalesReportExcelDetailed(self)
        else:
            report = SalesReportExcelComparison(self)

        # Gera o relatório
        try:
            xlsx_file = report.generate_report()
        except Exception as e:
            _logger.exception("Error generating Excel report")
            raise UserError(_('Error generating report: %s') % str(e))

        # Cria o attachment para download
        filename = report.get_filename()
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(xlsx_file),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        # Retorna ação para download
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }


# =============================================================================
# 2. CLASSE BASE PARA RELATÓRIOS EXCEL
# =============================================================================
class ExcelReportBase:
    """
    Classe base para todos os relatórios Excel.
    Fornece métodos comuns e estrutura básica.
    """

    def __init__(self, wizard):
        """
        Inicializa o relatório com os parâmetros do wizard.

        Args:
            wizard: Instância do wizard com os parâmetros
        """
        self.wizard = wizard
        self.env = wizard.env
        self.workbook = None
        self.output = None
        self.formats = {}

    # -------------------------------------------------------------------------
    # MÉTODOS DE CONFIGURAÇÃO
    # -------------------------------------------------------------------------
    def _setup_workbook(self):
        """
        Configura o workbook e cria formatos de célula padrão.
        """
        # Cria buffer de memória para o arquivo Excel
        self.output = io.BytesIO()

        # Cria workbook com opções
        self.workbook = xlsxwriter.Workbook(self.output, {
            'in_memory': True,
            'default_date_format': 'dd/mm/yyyy',
            'remove_timezone': True,
        })

        # Define formatos padrão
        self._create_formats()

    def _create_formats(self):
        """
        Cria todos os formatos de célula usados no relatório.
        Os formatos são armazenados no dicionário self.formats.
        """
        # Formato para título principal
        self.formats['title'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 16,
            'bold': True,
            'font_color': '#FFFFFF',
            'bg_color': '#2C3E50',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
        })

        # Formato para subtítulos
        self.formats['subtitle'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 12,
            'bold': True,
            'font_color': '#2C3E50',
            'bg_color': '#ECF0F1',
            'align': 'left',
            'valign': 'vcenter',
            'border': 1,
        })

        # Formato para cabeçalho de tabela
        self.formats['header'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'bold': True,
            'font_color': '#FFFFFF',
            'bg_color': '#34495E',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True,
        })

        # Formato para células de dados normais
        self.formats['cell'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'align': 'left',
            'valign': 'vcenter',
            'border': 1,
        })

        # Formato para células numéricas
        self.formats['number'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '#,##0.00',
        })

        # Formato para células de moeda
        self.formats['currency'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,##0.00',
        })

        # Formato para percentuais
        self.formats['percent'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '0.00%',
        })

        # Formato para datas
        self.formats['date'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'num_format': 'dd/mm/yyyy',
        })

        # Formato para data e hora
        self.formats['datetime'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'num_format': 'dd/mm/yyyy hh:mm',
        })

        # Formato para totalizadores
        self.formats['total'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'bold': True,
            'font_color': '#FFFFFF',
            'bg_color': '#27AE60',
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,##0.00',
        })

        # Formato para subtotais
        self.formats['subtotal'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'bold': True,
            'bg_color': '#D5DBDB',
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,##0.00',
        })

        # Formato para valores negativos (vermelho)
        self.formats['negative'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'font_color': '#E74C3C',
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,##0.00',
        })

        # Formato para valores positivos (verde)
        self.formats['positive'] = self.workbook.add_format({
            'font_name': 'Arial',
            'font_size': 10,
            'font_color': '#27AE60',
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '$#,##0.00',
        })

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES
    # -------------------------------------------------------------------------
    def _write_header(self, worksheet, row, col, data):
        """
        Escreve um cabeçalho de coluna.

        Args:
            worksheet: Worksheet onde escrever
            row: Linha
            col: Coluna
            data: Texto do cabeçalho
        """
        worksheet.write(row, col, data, self.formats['header'])

    def _write_cell(self, worksheet, row, col, data, format_name='cell'):
        """
        Escreve uma célula com formato específico.

        Args:
            worksheet: Worksheet onde escrever
            row: Linha
            col: Coluna
            data: Dados a escrever
            format_name: Nome do formato a usar
        """
        fmt = self.formats.get(format_name, self.formats['cell'])
        worksheet.write(row, col, data, fmt)

    def _write_title(self, worksheet, title, merge_range='A1:F1'):
        """
        Escreve o título principal do relatório.

        Args:
            worksheet: Worksheet onde escrever
            title: Texto do título
            merge_range: Range de células para merge
        """
        worksheet.merge_range(merge_range, title, self.formats['title'])
        worksheet.set_row(0, 30)  # Altura da linha do título

    def _write_info_section(self, worksheet, row_start):
        """
        Escreve seção de informações do relatório (parâmetros, data, etc).

        Args:
            worksheet: Worksheet onde escrever
            row_start: Linha inicial

        Returns:
            int: Próxima linha disponível
        """
        row = row_start

        # Data de geração
        worksheet.write(row, 0, 'Generated on:', self.formats['subtitle'])
        worksheet.write(row, 1, datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                       self.formats['cell'])
        row += 1

        # Período do relatório
        worksheet.write(row, 0, 'Period:', self.formats['subtitle'])
        period_text = f"{self.wizard.date_from.strftime('%d/%m/%Y')} to {self.wizard.date_to.strftime('%d/%m/%Y')}"
        worksheet.write(row, 1, period_text, self.formats['cell'])
        row += 1

        # Filtros aplicados
        if self.wizard.partner_ids:
            worksheet.write(row, 0, 'Customers:', self.formats['subtitle'])
            partners = ', '.join(self.wizard.partner_ids.mapped('name'))
            worksheet.write(row, 1, partners, self.formats['cell'])
            row += 1

        # Linha em branco
        row += 1

        return row

    def _get_data(self):
        """
        Método abstrato para obter os dados do relatório.
        Deve ser implementado nas classes filhas.

        Returns:
            dict: Dados do relatório
        """
        raise NotImplementedError("Subclasses must implement _get_data()")

    def generate_report(self):
        """
        Método principal para gerar o relatório.
        Orquestra todo o processo de geração.

        Returns:
            bytes: Conteúdo do arquivo Excel
        """
        # Setup inicial
        self._setup_workbook()

        # Gera o conteúdo (implementado nas subclasses)
        self._generate_content()

        # Fecha o workbook e retorna os bytes
        self.workbook.close()
        self.output.seek(0)
        return self.output.read()

    def _generate_content(self):
        """
        Método abstrato para gerar o conteúdo do relatório.
        Deve ser implementado nas classes filhas.
        """
        raise NotImplementedError("Subclasses must implement _generate_content()")

    def get_filename(self):
        """
        Gera o nome do arquivo Excel.

        Returns:
            str: Nome do arquivo
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"report_{timestamp}.xlsx"


# =============================================================================
# 3. RELATÓRIO DE VENDAS - RESUMO
# =============================================================================
class SalesReportExcelSummary(ExcelReportBase):
    """
    Relatório de vendas em formato de resumo.
    Contém uma visão geral com totalizadores.
    """

    def _get_data(self):
        """
        Obtém os dados de vendas do banco de dados.

        Returns:
            dict: Dicionário com os dados organizados
        """
        # Domain base para filtrar pedidos
        domain = [
            ('date_order', '>=', self.wizard.date_from),
            ('date_order', '<=', self.wizard.date_to),
            ('state', 'in', ['sale', 'done']),
        ]

        # Adiciona filtro de parceiros se selecionado
        if self.wizard.partner_ids:
            domain.append(('partner_id', 'in', self.wizard.partner_ids.ids))

        # Busca os pedidos
        orders = self.env['sale.order'].search(domain, order='date_order desc')

        # Agrupa dados por cliente
        data = {}
        for order in orders:
            partner_key = order.partner_id.id

            if partner_key not in data:
                data[partner_key] = {
                    'partner': order.partner_id,
                    'orders': [],
                    'total': 0.0,
                    'qty': 0,
                }

            data[partner_key]['orders'].append(order)
            data[partner_key]['total'] += order.amount_total
            data[partner_key]['qty'] += len(order.order_line)

        return data

    def _generate_content(self):
        """
        Gera o conteúdo do relatório de resumo.
        """
        # Cria a worksheet principal
        ws_summary = self.workbook.add_worksheet('Summary')

        # Obtém os dados
        data = self._get_data()

        # Escreve o título
        self._write_title(ws_summary, 'SALES REPORT - SUMMARY', 'A1:F1')

        # Escreve seção de informações
        row = self._write_info_section(ws_summary, row_start=2)

        # Cabeçalhos da tabela
        headers = ['Customer', 'Orders', 'Total Items', 'Total Amount', 'Avg Order', '% of Total']
        for col, header in enumerate(headers):
            self._write_header(ws_summary, row, col, header)
        row += 1

        # Calcula total geral para percentuais
        grand_total = sum(d['total'] for d in data.values())

        # Escreve dados dos clientes
        data_start_row = row
        for partner_data in sorted(data.values(), key=lambda x: x['total'], reverse=True):
            partner = partner_data['partner']
            order_count = len(partner_data['orders'])
            total_items = partner_data['qty']
            total_amount = partner_data['total']
            avg_order = total_amount / order_count if order_count else 0
            percentage = (total_amount / grand_total * 100) if grand_total else 0

            # Nome do cliente
            self._write_cell(ws_summary, row, 0, partner.name)

            # Número de pedidos
            self._write_cell(ws_summary, row, 1, order_count, 'number')

            # Total de itens
            self._write_cell(ws_summary, row, 2, total_items, 'number')

            # Valor total
            self._write_cell(ws_summary, row, 3, total_amount, 'currency')

            # Média por pedido
            self._write_cell(ws_summary, row, 4, avg_order, 'currency')

            # Percentual do total
            self._write_cell(ws_summary, row, 5, percentage / 100, 'percent')

            row += 1

        # Linha de total
        total_orders = sum(len(d['orders']) for d in data.values())
        total_items = sum(d['qty'] for d in data.values())

        ws_summary.write(row, 0, 'TOTAL', self.formats['total'])
        ws_summary.write(row, 1, total_orders, self.formats['total'])
        ws_summary.write(row, 2, total_items, self.formats['total'])
        ws_summary.write(row, 3, grand_total, self.formats['total'])
        ws_summary.write(row, 4, '', self.formats['total'])
        ws_summary.write(row, 5, 1.0, self.formats['total'])

        # Ajusta largura das colunas
        ws_summary.set_column('A:A', 30)  # Customer
        ws_summary.set_column('B:B', 12)  # Orders
        ws_summary.set_column('C:C', 15)  # Total Items
        ws_summary.set_column('D:D', 15)  # Total Amount
        ws_summary.set_column('E:E', 15)  # Avg Order
        ws_summary.set_column('F:F', 12)  # % of Total

        # Adiciona gráfico se solicitado
        if self.wizard.include_charts:
            self._add_summary_chart(ws_summary, data_start_row, row)

    def _add_summary_chart(self, worksheet, data_start_row, data_end_row):
        """
        Adiciona um gráfico de pizza ao relatório de resumo.

        Args:
            worksheet: Worksheet onde adicionar o gráfico
            data_start_row: Linha inicial dos dados
            data_end_row: Linha final dos dados
        """
        # Cria gráfico de pizza
        chart = self.workbook.add_chart({'type': 'pie'})

        # Adiciona série de dados
        chart.add_series({
            'name': 'Sales by Customer',
            'categories': [worksheet.name, data_start_row, 0, data_end_row - 1, 0],
            'values': [worksheet.name, data_start_row, 3, data_end_row - 1, 3],
            'data_labels': {'percentage': True},
        })

        # Configura título e estilo
        chart.set_title({'name': 'Sales Distribution by Customer'})
        chart.set_style(10)

        # Insere o gráfico na worksheet
        worksheet.insert_chart('H2', chart, {
            'x_scale': 1.5,
            'y_scale': 1.5
        })

    def get_filename(self):
        """Retorna nome do arquivo específico para este relatório."""
        date_str = self.wizard.date_from.strftime('%Y%m%d')
        return f"sales_summary_{date_str}.xlsx"


# =============================================================================
# 4. RELATÓRIO DE VENDAS - DETALHADO
# =============================================================================
class SalesReportExcelDetailed(ExcelReportBase):
    """
    Relatório de vendas detalhado.
    Contém todos os pedidos e linhas de pedido.
    """

    def _get_data(self):
        """
        Obtém os dados detalhados de vendas.

        Returns:
            recordset: Pedidos de venda
        """
        # Domain base
        domain = [
            ('date_order', '>=', self.wizard.date_from),
            ('date_order', '<=', self.wizard.date_to),
            ('state', 'in', ['sale', 'done']),
        ]

        # Filtro de parceiros
        if self.wizard.partner_ids:
            domain.append(('partner_id', 'in', self.wizard.partner_ids.ids))

        # Busca pedidos
        orders = self.env['sale.order'].search(domain, order='date_order desc, name')

        return orders

    def _generate_content(self):
        """
        Gera o conteúdo do relatório detalhado.
        Cria múltiplas worksheets: uma por cliente + resumo geral.
        """
        # Obtém os dados
        orders = self._get_data()

        # Agrupa pedidos por cliente
        orders_by_partner = {}
        for order in orders:
            partner_id = order.partner_id.id
            if partner_id not in orders_by_partner:
                orders_by_partner[partner_id] = {
                    'partner': order.partner_id,
                    'orders': []
                }
            orders_by_partner[partner_id]['orders'].append(order)

        # Cria worksheet de resumo geral
        self._create_overview_sheet(orders_by_partner)

        # Cria uma worksheet para cada cliente (máximo 10 para não ficar muito pesado)
        for idx, (partner_id, data) in enumerate(
            sorted(orders_by_partner.items(),
                   key=lambda x: sum(o.amount_total for o in x[1]['orders']),
                   reverse=True)[:10]
        ):
            self._create_partner_sheet(data['partner'], data['orders'])

    def _create_overview_sheet(self, orders_by_partner):
        """
        Cria worksheet com visão geral de todos os pedidos.

        Args:
            orders_by_partner: Dicionário com pedidos agrupados por parceiro
        """
        ws = self.workbook.add_worksheet('Overview')

        # Título
        self._write_title(ws, 'SALES REPORT - DETAILED', 'A1:H1')

        # Informações
        row = self._write_info_section(ws, row_start=2)

        # Cabeçalhos
        headers = ['Order', 'Date', 'Customer', 'Salesperson', 'Items', 'Subtotal', 'Taxes', 'Total']
        for col, header in enumerate(headers):
            self._write_header(ws, row, col, header)
        row += 1

        # Dados dos pedidos
        data_start_row = row
        grand_total = 0.0

        for partner_data in orders_by_partner.values():
            for order in partner_data['orders']:
                # Número do pedido
                self._write_cell(ws, row, 0, order.name)

                # Data do pedido
                self._write_cell(ws, row, 1, order.date_order.strftime('%d/%m/%Y'), 'date')

                # Cliente
                self._write_cell(ws, row, 2, order.partner_id.name)

                # Vendedor
                self._write_cell(ws, row, 3, order.user_id.name if order.user_id else '')

                # Número de itens
                self._write_cell(ws, row, 4, len(order.order_line), 'number')

                # Subtotal
                self._write_cell(ws, row, 5, order.amount_untaxed, 'currency')

                # Impostos
                self._write_cell(ws, row, 6, order.amount_tax, 'currency')

                # Total
                self._write_cell(ws, row, 7, order.amount_total, 'currency')

                grand_total += order.amount_total
                row += 1

        # Linha de total
        ws.write(row, 0, 'TOTAL', self.formats['total'])
        ws.write(row, 1, '', self.formats['total'])
        ws.write(row, 2, '', self.formats['total'])
        ws.write(row, 3, '', self.formats['total'])
        ws.write(row, 4, '', self.formats['total'])
        ws.write(row, 5, '', self.formats['total'])
        ws.write(row, 6, '', self.formats['total'])
        ws.write(row, 7, grand_total, self.formats['total'])

        # Ajusta colunas
        ws.set_column('A:A', 15)
        ws.set_column('B:B', 12)
        ws.set_column('C:C', 30)
        ws.set_column('D:D', 20)
        ws.set_column('E:E', 10)
        ws.set_column('F:G', 15)
        ws.set_column('H:H', 15)

        # Congela painéis (fixa cabeçalhos)
        ws.freeze_panes(data_start_row, 0)

        # Adiciona filtro automático
        ws.autofilter(data_start_row - 1, 0, row - 1, 7)

    def _create_partner_sheet(self, partner, orders):
        """
        Cria worksheet detalhada para um cliente específico.

        Args:
            partner: Registro do parceiro
            orders: Lista de pedidos do parceiro
        """
        # Nome da worksheet (limitado a 31 caracteres)
        sheet_name = partner.name[:28] + '...' if len(partner.name) > 28 else partner.name
        # Remove caracteres inválidos
        sheet_name = sheet_name.replace('/', '-').replace('\\', '-').replace('*', '').replace('[', '').replace(']', '')

        ws = self.workbook.add_worksheet(sheet_name)

        # Título
        self._write_title(ws, f'CUSTOMER: {partner.name}', 'A1:I1')

        # Informações do cliente
        row = 2
        ws.write(row, 0, 'Customer Code:', self.formats['subtitle'])
        ws.write(row, 1, partner.ref or '', self.formats['cell'])
        row += 1

        ws.write(row, 0, 'Email:', self.formats['subtitle'])
        ws.write(row, 1, partner.email or '', self.formats['cell'])
        row += 1

        ws.write(row, 0, 'Phone:', self.formats['subtitle'])
        ws.write(row, 1, partner.phone or '', self.formats['cell'])
        row += 2

        # Cabeçalhos para linhas de pedido
        headers = ['Order', 'Date', 'Product', 'Description', 'Qty', 'Unit', 'Unit Price', 'Discount %', 'Subtotal']
        for col, header in enumerate(headers):
            self._write_header(ws, row, col, header)
        row += 1

        # Dados das linhas de pedido
        order_totals = {}
        for order in orders:
            order_start_row = row

            for line in order.order_line:
                # Número do pedido
                self._write_cell(ws, row, 0, order.name)

                # Data
                self._write_cell(ws, row, 1, order.date_order.strftime('%d/%m/%Y'))

                # Produto
                self._write_cell(ws, row, 2, line.product_id.name)

                # Descrição
                description = line.name if line.name != line.product_id.name else ''
                self._write_cell(ws, row, 3, description)

                # Quantidade
                self._write_cell(ws, row, 4, line.product_uom_qty, 'number')

                # Unidade
                self._write_cell(ws, row, 5, line.product_uom.name)

                # Preço unitário
                self._write_cell(ws, row, 6, line.price_unit, 'currency')

                # Desconto
                self._write_cell(ws, row, 7, line.discount / 100 if line.discount else 0, 'percent')

                # Subtotal
                self._write_cell(ws, row, 8, line.price_subtotal, 'currency')

                row += 1

            # Subtotal do pedido
            ws.write(row, 0, f'Subtotal {order.name}', self.formats['subtotal'])
            for col in range(1, 8):
                ws.write(row, col, '', self.formats['subtotal'])
            ws.write(row, 8, order.amount_total, self.formats['subtotal'])
            row += 1

        # Total geral do cliente
        total = sum(order.amount_total for order in orders)
        ws.write(row, 0, 'GRAND TOTAL', self.formats['total'])
        for col in range(1, 8):
            ws.write(row, col, '', self.formats['total'])
        ws.write(row, 8, total, self.formats['total'])

        # Ajusta colunas
        ws.set_column('A:A', 15)
        ws.set_column('B:B', 12)
        ws.set_column('C:C', 30)
        ws.set_column('D:D', 40)
        ws.set_column('E:E', 10)
        ws.set_column('F:F', 10)
        ws.set_column('G:G', 12)
        ws.set_column('H:H', 12)
        ws.set_column('I:I', 15)

    def get_filename(self):
        """Retorna nome do arquivo."""
        date_str = self.wizard.date_from.strftime('%Y%m%d')
        return f"sales_detailed_{date_str}.xlsx"


# =============================================================================
# 5. RELATÓRIO DE COMPARAÇÃO COM GRÁFICOS
# =============================================================================
class SalesReportExcelComparison(ExcelReportBase):
    """
    Relatório de comparação entre períodos.
    Inclui gráficos de linha e barras para visualização.
    """

    def _get_data(self):
        """
        Obtém dados de dois períodos para comparação.

        Returns:
            dict: Dados dos dois períodos
        """
        # Calcula período anterior
        days_diff = (self.wizard.date_to - self.wizard.date_from).days
        previous_date_to = self.wizard.date_from - timedelta(days=1)
        previous_date_from = previous_date_to - timedelta(days=days_diff)

        # Função auxiliar para buscar dados de um período
        def get_period_data(date_from, date_to):
            domain = [
                ('date_order', '>=', date_from),
                ('date_order', '<=', date_to),
                ('state', 'in', ['sale', 'done']),
            ]
            if self.wizard.partner_ids:
                domain.append(('partner_id', 'in', self.wizard.partner_ids.ids))

            orders = self.env['sale.order'].search(domain)

            # Agrupa por mês
            monthly_data = {}
            for order in orders:
                month_key = order.date_order.strftime('%Y-%m')
                if month_key not in monthly_data:
                    monthly_data[month_key] = {
                        'orders': 0,
                        'amount': 0.0,
                        'items': 0,
                    }
                monthly_data[month_key]['orders'] += 1
                monthly_data[month_key]['amount'] += order.amount_total
                monthly_data[month_key]['items'] += len(order.order_line)

            return monthly_data

        # Obtém dados dos dois períodos
        current_data = get_period_data(self.wizard.date_from, self.wizard.date_to)
        previous_data = get_period_data(previous_date_from, previous_date_to)

        return {
            'current': current_data,
            'previous': previous_data,
            'current_period': (self.wizard.date_from, self.wizard.date_to),
            'previous_period': (previous_date_from, previous_date_to),
        }

    def _generate_content(self):
        """
        Gera o conteúdo do relatório de comparação.
        """
        # Obtém dados
        data = self._get_data()

        # Cria worksheet
        ws = self.workbook.add_worksheet('Comparison')

        # Título
        self._write_title(ws, 'SALES COMPARISON REPORT', 'A1:H1')

        # Informações dos períodos
        row = 2
        ws.write(row, 0, 'Current Period:', self.formats['subtitle'])
        ws.write(row, 1, f"{data['current_period'][0].strftime('%d/%m/%Y')} to {data['current_period'][1].strftime('%d/%m/%Y')}", self.formats['cell'])
        row += 1

        ws.write(row, 0, 'Previous Period:', self.formats['subtitle'])
        ws.write(row, 1, f"{data['previous_period'][0].strftime('%d/%m/%Y')} to {data['previous_period'][1].strftime('%d/%m/%Y')}", self.formats['cell'])
        row += 2

        # Cabeçalhos
        headers = ['Month', 'Current Orders', 'Current Amount', 'Previous Orders', 'Previous Amount', 'Orders Var %', 'Amount Var %', 'Trend']
        for col, header in enumerate(headers):
            self._write_header(ws, row, col, header)
        row += 1

        data_start_row = row

        # Combina todos os meses únicos
        all_months = sorted(set(list(data['current'].keys()) + list(data['previous'].keys())))

        # Escreve dados comparativos
        for month in all_months:
            current = data['current'].get(month, {'orders': 0, 'amount': 0.0})
            previous = data['previous'].get(month, {'orders': 0, 'amount': 0.0})

            # Calcula variações
            orders_var = ((current['orders'] - previous['orders']) / previous['orders'] * 100) if previous['orders'] else 0
            amount_var = ((current['amount'] - previous['amount']) / previous['amount'] * 100) if previous['amount'] else 0

            # Mês
            self._write_cell(ws, row, 0, month)

            # Pedidos atuais
            self._write_cell(ws, row, 1, current['orders'], 'number')

            # Valor atual
            self._write_cell(ws, row, 2, current['amount'], 'currency')

            # Pedidos anteriores
            self._write_cell(ws, row, 3, previous['orders'], 'number')

            # Valor anterior
            self._write_cell(ws, row, 4, previous['amount'], 'currency')

            # Variação de pedidos
            format_name = 'positive' if orders_var >= 0 else 'negative'
            self._write_cell(ws, row, 5, orders_var / 100, 'percent')

            # Variação de valor
            format_name = 'positive' if amount_var >= 0 else 'negative'
            self._write_cell(ws, row, 6, amount_var / 100, 'percent')

            # Trend (ícone)
            trend = '↑' if amount_var > 0 else '↓' if amount_var < 0 else '→'
            self._write_cell(ws, row, 7, trend)

            row += 1

        # Ajusta colunas
        ws.set_column('A:A', 12)
        ws.set_column('B:B', 15)
        ws.set_column('C:C', 18)
        ws.set_column('D:D', 15)
        ws.set_column('E:E', 18)
        ws.set_column('F:F', 15)
        ws.set_column('G:G', 15)
        ws.set_column('H:H', 8)

        # Adiciona gráficos
        if self.wizard.include_charts:
            self._add_comparison_charts(ws, data_start_row, row - 1)

    def _add_comparison_charts(self, worksheet, data_start_row, data_end_row):
        """
        Adiciona gráficos de comparação.

        Args:
            worksheet: Worksheet onde adicionar
            data_start_row: Linha inicial dos dados
            data_end_row: Linha final dos dados
        """
        # Gráfico de linhas para valores
        chart1 = self.workbook.add_chart({'type': 'line'})

        # Série período atual
        chart1.add_series({
            'name': 'Current Period',
            'categories': [worksheet.name, data_start_row, 0, data_end_row, 0],
            'values': [worksheet.name, data_start_row, 2, data_end_row, 2],
            'line': {'color': '#27AE60', 'width': 2},
            'marker': {'type': 'circle', 'size': 6},
        })

        # Série período anterior
        chart1.add_series({
            'name': 'Previous Period',
            'categories': [worksheet.name, data_start_row, 0, data_end_row, 0],
            'values': [worksheet.name, data_start_row, 4, data_end_row, 4],
            'line': {'color': '#3498DB', 'width': 2},
            'marker': {'type': 'square', 'size': 6},
        })

        chart1.set_title({'name': 'Sales Comparison - Line Chart'})
        chart1.set_x_axis({'name': 'Month'})
        chart1.set_y_axis({'name': 'Amount', 'num_format': '$#,##0'})
        chart1.set_style(10)

        worksheet.insert_chart('J2', chart1, {'x_scale': 2, 'y_scale': 1.5})

        # Gráfico de barras para variação percentual
        chart2 = self.workbook.add_chart({'type': 'column'})

        chart2.add_series({
            'name': 'Amount Variation %',
            'categories': [worksheet.name, data_start_row, 0, data_end_row, 0],
            'values': [worksheet.name, data_start_row, 6, data_end_row, 6],
            'fill': {'color': '#E74C3C'},
        })

        chart2.set_title({'name': 'Sales Variation %'})
        chart2.set_x_axis({'name': 'Month'})
        chart2.set_y_axis({'name': 'Variation %', 'num_format': '0%'})
        chart2.set_style(11)

        worksheet.insert_chart('J24', chart2, {'x_scale': 2, 'y_scale': 1.5})

    def get_filename(self):
        """Retorna nome do arquivo."""
        date_str = self.wizard.date_from.strftime('%Y%m%d')
        return f"sales_comparison_{date_str}.xlsx"


# =============================================================================
# NOTAS E BOAS PRÁTICAS
# =============================================================================
"""
RECURSOS AVANÇADOS DO XLSXWRITER:

1. FORMATAÇÃO CONDICIONAL:
   worksheet.conditional_format('A1:A10', {
       'type': 'cell',
       'criteria': '>',
       'value': 1000,
       'format': positive_format
   })

2. VALIDAÇÃO DE DADOS:
   worksheet.data_validation('B2:B10', {
       'validate': 'list',
       'source': ['Option 1', 'Option 2', 'Option 3']
   })

3. COMENTÁRIOS EM CÉLULAS:
   worksheet.write_comment('A1', 'This is a comment')

4. PROTEÇÃO DE WORKSHEET:
   worksheet.protect('password', options)

5. FÓRMULAS:
   worksheet.write_formula('D2', '=SUM(B2:C2)')

6. SPARKLINES (mini gráficos em células):
   worksheet.add_sparkline('F2', {
       'range': 'A2:E2',
       'type': 'column'
   })

7. RICH TEXT:
   worksheet.write_rich_string('A1',
       'This is ', bold, 'bold', ' and this is ', italic, 'italic')

8. HYPERLINKS:
   worksheet.write_url('A1', 'https://example.com', string='Click here')

PERFORMANCE:

1. Use constant_memory=True para arquivos muito grandes
2. Minimize formatações únicas (reuse formatos)
3. Evite muitas worksheets (máximo ~30-40)
4. Use write_row() e write_column() para múltiplos valores

DEBUGGING:

1. Use try/except para capturar erros
2. Log progressos importantes
3. Valide dados antes de escrever
4. Teste com datasets pequenos primeiro

"""
