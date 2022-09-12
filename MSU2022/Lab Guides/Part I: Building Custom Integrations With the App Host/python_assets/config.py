# -*- coding: utf-8 -*-

"""Generate a default configuration-file section for fn_my_ldap"""


def config_section_data():
    """
    Produce add the default configuration section to app.config,
    for fn_my_ldap when called by `resilient-circuits config [-c|-u]`
    """

    config_data = u"""[fn_my_ldap]
server=<ldap_server_here>
port=<ldap_port_here>
admin_user=<admin_user_dn>
admin_password=<admin_user_secret>
search_base=ou=people,dc=planetexpress,dc=com
"""

    return config_data