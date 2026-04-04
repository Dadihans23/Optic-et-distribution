"""
Bon de Livraison PDF — reproduction pixel-perfect du design app mobile.

Technique clé : BaseDocTemplate + PageTemplate + onPage callback
pour dessiner Service Client + divider + footer à positions fixes sur la page,
exactement comme pw.Spacer() + footer dans le mobile.
"""
from io import BytesIO
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

pt = 1  # ReportLab : 1pt = 1 unité native

# ── Couleurs (identiques au mobile) ──────────────────────────────────────────
GREY300 = colors.Color(0.878, 0.878, 0.878)
GREY200 = colors.Color(0.933, 0.933, 0.933)
GREY600 = colors.Color(0.459, 0.459, 0.459)
GREY400 = colors.Color(0.741, 0.741, 0.741)
GREY_TXT = colors.Color(0.4, 0.4, 0.4)

# Marges identiques au mobile : fromLTRB(36, 28, 36, 24)
LM = RM = 36
TM = 28
BM = 24
PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - LM - RM

# Espace réservé en bas pour Service Client + divider + footer
# Mobile : SizedBox(100) sous Service Client + SizedBox(14) + divider + SizedBox(5) + footer
# Positions depuis le BAS de la page (coordonnées canvas ReportLab) :
Y_SERVICE_CLIENT = 154   # pt from bottom  (100 + ~14 + ~footer_h + BM)
Y_DIVIDER        = 42    # pt from bottom
Y_FOOTER_START   = 33    # pt from bottom  (1re ligne = adresse)
FOOTER_LINE_H    = 11    # hauteur de ligne pour police 8pt
RESERVED_BOTTOM  = 170   # hauteur réservée (frame commence au-dessus)

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
    """Première lettre de chaque mot = orange, reste = bleu — 20pt bold."""
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


def _make_on_page(company: dict):
    """Retourne le callback onPage qui dessine les éléments fixes sur chaque page."""
    def on_page(canvas, doc):
        canvas.saveState()

        # ── Service Client (italic bold 11pt, aligné à droite) ───────────────
        canvas.setFont('Helvetica-BoldOblique', 11)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.drawRightString(PAGE_W - RM, Y_SERVICE_CLIENT, 'Service Client')

        # ── Divider ──────────────────────────────────────────────────────────
        canvas.setStrokeColorRGB(0.741, 0.741, 0.741)
        canvas.setLineWidth(0.5)
        canvas.line(LM, Y_DIVIDER, PAGE_W - RM, Y_DIVIDER)

        # ── Footer (8pt centré gris) ──────────────────────────────────────────
        canvas.setFont('Helvetica', 8)
        canvas.setFillColorRGB(0.4, 0.4, 0.4)
        cx = PAGE_W / 2

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


