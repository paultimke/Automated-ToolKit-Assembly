import smtplib, ssl
from email.mime.text import MIMEText
from email.message import EmailMessage



kit_num = str(5)
email_pass : str = 'Robocop22'
sender : str = 'modula.vision@gmail.com'
receivers : list = ['A01566664@tec.mx','christianloyapena@hotmail.com']
port : int = 465
kit_type=str(5)

msg =EmailMessage()
msg['Subject']='Kit ' + kit_type + ' Terminado'
msg['From']= sender
msg['To']=receivers[0]
msg.set_content('La estación de armado de kits del ModulaLift ha elaborado ' + kit_num + ' veces el kit ' + kit_type)




with smtplib.SMTP_SSL('smtp.gmail.com', port) as smtp:
    smtp.login(sender,email_pass)

    smtp.send_message(msg)

