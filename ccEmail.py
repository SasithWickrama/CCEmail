# import necessary packages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

from log import getLogger

logger = getLogger('email', 'logs/email')

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def get_contacts(filename):
    email = []
    date = []
    account = []
    amount = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            email.append(a_contact.split()[1])
            #date.append(a_contact.split()[1])
            account.append(a_contact.split()[0])
            amount.append(a_contact.split()[2])
    return email, account,amount


# For each contact, send the email:

# s = smtplib.SMTP(host='124.43.129.50', port=25)
# s.starttls()
# s.login('sltbillcc@slt.lk', 'wYS#qa?MP5')

#email, account, amount = get_contacts('files/detail.txt')  # read contacts
#message_template = read_template('files/message.txt')

#for email, account, amount in zip(email, account, amount):
    #msg = MIMEMultipart()  # create a message

    # add in the actual person name to the message template
    #messagestr = message_template.substitute(DATE=date, ACCOUNT_NUM=account, AMOUNT=amount,CONTACT='0112396502')
    #messagestr = message_template.substitute(ACCOUNT_NUM=account, AMOUNT=amount)
    #logger.info(messagestr)
    #print(messagestr)


    # connect with Google's servers
    #smtp_ssl_host = 'mail.slt.com.lk'
    smtp_ssl_host = '124.43.129.50'
    smtp_ssl_port = 25
    # use username or email to log in
    #username = 'origin@gmail.com'
    #password = 'password'

    #from_addr = 'oss@slt.com.lk'
    from_addr = 'sltbillcc@slt.lk'

    to_addrs = ['prabodha@slt.com.lk']

    # the email lib has a lot of templates
    # for different message formats,
    # on our case we will use MIMEText
    # to send only text
    sub = 'SLTMobitel - Home bill outstanding as at 24/08/2022'

    try:
        message = MIMEText("This is test message")
        message['subject'] = sub
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)

        # we'll connect using SSL
        server = smtplib.SMTP(smtp_ssl_host, smtp_ssl_port)
        # to interact with the server, first we log in
        # and then we send the message
        #server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        logger.info(email)
        logger.info('mail sent.....')
        print('mail sent.....')
        logger.info('========================================================================================')
        server.quit()
    except Exception as e:
        print(e)
        logger.info(e)
        logger.info('========================================================================================')

