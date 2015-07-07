===============
django-debian
===============

Reference Django application for building Debian packages.

All feedback or enhancements appreciated!

Installation
============

To follow some Debian packaging guides as well as LSB/FHS standards, following
hierarchy is used for Django installations:

.. list-table::
   :header-rows: 1

   *  - **Location**
      - **Purpose**
   *  - ``/usr/lib/django-debian``
      - Virtualenv root, this is read-only place where app ant it's
        dependencies live.
        Additional scripts like ``manage.py`` and ``gunicorn_start.sh`` are
        installed in bin directory of this root.
   *  - ``/var/lib/django-debian``

        ``/var/lib/django-debian/media``

        ``/var/lib/django-debian/static``
      - Variable files, media and statically served files.
        Static files are collected during package configuration with
        ``manage.py collectstatic``, run ``dpkg-reconfigure django-debian``
        to re-create static directory.
   *  - ``/etc/django-debian``

        ``/etc/django-debian/{settings,celery}.py``

        ``/etc/django-debian/gunicorn``
      - Configuration directory, place for overrides of default configuration,
        shipped with package.
        This configuration is also managed by `debconf`.
   *  - ``/etc/django-debian/templates``
      - Optional place for sysadmin maintained templates.
   *  - ``/usr/share/django-debian``

        ``/usr/share/django-debian/templates``
      - All support files that are not being changed over time and are not
        binaries or libraries should belong to ``/usr/share``. For Django
        application, templates are the best example.
   *  - ``/var/log/django-debian``

        ``/var/log/django-debian/django.log``
      - Place for non-syslog log files. Debconf script will set correct
        permissions on directory and ``django.log`` file for user/group used
        to run Django app.
   *  - ``/usr/share/doc/django-debian``
      - Additional documentation, readme, debian changelog, etc.

Reference
---------

- `Python virtualenv in Debian packages <https://github.com/spotify/dh-virtualenv>`_
- `Debian Django Packaging Guidelines <https://wiki.debian.org/DjangoPackagingDraft>`_

Configuration
=============

Sane defaults should be already part of distribution and set in
``django_helpdesk.settings`` and eventually
``django_helpdesk.celery_settings``. At best it should be defaults that will
run on any machine without additional configuration.

Default settings can be overriden in:

* ``/etc/django-debian/settings.py``
* ``/etc/django-debian/celery.py``
* ``/etc/django-debian/gunicorn``

  * this is sourced by ``gunicorn_start.sh`` script
  * it could be also ``/etc/default/django-debian`` as it contains common
    and startup settings for application

These configuration files are included from distribution ``settings.py`` by
following simple mechanism:

.. code-block:: python

   try:
       with open("/etc/django-debian/settings.py") as f:
           code = compile(f.read(), "/etc/django-debian/settings.py", 'exec')
           exec(code)
   except IOError:
       pass

Alternatively it can support configuration overrides in some common
configuration format, like yaml, ini, etc.

Some basic configuration is done immediately after package installation or
when ``dpkg-reconfigure``.
For more informations see ``debian/templates`` and ``debian/postinst``.

Package build
=============

To build version in current branch, you should use git-buildpackage and
pbuilder.
Pbuilder will create clean chroot environment and install required
dependencies so you don't need to mess up your system.

Alternatively you can install build dependencies on your own and execute plain
``dpkg-buildpackage -uc -us``

Install required packages
   .. code-block:: bash

      apt-get install cowbuilder pbuilder git-buildpackage dh-virtualenv dh-python

   .. attention::

       In case you are building whole virtualenv, you need latest dh-virtualenv (latest master, unreleased version 0.10) with support for overriding destination directory. This package is built in our repository but it probably won't be present in your OS distribution. Install it manually from our repo or build it on your own from https://github.com/spotify/dh-virtualenv

Configure pbuilder to allow network access (dh-virtualenv only)
    Create or edit ``~/.pbuilderrc`` and put following inside:

    .. code-block:: bash

       USENETWORK=yes

Create cowbuilder environment
    .. code-block:: bash

       cowbuilder --create

Build the package
   .. code-block:: bash

       git-buildpackage --git-pbuilder -uc -us --git-ignore-branch

   That will create source archive and run pbuilder which will create chroot,
   You need to commit or stash all your changes first.

TODO
====

- setup gunicorn and optionally nginx or apache
- setup database with dbconfig-common
