keystone:
  server:
    enabled: true
    version: liberty
    service_token: token
    service_tenant: service
    admin_tenant: admin
    admin_name: admin
    admin_password: passw0rd
    admin_email: root@localhost
    bind:
      address: 0.0.0.0
      private_address: 127.0.0.1
      private_port: 35357
      public_address: 127.0.0.1
      public_port: 5000
    region: RegionOne
    database:
      engine: mysql
      host: localhost
      name: keystone
      password: passw0rd
      user: keystone
    tokens:
      engine: fernet
      expiration: 86400
      location: /etc/keystone/fernet-keys/
      max_active_keys: 4
    notification: false
    notification_format: cadf
# CI related dependencies
mysql:
  client:
    enabled: false
    version: '5.7'
    admin:
      host: localhost
      port: 3306
      user: admin
      password: password
      encoding: utf8
  server:
    enabled: true
    version: "5.7"
    force_encoding: utf8
    bind:
      address: 0.0.0.0
      port: 3306
      protocol: tcp
    database:
      keystone:
        encoding: utf8
        users:
        - host: '%'
          name: keystone
          password: passw0rd
          rights: all
        - host: 127.0.0.1
          name: keystone
          password: passw0rd
          rights: all
