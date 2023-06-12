# Final Project Progjar A Kelompok 3

## Nama Anggota Kelompok 3
1. Danial Farros Maulana / 5025201004 
2. Helsa Nesta Dhaifullah / 5025201005
3. Kurnia Cahya Febryanto / 5025201073
4. Hansen Idden / 5025201100
5. Mochamad Revanza Kurniawan / 5025201145
6. Eldenabih Tavirazin Lutvie  / 5025201213

## Protokol
server 
- berjalan di port 8889
- lokasi program ./app/server/server.py

client 
- berjalan di mode web port 8550
- lokasi program ./app/client/client-flet.py

client desktop
- cd ./app/client-desktop
- sh run.sh

## Fungsionalitas
A. Autentikasi
  - Login user <br>
  ```auth <username> <password>``` <br>
  ```auth messi surabaya```
  - Register <br>
  ```register <username> <password> <nama (kalo lebih dari 1, pisahkan dengan '_'> <negara>``` <br>
  ```register ronaldo surabaya Cristiano_Ronaldo Portugal```
  - Info user aktif <br>
  ```info```
  - Logout <br>
  ```logout```
  - Daftar User Password :
    - messi surabaya
    - henderson surabaya
    - lineker surabaya
   
B. Komunikasi dalam satu server
  - send private message <br>
   ```send <user_dest> <message>``` <br>
    ```send henderson apa kabar son```
  - send group message <br>
  ```sendgroup <user_dest 1>,<user_dest 2>,...,<user_dest n> <message>``` <br>
  ```sendgroup henderson,lineker halo gaiss apa kabar```
  - send file + simpan file <br>
  ```sendfile <user_dest> <file_path>``` <br>
  ```sendfile henderson pokijan.jpg```
  - send group file (banyak user) + simpan file <br>
  ```sendgroupfile <user_dest 1>,<user_dest 2>,...,<user_dest n> <file path>``` <br>
  ```sendgroupfile henderson,lineker pokijan.jpg```
  - inbox <br>
  ```inbox```

C. Komunikasi dengan server lain
  - addrealm <br>
  ```addrealm <nama_realm> <ip_dest> <port_dest>``` <br>
  ```addrealm realm1 172.16.16.102 8890```
  - send private message realm <br>
  ```sendprivaterealm <nama_realm> <user_dest> <message>``` <br>
  ```sendprivaterealm realm1 henderson bagaimana son di mesin 2```
  - send group message realm <br>
   ```sendgrouprealm <nama_realm> <user_dest 1>,<user_dest 2>,...,<user_dest n> <message>``` <br>
   ```sendgrouprealm realm1 henderson,lineker bagaimana kalian di mesin 2```
  - send file realm + simpan file <br>
  ```sendfilerealm <nama_realm> <user_dest> <file_path>``` <br>
  ```sendfilerealm realm1 henderson pokijan.jpg```
  - send group file realm (banyak user) + simpan file <br>
  ```sendgroupfilerealm <nama_realm> <user_dest 1>,<user_dest 2>,...,<user_dest n> <file_path>``` <br>
  ```sendgroupfilerealm realm1 henderson,lineker pokijan.jpg```
  - inbox realm <br>
  ```getinboxrealm <nama_realm> <username>``` <br>
  ```getinboxrealm realm1 henderson```
