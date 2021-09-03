#!/usr/bin/env python

"""
source ~/custom/ansible/hacking/env-setup

~/custom/ansible/hacking/test-module -m ./tomcat_resource_link.py -a \
  '{ "name":"dwDatasource", "global_name":"someglobal", "catalina_home":"/Users/dboitnot/Downloads/test_cat" }'
"""

"""
Module for managing Tomcat resource links
"""

import sys
import xml.dom.minidom
from ansible.module_utils.basic import AnsibleModule


XML_WRITE_MODE = 'wb' if sys.version_info[0] < 3 else 'w'


def main():
    """Entry point for module"""

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent']),
            name=dict(required=True),
            global_name=dict(required=True),
            type_class=dict(default='javax.sql.DataSource'),
            catalina_home=dict(type='path'),
            context=dict(type='path')
        ),
        mutually_exclusive=[['catalina_home', 'context']],
        required_one_of=[['catalina_home', 'context']],
        supports_check_mode=True
    )

    state = module.params['state']
    context = module.params['context']
    name = module.params['name']
    global_name = module.params['global_name']
    type_class = module.params['type_class']

    if not context:
        context = module.params['catalina_home'] + '/conf/context.xml'

    # Parse the context file
    dom = xml.dom.minidom.parse(context)
    root = dom.documentElement
    link_res = [node for node in dom.getElementsByTagName("ResourceLink")
                if node.getAttribute("name") == name]

    if state == 'present':
        if len(link_res) > 0:
            link = link_res[0]
        else:
            link = dom.createElement("ResourceLink")
            link.setAttribute("name", name)
            root.appendChild(link)

        need_change = (   link.getAttribute("global") != global_name
                       or link.getAttribute("type")   != type_class)

        if module.check_mode:
            module.exit_json(changed=need_change)
            return

        if need_change:
            link.setAttribute("global", global_name)
            link.setAttribute("type", type_class)
            with open(context, XML_WRITE_MODE) as out:
                root.writexml(out)

        module.exit_json(changed=need_change)
    elif state == 'absent':
        if module.check_mode:
            module.exit_json(changed=len(link_res) > 0)
        else:
            was_changed = False
            for node in link_res:
                node.parentNode.removeChild(node)
                was_changed = True
            if was_changed:
                with open(context, XML_WRITE_MODE) as out:
                    root.writexml(out)
            module.exit_json(changed=was_changed)

if __name__ == '__main__':
    main()
