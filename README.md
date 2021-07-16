SIG's Parameterized Tomcat Role
===============================

Install and configure Apache Tomcat.

Requirements
------------

* `tomcat_java_home` must be set to an appropriate JAVA_HOME path.

Role Variables
--------------

* `tomcat_java_home` (string) - *Required* - Path to the JAVA_HOME Tomcat will use.

* `tomcat_version` (string) - *Recommended* - Tomcat version to install.
  * **Default:** `8.5.68`
  * **Allowed Values:** `8.5.4`, `8.5.40`, `8.5.66`, `8.5.68`, `9.0.43`
  * **Note:** It is recommended that you supply a `tomcat_version` rather than
    using the default as the default is subject to change without notice.
    
* `tomcat_add_jars` (list of strings) - A list of paths to JAR files to be added
  to the Tomcat `lib` directory.
  * **Note:** These files must be pre-staged on the server. To have the role
    download the JARs, use `tomcat_download_jars` instead.
    
* `tomcat_ajp_enabled` (boolean) - When `false` the AJP connector will be
  removed from `conf/server.xml`.
  * **Default:** `false`
  * **Known Issue:** If the role is applied with `tomcat_ajp_enabled` set to
    `false`, a subsequent run with it set to `true` will *not* restore the AJP
    connector. It will have to be added back by hand.
    
* `tomcat_ajp_port` (integer) - Tomcat AJP port.
  * **Default:** `{{ 8009 + tomcat_port_offset }}`
    
* `tomcat_base` (string) - Base directory for the Tomcat installation. 
  * **Note:** By default, Tomcat will be installed at 
  `{{ tomcat_base }}/{{ tomcat_service_name}}-{{ tomcat_version }}` 
  with as symlink at `{{ tomcat_base }}/{{ tomcat_service_name }}`
    
* `tomcat_censor_ansible_output` (boolean) - When `true` certain output will be
  elided from the log to avoid exposing secrets. You can set this to `false` to
  troubleshoot failures in those steps.
  * **Default:** `true`
  
* `tomcat_context_cookie_processor_same_site_cookies` - Sets the value for the
  `sameSiteCookies` attribute of the `CookieProcessor` in `conf/context.xml`.
  