def generate_bon_livraison(delivery: dict, company: dict) -> bytes:
    buf = BytesIO()

    # Frame : occupe la zone au-dessus des éléments fixes
    frame = Frame(
        LM,
        RESERVED_BOTTOM,          # bottom y of frame
        CONTENT_W,
        PAGE_H - TM - RESERVED_BOTTOM,   # height
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )
    template = PageTemplate(
        id='bon',
        frames=[frame],
        onPage=_make_on_page(company),
    )
    doc = BaseDocTemplate(
        buf, pagesize=A4,
        pageTemplates=[template],
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
    )

    story = []
    comp_name = company.get('name', 'OPTIQUE & DISTRIBUTION')
    comp_desc = company.get('description', "Fournisseur d'équipements Optiques")

    # ── EN-TÊTE : logo 62×62 + [nom\ndesc] centré sur la page ────────────────
    # Mobile : pw.Center(pw.Row(mainAxisSize.min, [logo, SizedBox(12), Column([name,desc])]))
    logo_p = _logo_path()
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
        # Colonne droite : Table à 1 colonne (name + desc)
        NAME_COL_W = 260
        right_col = Table(
            [[name_para], [desc_para]],
            colWidths=[NAME_COL_W],
        )
        right_col.setStyle(TableStyle([
            ('TOPPADDING',    (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING',   (0, 0), (-1, -1), 0),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (0, 0),   3),  # 3pt entre nom et desc
        ]))
        # Table principale : logo (74pt) | right_col — centrée sur la page
        header_t = Table(
            [[logo_img, right_col]],
            colWidths=[74, NAME_COL_W],
        )
        header_t.hAlign = 'CENTER'
        header_t.setStyle(TableStyle([
            ('VALIGN',         (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING',    (0, 0), (-1, -1), 0),
            ('RIGHTPADDING',   (0, 0), (-1, -1), 0),
            ('TOPPADDING',     (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING',  (0, 0), (-1, -1), 0),
        ]))
        story.append(header_t)
    else:
        story.append(Paragraph(
            _company_name_rich(comp_name),
            ParagraphStyle('cn', alignment=TA_CENTER),
        ))
        story.append(Paragraph(
            f'<font color="#666666" size="10"><i>{comp_desc}</i></font>',
            ParagraphStyle('cd', alignment=TA_CENTER),
        ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GREY400))
    story.append(Spacer(1, 18))

    # ── TITRE ────────────────────────────────────────────────────────────────
    # Mobile : "BON DE LIVRAISON N° ___________________" — une seule ligne centrée
    story.append(Paragraph(
        '<b>BON DE LIVRAISON N° ___________________</b>',
        ParagraphStyle('title', fontSize=13, fontName='Helvetica-Bold',
                       alignment=TA_CENTER),
    ))
    story.append(Spacer(1, 20))

    # ── BLOC CLIENT ──────────────────────────────────────────────────────────
    body = ParagraphStyle('body', fontSize=11, fontName='Helvetica', leading=14)

    story.append(Paragraph(f'Client : {delivery.get("shopName") or "-"}', body))
    story.append(Spacer(1, 4))
    phone = delivery.get('phoneNumber', '')
    if phone:
        story.append(Paragraph(f'Tél : {phone}', body))
        story.append(Spacer(1, 4))
    story.append(Paragraph(f'Patient : {delivery.get("wearerName") or "Non spécifié"}', body))
    story.append(Spacer(1, 4))
    created  = delivery.get('createdAt')
    date_str = created.strftime('%d/%m/%Y') if hasattr(created, 'strftime') else 'Inconnue'
    story.append(Paragraph(f'Date : {date_str}', body))
    story.append(Spacer(1, 24))

    # ── TABLEAU DÉSIGNATION (1 colonne pleine largeur) ────────────────────────
    type_v = delivery.get('typeVerre') or '-'
    treat  = delivery.get('treatmentOption') or '-'

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
        colWidths=[CONTENT_W],
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
    story.append(desig_t)

    # ── TABLEAU PRESCRIPTION (5 colonnes ratio 2:1:1:1:1) ────────────────────
    def _c(text, bold=False, left=False):
        return Paragraph(
            f'<b>{text}</b>' if bold else text,
            ParagraphStyle('pc', fontSize=10,
                           fontName='Helvetica-Bold' if bold else 'Helvetica',
                           alignment=TA_LEFT if left else TA_CENTER,
                           leading=13),
        )

    def _v(key):
        val = delivery.get(key)
        return str(val) if val else '-'

    cw = [CONTENT_W * 2/6] + [CONTENT_W / 6] * 4
    presc_t = Table(
        [
            [_c('', bold=True), _c('SPH', bold=True), _c('CYL', bold=True),
             _c('AXE', bold=True), _c('ADD', bold=True)],
            [_c('OD (Droit)',  bold=True, left=True),
             _c(_v('rightSph')), _c(_v('rightCyl')), _c(_v('rightAxe')), _c(_v('rightAdd'))],
            [_c('OG (Gauche)', bold=True, left=True),
             _c(_v('leftSph')),  _c(_v('leftCyl')),  _c(_v('leftAxe')),  _c(_v('leftAdd'))],
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
    story.append(presc_t)
    # (Pas de Spacer ici — le vide jusqu'à Service Client est géré par le frame)

    doc.build(story)
    return buf.getvalue()
