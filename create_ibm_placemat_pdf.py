from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A3
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# --- CONFIGURATION ---
OUTPUT_FILE = "IBM_Product_Placemat.pdf"
# Using A3 Landscape (16.5 x 11.7 inches) gives us plenty of room
PAGE_WIDTH, PAGE_HEIGHT = landscape(A3)

# --- COLORS ---
# Hex codes extracted to match the template closely
C_BLUE_HEADER = colors.HexColor("#16365C")  # Deep Blue
C_PURPLE_HEADER = colors.HexColor("#7030A0") # Purple
C_GREY_HEADER = colors.HexColor("#404040")   # Dark Grey
C_RED_TEXT = colors.HexColor("#C00000")      # Dark Red
C_BLUE_BTN = colors.HexColor("#4472C4")      # Bright Blue
C_BG_LEGEND_1 = colors.HexColor("#BDD7EE")   # Entitled
C_BG_LEGEND_2 = colors.HexColor("#A9D08E")   # Opportunity
C_BG_LEGEND_3 = colors.HexColor("#FFE699")   # Explore
C_BG_LEGEND_4 = colors.HexColor("#F4B084")   # At Risk
C_WHITE = colors.white
C_BLACK = colors.black
C_GREY_BORDER = colors.HexColor("#BFBFBF")   # Light Grey Border

# --- LAYOUT CONSTANTS ---
MARGIN = 0.3 * inch
TOP_Y = PAGE_HEIGHT - MARGIN
CONTENT_W = PAGE_WIDTH - (2 * MARGIN)

# Width Ratios
# Left Bar (CE) | Security | Center (Wide) | Right (IT Auto)
W_CE = 0.4 * inch
W_SEC = 2.4 * inch
W_RIGHT = 2.4 * inch
GAP = 0.08 * inch

# Calculate Center Width dynamically
W_CENTER = CONTENT_W - W_CE - W_SEC - W_RIGHT - (3 * GAP)

# X Coordinates
X_CE = MARGIN
X_SEC = X_CE + W_CE + GAP
X_CENTER = X_SEC + W_SEC + GAP
X_RIGHT = X_CENTER + W_CENTER + GAP

# --- HELPER FUNCTION: DRAW BOX ---
def draw_box(c, x, y, w, h, text, bg_color=C_WHITE, text_color=C_BLACK, 
             border_color=C_BLUE_HEADER, border_width=0.5, font_size=7, 
             bold=False, vertical=False):
    
    # Draw Rectangle
    c.setFillColor(bg_color)
    c.setStrokeColor(border_color)
    c.setLineWidth(border_width)
    c.rect(x, y, w, h, fill=1, stroke=1)
    
    # Draw Text
    c.setFillColor(text_color)
    font_name = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font_name, font_size)
    
    if vertical:
        c.saveState()
        # Rotate 90 degrees for vertical text
        c.translate(x + w/2 + (font_size/3), y + h/2)
        c.rotate(90)
        c.drawCentredString(0, 0, text)
        c.restoreState()
    else:
        # Check text width and scale if necessary (simple fitting)
        text_w = c.stringWidth(text, font_name, font_size)
        if text_w > w - 4:
            # Simple condense if too long
            c.saveState()
            scale = (w - 6) / text_w
            c.translate(x + w/2, y + h/2 - (font_size/3))
            c.scale(scale, 1)
            c.drawCentredString(0, 0, text)
            c.restoreState()
        else:
            c.drawCentredString(x + w/2, y + h/2 - (font_size/3), text)

def draw_grid(c, x, y, w, h, items, cols=1, border_color=C_BLUE_HEADER):
    if not items: return
    rows = (len(items) + cols - 1) // cols
    
    box_w = (w - ((cols - 1) * GAP)) / cols
    box_h = (h - ((rows - 1) * GAP)) / rows
    
    # Cap max height for aesthetics
    if box_h > 0.35 * inch: box_h = 0.35 * inch
    
    # Start drawing from Top-Left of the defined area (Y moves down)
    curr_y = y + h - box_h
    
    for i, item in enumerate(items):
        col_idx = i % cols
        row_idx = i // cols
        
        # If new row, reset X, lower Y
        if col_idx == 0 and i != 0:
            curr_y -= (box_h + GAP)
            
        curr_x = x + (col_idx * (box_w + GAP))
        
        draw_box(c, curr_x, curr_y, box_w, box_h, item, border_color=border_color, font_size=7)

