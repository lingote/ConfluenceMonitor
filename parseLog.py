#-*- encoding: utf-8 -*-

"""
 Author: Ignacio Aracena
 Simple script to parse output
 of mysqldbcompare
"""

#from chardet import detect
#encoding = lambda x: detect(x)['encoding']
import pandas as pd
import requests
import json
import time
import subprocess
import smtplib
from email.mime.text import MIMEText
import email.utils
import openpyxl


#infile = 'C:/Users/euroadmin/MasterSlaveComp/masterslave_comp.log'
#pd.read_csv(infile, delimiter=' ')
BASE_URL = 'http://192.168.10.49:8090/rest/api/content'


def rundbcompare():
    """
    Run mysqldbcompare.exe
    :return:
    """
    try:
        output = subprocess.check_output(['C:\Program Files (x86)\MySQL\MySQL Utilities 1.3.4\mysqldbcompare.exe',
                                      #'--format=csv',  '--skip-data-check',
                                      '--server1=euroUser:euro!!User!!@192.168.10.39:3307',
                                      '--server2=euroUser:euro!!User!!@192.168.10.49:3306', 'eurodb:eurodb'
                                      ], shell=True)
        f = open('C:/Users/euroadmin/MasterSlaveComp/dummy.txt','w')
        f.write(str(output.decode()))
        f.close()
        output = str(output.decode()).split('\r\n')
        return output
    except subprocess.CalledProcessError as e:
        print(e.output)
        return str(e.output.decode()).split('\r\n')


def getquizstatus(excelfile='F:/share/moodlebackup/FragenErfassungStatus.xlsx'):
    """
    Get status of moodle quiz question
    :return:
    """
    dfs = {}
    wb = openpyxl.load_workbook(excelfile)
    for i in wb.get_sheet_names():
        dfs[i] = pd.DataFrame(wb[i].values)
        dfs[i].columns = dfs[i].iloc[0,:].tolist()
        dfs[i].drop(dfs[i].index[0], inplace=True)
        dfs[i] = dfs[i].to_html(index=False).replace('\n', '')
    return dfs


def alertemail(inline):
    """
    Send email if difference found in DB compare
    :param inline: Line from mysqldbcompare
    :return:
    """
    msg = MIMEText(inline)
    msg['Subject'] = 'Problem with Master-Slave replication'
    msg['From'] = email.utils.formataddr(('Master-Slave replication', 'noreply@test'))
    recipients = ['ignacioaracenar@gmail.com']
    msg['To'] = ", ".join(recipients)
    #msg['To'] = email.utils.formataddr(('Recipient', 'ignacioaracenar@gmail.com'))
    try:
        server = smtplib.SMTP('gmail-smtp-in.l.google.com:25')
        server.starttls()
        server.ehlo("euroserver.com")
        #server.mail('noreply@test')
        #server.rcpt(recipients)
        #server.data(str(msg))
        server.sendmail('noreply@test', recipients, str(msg))
    finally:
        server.quit()


def list2html(inlist):
    """
    Takes outout of mysqldbcompare and turns it into an HTML table
    :param inlist: input log file
    :param outdir: directory
    :return: string with HTML
    """
    data = []
    difflist = []
    j = 0
    for line in inlist:
        if line.find('TABLE') != -1:
            line = line.strip('#')
            data.append(line.split())
            print(line)
            if line.lower().find('fail') != -1:
                if data[-1][1] == 'customerimages':
                    # hack: for some reason blob data differs
                    continue
                difflist.append(line)
        j += 1
    if len(difflist) > 0:
        alertemail('\r'.join(difflist))
        return '<h2>{}</h2>'.format('\r'.join(difflist))
    #print(difflist)
    # if len(difflist) > 0:
    #     msg = MIMEText(' '.join(difflist))
    #     # me == the sender's email address
    #     # you == the recipient's email address
    #     msg['Subject'] = 'Problem with Master-Slave replication'
    #     msg['From'] = email.utils.formataddr(('Master-Slave replication', 'noreply@test'))
    #     msg['To'] = email.utils.formataddr(('Recipient', 'ignacioaracenar@gmail.com'))
    #     #server = smtplib.SMTP('192.168.10.49', 1025)
    #     #server.set_debuglevel(True)  # show communication with the server
    #     #try:
    #     #    server.sendmail('noreply@test', ['ignacioaracenar@gmail.com'], msg.as_string())
    #     #    print('send email')
    #     #finally:
    #     #    server.quit()
    #     # send email.
    #     sender = 'noreply@localhost'
    #     receivers = ['ignacioaracenar@gmail.com','it-desk@eurodriver.ch']
    #     #This is a test e-mail message.
    #     try:
    #         server = smtplib.SMTP('gmail-smtp-in.l.google.com:25')
    #         server.starttls()
    #         server.ehlo("example.com")
    #         server.mail(sender)
    #         server.rcpt(receivers[0])
    #         server.data(str(msg))
    #     finally:
    #         server.quit()
        """
        try:
            smtpObj = smtplib.SMTP('localhost',1025)
            smtpObj.sendmail(sender, receivers, message)
            print("Successfully sent email")
        except smtplib.SMTPException:
            print("Error: unable to send email")
        """
    df = pd.DataFrame(data, columns=['Type', 'Table', 'Def. Diff',
                                     'Row Count', 'Data Check'])
    return df.to_html(index=False).replace('\n','')


