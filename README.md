SIG's Parameterized Tomcat Role
===============================

Install and configure Apache Tomcat.

  * [Requirements](#requirements)
  * [Role Variables](#role-variables)
    + [JAR Download Objects](#jar-download-objects)
    + [JNDI Resource Link Objects](#jndi-resource-link-objects)
    + [JNDI Resource Objects](#jndi-resource-objects)
    + [Tomcat User Objects](#tomcat-user-objects)
  * [Dependencies](#dependencies)
  * [Example Playbook](#example-playbook)
  * [License](#license)
  * [Author Information](#author-information)

Requirements
------------

* `tomcat_java_home` must be set to an appropriate JAVA_HOME path.

Role Variables
--------------

* `stage_dir` (string) - *Required* - Path to a staging directory used during
  the installation process.
  * **Note:** While no default is provided, `/tmp` is usually sufficient.

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
  
* `tomcat_catalina_extra_opts` (string) - Extra JVM arguments to include at
  start time.
    
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

``` yaml
  - role: sig-ansible.tomcat
    vars:
      stage_dir: /tmp
      tomcat_self_signed: yes
      tomcat_base: /u01/app
      tomcat_memory_args: "-Xms2048m -Xmx6g -XX:MaxPermSize=2048m -Doracle.jdbc.autoCommitSpecCompliant=false"
      tomcat_catalina_extra_opts: "-Dbanner.logging.dir=/u01/app/logs"
      tomcat_download_jars:
        - url: https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc8/19.3.0.0/ojdbc8-19.3.0.0.jar
          checksum: 'sha256:a66d27a14f3adee484427cc4de008af85a5c3e78e2e3285a4dba1277332978a5'
          filename: ojdbc8.jar
        - url: https://repo1.maven.org/maven2/com/oracle/database/xml/xdb/19.3.0.0/xdb-19.3.0.0.jar
          checksum: 'sha256:a3f0545da9651359f05e6538886679f546632f63d409bb7247a0e2c8ae07d078'
          filename: xdb.jar
        - url: https://repo1.maven.org/maven2/com/oracle/database/jdbc/ucp/19.3.0.0/ucp-19.3.0.0.jar
          checksum: 'sha256:23d8debe40a764df74d5eda7e8c1ce9b2c190a34f739ca4d751eaa94114d31cc'

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
            validationQueryTimeout: 300

        - name: jdbc/bannerSsbDataSource
          attrs:
            auth: Container
            type: javax.sql.DataSource
            url: "{{ banner_jdbc_url }}"
            username: ban_ss_user
            password: "{{ ban_ss_user_pw }}"
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
            validationQueryTimeout: 300

      tomcat_resource_links:
        - name: jdbc/bannerDataSource
          global_name: jdbc/bannerDataSource
        - name: jdbc/bannerSsbDataSource
          global_name: jdbc/bannerSsbDataSource
```

License
-------

Copyright 2021 Strata Information Group

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Author Information
------------------

* Dan Boitnott <boitnott@sigcorp.com>
* Ian Becker <becker@sigcorp.com>
* Dan Arnold <arnold@sigcorp.com>
* Ron Kwong <kwong@sigcorp.com>

