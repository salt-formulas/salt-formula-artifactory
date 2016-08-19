{%- if pillar.artifactory is defined %}
include:
{%- if pillar.artifactory.server is defined %}
- artifactory.server
{%- endif %}
{%- endif %}
