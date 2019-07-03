import mock
import unittest
import gitlab_runner.docker as docker


class GitlabRunnerDockerTest(unittest.TestCase):

    @mock.patch('gitlab_runner.docker.run')
    def test_it_sets_up_runner(self, _run):
        docker.run_container()
        _run.assert_called_once_with(
            'gitlab_runner', container='gitlab/gitlab-runner:latest',
            volumes=[
                '/srv/gitlab-runner/config:/etc/gitlab-runner',
                '/var/run/docker.sock:/var/run/docker.sock',
            ])

    @mock.patch('gitlab_runner.docker.subprocess.check_output')
    def test_it_runs_container(self, _check_output):
        docker.run(
            'gitlab_runner', container='gitlab/gitlab-runner:latest',
            volumes=[
                '/srv/gitlab-runner/config:/etc/gitlab-runner',
                '/var/run/docker.sock:/var/run/docker.sock',
            ])
        _check_output.assert_called_once_with([
            'docker', 'run', '-d', '--name', 'gitlab_runner',
            '--restart', 'always',
            '-v', '/srv/gitlab-runner/config:/etc/gitlab-runner',
            '-v', '/var/run/docker.sock:/var/run/docker.sock',
            'gitlab/gitlab-runner:latest'
        ])