def filetohtml(infile='masterslave_comp.log', outdir='C:/Users/euroadmin/MasterSlaveComp/'):
    """
    Takes outout of mysqldbcompare from txt file and turns it into an HTML table
    :param infile: input log file
    :param outdir: directory
    :return: string with HTML
    """
    with open(outdir+infile, 'r',encoding='utf-16le') as f:
        data = []
        for line in f:
            if line.find('TABLE')!=-1:
                line = line.strip('#')
                line = line.split()
                data.append(line)
        df = pd.DataFrame(data, columns=['Type','Table','Def. Diff',
                                         'Row Count','Data Check'])
        x = df.to_html(index=False).replace('\n','') #.replace('\"','\\"')
        #ff = open('C:/Users/euroadmin/MasterSlaveComp/ll3.log', 'w')
        #print(x)
        #df.to_csv('C:/Users/euroadmin/MasterSlaveComp/ll2.log', index=False)
        return x


def get_page_info(pageid=65628):
    """
    Get confluence page info
    :param pageid:
    :return: json dict
    """
    url = '{base}/{pageid}'.format(
        base = BASE_URL,
        pageid = pageid)

    auth = ('admin', '1234')
    r = requests.get(url, auth = auth)
    r.raise_for_status()
    print(r.json())
    return r.json()


def updateconf(htmlcode):
    """
    Takes html and updates the Master-Slave status confluence page
    :param htmlcode:
    :return:
    """
    url = 'http://192.168.10.49:8090/rest/api/content/65628'
    #requests.put(url, data={'value',htmlcode.encode('ascii')}, auth=('admin','1234'))
    timeinfo = '<h2>Status at {timenow}</h2>'.format(timenow = time.strftime('%X %x %Z'))
    timeinfo = timeinfo.replace('\n','')
    comment = ('<p>This is page is automatically generated',
              ' - do not edit manually (edits won\'t be saved)</p>')
    pageinfo = get_page_info()
    htmlcode = str(timeinfo + htmlcode)
    print(htmlcode)
    updata = {
        'id' : str(65628),
        'type' : 'page',
        'title' : 'Master - Slave Status',
        'version' : {'number' : pageinfo['version']['number'] + 1},
        'space' : {'key' : "IT"},
        #'ancestors' : [anc],
        'body'  : {
            'storage' :
            {
                'representation' : 'storage',
                'value' : htmlcode,
            }
        }
    }
    updata = json.dumps(updata)
    r = requests.put(url, data=updata, auth=('admin','1234') ,headers = { 'Content-Type' : 'application/json' })
    print(r.text)
    return r


def updatequizstatus(key=u'CZV Gütertransporte', id=3145737):
    """
    Takes html and updates the Master-Slave status confluence page
    :param htmlcode:
    :return:
    """
    url = 'http://192.168.10.49:8090/rest/api/content/{}'.format(id)
    htmlcode = getquizstatus()
    for k,v in htmlcode.items():
        print(k)
    htmlcode = htmlcode[key]
    #requests.put(url, data={'value',htmlcode.encode('ascii')}, auth=('admin','1234'))
    timeinfo = '<h2>Status at {timenow}</h2>'.format(timenow = time.strftime('%X %x %Z'))
    timeinfo = timeinfo.replace('\n','')
    comment = ('<p>This is page is automatically generated',
              ' - do not edit manually (edits won\'t be saved)</p>')
    pageinfo = get_page_info(pageid=id)
    htmlcode = str(timeinfo + htmlcode)
    print(htmlcode)
    mykey = 'CZV - Gütertransporte'
    updata = {
        'id' : str(id),
        'type' : 'page',
        'title' : str(key),
        'version' : {'number' : pageinfo['version']['number'] + 1},
        'space' : {'key' : "EL"},
        #'ancestors' : [anc],
        'body'  : {
            'storage' :
            {
                'representation' : 'storage',
                'value' : htmlcode,
            }
        }
    }
    updata = json.dumps(updata)
    r = requests.put(url, data=updata, auth=('admin','1234') ,headers = { 'Content-Type' : 'application/json' })
    print(r.text)
    return r


def main():
    #r = updateconf(filetohtml())
    r = updateconf(list2html(rundbcompare()))
    print(r.status_code)
    assert r.status_code == 200


if __name__=='__main__':
    main()