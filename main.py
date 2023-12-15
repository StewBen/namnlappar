"""
- README -
Namnlappskapare för AU-evenemang.

Storleken på varje ruta är anpassad för att vikas på mitten och därav vara dubbelsidig.
Passar standardstorlek för plastfickor (85mm x 54mm).

Nödvändiga pythonpaket: reportlab, installeras enklast med "pip install reportlab" i terminalen.

Namnlistan ändras i namn.txt, textstorleken anpassas automatiskt för att passa på en rad.
Korresponderande roller kan ändras i roles.txt eller lämnas tom.

Mail:a viktor.stubbfalt@au.se vid frågor!
Skrivet av Viktor Stubbfält - 2023-09-12
"""


### Imports:
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

### Custom Fonts (located in font folder):
pdfmetrics.registerFont(TTFont('Exo', 'Fonts/Exo/Exo-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Exo Bold', 'Fonts/Exo/Exo-Bold.ttf'))

### Import Names:
names = []
with open('names.txt', encoding = 'utf8') as name_file:
    lines = name_file.read().splitlines()
    for line in lines:
        names.append(line)
        names.append(line) # Two times for folding

### Import Roles:
roles = []
with open('roles.txt', encoding = 'utf8') as role_file:
    lines = role_file.read().splitlines()
    for line in lines:
        roles.append(line)
        roles.append(line) # Two times for folding

### Set up Page Environment (1pt = 1/72 inch):
page = canvas.Canvas("namnlappar.pdf")
page.setFont('Exo Bold', 24)
page.setStrokeColorRGB(0.9, 0.9, 0.9) 
page_width = 595.27  # A4 standard
page_height = 841.89 # A4 standard
tag_width = 250
padding = 50

### Main loop for writing text/logo/lines:
for i, name in enumerate(names):
    font_size = 24 # Default fontsize

    ### Create a new page every 10 names:
    if i % 10 == 0:
        if i != 0:                              # (If not first page)
            page.showPage()                     # This adds a new page
            page.setFont('Exo Bold', font_size) # Font must be reset

        ### Horizontal lines:
        for k in range(6):

            ### Gray lines (for cutting):
            page.setLineWidth(2)
            page.setStrokeColorRGB(0.95, 0.95, 0.95) 
            page.line(padding,               (k)*(page_height/5),
                      padding + tag_width*2, (k)*(page_height/5))
            
            ### Yellow lines:
            page.setLineWidth(4)
            page.setStrokeColorCMYK(0, 0.29, 1, 0)
            page.line(padding,               (k+1)*(page_height/5) - 89,
                      padding + tag_width*2, (k+1)*(page_height/5) - 89)

            ### Blue lines:
            page.setLineWidth(4)
            page.setStrokeColorCMYK(0.52, 0.23, 0, 0.12)
            page.line(padding,               (k+1)*(page_height/5) - 85,
                      padding + tag_width*2, (k+1)*(page_height/5) - 85)
        
        ### Vertical gray lines (for cutting):
        page.setLineWidth(2)
        page.setStrokeColorRGB(0.95, 0.95, 0.95)
        page.line(padding + tag_width*2, 0, padding + tag_width*2, page_height)
        page.line(padding, 0, padding, page_height)
        
    ### Resize if current name is super long:
    while stringWidth(name, 'Exo Bold', font_size) >= tag_width * 0.9:
        font_size = font_size - 1
    page.setFont('Exo Bold', font_size)
    
    ### Writes current name:
    text_width = stringWidth(name, 'Exo Bold', font_size)
    if i % 2 == 0:
        text_x = padding + (tag_width / 2) - (text_width / 2)
        text_y = page_height - 40 - (i % 10) * page_height / 10 
    else:
        text_x = padding + (3 * tag_width / 2) - (text_width / 2)
    page.drawString(text_x, text_y, name)

    ### Writes the role underneath the name:
    page.setFont('Exo Bold', 14)
    role_width = stringWidth(roles[i], 'Exo Bold', 14)
    if i % 2 == 0:
        role_x = padding + (tag_width / 2) - (role_width / 2)
        role_y = page_height - 67 - (i % 10) * page_height / 10 
    else:
        role_x = padding + (3 * tag_width / 2) - (role_width / 2)
    page.drawString(role_x, role_y, roles[i])
    
    ### Draws the logo:
    logo_width = 200
    if i % 2 == 0:
        logo_x = padding + (tag_width / 2) - (logo_width / 2)
        logo_y = 170 - page_height / 10 * (i % 10)
    else:
        logo_x = padding + (3 * tag_width / 2) - (logo_width / 2)
    page.drawImage(image = "au-logotyp.jpg",
                   x = logo_x,
                   y = logo_y,
                   width = logo_width,
                   preserveAspectRatio = True)

### Save file as PDF:
page.save()
