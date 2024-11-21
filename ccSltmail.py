import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

from log import getLogger
import db

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

conn = db.DbConnection.dbconnHadwh("")
logger = getLogger('email', 'logs/sltemail')

message_template = read_template('files/message.txt')

sql='select * from CREDIT_CONTROL_EMAIL where stat is null'
c = conn.cursor()
c.execute(sql)

for row in c:
    account, email,amount,stat = row
    #print(amount)
    
    msg = MIMEMultipart()  # create a message

    # add in the actual person name to the message template
    #messagestr = message_template.substitute(DATE=date, ACCOUNT_NUM=account, AMOUNT=amount,CONTACT='0112396502')
    messagestr = message_template.substitute(ACCOUNT_NUM=account, AMOUNT=amount)
    logger.info(messagestr)
    #print(messagestr)
    
    #smtp_ssl_host = 'mail.slt.com.lk'
    smtp_ssl_host = '124.43.129.50'
    smtp_ssl_port = 25
    from_addr = 'sltbillcc@slt.lk'
    #from_addr = 'oss@slt.com.lk'
    to_addrs = [email]
    sub = 'SLTMobitel - Home bill outstanding as at 24/08/2022'
    
    try:
        message = MIMEText(messagestr)
        message['subject'] = sub
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)

        # we'll connect using SSL
        server = smtplib.SMTP(smtp_ssl_host, smtp_ssl_port)
        # to interact with the server, first we log in
        # and then we send the message
        #server.login(username, password)
        #server.sendmail(from_addr, to_addrs, message.as_string())
        logger.info(email)
        logger.info('mail sent.....')
        print('mail sent.....')
        logger.info('========================================================================================')
        server.quit()
        
        #sql2 = "update CREDIT_CONTROL_EMAIL set stat=:stat where  EMAIL_NAME =:EMAIL_NAME and ACCOUNT_NO=:ACCOUNT_NO and stat is null"
        sql2="update CREDIT_CONTROL_EMAIL set STAT=:STAT where  EMAIL_NAME =:EMAIL_NAME and ACCOUNT_NO=:ACCOUNT_NO and stat is null"
        with conn.cursor() as cursor3:
            cursor3.execute(sql2,["10",email,account])
            conn.commit()
            print(cursor3.rowcount)
    except Exception as e:
        print(e)
        logger.info(e)
        logger.info('========================================================================================')