# -*- coding: utf-8 -*-

"""AppFunction implementation"""

from ldap3 import Server, Connection, SAFE_SYNC, MODIFY_REPLACE
from resilient_circuits import AppFunctionComponent, app_function, FunctionResult
from resilient_lib import IntegrationError, validate_fields

PACKAGE_NAME = "fn_my_ldap"
FN_NAME = "my_ldap_toggle_access"

LDAP_FIELD_DESCRIPTION = "description"
LDAP_STATUS_ENABLED = "ENABLED"
LDAP_STATUS_DISABLED = "DISABLED"


class FunctionComponent(AppFunctionComponent):
    """Component that implements function 'my_ldap_toggle_user_access'"""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function(FN_NAME)
    def _app_function(self, fn_inputs):
        """
        Function: None
        Inputs:
            -   fn_inputs.my_ldap_disable
            -   fn_inputs.my_ldap_enable
            -   fn_inputs.my_ldap_user_dn
        """        
        
        yield self.status_message("Starting App Function: '{0}'".format(FN_NAME))

        # validate app.configs
        validate_fields(["server", "port", "admin_user", "admin_password", "search_base"], self.app_configs)

        validate_fields(["my_ldap_user_dn"], fn_inputs)

        enable = getattr(fn_inputs, "my_ldap_enable", None)
        disable = getattr(fn_inputs, "my_ldap_disable", None)

        # Check that neither both are set nor neither are set.
        if enable and disable:
            raise IntegrationError("Cannot set both enable and disable to True. Pick one.")
        elif not enable and not disable:
            raise IntegrationError("Must set one of enable and disable to True.")

        if disable:
            change = LDAP_STATUS_DISABLED
        else:
            change = LDAP_STATUS_ENABLED

        # once fields from app.config and fn_inputs have been validated,
        # set them to local variables for easier use
        server_address = self.app_configs.server
        server_port = int(self.app_configs.port)
        admin_user = self.app_configs.admin_user
        admin_secret = self.app_configs.admin_password

        # Instantiate `Server` object and establish connection
        server = Server(server_address, port=server_port)
        connection = Connection(server, admin_user, admin_secret, client_strategy=SAFE_SYNC, auto_bind=True)

        # make the modification
        connection.modify(fn_inputs.my_ldap_user_dn, {LDAP_FIELD_DESCRIPTION: [(MODIFY_REPLACE, [change])]})

        results = {
            # return the status as "DISABLED" or "ENABLED"
            "status": change if change == LDAP_STATUS_DISABLED else LDAP_STATUS_ENABLED
        }

        yield self.status_message("Finished running App Function: '{0}'".format(FN_NAME))

        yield FunctionResult(results)