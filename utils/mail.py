# pylint: disable=maybe-no-member

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    def __init__(self, **kwargs):
        mandatory_args = ["username", "password", "server", "port"]
        for x in mandatory_args:
            if kwargs.get(x, False) == False:
                raise ValueError("%s must be provided" % (x))
            self.__dict__[x] = kwargs[x]

    def send(self, **kwargs):
        mandatory_args = ["subject", "source", "to", "content", "content_type"]
        for x in mandatory_args:
            if not kwargs.get(x, False):
                raise ValueError("%s is mandatory" % (x))

        msg = MIMEMultipart('alternative')
        msg['Subject'] = kwargs['subject']
        msg['From'] = kwargs['source']
        msg['To'] = kwargs['to']

        content = MIMEText(kwargs['content'], kwargs['content_type'])
        msg.attach(content)
        s = smtplib.SMTP(self.server, self.port)
        s.login(self.username, self.password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

    def sendHTML(self, **kwargs):
        kwargs['content_type'] = "html"
        return self.send(**kwargs)

    def sendText(self, **kwargs):
        kwargs['content_type'] = "plain"
        return self.send(**kwargs)
