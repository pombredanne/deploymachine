import os
from kokki import Execute, File, Package, Service, Template


Service("sendmail",
    supports_restart=True,
    supports_reload=True,
    supports_status=True,
    action="nothing")

Package("sasl2-bin")
Package("sendmail")

Execute("sendmailconfig", command="sendmailconfig --no-reload", action="nothing")
Execute("newaliases", command="newaliases", action="nothing")

File("/etc/mail/sendmail.mc",
    owner="root",
    group="smmsp",
    mode=0644,
    content=Template("sendmail/sendmail.mc.j2"),
    notifies=[("run", env.resources["Execute"]["sendmailconfig"], True),
              ("restart", env.resources["Service"]["sendmail"])])

File("/etc/mail/submit.mc",
    owner="root",
    group="smmsp",
    mode=0644,
    content=Template("sendmail/submit.mc.j2"),
    notifies=[("run", env.resources["Execute"]["sendmailconfig"], True),
              ("restart", env.resources["Service"]["sendmail"])])

File("/etc/aliases",
    owner="root",
    group="root",
    mode=0644,
    content=Template("sendmail/aliases.j2"),
    notifies=[("run", env.resources["Execute"]["newaliases"], True)])

# Unfortunately, there is no automagic way to migrate to /etc/sasldb2 :(
# You'll want to make sure /etc/default/saslauthd is setup to start,
# and has at least MECHANISMS="pam" !


#❄  sudo newaliases
#WARNING: local host name (dbserver) is not qualified; see cf/README: WHO AM I?
