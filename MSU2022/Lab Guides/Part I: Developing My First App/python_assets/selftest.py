# -*- coding: utf-8 -*-

"""
Function implementation test.
Usage: 
    resilient-circuits selftest -l fn-my-ldap
    resilient-circuits selftest --print-env -l fn-my-ldap

Return examples:
    return {
        "state": "success",
        "reason": "Successful connection to third party endpoint"
    }

    return {
        "state": "failure",
        "reason": "Failed to connect to third party endpoint"
    }
"""

import logging

from ldap3 import Server, Connection, SAFE_SYNC
from resilient_lib import validate_fields

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def selftest_function(opts):
    """
    Placeholder for selftest function. An example use would be to test package api connectivity.
    Suggested return values are be unimplemented, success, or failure.
    """
    app_configs = opts.get("fn_my_ldap", {})

    try:
        validate_fields(["server", "port", "admin_user", "admin_password", "search_base"], app_configs)

        server = Server(app_configs.get("server"), port=int(app_configs.get("port")))
        connection = Connection(server, app_configs.get("admin_user"), app_configs.get("admin_password"), client_strategy=SAFE_SYNC, auto_bind=True)

        return {
            "state": "success",
            "reason": None
        }
    except Exception as e:
        return {
            "state": "failure",
            "reason": str(e)
        }