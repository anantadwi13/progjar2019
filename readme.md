# Pemrograman Jaringan

Ananta Dwi Prasetya Purna Yuda  
05111740000029

## Tugas 9

### Test Benchmark

#### a. server_async_http  

Command

``` shell script
ab -n 1000 -c <concurrency> http://127.0.0.1:45000/testing.txt
```

Result  

No test|Concurrency level|Time taken for test (seconds)|Complete request|Failed request|Total transferred (bytes)|Request per second|Time per request (ms)|Transfer rate (KBps)
:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:
1|1|0.421|1000|0|159000|2374.63|0.421|368.72
2|5|0.332|1000|0|159000|3006.87|0.330|466.89
3|10|0.329|1000|0|159000|3037.46|0.329|471.64
4|20|0.342|1000|0|159000|2925.69|0.342|454.28
5|25|0.346|1000|0|159000|2892.05|0.346|449.06



#### b. server_thread_http

Command

``` shell script
ab -n 1000 -c <concurrency> http://127.0.0.1:46000/testing.txt
```

Result  

No test|Concurrency level|Time taken for test (seconds)|Complete request|Failed request|Total transferred (bytes)|Request per second|Time per request (ms)|Transfer rate (KBps)
:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:
1|1|0.488|1000|0|159000|2049.64|0.488|318.26
2|5|0.489|1000|0|159000|2045.84|0.489|317.66
3|10|-|-|-|-|-|-|-
4|20|-|-|-|-|-|-|-
5|25|-|-|-|-|-|-|-

Test ke 3 - 5 gagal dengan pesan error `Connection reset by peer`