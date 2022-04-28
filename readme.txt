sudo apt install docker.io -y
с этой команды норм запускается: sudo docker compose up --build

ОШИБКА С ПОДКЛЮЧЕНИЕМ К ПОРТУ И НЕПРАВИЛЬНЫМ ПАРОЛЕМ
{$ sudo -u postgres psql
\password
Enter password: ...
$ psql -U postgres -h localhost}

if not Group.objects.filter(name='customer').exists():