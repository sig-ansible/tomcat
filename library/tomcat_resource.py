"""
source ~/custom/ansible/hacking/env-setup

~/custom/ansible/hacking/test-module -m ./tomcat_resource.py -a \
  '{ "name":"someresource", "catalina_home":"/Users/dboitnot/Downloads/test_cat", "attrs":{"test":"west", "jest":"fest"} }'

~/custom/ansible/hacking/test-module -m ./tomcat_resource.py -a \
  '{ "name":"someresource", "state":"absent", "catalina_home":"/Users/dboitnot/Downloads/test_cat"}'
"""

"""
Module for managing Tomcat GlobalNamingResources
"""

import os
import sys
import xml.dom.minidom
import tempfile
from ansible.module_utils.basic import AnsibleModule

XML_WRITE_MODE = "wb" if sys.version_info[0] < 3 else "w"


class TomcatResourceRun(object):
    def __init__(self):
        self.changed = False

        self.module = AnsibleModule(
            argument_spec=dict(
                state=dict(default="present", choices=["present", "absent"]),
                name=dict(required=True),
                catalina_home=dict(type="path"),
                xml_path=dict(type="path"),
                attrs=dict(type="dict", default={}),
            ),
            mutually_exclusive=[["catalina_home", "xml_path"]],
            required_one_of=[["catalina_home", "xml_path"]],
            supports_check_mode=True,
        )

    def go(self):
        state = self.module.params["state"]
        xml_path = self.module.params["xml_path"]

        self.name = self.module.params["name"]
        self.attrs = self.module.params["attrs"]

        if not xml_path:
            xml_path = self.module.params["catalina_home"] + "/conf/server.xml"

        # Parser the XML
        self.dom = xml.dom.minidom.parse(xml_path)
        self.root = self.dom.documentElement
        self.gnr_node = self.root.getElementsByTagName("GlobalNamingResources")

        # It's unlikely, but there may not be a GNR node. If not create one.
        if not self.gnr_node:
            self.gnr_node = self.dom.createElement("GlobalNamingResources")
            self.root.appendChild(self.gnr_node)
        else:
            self.gnr_node = self.gnr_node[0]

        self.gnr_res = [
            node
            for node in self.gnr_node.getElementsByTagName("Resource")
            if node.getAttribute("name") == self.name
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
        for node in self.gnr_res:
            node.parentNode.removeChild(node)
            self.changed = True

    def ensure_present(self):
        if len(self.gnr_res) > 0:
            link = self.gnr_res[0]
        else:
            link = self.dom.createElement("Resource")
            self.gnr_node.appendChild(link)
            link.setAttribute("name", self.name)
            self.changed = True

        # We make a copy here and also string-ify booleans
        pending_attrs = {}
        for k in self.attrs.keys():
            v = self.attrs[k]
            if isinstance(v, bool):
                if v:
                    v = "true"
                else:
                    v = "false"
            pending_attrs[k] = str(v)

        attrs_to_remove = []

        for i in range(link.attributes.length):
            attr = link.attributes.item(i)
            if attr.name == "name":
                continue
            if attr.name in pending_attrs.keys():
                if attr.value != pending_attrs[attr.name]:
                    link.setAttribute(attr.name, pending_attrs[attr.name])
                    self.changed = True
                del pending_attrs[attr.name]
            else:
                attrs_to_remove = attrs_to_remove + [attr.name]

        if len(attrs_to_remove) > 0:
            self.changed = True
            for n in attrs_to_remove:
                link.removeAttribute(n)

        for k in pending_attrs.keys():
            self.changed = True
            link.setAttribute(k, pending_attrs[k])


if __name__ == "__main__":
    TomcatResourceRun().go()
