sudo apt install docker.io -y
с этой команды норм запускается: sudo docker compose up --build


ОШИБКА С ПОДКЛЮЧЕНИЕМ К ПОРТУ И НЕПРАВИЛЬНЫМ ПАРОЛЕМ
$ sudo -u postgres psql
\password
Enter password: ...
$ psql -U postgres -h localhost


ОШИБКА С ПОРТОМ И НЕ ПОДКЛЮЧЕНИЕМ
Go to Program Files/Postgres/<required_version>/data
Open the postgresql.conf file
Search for Port and change the port number to 5432.
Open Windows Services (Press Cmd + R then type services.msc)
Stop the service for the version you don't want (You can stop it permanentally from the Right Click > Properties menu.)
Start the service for the version you want.



ЕМАИЛ СЕРВИС
GMAIL login grsmu.check
password: fc6-5KJ-sT8-KK7



t = TemperatureData.objects.get(id=1)
t.value = 999  # change field
t.save() # this will update only


if not Group.objects.filter(name='customer').exists():

Для выбора предмета подойдет class Select
