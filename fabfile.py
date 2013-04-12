"""
Generic fabfile for my "static" web sites hosted on TextDrive. Knows how to
bootstrap and deploy those sites.

Assumptions:
 * We're operating in a directory with the same name as the web site
 * The github repo for the site has the same name as well
"""

import os
from fabric.api import abort, env, local, run, task

env.hosts = ['overloaded.org']
env.use_ssh_config = True


def domain():
    return os.path.basename(os.path.dirname(__file__))


def web_dir():
    if domain() == 'overloaded.org':
        return '~/web/public'
    return '~/domains/{}/web/public'.format(domain())


def dir_exists(dirname):
    cmd = '[ -d {} ]'.format(dirname)
    return run(cmd, warn_only=True, quiet=True).return_code == 0


@task
def check_domain():
    """Check to see whether this domain has been set up on the server side."""
    if not dir_exists(web_dir()):
        abort('Domain {} not configured'.format(domain()))


@task
def deploy():
    """Build and deploy a new version of the site."""
    check_domain()
    build()
    src = 'dist/'
    dst = '{}:{}'.format(env.hosts[0], web_dir())
    if not dst.endswith('/'):
        dst = dst + '/'
    local('rsync --verbose --progress --recursive --delete {} {}'.format(src, dst))
    clean()


@task
def build():
    """Build a new index.html page from the Python docs."""
    clean()
    local('cp -r resources dist')
    local('./build.py > dist/index.html')


@task
def clean():
    """Clean up after a build."""
    local('rm -rf dist')