* `tomcat_download_jars` (list of [JAR Download
  Objects](#jar-download-objects)) - JARS to be downloaded to Tomcat's `lib`
  directory.

* `tomcat_group` (string) - Primary group for `tomcat_user`
  * **Default:** `tomcat`
  
* `tomcat_http_port` (integer) - HTTP listener port
  * **Default:** `{{ 8080 + tomcat_port_offset }}`
  
* `tomcat_https_port` (integer) - SSL listener port
  * **Default:** `{{ 8443 + tomcat_port_offset }}`
  
* `tomcat_log_retain_days` (integer) - Number of days to retain Tomcat logs.
  * **Default:** `30`

* `tomcat_manage_context_xml` (boolean) - Set to `false` to prevent the role
  making changes to `conf/context.xml`.
  * **Default:** `true`
  
* `tomcat_manage_logging` (boolean) - Set to `false` to prevent the role making
  changes to `conf/logging.properties`
  * **Default:** `true`
  
* `tomcat_manage_server_xml` (boolean) - Set to `false` to prevent the role
  making changes to `conf/server.xml`.
  * **Default:** `true`
  
* `tomcat_manage_tomcat_users_xml` (boolean) - Set to `false` to prevent the
  role making changes to `conf/users.xml`.
  * **Default:** `true`
  
* `tomcat_max_http_header_size` (integer) - When specified, sets the
  `maxHttpHeaderSize` attribute of the HTTP and HTTPS connectors.
  
* `tomcat_memory_args` (string) - Memory arguments passed to the JVM. These will
  often need to be adjusted to suit the deployed webapps.
  * **Default:** `-Xms512M -Xmx1024M`
  
* `tomcat_port_offset` (integer) - This value is added to all default port numbers.
  * **Default:** `0`
  * **Example:** If you are installing two Tomcat instances, "A" and "B" then
    you can set `tomcat_port_offset` for instance B to `1000` so that instance A
    will listen on port 8080 and instance B on 9080.
    
* `tomcat_remove_delivered_apps` (boolean) - The Tomcat installation package
  comes with several applications which are usually not desired in a production
  environment. When this value is `true` these apps will be removed after
  installation.
  * **Default:** `true`
  
* `tomcat_resource_links` (list of [JNDI Resource Link
  Objects](#jndi-resource-link-objects)) - JNDI resource links to add to
  `conf/context.xml`.
  
* `tomcat_resources` (list of [JNDI Resource Objects](#jndi-resource-objects)) -
  JNDI resources to add to `conf/server.xml`.

* `tomcat_self_signed` (boolean) - When `true` the role will create a
  self-signed certificate and enable the SSL listener.
  * **Default:** `false`

* `tomcat_service_name` (string) - The name of the system service created to
  start & stop Tomcat. You can install multiple versions of Tomcat by specifying
  different values for `tomcat_service_name`.
  * **Default:** `tomcat`
  
* `tomcat_shutdown_port` (integer) - Tomcat shutdown port.
  * **Default:** `{{ 8005 + tomcat_port_offset }}`
  
* `tomcat_ssl_fqdn` (string) - The FQDN used for the self-signed certificate.
  * **Default:** `{{ ansible_fqdn }}`
  
* `tomcat_ssl_org_name` (string) - The organization name used in the self-signed CSR.
  * **Default:** `{{ ansible_domain }}`
  
* `tomcat_ssl_max_threads` (integer) - Number of threads for the SSL listener.
  * **Default:** `150`
  
* `tomcat_timezone` (string) - Time zone setting for the JVM. This value is
  passed with `-Duser.timezone=` at start time.
  * **Default:** If `current_timezone` is set the role will use its value.
    Otherwise it will attempt to detect the time zone.
  * **Note:** A time zone is required because certain JDBC drivers will throw
    errors if none is set in the JVM.
  
* `tomcat_urandom` (boolean) - If `true`, the JVM will be set to use
  `/dev/urandom` instead of `/dev/random`. This is often critical to performance
  on virtual machines.
  * **Default:** `true`
  
* `tomcat_user` (string) - Name of the O/S user Tomcat runs under.
  * **Default:** `tomcat`
  
* `tomcat_user_shell` (string) - Default shell for `tomcat_user`
  * **Default:** `/sbin/nologin`
  
* `tomcat_users` (list of [Tomcat User Objects](#tomcat-user-objects)) - Users
  to add to `conf/tomcat-users.xml`.
  
* `tomcat_x_forwarded_enable` (boolean) - Enable support for X-Forwarded-For headers.
  * **Default:** `true`
  
### JAR Download Objects

* `checksum` (string) - *Required* - Checksum of the downloaded file. This value
  is required for security.
  * **Note:** It is recommended to use the SHA1 hash for compatibility.
  * **Example:** `checksum: "sha1:1ec446f2bfab6f87f4e4ab1c738469c982bc5961"`
* `url` (string) - *Required* - URL to download
* `filename` (string) - Name of the file to be stored in `lib`
  * **Default:** The filename in the URL
  
### JNDI Resource Link Objects

* `global_name` (string) - *Required* - Global JNDI name for the resource link.
* `name` (string) - *Required* - Name of the resource

**Example:**
``` yaml
      tomcat_resource_links:
        - name: jdbc/bannerDataSource
        - global_name: jdbc/bannerDataSource
```

### JNDI Resource Objects

* `name` (string) - *Required* - Name of the resource. 
* `attrs` (string:string dict) - Attributes for the resource.

**Example:**
``` yaml
      tomcat_resources:
        - name: jdbc/bannerDataSource
          attrs:
            auth: Container
            type: javax.sql.DataSource
            url: "{{ banner_jdbc_url }}"
            username: banproxy
            password: "{{ banproxy_pw }}"
            driverClassName: oracle.jdbc.OracleDriver
            initialSize: 25
            maxIdle: 10
            maxTotal: 400
            maxWaitMillis: 30000
            minIdle: 10
            timeBetweenEvictionRunsMillis: 1800000
            testOnBorrow: true
            testWhileIdle: true
            accessToUnderlyingConnectionAllowed: true
            validationQuery: select * from dual
```

### Tomcat User Objects

* `name` (string) - *Required* - User's login name
* `password` (string) - User's password
* `roles` (string) - Comma-separated list of user's roles
* `append` (boolean) - When `true` the specified `roles` will be appended to the
  user's existing role list rather than replacing it.
  * **Default:** `false`

Dependencies
------------

This role has no required dependencies. It will, however, create "about" info if
the [sig-ansible.about](https://galaxy.ansible.com/sig-ansible/about) role is
enabled.


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
