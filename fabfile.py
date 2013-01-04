"""
Generic fabfile for my "static" web sites hosted on TextDrive. Knows how to
bootstrap and deploy those sites.

Assumptions:
 * We're operating in a directory with the same name as the web site
 * The github repo for the site has the same name as well
"""

import os
from fabric.api import abort, cd, env, run, task


env.hosts = ['overloaded.org']
env.use_ssh_config = True


def domain():
    return os.path.basename(os.path.dirname(__file__))


def web_dir():
    if domain() == 'overloaded.org':
        return '~/web/public'
    return '~/domains/{}/web/public'.format(domain())


def git_repo():
    return 'git@github.com:mccutchen/{}.git'.format(domain())


def dir_exists(dirname):
    cmd = '[ -d {} ]'.format(dirname)
    return run(cmd, warn_only=True, quiet=True).return_code == 0


@task
def check_domain():
    """Check to see whether this domain has been set up on the server side."""
    if not dir_exists(web_dir()):
        abort('Domain {} not configured'.format(domain()))


@task
def bootstrap():
    """Ensures that the server has the domain set up and makes a clean
    checkout of the site's source code and moves it into place.
    """
    check_domain()
    if dir_exists(os.path.join(web_dir(), '.git')):
        abort('Web directory already a git repo: {}'.format(web_dir()))

    run('mkdir -p ~/tmp')
    with cd('~/tmp'):
        run('rm -rf repo')
        run('git clone {} repo'.format(git_repo()))
        run('mv repo/.git {}'.format(web_dir()))
        run('rm -rf repo')

    with cd(web_dir()):
        run('rm -f index.*')

    deploy()


@task
def deploy(branch='master'):
    """Deploy latest code in origin/master (or the specified branch)."""
    check_domain()
    with cd(web_dir()):
        run('git fetch origin && git reset --hard origin/{}'.format(branch))
