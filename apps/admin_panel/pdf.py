"""
Fiche Finale PDF (commandes + bons de livraison) — reproduction du design app mobile.

- Fiche Finale Commandes  → all_orders_screen_admin.dart  : titre 18pt, cartes par commande
- Fiche Finale Livraisons → admin_delivery_requests_screen.dart : en-tête logo + cartes
  avec footer fixe en bas (même technique que le Bon de Livraison)
"""
from io import BytesIO
from datetime import date as _date
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, SimpleDocTemplate,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether, PageBreak,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

pt = 1

GREY200  = colors.Color(0.933, 0.933, 0.933)
GREY300  = colors.Color(0.878, 0.878, 0.878)
GREY400  = colors.Color(0.741, 0.741, 0.741)
GREY600  = colors.Color(0.459, 0.459, 0.459)
GREY_TXT = colors.Color(0.4, 0.4, 0.4)

PAGE_W, PAGE_H = A4

# Fiche Finale Commandes : marges all(20) comme le mobile
FC_LM = FC_RM = FC_TM = FC_BM = 20
FC_W  = PAGE_W - FC_LM - FC_RM

# Fiche Finale Livraisons : marges identiques au Bon de Livraison
FL_LM = FL_RM = 36
FL_TM = 28
FL_BM = 24
FL_W  = PAGE_W - FL_LM - FL_RM

# Positions fixes pour footer / Service Client (livraisons)
Y_SERVICE_CLIENT = 154
Y_DIVIDER        = 42
Y_FOOTER_START   = 33
FOOTER_LINE_H    = 11
RESERVED_BOTTOM  = 170

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGO_PATHS = [
    BASE_DIR / 'static' / 'images' / 'logo.png',
    Path(r'c:\Users\HP I7\Desktop\Optic Vison\optic_vision\assets\images\logo.png'),
]


def _logo_path():
    for p in LOGO_PATHS:
        if p.exists():
            return str(p)
    return None


def _company_name_rich(name: str) -> str:
    parts = []
    for word in name.split():
        if word == '&':
            parts.append('<font color="#1F77B5" size="20"><b> &amp; </b></font>')
        else:
            parts.append(
                f'<font color="#D46104" size="20"><b>{word[0]}</b></font>'
                f'<font color="#1F77B5" size="20"><b>{word[1:]}</b></font>'
            )
        parts.append(' ')
    return ''.join(parts).strip()


def _val(d: dict, key: str) -> str:
    v = d.get(key)
    return str(v) if v else '-'


# ─────────────────────────────────────────────────────────────────────────────
# FICHE FINALE COMMANDES
# Source : all_orders_screen_admin.dart → _generatePdfBytes()
# Design mobile : titre seul 18pt centré, cartes bordées par commande
# ─────────────────────────────────────────────────────────────────────────────

