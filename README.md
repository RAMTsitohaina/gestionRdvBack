# Backend gestion de rendez-vous


## Configuration

Cloner le repository: 
```sh
$ git clone https://github.com/RAMTsitohaina/gestionRdvBack.git
$ cd gestionRdvBack
```

Créer un environnement virtuel pour installer tous les dépendences et l'activer: 

Linux
```sh
$ virtualenv --python=python3 venv
$ source venv/bin/activate
```
Windows
```sh
$ py -m venv venv
$ venv\Scripts\activate
```

Installer les dépendences:
```sh
(env)$ cd gestionContactRdvBack
(env)$ pip install -r requirements.txt
```
À noter que le `(env)` avant la commande indique que le terminal fonctionne dans un environnement virtuel.  

Configurer l'environnement pour accéder au base de données : 

Créer un fichier .env

Copier les codes dans .env-examples vers le nouveau fichier .env en suivant les instructions dans .env-examples

Une fois que pip a fini de télécharger les dépendances :
```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
