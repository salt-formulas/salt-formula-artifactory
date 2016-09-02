
===========
Artifactory
===========

JFrog Artifactory is the only Universal Repository Manager supporting all major packaging formats, build tools and CI servers.


Sample pillars
==============

Server
------

Single artifactory OSS edition from OS package

.. code-block:: yaml

    artifactory:
      server:
        enabled: true
        edition: oss
        version: 4
        source:
          engine: pkg

Single artifactory pro edition from OS package

.. code-block:: yaml

    artifactory:
      server:
        enabled: true
        edition: pro
        version: 4
        source:
          engine: pkg

Single artifactory with PostgreSQL database

.. code-block:: yaml

    artifactory:
      server:
        database:
          engine: postgresql
          host: localhost
          port: 5432
          name: artifactory
          user: artifactory
          password: pass

Client
------

Basic client setup

.. code-block:: yaml

    artifactory:
      client:
        enabled: true
        server:
          host: 10.10.10.148
          port: 8081
          user: admin
          password: password

Artifactory repository definition

.. code-block:: yaml

    artifactory:
      client:
        enabled: true
      repo:
        local_artifactory_repo:
          name: local_artifactory_repo
          package_type: docker
          repo_type: local
        remote_artifactory_repo:
          name: remote_artifactory_repo
          package_type: generic
          repo_type: remote
          url: "http://totheremoterepo:80/"

Read more
=========

* https://www.jfrog.com/confluence/display/RTF/Debian+Repositories
* https://www.jfrog.com/confluence/display/RTF/PostgreSQL
* https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API#ArtifactoryRESTAPI-REPOSITORIES
* https://www.jfrog.com/confluence/display/RTF/Repository+Configuration+JSON