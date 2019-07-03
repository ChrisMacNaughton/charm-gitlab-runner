#!/bin/bash

set -eu -o pipefail
out=$(docker pull gitlab/gitlab-runner:latest)

date=$(date +%Y%m%d)
echo $out | grep "Downloaded newer image" || echo "$date: Already up to date" >> /var/log/update-gitlab-runner && exit 0

docker stop gitlab-runner && docker rm gitlab-runner

docker run -d --name gitlab-runner --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  gitlab/gitlab-runner:latest

echo "date: Updated runner" >> /var/log/update-gitlab-runner
