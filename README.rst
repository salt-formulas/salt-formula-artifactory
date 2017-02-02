
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
Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate issue tracker. Use Github issue tracker for specific salt
formula:

    https://github.com/salt-formulas/salt-formula-artifactory/issues

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

You can also join salt-formulas-users team and subscribe to mailing list:

    https://launchpad.net/~salt-formulas-users

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit pull request against specific formula.

    https://github.com/salt-formulas/salt-formula-artifactory

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net
