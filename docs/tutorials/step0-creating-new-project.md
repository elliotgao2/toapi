## New Project

You can run the command 'toapi new' whenever you want to start a new api server.

```text
$ toapi new toapi/toapi-pic
2017/12/26 11:41:38 [New project] OK Creating project directory "toapi-pic" 
Cloning into 'toapi-pic'...
remote: Counting objects: 13, done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 13 (delta 2), reused 9 (delta 1), pack-reused 0
Unpacking objects: 100% (13/13), done.
Checking connectivity... done.
2017/12/26 11:41:40 [New project] OK Success! 

     cd toapi-pic
     toapi run

```

This command create a new folder named `toapi-pic`, which include some files:

```text
$ tree .                   
.
├── app.py
├── items
│   ├── __init__.py
│   ├── pexels.py
│   └── pixabay.py
├── README.md
├── settings.py
└── wsgi.py

1 directory, 7 files
```

- app.py: define the app instance.
- settings.py: global configs.
- items: define items you want to extract.
- wsgi.py: expose interface to gunicorn, uwsgi .etc for serving.