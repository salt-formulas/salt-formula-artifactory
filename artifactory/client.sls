{% from "artifactory/map.jinja" import client with context %}
{%- if client.enabled %}

artifactory_client_install:
  pkg.installed:
  - names: {{ client.pkgs }}

/etc/salt/minion.d/_artifactory.conf:
  file.managed:
  - source: salt://artifactory/files/_artifactory.conf
  - template: jinja

{%- for repo_name, repo in client.repo.iteritems() %}

artifactory_client_repo_{{ repo_name }}:
  artifactory_repo.repo_present:
  - name: {{ repo_name }}
  - repo_type: {{ repo.repo_type }}
  - package_type: {{ repo.package_type }}
  {%- if repo.url is defined %}
  - url: {{ repo.url }}
  {%- endif %}

{%- endfor %}

{%- endif %}
