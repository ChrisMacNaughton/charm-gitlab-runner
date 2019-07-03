#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.core import (
    hookenv,
    templating,
)

import gitlab_runner.docker as docker
import charmhelpers.fetch.ubuntu as ubuntu


hooks = hookenv.Hooks()


@hooks.hook('install')
def install():
    hookenv.log('Installing gitlab-runner')
    ubuntu.apt_install(ubuntu.filter_installed_packages(['docker.io']))
    docker.run_container()
    hookenv.log('Started gitlab-runner container')
    templating.render(
        source='update-gitlab-runner.sh',
        target='/etc/cron.daily/update-gitlab-runner.sh', context={},
        perms=0o755, owner='root', group='root'
    )


@hooks.hook('config-changed')
def config_changed():
    hookenv.log('Upgrading gitlab-runner')
    config = hookenv.config()
    gitlab_url = config.get('gitlab-url')
    runner_token = config.get('runner-token')

    if (gitlab_url is None or
        runner_token is None):
        hookenv.status_set('blocked', 'gitlab-url and runner-token are required')
        return
    docker.configure_container(
        gitlab_url=gitlab_url,
        runner_token=runner_token,
        tags=config.get('tags'),
        run_untagged=config.get('run-untagged'),
        base_image=config.get('docker-image'))
    hookenv.log('Configured gitlab-runner')
    hookenv.status_set('active', 'gitlab-runner is ready')


@hooks.hook('start')
def start():
    hookenv.log('Starting gitlab-runner')


@hooks.hook('stop')
def stop():
    hookenv.log('Stopping gitlab-runner')


@hooks.hook('upgrade-charm')
def upgrade_charm():
    hookenv.log('Upgrading gitlab-runner')


if __name__ == "__main__":
    # execute a hook based on the name the program is called by
    hooks.execute(sys.argv)
