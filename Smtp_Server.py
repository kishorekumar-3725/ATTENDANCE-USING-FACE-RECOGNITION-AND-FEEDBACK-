import smtplib
from email.message import EmailMessage
%store -r dic

def email(sub,body,to):
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=sub
    msg['to']=to
    
    user="latish9347@gmail.com"
    msg['from']=user
    password="umljhzlkolkaynrn"
    
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()
name="Sai_latish"
name1="x"
for i in dic:
    if(i==name):
        emid=dic[i]
        for i in range(10):
            if(name1==name):
                print("hey")
                break
            else:
                print("hei")
                email("Hey!","Your attendence have been marked",emid)
            name1=name
        break