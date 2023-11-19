from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.graphics.barcode import createBarcodeDrawing
import math

def fillTemplate(quantity, wallet_info, templateFile, config, verbose=False):
  
  horizontalCenters_m = config['m']['position']
  horizontalCenters_qr = config['qr']['position']
  horizontalCenters_address = config['address']['position']
  fileName = 'paperWallet'

  numPages = int(math.ceil(quantity/3))
  print('Preparing {} Pages for {} Wallets'.format(numPages, quantity))

  wallet_number = 0

  # Set Up Page
  for pageNum in range(0, numPages):

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Set Up Wallet
    for num_wallet_on_page in range(0, 3): # 3 Paper Wallets
            
      # Cast to local variables
      mnemonic = wallet_info[wallet_number]['mnemonic'].split()    
      address = wallet_info[wallet_number]['address']

      # Add QR code
      qr_addr = createBarcodeDrawing('QR', value= address, width=75, height=75, humanReadable=1)
      qr_addr.drawOn(can, 359, horizontalCenters_qr[num_wallet_on_page])

      # Add Mneumonic to Grey Box
      can.setFont('Times-Roman', 5.4)
      can.setFillColor(HexColor('#000000'))
      for line in range(0, 4): # 4 Lines of 6 Words Each
        wordLine = mnemonic[0 + line*6 : 6 + line*6]
        can.drawCentredString(131.5, horizontalCenters_m[num_wallet_on_page]-line*11, " ".join(wordLine).upper())

      # Add Address
      can.setFont('Times-Roman', 6.5)
      can.drawCentredString(395, horizontalCenters_address[num_wallet_on_page], address)
      
      # Add Quantity
      can.setFont('Times-Roman', 8)
      can.setFillColor(HexColor('#214F79'))
      #can.drawCentredString(580, 460, quantity_lovelace+' Lovelace')
      

      print('Set Up Wallet #{}: {}/3 on Page {}/{}'.format(wallet_number+1, num_wallet_on_page+1, pageNum+1, numPages))
      wallet_number = wallet_number + 1
      if wallet_number-1 == quantity: break
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)

    # Create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)

    # Read your existing PDF
    existing_pdf = PdfFileReader(open(templateFile, "rb"))
    output = PdfFileWriter()

    # Add contents
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # Finally, write "output" to a real file
    outputStream = open(fileName+str(pageNum+1)+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()