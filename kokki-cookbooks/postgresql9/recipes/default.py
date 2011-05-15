
import os
from kokki import Execute, Package

apt_list_path = '/etc/apt/sources.list.d/pitti-postgresql-lucid.list'

Execute("apt-update-postgresql9", command = "apt-get update", action = "nothing")

apt = None
if env.system.platform == "ubuntu":
    Package("python-software-properties")
    Execute("add-apt-repository ppa:pitti/postgresql",
        not_if = lambda:os.path.exists(apt_list_path),
        notifies = [("run", env.resources["Execute"]["apt-update-postgresql9"], True)])
