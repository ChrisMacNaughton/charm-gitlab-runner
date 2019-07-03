import subprocess
from charmhelpers.core.hookenv import log


def configure_container(gitlab_url, runner_token, tags,
                        run_untagged, base_image):
    command="""register \
--non-interactive \
--url="{}" \
--registration-token="{}" \
--executor="docker" \
--docker-image {} \
--description="docker-runner" \
--tag-list="{}" \
--run-untagged={} \
--locked=false
""".format(
        gitlab_url, runner_token, base_image, tags, str(run_untagged).lower()).split()
    run_command('gitlab/gitlab-runner', command=command,
                volumes=['/srv/gitlab-runner/config:/etc/gitlab-runner'])


def run_container():
    run(
        'gitlab_runner', container='gitlab/gitlab-runner:latest',
        volumes=[
            '/srv/gitlab-runner/config:/etc/gitlab-runner',
            '/var/run/docker.sock:/var/run/docker.sock',
        ])


def run(container_name, container, restart="always", volumes=None):
    if not volumes:
        volumes = []
    cmd = [
        'docker', 'run', '-d', '--name', container_name, '--restart', restart,
    ]
    for volume in volumes:
        cmd.append('-v')
        cmd.append(volume)
    cmd.append(container)
    return subprocess.check_output(cmd)


def run_command(container_name, command, volumes=None):
    if not volumes:
        volumes = []
    cmd = [
        'docker', 'run', '--rm', '-i'
    ]
    for volume in volumes:
        cmd.append('-v')
        cmd.append(volume)
    cmd.append(container_name)
    cmd.extend(command)
    log('Running "{}"'.format(cmd))
    return subprocess.check_output(cmd)