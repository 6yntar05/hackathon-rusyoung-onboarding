#!/bin/sh

podman volume create nextcloud-app
podman volume create nextcloud-data
podman volume create nextcloud-db

podman run --detach --replace --env MYSQL_DATABASE=nextcloud \
        --env MYSQL_USER=nextcloud \
        --env MYSQL_PASSWORD=Y2lybm8K \
        --env MYSQL_ROOT_PASSWORD=Y2lybm8K \
        --volume nextcloud-db:/var/lib/mysql \
        --network nextcloud-net --restart on-failure \
        --name nextcloud-db docker.io/library/mariadb
    
podman run --replace --env MYSQL_HOST=nextcloud-db.dns.podman \
        --env MYSQL_DATABASE=nextcloud \
        --env MYSQL_USER=nextcloud \
        --env MYSQL_PASSWORD=Y2lybm8K \
        --env NEXTCLOUD_ADMIN_USER=admin \
        --env NEXTCLOUD_ADMIN_PASSWORD=cmVpbXUK \
        --env NEXTCLOUD_TRUSTED_DOMAINS=yourhost.com \
        --env NEXTCLOUD_HOSTNAME=yourhost.com \
        --env PHP_MEMORY_LIMIT=4096M \
        --volume nextcloud-app:/var/www/html \
        --volume nextcloud-data:/var/www/html/data \
        --volume yb-apache:/etc/apache2/ \
        --network nextcloud-net \
        --restart on-failure \
        --publish 80:80 --publish 443:443 \
        --name nextclown docker.io/library/nextcloud:24-apache
