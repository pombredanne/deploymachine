# scenemachine specific
from fabric.api import cd, env, local, sudo

from deploymachine.conf import settings
from deploymachine.fablib.django import collectstatic, settings_local
from deploymachine.fablib.dvcs.git import git_pull, git_pull_deploymachine
from deploymachine.fablib.supervisor import supervisor
from deploymachine.fablib.fab import venv, venv_local


PYDISCOGS_ROOT = "{0}/pydiscogs/pydiscogs".format(LIB_ROOT)


def deploy_git_rizumu():
    git_pull("rizumu")
    git_pull_scenemachine()
    collectstatic("rizumu")
    supervisor("rizumu")


def git_pull_sceneachine():
    with cd(settings.SCENEMACHINE_ROOT):
        sudo("git pull", user=env.user)


def git_pull_pinax():
    with cd(settings.PINAX_ROOT):
        sudo("git pull", user=env.user)


def dump_data_rizumu():
    venv("python manage.py dumpdata --format=yaml --indent=4 --natural \
          events people music places hyperlinks > ../../dumps/sitedump.yaml", "rizumu")


def loaddata_sites(connection):
    if connection == 'dev':
        venv_local("python manage.py loaddata\
        /home/deploy/www/lib/scenemachine/scenemachine/fixtures/sites/site_data.yaml", "smus")
    elif connection == "prod":
        venv("python manage.py loaddata\
        /home/deploy/www/lib/scenemachine/scenemachine/fixtures/sites/site_data.yaml", "smus")
    else:
        print("Bad connection type. Use ``dev`` or ``prod``.")


def full_deploy(collectstatic=False):
    """
    Full scenemachine deploy
    Usage:
        fab appbalancer full_deploy:collectstatic=True

    Remember to handle requirements separately.
    """
    git_pull_deploymachine()
    git_pull_scenemachine()
    settings_local("prod")
    git_pull()
    if collectstatic:
        collectstatic()


def symlinks(connection, site=None):
    """
    Link pinax & pydiscogs into the virtualenv's site-packages.
    @@@ this is hardcoded ugliness
    Usage:
        fab appnode symlinks:prod,sitename
    """
    if site is None:
        site_list = settings.SITES
    else:
        site_list = [site]
    if connection == "dev":
        site_packages = join(settings.VIRTUALENVS_ROOT, site,
                        "/lib/python{0}".format(settings.PYTHON_VERSION),
                        "/site-packages/")
        for site in site_list:
            local("ln -sf {0} {1}".format(settings.PINAX_ROOT, 
                  join(site_packages, "/pinax")))
            local("ln -sf {0} {1}".format(settings.PYDISCOGS_ROOT, 
                  join(site_packages, "/pydiscogs")))
            local("ln -sf {0} {1}".format(join(settings.DEPLOYMACHINE_ROOT, "/fabfile.py", 
                                          join(settings.SITES_ROOT, site, site, "/fabfile.py"))
            local("ln -sf {0} {1}".format(join(settings.DEPLOYMACHINE_ROOT, "/settings.py"), 
                                          join(settings.SITES_ROOT, site, site, "/settings.py")
            local("ln -sf {0} {1}".format(join(settings.DEPLOYMACHINE_ROOT, "/fablib/"),
                                          join(settings.SITES_ROOT, site, site, "/fablib/"))
        local("ln -sf {0} {1}".format(join(settings.SCENEMACHINE_ROOT, "/fabfile.py"),
                                      join(settings.DEPLOYMACHINE_ROOT, "/fabfile.py"))
        local("ln -sf {0} {1}".format(join(settings.SCENEMACHINE_ROOT, "/settings.py"),
                                      join(settings.DEPLOYMACHINE_ROOT, "/settings.py"))
        local("ln -sf {0} {1}".format(join(settings.SCENEMACHINE_ROOT, "/fablib/"),
                                      join(settings.DEPLOYMACHINE_ROOT, "/fablib/"))
    elif connection == "prod":
        for site in site_list:
1            with cd(site_packages):
                sudo("ln -sf {0}".format(settings.PINAX_ROOT, user="deploy")
                sudo("ln -sf {0}".format(settings.PYDISCOGS_ROOT), user="deploy")
    else:
        print("Bad connection type. Use ``dev`` or ``prod``.")

