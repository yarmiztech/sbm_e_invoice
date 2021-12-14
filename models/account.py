from odoo import fields, models,api,_
from uuid import uuid4
import qrcode
import base64
import logging

from lxml import etree




class AccountMove(models.Model):
    _inherit = "account.move"

    work_order = fields.Char()
    date_of_supply = fields.Date()
    place_of_supply = fields.Char()
    po_number = fields.Char()
    delivery_no = fields.Char()

    def _ubl_add_attachments(self, parent_node, ns, version="2.1"):
        self.ensure_one()
        self.billing_refence(parent_node, ns, version="2.1")
        # if self.decoded_data:
        self.testing()
        self.qr_code(parent_node, ns, version="2.1")
        self.qr_1code(parent_node, ns, version="2.1")
        self.pih_code(parent_node, ns, version="2.1")

        # self.signature_refence(parent_node, ns, version="2.1")
        # if self.company_id.embed_pdf_in_ubl_xml_invoice and not self.env.context.get(
        #     "no_embedded_pdf"
        # ):
        # self.signature_refence(parent_node, ns, version="2.1")
        filename = "Invoice-" + self.name + ".pdf"
        docu_reference = etree.SubElement(
            parent_node, ns["cac"] + "AdditionalDocumentReference"
        )
        docu_reference_id = etree.SubElement(docu_reference, ns["cbc"] + "ID")
        docu_reference_id.text = filename
        attach_node = etree.SubElement(docu_reference, ns["cac"] + "Attachment")
        binary_node = etree.SubElement(
            attach_node,
            ns["cbc"] + "EmbeddedDocumentBinaryObject",
            mimeCode="application/pdf",
            filename=filename,
        )
        ctx = dict()
        ctx["no_embedded_ubl_xml"] = True
        ctx["force_report_rendering"] = True
        # pdf_inv = (
        #     self.with_context(ctx)
        #     .env.ref("account.account_invoices")
        #     ._render_qweb_pdf(self.ids)[0]
        # )
        ########changed########################
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_1')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2b')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2b_credit')._render_qweb_pdf(self.ids)[0]
        # pdf_inv = self.with_context(ctx).env.ref(
        #     'account_invoice_ubl.account_invoices_b2b_debit')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2c')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2c_credit')._render_qweb_pdf(self.ids)[0]
        # +++++++++++++++++++++++++++++++OUR CUSTOMES ADD HERE+++++++++++++++++++++++++++++++++++++
        # pdf_inv = self.with_context(ctx).env.ref(
        pdf_inv = \
        self.with_context(ctx).env.ref('sbm_e_invoice.sbm_invoice_report')._render_qweb_pdf(
            self.ids)[0]

        # -----------------------------aboveeeeeeee---------------------------------

        binary_node.text = base64.b64encode(pdf_inv)
        # self.qr3_code(parent_node, ns, version="2.1")

        # filename = "ICV"
        # icv_reference = etree.SubElement(
        #     parent_node, ns["cac"] + "AdditionalDocumentReference"
        # )
        # icv_reference_id = etree.SubElement(icv_reference, ns["cbc"] + "ID")
        # icv_reference_id.text = filename
        # icv_reference_node = etree.SubElement(icv_reference, ns["cac"] + "UUID")
        # icv_reference_node.text = self.name

    @api.model
    def _get_invoice_report_names(self):
        return [
            "account.report_invoice",
            "account.report_invoice_with_payments",
            "account_invoice_ubl.report_invoice_1",
            "account_invoice_ubl.report_invoice_b2b",
            "account_invoice_ubl.report_invoice_b2b_credit",
            # "account_invoice_ubl.report_invoice_b2b_debit",
            "account_invoice_ubl.report_invoice_b2c",
            "account_invoice_ubl.report_invoice_b2c_credit",
            # "account_invoice_ubl.report_invoice_b2c_debit",
            "sbm_e_invoice.sbm_invoice_report",

        ]



    # def disc(self):
    #     for line in self.invoice_line_ids:
    #         disct=line.discount
    #         return disct

    check_amount_in_words = fields.Char()

    # # @api.depends('price_unit')
    # def ar_invoice_date(self):
    #     m = str(self.invoice_date)
    #     if m.split('-'):
    #         interger_part_arabic = ''
    #         for each in m.split('-'):
    #             if interger_part_arabic:
    #                 interger_part_arabic = interger_part_arabic + '-'
    #             interger_part_arabic += convert_numbers.english_to_arabic(int(each))
    #
    #     print('interger_part_arabic')
    #     return interger_part_arabic
    #         # else:
    #         #     line.ar_invoice_date = "-"
    #
    #
    #
    #
    # def total_price(self):
    #     for line in self.invoice_line_ids:
    #         day_book = self.env['account.tax'].search(
    #             [('name', '=', line.tax_ids.name), ('type_tax_use', '=', line.tax_ids.type_tax_use)])
    #         print(day_book)
    #         # total=sum(day_book.children_tax_ids.mapped('amount'))
    #         # print(total)
    #         # return total
    #         amount = 0
    #
    #         total = 0.0
    #         tot = 0
    #         amount = line.price_unit
    #         total = total + day_book.amount / 100
    #
    #         tot = amount * total
    #
    #         amount=amount + tot
    #         return amount






    def amount_words(self):
        # amount_total_words = self.currency_id.amount_to_text(self.amount_total)
        return self.currency_id.amount_to_text(self.amount_total)

    def calculate_discount(self):
        disct = 0
        for line in self.invoice_line_ids:
           disct = line.discount
        return disct

    def testing(self):
        # data = "\n BROTHERS GROUP55\n"+"\n300090000000003\n"+"\n2021-11-05T13:45:38\n"+"\n9.00'+'\n1.18"
        # data = "  BROTHERS GROUP     300090000000003  2021-11-08T13:45:38  9.00  1.18"
        # data = ""+"BROTHERS GROUP   "+""+"300090000000003"+""+"2021-11-08"+"T"+"13:45:38"+""+"9.00"+""+"1.18"
        leng = len(self.company_id.name)
        company_name = self.company_id.name
        if 17 > leng:
            for r in range(17 - leng):
                if len(company_name) != 17:
                    company_name += ' '
                else:
                    break
        else:
            if 17 < leng:
                company_name = company_name[:17]
        vat_leng = len(self.company_id.vat)
        vat_name = self.company_id.vat
        if 17 > vat_leng:
            for r in range(15 - vat_leng):
                if len(vat_name) != 15:
                    vat_name += ' '
                else:
                    break
        else:
            if 17 < leng:
                vat_name = vat_name[:17]

        amount_total = str(round(self.amount_total))
        amount_leng = len(str(round(self.amount_total)))
        if len(amount_total) < 17:
            for r in range(17 - amount_leng):
                if len(amount_total) != 17:
                    amount_total += ' '
                else:
                    break

        tax_leng = len(str(round(self.amount_tax)))
        amount_tax_total = str(round(self.amount_tax))
        if len(amount_tax_total) < 17:
            for r in range(17 - tax_leng):
                if len(amount_tax_total) != 17:
                    amount_tax_total += ' '
                else:
                    break

        # print("The number of digits in the number are:", amount_total)

        # data = ""+'Salah Hospital'+""+'31012239350000311123'+""+'2023-01-01'+"T"+str(self.datetime_field.time())+""+str(200.00)+""+str(-125.00)
        # data = ""+str(company_name)+""+str(self.company_id.vat)+""+str(self.invoice_date)+"T"+str(self.datetime_field.time())+""+str(self.amount_total)+""+str(self.amount_tax)
        # data = ""+str(company_name)+""+str(self.company_id.vat)+""+str(self.invoice_date)+"T"+str(self.datetime_field.time())+""+str(self.amount_total)+""+str(self.amount_tax)+""+'nMkXME2tSovykLKU6VUnIq8667SMCoc6A7tKcMKpY0 ='+""+"3056301006072"
        # data = ""+str(company_name)+""+str(self.company_id.vat)+""+str(self.invoice_date)+"T"+str(self.datetime_field.time())+"Z"+""+str(self.amount_total)+""+str(self.amount_tax)

        # data = ""+str(company_name)+""+str(self.company_id.vat)+""+str(self.invoice_date)+"T"+str(self.datetime_field.time())+"Z"+""+amount_total+""+amount_tax_total

        data = "" + str(company_name) + "" + str(vat_name) + "" + str(self.invoice_date) + "T" + str(
            self.datetime_field.time()) + "Z" + "" + amount_total + "" + amount_tax_total
        import base64
        mou = base64.b64encode(bytes(data, 'utf-8'))
        # print(str(mou),'888888888888')
        # print(mou.decode(),'111888888888888')
        # mou =
        #
        # qr_image = base64.b64encode(data)
        # # self.qr_code_image = qr_image
        # # print(base64.b64decode(data),'jjjjjjjjjjjjjjjjjj')
        # print(self.qr_code_image.decode())
        # print(base64.b64decode(data))
        self.decoded_data = str(mou.decode())
        # test =mou.decode('ascii')
        # print(self.decoded_data,'decoded_data')
        # print(test,'test')

        ####below 3 working
        # return 'AQpGaXJzdCBTaG9wAg8zMTAxODkzNzU5MjAwMDMDFDIwMjEtMDEtMDVUMDk6MzI6NDBaBAYyNTAuMDAFBDEwLjAwBkA4YjBhNWY5OWFkNjIxM2Y1ZmRiYTNmMmRiOGY5ODlmYjk5MmMwYWI0ODZhMjkyMmIyMjFiMTViYzg2Mzg5ZDVh'
        # return 'ARFGaXJzdCBTaG9wICAgICAgIAIPMzEwMTg5Mzc1OTIwMDAzAxQyMDIxLTAxLTA1VDA5OjMyOjQwWgQGMjUwLjAwBQQxMC4wMAZAOGIwYTVmOTlhZDYyMTNmNWZkYmEzZjJkYjhmOTg5ZmI5OTJjMGFiNDg2YTI5MjJiMjIxYjE1YmM4NjM4OWQ1YQ=='
        # return 'ARFGaXJzdCBTaG9wICAgICAgIAIPMzEwMTg5Mzc1OTIwMDAzAxQyMDIxLTAxLTA1VDA5OjMyOjQwWgQGMTI1OTAwBQY2MDAwMDAGQDhiMGE1Zjk5YWQ2MjEzZjVmZGJhM2YyZGI4Zjk4OWZiOTkyYzBhYjQ4NmEyOTIyYjIyMWIxNWJjODYzODlkNWE='

        #
        #
        # First
        # Shop       3101893759200032021 - 01 - 05
        # T09: 32:40
        # Z250.0010.00
        #
        # @8
        #
        # b0a5f99ad6213f5fdba3f2db8f989fb992c0ab486a2922b221b15bc86389d5a

        return str(mou.decode())

        # return 'ARFCUk9USEVSUyBHUk9VUCAgIAIPMzAwMDkwMDAwMDAwMDAzAxMyMDIxLTExLTA4VDEzOjQ1OjM4BAQ5LjAwBQQxLjE4'

    # @api.depends('amount_total')
    # def compute_total_words(self):
    #     for invoice in self:
    #         amount_total_words = invoice.currency_id.amount_to_text(invoice.amount_total)
    #         print(amount_total_words)
    #     return amount_total_words


    # def amount_to_words(self):
    #     amount_total_words = self.currency_id.amount_to_text(self.amount_total)
    #     # print(invoice.currency_id,"currency")
    #     print(amount_total_words)
    #     return amount_total_words






    datetime_field = fields.Datetime(string="Create Date", default=lambda self: fields.Datetime.now())
    decoded_data = fields.Char(string="Decoded Data")

    # def total_amount_to_words_natcom(self):
    #     for invoice in self:
    #         print(invoice.amount_total)
    #         print(invoice.currency_id)
    #         # amount_total_words = invoice.currency_id.amount_to_text(invoice.amount_total)
    #         amount_total_words = invoice.currency_id.amount_to_text(invoice.amount_untaxed)
    #         print(amount_total_words)
    #         return invoice.currency_id.amount_to_text(invoice.amount_untaxed)


    # def total_amount_to_words(self):
    #     self.check_amount_in_words = self.currency_id.amount_to_text(self.amount_untaxed)
    #     print(self.check_amount_in_words)
    #     # return self.check_amount_in_words
    #     return self.currency_id.amount_to_text(self.amount_untaxed)

    # @api.onchange('




