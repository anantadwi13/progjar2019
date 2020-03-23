# Pemrograman Jaringan

Ananta Dwi Prasetya Purna Yuda  
05111740000029

## Tugas 4

## Usage
### Running Server
```bash
python3 server.py <IP> <PORT>

# example
python3 server.py
python3 server.py localhost 80
```
### Running Client
```bash
python3 client.py <IP> <PORT> <COMMAND> <ARG_COMMAND>

# example
python3 client.py localhost 80 list
python3 client.py localhost 80 delete screenshot.jpg
```

## Environment
- Client dan Server memiliki direktori penyimpanan masing-masing (terltak pada client_data/data dan server_data/data)
- Client dan Server memiliki file config masing-masing, yang berisi path `base_directory` yang digunakan sebagai penyimpanan sementara
- Terdapat fitur list, put, get, delete
    ```bash
    python3 client.py localhost 80 list # melihat isi base_directory server
    python3 client.py localhost 80 put xyz # upload file xyz dari base_directory client ke base_directory server
    python3 client.py localhost 80 get xyz # download file xyz dari base_directory server ke base_directory client
    python3 client.py localhost 80 delete xyz # hapus file xyz yang ada pada base_directory server
    ```
-  API untuk komunikasi antara client dan server menggunakan format JSON
    ```json
    {"command": "get", "payload": "data", "is_bytes": false}
    ```
   - `command` sebagai perintah yang akan dijalankan, daftar `command` dapat dilihat pada [Network.py](dependencies/Network.py)
   - `payload` berisikan data yang akan ditransfer
   - `is_bytes` menandakan apakah payload yang dikirim perlu diencode atau tidak
- Format response yang diterima client sama seperti format JSON di atas. Namun apabila response yang diterima error, atribut `command` akan berisikan `error` 