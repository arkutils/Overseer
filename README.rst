Overseer
========

Project Overseer - watching Ark data

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Requirements
------------

This project is configured to work with Docker inside of VS Code using the
Remote Containers extension_. It is recommend to use those. So make sure you have:

* Docker_
* VS Code_ with the Remote Containers extension_.

.. _Docker: https://docs.docker.com/get-docker/
.. _VS Code: https://code.visualstudio.com/
.. _Remote Containers extension_: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

Setup
-----

1. Clone the repo.
2. Copy `docker-compose.override.example.yml` to `docker-compose.override.yml`
     and update the path you your local ARK install
3. Then open the `overseer` folder in VS Code.
4. You should be prompted to "Reopen in Container". If you are not, run the
     "Remote-Containers: Reopen in Container" from the Command Palette
     (`View -> Command Palette...` or `Ctrl+Shift+P`)
5. VS Code will now build the Docker images and start them up. When it is
     done, you should see a normal VS Code Workspace
6. Go to http://127.0.0.1:8000 in your Web browser and click "Sign In".
     Then sign in with Discord or Github
7. Back in VS Code, run the command "Tasks: Run Task" and then "Overseer: Make Superuser".
     Enter the username for your user when prompted.