class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def tax(self):
        day_book = self.env['account.tax'].search([('name', '=', self.tax_ids.name),('type_tax_use','=',self.tax_ids.type_tax_use)])
        # total=sum(day_book.children_tax_ids.mapped('amount'))
        # print(total)
        # return total
        total = 0.0
        # for line in day_book.children_tax_ids:
        amount = self.price_unit
        total=total + day_book.amount/100

        tot=amount * total
        # # amount=line.mapped('amount')
        # # amount = sum(m.mapped('amount'))
        # return amount
        return tot

    def compute_amount_tax(self):
        amount = 0
        for line in self.tax_ids:
            amount = amount + line.amount
        return (self.price_subtotal * amount)/100

    def compute_amount_total(self):
        amount = 0
        for line in self.tax_ids:
            amount = amount + line.amount
        return ((self.price_subtotal * amount) / 100) + self.price_subtotal

    def total_tax(self):
        for line in self.invoice_line_ids:

         day_book = self.env['account.tax'].search([('name', '=', line.tax_ids.name),('type_tax_use','=',line.tax_ids.type_tax_use)])
        # total=sum(day_book.children_tax_ids.mapped('amount'))
        # print(total)
        # return total
        #  amount = 0

         # total = 0.0
         # tot = 0
         # amount = line.price_unit
         # amount = line.price_subtotal
         # total+= amount * day_book.amount/100
         #
         # tot=amount * total
         # print(total)
            # # amount=line.mapped('amount')
            # # amount = sum(m.mapped('amount'))
            # return amount
         # return tot


    def price(self):
        day_book = self.env['account.tax'].search(
            [('name', '=', self.tax_ids.name), ('type_tax_use', '=', self.tax_ids.type_tax_use)])
        total = 0.0
        # for line in day_book.children_tax_ids:
        amount = self.price_unit
        total = total + day_book.amount / 100

        tot = amount * total

        amount=amount + tot
        return amount

    #     # day_book = self.env['account.tax'].search([('name', '=', self.tax_ids.name)])
    #     # print(day_book)
    #     # for m in day_book.children_tax_ids:
    #     #     amount=m.mapped('amount')
    #     #     return amount
    #
    #
    #

    # datetime_field = fields.Datetime(string="Create Date", default=lambda self: fields.Datetime.now())
    # decoded_data = fields.Char(string="Decoded Data")


    # def ghju(self):


    # datetime_field=fields.Datetime()





class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    @classmethod
    def _get_invoice_reports_ubl(cls):
        return [
            "account.report_invoice",
            'account_invoice_ubl.report_invoice_1',
            'account_invoice_ubl.report_invoice_b2b',
            'account_invoice_ubl.report_invoice_b2b_credit',
            'account_invoice_ubl.report_invoice_b2b_debit',
            'account_invoice_ubl.report_invoice_b2c',
            'account_invoice_ubl.report_invoice_b2c_credit',
            'account_invoice_ubl.report_invoice_b2c_debit',
            "account.report_invoice_with_payments",
            "account.account_invoice_report_duplicate_main",
            "sbm_e_invoice.invoice_format_view4",

        ]
