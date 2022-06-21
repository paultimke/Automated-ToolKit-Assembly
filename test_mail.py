import smtplib 
from email.message import EmailMessage
import helper as hp

from datetime import datetime
import pywhatkit as wpp




#ref = {'grande': 1, 'mediano': 2, 'flaco': 3, 'tuerca': 2}

#hp.send_alert_email1('Hola POLO', 69)

#hp.send_alert_email('Hola POLO', 69)
now = datetime.now()
h = now.hour 
m = now.minute +1

#wpp.sendwhatmsg("+526145120481","hola\n",h,m,10,True,10)

wpp.sendwhatmsg_instantly("+526145120481","hola\n", 10, True, 5)