# --- MAIN DRAWING LOGIC ---
def create_pdf():
    c = canvas.Canvas(OUTPUT_FILE, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # 1. HEADER
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(C_BLACK)
    c.drawString(MARGIN, TOP_Y - 0.6*inch, "IBM Technology")
    
    # Legends
    leg_w = 1.2 * inch
    leg_h = 0.3 * inch
    leg_y = TOP_Y - 0.6 * inch
    leg_x_start = PAGE_WIDTH - MARGIN - (4 * (leg_w + GAP))
    
    legends = [("Entitled", C_BG_LEGEND_1), ("Opportunity", C_BG_LEGEND_2), 
               ("Explore", C_BG_LEGEND_3), ("No Interest/At Risk", C_BG_LEGEND_4)]
    
    for i, (txt, col) in enumerate(legends):
        lx = leg_x_start + (i * (leg_w + GAP))
        draw_box(c, lx, leg_y, leg_w, leg_h, txt, bg_color=col, border_width=0, font_size=9)
        
    # ELA Star
    draw_box(c, PAGE_WIDTH - MARGIN - 1.5*inch, leg_y - 0.4*inch, 1.5*inch, 0.25*inch, 
             "★ ELA Product", bg_color=colors.HexColor("#E7E6E6"), border_width=0)

    # --- BODY LAYOUT CALCS ---
    # Define vertical areas
    HEADER_H = 1.0 * inch
    FOOTER_H = 0.5 * inch
    INFRA_H = 1.4 * inch
    REDHAT_H = 0.4 * inch
    
    BODY_TOP = PAGE_HEIGHT - MARGIN - HEADER_H
    BODY_H = BODY_TOP - MARGIN - FOOTER_H - INFRA_H - REDHAT_H - (2*GAP)
    
    # 2. CLIENT ENGINEERING (Far Left)
    # Spans full body height + infra height + redhat height
    CE_H = BODY_H + REDHAT_H + INFRA_H + (2*GAP)
    CE_Y = MARGIN + FOOTER_H + GAP
    draw_box(c, X_CE, CE_Y, W_CE, CE_H, "IBM Client Engineering (CE)", 
             bold=True, vertical=True, border_color=C_BLACK, border_width=1)

    # 3. SECURITY (Left)
    SEC_Y = MARGIN + FOOTER_H + INFRA_H + REDHAT_H + (3*GAP)
    # Security Header
    draw_box(c, X_SEC, BODY_TOP - 0.3*inch, W_SEC, 0.3*inch, "Security", bg_color=C_WHITE, border_width=0, bold=True, font_size=10)
    
    # Data Security
    DS_H = 3.2 * inch
    DS_Y = BODY_TOP - 0.35*inch - 0.3*inch - DS_H
    draw_box(c, X_SEC, BODY_TOP - 0.35*inch - 0.3*inch, W_SEC, 0.3*inch, "Data Security", bg_color=C_BLUE_HEADER, text_color=C_WHITE, bold=True)
    draw_grid(c, X_SEC, DS_Y, W_SEC, DS_H, 
              ["Guardium Data Encryption", "Guardium Data Protection", "Guardium Data Security Center", "Guardium Discover and Classify", "Guardium Key Lifecycle Management"])

    # Identity
    ID_H = 3.6 * inch
    ID_Y = DS_Y - 0.35*inch - GAP - ID_H
    draw_box(c, X_SEC, DS_Y - 0.35*inch - GAP, W_SEC, 0.3*inch, "Identity & Access Mgmt", bg_color=C_PURPLE_HEADER, text_color=C_WHITE, bold=True)
    draw_grid(c, X_SEC, ID_Y, W_SEC, ID_H, 
              ["HashiCorp Boundary", "HashiCorp Consul", "HashiCorp Vault", "ILMT", "Security Verify (IAM)", "Security MaaS 360", "Trusteer (Anti-fraud)"], border_color=C_PURPLE_HEADER)

    # 4. CENTER COLUMN
    # Client Apps
    CA_H = 1.2 * inch
    CA_Y = BODY_TOP - 0.35*inch - CA_H
    draw_box(c, X_CENTER, BODY_TOP - 0.3*inch, W_CENTER, 0.3*inch, "Client Applications", bg_color=C_GREY_HEADER, text_color=C_WHITE, bold=True)
    draw_grid(c, X_CENTER, CA_Y, W_CENTER, CA_H, 
              ["ERP", "CRM", "B2B", "B2C", "B2E", "Omnichannel", "CRM (on-prem)", "IA", 
               "Fraud", "Credit", "PCP", "Supply Chain", "Engineering / Network", "Portal / Mobile / APP", "Payment Instantaneous", "Customer Service"], cols=8, border_color=C_GREY_HEADER)

    # 6 Pillars
    P6_TOP = CA_Y - GAP
    P6_H = 4.2 * inch
    P6_Y = P6_TOP - P6_H
    
    pillars = [
        ("AI Assistants", C_BLUE_HEADER, ["Automation", "Blueworks Live", "Business Analytics", "Business Automation", "CP4BA", "Cognos Analytics", "Decision Mgmt", "Planning Analytics", "Process Mining", "RPA", "SPSS Modeler", "watsonx Assistants", "watsonx BI Assistant", "watsonx Code Assistant", "watsonx Orchestrate", "Workflow Automation"], 2),
        ("AI/MLOps", C_BLUE_HEADER, ["CP4D", "OpenPages", "Orchestrate (SaaS)", "WCA Ansible & Java", "WCAz", "watsonx.ai", "watsonx.governance"], 1),
        ("Databases", C_BLUE_HEADER, ["CM8", "CMOD", "CP4D", "Capture", "Cloudera", "Content", "DB2", "Database Eco", "FileNet", "Hadoop", "Informix", "Netezza", "watsonx.data", "watsonx.ai (SaaS)"], 2),
        ("Data Intelligence", C_BLUE_HEADER, ["CP4D", "Data Product Hub", "Decision Optimization", "Knowledge Catalog", "Manta Data Lineage", "Optim & Master Data Mgmt", "SPSS Stats"], 1),
        ("Data Integration", C_BLUE_HEADER, ["CP4D", "Data Fabric", "Data Integration", "DataStage", "Databand", "Replication", "StreamSets"], 1),
        ("Asset Lifecycle Mgmt", C_PURPLE_HEADER, ["EI", "Envizi", "HashiCorp Terraform", "Maximo", "Sterling Order & Inventory Mgmt", "Supply Chain", "TRIRIGA"], 1)
    ]
    
    col_w = (W_CENTER - (5*GAP)) / 6
    
    for i, (title, color, items, cols) in enumerate(pillars):
        px = X_CENTER + (i * (col_w + GAP))
        draw_box(c, px, P6_TOP - 0.3*inch, col_w, 0.3*inch, title, bg_color=color, text_color=C_WHITE, bold=True, font_size=6)
        draw_grid(c, px, P6_Y, col_w, P6_H - 0.3*inch - GAP, items, cols=cols, border_color=color)

    # App Dev & Int
    AD_TOP = P6_Y - GAP
    AD_H = 1.4 * inch
    AD_Y = AD_TOP - AD_H
    ad_w = (W_CENTER - GAP) / 2
    
    # App Dev
    draw_box(c, X_CENTER, AD_TOP - 0.3*inch, ad_w, 0.3*inch, "Application Development", bg_color=C_PURPLE_HEADER, text_color=C_WHITE, bold=True)
    draw_grid(c, X_CENTER, AD_Y, ad_w, AD_H - 0.3*inch - GAP, 
              ["App Run", "CP4Apps", "CP4Systems", "DevOps", "ELM", "Project Harmony", "Runtimes", "Spectrum LSF", "UnifyBlue", "WAS", "WCA Java", "Web Hybrid ED"], cols=4, border_color=C_PURPLE_HEADER)
    
    # App Int
    draw_box(c, X_CENTER + ad_w + GAP, AD_TOP - 0.3*inch, ad_w, 0.3*inch, "Application Integration", bg_color=C_PURPLE_HEADER, text_color=C_WHITE, bold=True)
    draw_grid(c, X_CENTER + ad_w + GAP, AD_Y, ad_w, AD_H - 0.3*inch - GAP, 
              ["API Connect", "APP Connect", "Aspera", "CP4I", "Connect:Direct", "DataPower", "DataPower Dashboard", "Event Automation", "FTM", "MQ", "Sterling B2B Integrator", "WebMethods"], cols=4, border_color=C_PURPLE_HEADER)

    # 5. RIGHT COLUMN
    IT_TOP = BODY_TOP - 0.35*inch
    IT_H = 4.2 * inch
    IT_Y = IT_TOP - IT_H
    
    draw_box(c, X_RIGHT, BODY_TOP - 0.3*inch, W_RIGHT, 0.3*inch, "IT Automation & Finops", bg_color=C_PURPLE_HEADER, text_color=C_WHITE, bold=True)
    draw_grid(c, X_RIGHT, IT_Y, W_RIGHT, IT_H, 
              ["Ansible", "Apptio", "Cloud Pak for AIOps", "Cloudability", "Concert", "Flexera One", "HashiCorp Terraform", "Instana", "Kubecost", "Operations Insights", "Targetprocess", "Turbonomic", "Workload Automation"], border_color=C_PURPLE_HEADER)
    
    NET_TOP = IT_Y - GAP
    NET_H = (IT_TOP - AD_Y) - IT_H - GAP # Fill remaining height to match Center bottom
    NET_Y = NET_TOP - NET_H
    
    draw_box(c, X_RIGHT, NET_TOP - 0.3*inch, W_RIGHT, 0.3*inch, "Network Mgmt", bg_color=C_PURPLE_HEADER, text_color=C_WHITE, bold=True)
    draw_grid(c, X_RIGHT, NET_Y, W_RIGHT, NET_H - 0.3*inch, 
              ["CP4NA", "Cloud Network Security", "Content Delivery Network", "Edge Application Manager", "HashiCorp Nomad", "Hybrid Cloud Mesh", "NS1 Connect", "SevOne"], border_color=C_PURPLE_HEADER)

    # 6. RED HAT BANNER (Spans Center + Right)
    RH_Y = AD_Y - GAP - REDHAT_H
    RH_W = W_CENTER + GAP + W_RIGHT
    draw_box(c, X_CENTER, RH_Y, RH_W, REDHAT_H, "Red Hat OpenShift", text_color=C_RED_TEXT, border_color=C_RED_TEXT, bold=True, font_size=12)

    # 7. INFRASTRUCTURE (Bottom Row)
    INFRA_Y = RH_Y - GAP - INFRA_H
    
    # Enterprise Storage (Aligns with Security Column)
    draw_box(c, X_SEC, INFRA_Y + INFRA_H - 0.3*inch, W_SEC, 0.3*inch, "Enterprise Storage", bg_color=C_GREY_HEADER, text_color=C_WHITE, bold=True)
    draw_grid(c, X_SEC, INFRA_Y, W_SEC, INFRA_H - 0.3*inch, ["DS8000 Series", "SAN Directors", "Tape (Hydra & Jaguar)/VTS"], border_color=C_GREY_HEADER)
    
    # Remaining Infra (Aligns with Center + Right)
    infra_w_total = W_CENTER + GAP + W_RIGHT
    # 3 units for Resilience, 2 for Power, 2 for Z, 2 for Cloud = 9 units
    unit_w = (infra_w_total - (3*GAP)) / 9
    
    infra_items = [
        ("Data Resilience Storage", 3, ["Scale", "Scale System", "Ceph", "CoS", "Defender/Protect", "Flash", "Fusion", "Fusion HCI", "Fusion HCI (on-prem)", "Hyperscaler", "SVC", "Ceph System", "Storage Insight", "Storage Virtualize", "Tape"]),
        ("Power", 2, ["AIX", "IBM i", "Linux", "Oracle", "Red Hat OpenShift", "SAP"]),
        ("Z System", 2, ["AI on Z", "IBM LinuxOne", "IBM zOS", "Z Monitoring Suite", "Z Security", "Z Software"]),
        ("Cloud", 2, ["Cloud Financial Server", "Cloud Satellite", "Power Virtual Server", "Red Hat OpenShift", "SAP", "VMware"])
    ]
    
    curr_x = X_CENTER
    for title, units, items in infra_items:
        w_actual = (unit_w * units) + (GAP * (units - 1))
        draw_box(c, curr_x, INFRA_Y + INFRA_H - 0.3*inch, w_actual, 0.3*inch, title, bg_color=C_GREY_HEADER, text_color=C_WHITE, bold=True)
        draw_grid(c, curr_x, INFRA_Y, w_actual, INFRA_H - 0.3*inch, items, cols=units, border_color=C_GREY_HEADER)
        curr_x += w_actual + GAP

    # 8. FOOTER
    FOOT_Y = MARGIN
    FOOT_W = (CONTENT_W - GAP) / 2
    draw_box(c, MARGIN, FOOT_Y, FOOT_W, FOOTER_H, "IBM Technology Lifecycle Services (TLS)", bg_color=colors.HexColor("#F2F2F2"), border_color=C_GREY_HEADER, bold=True, font_size=10)
    draw_box(c, MARGIN + FOOT_W + GAP, FOOT_Y, FOOT_W, FOOTER_H, "IBM Expert Labs (EL)", bg_color=colors.HexColor("#F2F2F2"), border_color=C_GREY_HEADER, bold=True, font_size=10)

    c.save()
    print(f"PDF Generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_pdf()
