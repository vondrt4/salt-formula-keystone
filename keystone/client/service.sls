{%- from "keystone/map.jinja" import client with context %}
{%- if client.enabled %}

keystone_client_packages:
  pkg.installed:
  - names: {{ client.pkgs }}

keystone_profile:
  file.managed:
  - name: /etc/salt/minion.d/_keystone.conf
  - source: salt://keystone/files/keystone.conf
  - template: jinja

{%- endif %}