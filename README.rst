==================
OpenStack Keystone
==================

Keystone provides authentication, authorization and service discovery mechanisms via HTTP primarily for use by projects in the OpenStack family. It is most commonly deployed as an HTTP interface to existing identity systems, such as LDAP.

From Kilo release Keystone v3 endpoint has definition without version in url

.. code-block:: bash

  +----------------------------------+-----------+--------------------------+--------------------------+---------------------------+----------------------------------+
  |                id                |   region  |        publicurl         |       internalurl        |          adminurl         |            service_id            |
  +----------------------------------+-----------+--------------------------+--------------------------+---------------------------+----------------------------------+
  | 91663a8db11c487c9253c8c456863494 | RegionOne | http://10.0.150.37:5000/ | http://10.0.150.37:5000/ | http://10.0.150.37:35357/ | 0fd2dba3153d45a1ba7f709cfc2d69c9 |
  +----------------------------------+-----------+--------------------------+--------------------------+---------------------------+----------------------------------+


Sample pillars
==============

Full stacked keystone

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        version: juno
        service_token: 'service_tokeen'
        service_tenant: service
        service_password: 'servicepwd'
        admin_tenant: admin
        admin_name: admin
        admin_password: 'adminpwd'
        admin_email: stackmaster@domain.com
        roles:
          - admin
          - Member
          - image_manager
        bind:
          address: 0.0.0.0
          private_address: 127.0.0.1
          private_port: 35357
          public_address: 127.0.0.1
          public_port: 5000
        api_version: 2.0
        region: RegionOne
        database:
          engine: mysql
          host: '127.0.0.1'
          name: 'keystone'
          password: 'LfTno5mYdZmRfoPV'
          user: 'keystone'

Keystone public HTTPS API

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        version: juno
        ...
        services:
        - name: nova
          type: compute
          description: OpenStack Compute Service
          user:
            name: nova
            password: password
          bind:
            public_address: cloud.domain.com
            public_protocol: https
            public_port: 8774
            internal_address: 10.0.0.20
            internal_port: 8774
            admin_address: 10.0.0.20
            admin_port: 8774

Keystone memcached storage for tokens

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        version: juno
        ...
        token_store: cache
        cache:
          engine: memcached
          host: 127.0.0.1
          port: 11211
        services:
        ...

Keystone clustered memcached storage for tokens

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        version: juno
        ...
        token_store: cache
        cache:
          engine: memcached
          members:
          - host: 192.160.0.1
            port: 11211
          - host: 192.160.0.2
            port: 11211
        services:
        ...

Keystone client

.. code-block:: yaml

    keystone:
      client:
        enabled: true
        server:
          host: 10.0.0.2
          public_port: 5000
          private_port: 35357
          service_token: 'token'
          admin_tenant: admin
          admin_name: admin
          admin_password: 'passwd'

Keystone cluster

.. code-block:: yaml

    keystone:
      control:
        enabled: true
        provider:
          os15_token:
            host: 10.0.0.2
            port: 35357
            token: token
          os15_tcp_core_stg:
            host: 10.0.0.5
            port: 5000
            tenant: admin
            name: admin
            password: password

Keystone fernet tokens for OpenStack Kilo release

.. code-block:: yaml

    keystone:
      server:
        ...
        tokens:
          engine: fernet
        ...

Note: Fernet is not a good idea until L. Breaks Horizon, at least in package version:
https://bugs.launchpad.net/django-openstack-auth/+bug/1439499

Read more
=========

* http://docs.openstack.org/developer/keystone/configuration.html
* http://docs.openstack.org/developer/keystone/architecture.html
* http://docs.saltstack.com/ref/states/all/salt.states.keystone.html
* http://docs.saltstack.com/ref/modules/all/salt.modules.keystone.html
* http://www.sebastien-han.fr/blog/2012/12/12/cleanup-keystone-tokens/
* http://www-01.ibm.com/support/knowledgecenter/SS4KMC_2.2.0/com.ibm.sco.doc_2.2/t_memcached_keystone.html?lang=en
* https://bugs.launchpad.net/tripleo/+bug/1203910

Things to improve
=================

* Keystone as service provider (SP) - must be running under Apache (same as with PKI token)
* Keystone with MongoDB backend - where is it?
* IdP is owned by domain, domain corresponds to billable account - IdP administration
* IdP Shiboleth alternatives - mod_auth_mellon

Generally this SP/IdP stuff is a little unstable - how to let SP know identity has changed, no visibility in UI (IBM has some not in upstream yet)
