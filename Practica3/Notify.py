import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getSNMP import consultaSNMP

COMMASPACE = ', '
# Define params dummycuenta3@gmail.com
rrdpath = 'RRD/'
imgpath = 'images/'
fname = 'trend.rrd'

mailsender = "eduardo009cs@gmail.com"
mailreceip = "dummycuenta3@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'airjqdmbgjdrhsgs'

def send_alert_attached(subject,content,imagen):

    consulta = consultaSNMP("gustavoRomero","localhost","1.3.6.1.2.1.1.1.0")
    if consulta.find("Linux") == 1:
        so = "Linux"
    else:
        so = "Windows"
    nombreDispositivo = consultaSNMP("gustavoRomero","localhost","1.3.6.1.2.1.1.5.0")
    contacto = consultaSNMP("gustavoRomero","localhost","1.3.6.1.2.1.1.4.0")
    ubicacion = consultaSNMP("gustavoRomero","localhost","1.3.6.1.2.1.1.6.0")
    
    content = content + "\n----------INFORMACIÓN----------" +"\nDispositivo: " + nombreDispositivo + " \nSistema Operativo: " + so + "\nContacto: " + contacto + "\nUbicacion: " + ubicacion

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imagen, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(MIMEText(content,'plain'))
    msg.attach(img)
    
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()