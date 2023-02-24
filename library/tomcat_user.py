"""
source ~/custom/ansible/hacking/env-setup

~/custom/ansible/hacking/test-module -m ./tomcat_user.py -a \
  '{ "name":"someguy", "catalina_home":"/Users/dboitnot/Downloads/test_cat", "password":"testpass", "roles":"AROLE" }'

~/custom/ansible/hacking/test-module -m ./tomcat_user.py -a \
  '{ "name":"someguy", "catalina_home":"/Users/dboitnot/Downloads/test_cat", "state":"absent"}'
"""

import os
import sys
import xml.dom.minidom
import tempfile
from ansible.module_utils.basic import AnsibleModule

XML_WRITE_MODE = "wb" if sys.version_info[0] < 3 else "w"


def role_list(comma_list):
    return sorted([s.strip() for s in set(comma_list.split(",")) if len(s.strip()) > 0])


def obfuscate(x):
    return "".join(["&#%d;" % ord(c) for c in x])


class TomcatUserRun(object):
    def __init__(self):
        self.changed = False

        self.module = AnsibleModule(
            argument_spec=dict(
                state=dict(default="present", choices=["present", "absent"]),
                name=dict(required=True),
                catalina_home=dict(type="path"),
                xml_path=dict(type="path"),
                roles=dict(),
                password=dict(no_log=True),
                append=dict(type="bool", default=False),
                update_password=dict(default="always", choices=["always", "on_create"]),
                obfuscate_password=dict(type="bool", default=True),
            ),
            mutually_exclusive=[["catalina_home", "xml_path"]],
            required_one_of=[["catalina_home", "xml_path"]],
            supports_check_mode=True,
        )

    def go(self):
        state = self.module.params["state"]
        xml_path = self.module.params["xml_path"]

        self.name = self.module.params["name"]
        self.roles = self.module.params["roles"]
        self.password = self.module.params["password"]
        self.append = self.module.params["append"]
        self.update_password = self.module.params["update_password"]

        # At the moment this gets messed up by the exporter
        # if self.password and self.module.params['obfuscate_password']:
        #     self.password = obfuscate(self.password);

        if not xml_path:
            xml_path = self.module.params["catalina_home"] + "/conf/tomcat-users.xml"

        # Parse the XML
        self.dom = xml.dom.minidom.parse(xml_path)
        self.root = self.dom.documentElement

        # Find the user entry
        self.user_res = [
            node
            for node in self.root.getElementsByTagName("user")
            if node.getAttribute("username") == self.name
        ]

        if state == "present":
            self.ensure_present()
        elif state == "absent":
            self.ensure_absent()
        else:
            self.module.fail_json(msg="Invalid state: " + state)

        # Save the XML only if it's been changed
        if self.changed and not self.module.check_mode:
            tmpfd, tmpfile = tempfile.mkstemp()
            with os.fdopen(tmpfd, XML_WRITE_MODE) as out:
                self.root.writexml(out)
            self.module.atomic_move(tmpfile, xml_path)

        self.module.exit_json(changed=self.changed)

    def ensure_absent(self):
        for node in self.user_res:
            node.parentNode.removeChild(node)
            self.changed = True

    def ensure_present(self):
        if len(self.user_res) > 0:
            self.user_node = self.user_res[0]
        else:
            self.user_node = self.dom.createElement("user")
            self.root.appendChild(self.user_node)
            self.user_node.setAttribute("username", self.name)
            if self.password:
                self.user_node.setAttribute("password", self.password)
            self.changed = True

        self.ensure_roles()
        self.ensure_password()

    def ensure_roles(self):
        has_roles = role_list(self.user_node.getAttribute("roles"))
        expect_roles = role_list(self.roles)

        if self.append:
            expect_roles = sorted(list(set(has_roles + expect_roles)))

        if expect_roles != has_roles:
            self.changed = True
            self.user_node.setAttribute("roles", ",".join(expect_roles))

    def ensure_password(self):
        if self.password and self.update_password:
            has_pass = self.user_node.getAttribute("password")
            if has_pass != self.password:
                self.changed = True
                self.user_node.setAttribute("password", self.password)


if __name__ == "__main__":
    TomcatUserRun().go()
