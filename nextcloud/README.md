## Web решение
Создано на основе nextcloud <br>
Эталонно использует rockylinux и podman для разворачивания <br>

## Деплой
### Подготовка ОС:
#### RockyLinux
- `dnf update && dnf install epel-release mod_ssl -y && dnf install git podman podman-compose certbot python3-certbot-apache`
- `cd hackathon-rusyoung-onboarding # К этому моменту у вас уже склонирован репозиторий`
#### Другие
- Похожим образом
  
### Разворачивание контейнеров
В репозиторие представлены docker-compose.yml и build.sh, оба делают примерно одно и то же. <br>
Развертку будем производить с помощью podman и podman-compose <br>
- `# Перейдите в папку c docker-compose:`
- `cd nextcloud`
- `# Измените содержимое docker-compose.yml, а именно пароли и домены под себя`
- `podman-compose up`
- `# Начнётся деплой, через некоторое время будет доступно соединение по http`

### Настройка и доводка
Все volumes от root хранятся в `/var/lib/containers/storage/volumes/`

#### Настройка SSL
В volume `yb-apache` создайте папку `pem`, содержащую `server.crt` и `server.key` - сертификат и закыртый ключ <br>
Скопируйте конфиги из volume/yb-apache для включения ssl <br>
Если apache по-умолчанию не загружает модуль ssl, подключитесь к контейнеру и введите `a2enmod ssl` <br>
По-умолчанию nextcloud разрешает логин только через https соединение <br>

#### Настройка nextcloud
В соответствии с данными из docker-compose.yml/build.sh войдите в админский аккаунт nextcloud. Приступайте к настройке для своей организации:
- Согласно `./usercase/groupList` установите плагины, их настройки будут доступны в общей вкладке настроек, вы сможете настроить всё под свою организацию.
- Согласно `./usercase/pluginsList` создайте группы, добавьте свои по вкусу. Там же описана их специфика и настройки.
- Согласно `./usercase/userList` создайте юзеров, добавьте своих, распределите их по группам
- Перейдите в настройки дизайна, смените логотип и акцентный свет, для целевой организации это `brending/*`