def _order_card(order: dict, card_w: float) -> Table:
    """Carte d'une commande (container bordé 0.5pt, identique au mobile)."""
    inner_w = card_w - 20  # -20 pour les paddings gauche+droite de la carte

    def _c(text, bold=False):
        return Paragraph(
            f'<b>{text}</b>' if bold else text,
            ParagraphStyle('c', fontSize=10,
                           fontName='Helvetica-Bold' if bold else 'Helvetica',
                           alignment=TA_CENTER, leading=13),
        )

    def _cl(text, bold=False):
        return Paragraph(
            f'<b>{text}</b>' if bold else text,
            ParagraphStyle('cl', fontSize=10,
                           fontName='Helvetica-Bold' if bold else 'Helvetica',
                           alignment=TA_LEFT, leading=13),
        )

    # Table prescription (colonnes ÉGALES — mobile : defaultColumnWidth = FlexColumnWidth())
    col_w5 = inner_w / 5
    presc = Table(
        [
            [_c('Œil', bold=True), _c('SPH', bold=True), _c('CYL', bold=True),
             _c('Axe', bold=True), _c('Add', bold=True)],
            [_cl('R'), _c(_val(order, 'rightSph')), _c(_val(order, 'rightCyl')),
             _c(_val(order, 'rightAxe')), _c(_val(order, 'rightAdd'))],
            [_cl('L'), _c(_val(order, 'leftSph')),  _c(_val(order, 'leftCyl')),
             _c(_val(order, 'leftAxe')),  _c(_val(order, 'leftAdd'))],
        ],
        colWidths=[col_w5] * 5,
    )
    presc.setStyle(TableStyle([
        ('BOX',           (0, 0), (-1, -1), 0.5, colors.black),
        ('INNERGRID',     (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 4),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
    ]))

    inner = [
        Paragraph(f'<b>{order.get("shopName", "—")}</b>',
                  ParagraphStyle('shop', fontSize=12, fontName='Helvetica-Bold', leading=15)),
        Paragraph(f'<b>{order.get("wearerName", "—")}</b>',
                  ParagraphStyle('wear', fontSize=12, fontName='Helvetica-Bold', leading=15)),
        Spacer(1, 6),
        presc,
        Spacer(1, 6),
        Paragraph(f'<b>{order.get("treatmentOption", "—")}</b>',
                  ParagraphStyle('treat', fontSize=11, fontName='Helvetica-Bold', leading=14)),
    ]

    card = Table([[inner]], colWidths=[card_w])
    card.setStyle(TableStyle([
        ('BOX',           (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    return card


def generate_fiche_finale_orders(orders: list, company: dict,
                                  date_from: str = None, date_to: str = None) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=FC_LM, rightMargin=FC_RM,
        topMargin=FC_TM,  bottomMargin=FC_BM,
    )
    story = []
    comp_name = company.get('name', 'OPTIQUE & DISTRIBUTION')

    # Titre centré 18pt bold — mobile : "FICHE FINALE - OPTIQUE & DISTRIBUTION"
    story.append(Paragraph(
        f'<b>FICHE FINALE - {comp_name.upper()}</b>',
        ParagraphStyle('title', fontSize=18, fontName='Helvetica-Bold',
                       alignment=TA_CENTER, leading=22),
    ))
    story.append(Spacer(1, 10))

    today  = _date.today().strftime('%d/%m/%Y')
    d_from = date_from or today
    d_to   = date_to   or today
    story.append(Paragraph(
        f'Période : {d_from} - {d_to}',
        ParagraphStyle('p', fontSize=12, fontName='Helvetica', leading=15),
    ))

    story.append(Paragraph(
        f'Nombre de commandes : {len(orders)}',
        ParagraphStyle('cnt', fontSize=12, fontName='Helvetica', leading=15),
    ))
    story.append(Spacer(1, 15))

    if not orders:
        story.append(Paragraph(
            'Aucune commande pour cette période.',
            ParagraphStyle('empty', fontSize=11, fontName='Helvetica'),
        ))
    else:
        for order in orders:
            story.append(KeepTogether(_order_card(order, FC_W)))
            story.append(Spacer(1, 15))

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# FICHE FINALE LIVRAISONS
# Source : admin_delivery_requests_screen.dart → _exportToPdf()
# Design mobile : en-tête logo + footer fixe + cartes par livraison
# ─────────────────────────────────────────────────────────────────────────────

def _make_fl_on_page(company: dict):
    """Callback canvas pour chaque page : Service Client + divider + footer."""
    def on_page(canvas, doc):
        canvas.saveState()
        cx = PAGE_W / 2

        # Service Client (italic bold 11pt, aligné à droite)
        canvas.setFont('Helvetica-BoldOblique', 11)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.drawRightString(PAGE_W - FL_RM, Y_SERVICE_CLIENT, 'Service Client')

        # Divider
        canvas.setStrokeColorRGB(0.741, 0.741, 0.741)
        canvas.setLineWidth(0.5)
        canvas.line(FL_LM, Y_DIVIDER, PAGE_W - FL_RM, Y_DIVIDER)

        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.setFillColorRGB(0.4, 0.4, 0.4)
        lines = []
        addr = company.get('address', '')
        tel  = company.get('phone', '')
        line1 = f'{addr}  Tél : {tel}' if (addr and tel) else (addr or tel)
        if line1.strip():
            lines.append(line1)
        if company.get('ncc'):
            lines.append(f'NCC : {company["ncc"]}')
        if company.get('rccm'):
            lines.append(f'RCCM : {company["rccm"]}')
        y = Y_FOOTER_START
        for line in lines:
            canvas.drawCentredString(cx, y, line)
            y -= FOOTER_LINE_H

        canvas.restoreState()

    return on_page


def _delivery_card(d: dict, card_w: float) -> Table:
    """Carte d'un bon de livraison (même structure que commande)."""
    inner_w = card_w - 20

    def _c(text, bold=False):
        return Paragraph(
            f'<b>{text}</b>' if bold else text,
            ParagraphStyle('c', fontSize=10,
                           fontName='Helvetica-Bold' if bold else 'Helvetica',
                           alignment=TA_CENTER, leading=13),
        )

    def _cl(text, bold=False):
        return Paragraph(
            f'<b>{text}</b>' if bold else text,
            ParagraphStyle('cl', fontSize=10,
                           fontName='Helvetica-Bold' if bold else 'Helvetica',
                           alignment=TA_LEFT, leading=13),
        )

    # Table prescription : ratio 2:1:1:1:1 (identique au Bon de Livraison)
    cw = [inner_w * 2/6] + [inner_w / 6] * 4
    presc = Table(
        [
            [_c('', bold=True), _c('SPH', bold=True), _c('CYL', bold=True),
             _c('AXE', bold=True), _c('ADD', bold=True)],
            [_cl('OD (Droit)', bold=True),
             _c(_val(d, 'rightSph')), _c(_val(d, 'rightCyl')),
             _c(_val(d, 'rightAxe')), _c(_val(d, 'rightAdd'))],
            [_cl('OG (Gauche)', bold=True),
             _c(_val(d, 'leftSph')),  _c(_val(d, 'leftCyl')),
             _c(_val(d, 'leftAxe')),  _c(_val(d, 'leftAdd'))],
        ],
        colWidths=cw,
    )
    presc.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  GREY200),
        ('BOX',           (0, 0), (-1, -1), 0.5, GREY600),
        ('INNERGRID',     (0, 0), (-1, -1), 0.5, GREY600),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))

    created  = d.get('createdAt')
    date_str = created.strftime('%d/%m/%Y') if hasattr(created, 'strftime') else ''
    type_v   = d.get('typeVerre') or '—'
    treat    = d.get('treatmentOption') or '—'

    inner = [
        Paragraph(f'<b>{d.get("shopName", "—")}</b>',
                  ParagraphStyle('shop', fontSize=12, fontName='Helvetica-Bold', leading=15)),
        Paragraph(f'<b>{d.get("wearerName", "—")}</b>',
                  ParagraphStyle('wear', fontSize=12, fontName='Helvetica-Bold', leading=15)),
        Spacer(1, 6),
        presc,
        Spacer(1, 6),
        Paragraph(f'{type_v} — <b>{treat}</b>',
                  ParagraphStyle('meta', fontSize=11, fontName='Helvetica', leading=14)),
    ]
    if date_str:
        inner.append(
            Paragraph(date_str,
                      ParagraphStyle('date', fontSize=9, fontName='Helvetica',
                                     leading=12, textColor=GREY_TXT))
        )

    card = Table([[inner]], colWidths=[card_w])
    card.setStyle(TableStyle([
        ('BOX',           (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    return card


def _build_bon_livraison_page(d: dict, comp_name: str, comp_desc: str, logo_p) -> list:
    """
    Retourne la liste de flowables pour UN bon de livraison complet (une page).
    Identique à generate_bon_livraison dans deliveries/pdf.py.
    """
    els = []
    body = ParagraphStyle('body', fontSize=11, fontName='Helvetica', leading=14)

    # ── EN-TÊTE ──────────────────────────────────────────────────────────────
    if logo_p:
        logo_img  = Image(logo_p, width=62, height=62)
        name_para = Paragraph(
            _company_name_rich(comp_name),
            ParagraphStyle('cn', alignment=TA_LEFT, leading=24),
        )
        desc_para = Paragraph(
            f'<font color="#666666" size="10"><i>{comp_desc}</i></font>',
            ParagraphStyle('cd', alignment=TA_LEFT, leading=13),
        )
        NAME_COL_W = 260
        right_col = Table([[name_para], [desc_para]], colWidths=[NAME_COL_W])
        right_col.setStyle(TableStyle([
            ('TOPPADDING',    (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING',   (0, 0), (-1, -1), 0),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (0, 0),   3),
        ]))
        header_t = Table([[logo_img, right_col]], colWidths=[74, NAME_COL_W])
        header_t.hAlign = 'CENTER'
        header_t.setStyle(TableStyle([
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING',   (0, 0), (-1, -1), 0),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
            ('TOPPADDING',    (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        els.append(header_t)
    else:
        els.append(Paragraph(_company_name_rich(comp_name),
                              ParagraphStyle('cn', alignment=TA_CENTER)))
        els.append(Paragraph(
            f'<font color="#666666" size="10"><i>{comp_desc}</i></font>',
            ParagraphStyle('cd', alignment=TA_CENTER)))

    els.append(Spacer(1, 10))
    els.append(HRFlowable(width='100%', thickness=0.5, color=GREY400))
    els.append(Spacer(1, 18))

    # ── TITRE ────────────────────────────────────────────────────────────────
    els.append(Paragraph(
        '<b>BON DE LIVRAISON N° ___________________</b>',
        ParagraphStyle('title', fontSize=13, fontName='Helvetica-Bold',
                       alignment=TA_CENTER),
    ))
    els.append(Spacer(1, 20))

    # ── BLOC CLIENT ──────────────────────────────────────────────────────────
    els.append(Paragraph(f'Client : {d.get("shopName") or "-"}', body))
    els.append(Spacer(1, 4))
    phone = d.get('phoneNumber', '')
    if phone:
        els.append(Paragraph(f'Tél : {phone}', body))
        els.append(Spacer(1, 4))
    els.append(Paragraph(f'Patient : {d.get("wearerName") or "Non spécifié"}', body))
    els.append(Spacer(1, 4))
    created  = d.get('createdAt')
    date_str = created.strftime('%d/%m/%Y') if hasattr(created, 'strftime') else 'Inconnue'
    els.append(Paragraph(f'Date : {date_str}', body))
    els.append(Spacer(1, 24))

    # ── TABLEAU DÉSIGNATION ───────────────────────────────────────────────────
    type_v = d.get('typeVerre') or '-'
    treat  = d.get('treatmentOption') or '-'
    row_style = ParagraphStyle('dr', fontSize=10, fontName='Helvetica', leading=13)
    hdr_style = ParagraphStyle('dh', fontSize=11, fontName='Helvetica-Bold',
                               alignment=TA_CENTER, leading=14)
    desig_t = Table(
        [
            [Paragraph('<b>DÉSIGNATION</b>', hdr_style)],
            [Paragraph('Libellé : Verres optiques', row_style)],
            [Paragraph(f'Type de verre : {type_v}', row_style)],
            [Paragraph(f'Traitements : {treat}', row_style)],
        ],
        colWidths=[FL_W],
    )
    desig_t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, 0),   GREY300),
        ('BOX',           (0, 0), (-1, -1), 0.5, GREY600),
        ('INNERGRID',     (0, 0), (-1, -1), 0.5, GREY600),
        ('TOPPADDING',    (0, 0), (0, 0),   7),
        ('BOTTOMPADDING', (0, 0), (0, 0),   7),
        ('LEFTPADDING',   (0, 0), (0, 0),   10),
        ('RIGHTPADDING',  (0, 0), (0, 0),   10),
        ('TOPPADDING',    (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING',   (0, 1), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 1), (-1, -1), 10),
    ]))
    els.append(desig_t)

    # ── TABLEAU PRESCRIPTION ─────────────────────────────────────────────────
    def _c(text, bold=False, left=False):
        return Paragraph(
            f'<b>{text}</b>' if bold else text,
            ParagraphStyle('pc', fontSize=10,
                           fontName='Helvetica-Bold' if bold else 'Helvetica',
                           alignment=TA_LEFT if left else TA_CENTER, leading=13),
        )

    cw = [FL_W * 2/6] + [FL_W / 6] * 4
    presc_t = Table(
        [
            [_c('', bold=True), _c('SPH', bold=True), _c('CYL', bold=True),
             _c('AXE', bold=True), _c('ADD', bold=True)],
            [_c('OD (Droit)',  bold=True, left=True),
             _c(_val(d, 'rightSph')), _c(_val(d, 'rightCyl')),
             _c(_val(d, 'rightAxe')), _c(_val(d, 'rightAdd'))],
            [_c('OG (Gauche)', bold=True, left=True),
             _c(_val(d, 'leftSph')),  _c(_val(d, 'leftCyl')),
             _c(_val(d, 'leftAxe')),  _c(_val(d, 'leftAdd'))],
        ],
        colWidths=cw,
    )
    presc_t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  GREY200),
        ('BOX',           (0, 0), (-1, -1), 0.5, GREY600),
        ('INNERGRID',     (0, 0), (-1, -1), 0.5, GREY600),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    els.append(presc_t)

    return els


def generate_fiche_finale_deliveries(deliveries: list, company: dict,
                                      date_from: str = None, date_to: str = None) -> bytes:
    """
    Génère un PDF multi-pages : chaque bon de livraison sur sa propre page.
    Identique au mobile : pdf.addPage() dans une boucle.
    """
    buf = BytesIO()

    frame = Frame(
        FL_LM,
        RESERVED_BOTTOM,
        FL_W,
        PAGE_H - FL_TM - RESERVED_BOTTOM,
        leftPadding=0, rightPadding=0,
        topPadding=0,  bottomPadding=0,
    )
    template = PageTemplate(
        id='fl',
        frames=[frame],
        onPage=_make_fl_on_page(company),
    )
    doc = BaseDocTemplate(
        buf, pagesize=A4,
        pageTemplates=[template],
        leftMargin=FL_LM, rightMargin=FL_RM,
        topMargin=FL_TM,  bottomMargin=FL_BM,
    )

    comp_name = company.get('name', 'OPTIQUE & DISTRIBUTION')
    comp_desc = company.get('description', "Fournisseur d'équipements Optiques")
    logo_p    = _logo_path()

    story = []
    for i, d in enumerate(deliveries):
        if i > 0:
            story.append(PageBreak())
        story.extend(_build_bon_livraison_page(d, comp_name, comp_desc, logo_p))

    if not story:
        story.append(Paragraph(
            'Aucun bon de livraison pour cette période.',
            ParagraphStyle('empty', fontSize=11, fontName='Helvetica'),
        ))

    doc.build(story)
    return buf.getvalue()
