Overseer
========

Project Overseer - bossing around Purlovia

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: LGPLv3


Requirements
------------

This project is configured to work with Docker inside of VS Code using the
Remote Containers extension. It is recommend to use those. So make sure you have:

* `Docker`_
* `VS Code`_ with the `Remote Containers extension`_.

.. _Docker: https://docs.docker.com/get-docker/
.. _VS Code: https://code.visualstudio.com/
.. _Remote Containers extension: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

Setup
-----

#. Clone the repo.
#. Copy `docker-compose.override.example.yml` to `docker-compose.override.yml`
   and update the path you your local ARK install
#. Then open the `overseer` folder in VS Code.
#. Ensure the extension "Remote - Containers" (ms-vscode-remote.remote-containers) is installed.
#. You should be prompted to "Reopen in Container". If you are not, run the
   "Remote-Containers: Reopen in Container" from the Command Palette
   (`View -> Command Palette...` or `Ctrl+Shift+P`)
#. VS Code will now build the Docker images and start them up. When it is
   done, you should see a normal VS Code Workspace
#. Go to http://127.0.0.1:8000 in your Web browser and click "Sign In".
   Then sign in with Discord or Github
#. Back in VS Code, run the command "Tasks: Run Task" and then "Overseer: Make Superuser".
#. Enter the username for your user when prompted.
