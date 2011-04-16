from fabric.api import local, put, sudo
from jinja2 import Environment, PackageLoader

from deploymachine.conf import settings
from deploymachine.fablib.fab import venv, venv_local


def collectstatic(site=None):
    """
    Build the static media files.
    Usage:
        fab collectstatic:sitename
    """
    if site is None:
        site_list = settings.SITES
    else:
        site_list = [site]
    for site in site_list:
        venv("python manage.py collectstatic --noinput", site)

def generate_settings_main(connection, site=None):
    """
    Generate the site(s) main ``settings.py`` file.
    Usage:
        fab settings:dev,sitename
    """
    env = Environment(loader=PackageLoader("deploymachine", "templates"))
    template = env.get_template("scene_machine_settings.j2")
    if site is None:
        site_list = settings.SITES
    else:
        site_list = [site]
    for site in site_list:
        result = template.render(settings.SETTINGS_CUSTOM[site])
        if connection == "dev":
            r_file = open("{0}{1}/{1}/settings.py".format(
                settings.SITES_LOCAL_ROOT, site), "w")
            r_file.write(result)
            r_file.close()
        elif connection == "prod":
            print("not implemented yet")
        else:
            print("Bad connection type. Use ``dev`` or ``prod``.")


def generate_settings_local(connection, site=None):
    """
    Generate the site(s) settings_local files.
    Usage:
        fab settings:dev,sitename
    """
    if site is None:
        site_list = settings.SITES
    else:
        site_list = [site]
    for site in site_list:
        if connection == "dev":
            print("TODO")
            #venv_local("cp {0}/settings_local_dev/{1}.py /var/www/{1}/settings_local.py".format(settings.DEPLOYMACHINE_ROOT, site), site)
        elif connection == "prod":
            print("TODO")
            #put("{0}/settings_local_prod/{1}.py".format(settings.DEPLOYMACHINE_ROOT, site), "/tmp/settings_local.py", mode=0755)
            #sudo("chown deploy:webmaster /tmp/settings_local.py && mv /tmp/settings_local.py /var/www/{0}/settings_local.py".format(site))
        else:
            print("Bad connection type. Use ``dev`` or ``prod``.")


def syncdb(site):
    "Call syncdb for the given site."
    venv("python manage.py syncdb --noinput".format(site), site)


def test():
    "Run tests."
    local("python manage.py test")


#@@ migrations stuff
