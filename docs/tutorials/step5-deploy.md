## Caddy

> Caddy is the HTTP/2 web server with automatic HTTPS.

[https://caddyserver.com/docs](https://caddyserver.com/docs)

Make sure you install caddy:

```text
$ caddy -version
Caddy 0.10.10 (non-commercial use only)
```

## Gunicorn 

> Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. 
It's a pre-fork worker model. 
The Gunicorn server is broadly compatible with various web frameworks, 
simply implemented, light on server resources, and fairly speedy.

Make sure you install caddy:

```text
$ gunicorn -v
gunicorn (version 19.7.1)
```

## Run!

Launch gunicorn: gunicorn -b "127.0.0.1:5000" wsgi Usually, 
you will have your gunicorn script on a supervisor, or something else

```text
$ gunicorn -b "127.0.0.1:5000" wsgi:app 
[2017-12-26 10:55:18 +0800] [21545] [INFO] Starting gunicorn 19.7.1
[2017-12-26 10:55:18 +0800] [21545] [INFO] Listening at: http://127.0.0.1:5000 (21545)
[2017-12-26 10:55:18 +0800] [21545] [INFO] Using worker: sync
[2017-12-26 10:55:18 +0800] [21548] [INFO] Booting worker with pid: 21548
2017/12/26 10:55:18 [Register] OK <Pixabay> 
2017/12/26 10:55:18 [Register] OK <Pexels> 
```

Create Caddyfile

```text
$ touch Caddyfile
```

Edit the Caddyfile as follows:

```text
:8080 {
    proxy / localhost:5000 {
        transparent
    }
}
```

Next step:

```text
$ caddy
Activating privacy features... done.
http://localhost:8080
```

Well done! Everything is ok! You can get more information from `topics` or just 
go to write your own APIs!

## The result directory structure:

```text
$ tree .   
.
├── app.py
├── Caddyfile
├── data.sqlite
├── items
│   ├── __init__.py
│   ├── pexels.py
│   ├── pixabay.py
│   └── __pycache__
│       ├── __init__.cpython-36.pyc
│       ├── pexels.cpython-36.pyc
│       └── pixabay.cpython-36.pyc
├── __pycache__
│   ├── app.cpython-36.pyc
│   ├── settings.cpython-36.pyc
│   └── wsgi.cpython-36.pyc
├── README.md
├── settings.py
└── wsgi.py

3 directories, 15 files
```