# -*- coding: utf-8 -*-

"""AppFunction implementation"""

from ldap3 import SAFE_SYNC, Connection, Server
from resilient_circuits import AppFunctionComponent, app_function, FunctionResult
from resilient_lib import IntegrationError, validate_fields

PACKAGE_NAME = "fn_my_ldap"
FN_NAME = "my_ldap_search"


class FunctionComponent(AppFunctionComponent):
    """Component that implements function 'my_ldap_search'"""

    def __init__(self, opts):
        super(FunctionComponent, self).__init__(opts, PACKAGE_NAME)

    @app_function(FN_NAME)
    def _app_function(self, fn_inputs):
        """
        Function: None
        Inputs:
            -   fn_inputs.my_ldap_search_filter
        """

        yield self.status_message("Starting App Function: '{0}'".format(FN_NAME))

        # validate app.configs
        validate_fields(["server", "port", "admin_user", "admin_password", "search_base"], self.app_configs)

        # validate inputs
        validate_fields(["my_ldap_search_filter"], fn_inputs)

        # once fields from app.config and fn_inputs have been validated,
        # set them to local variables for easier use
        server_address = self.app_configs.server
        server_port = int(self.app_configs.port)
        admin_user = self.app_configs.admin_user
        admin_secret = self.app_configs.admin_password

        search_filter = fn_inputs.my_ldap_search_filter
        search_base = self.app_configs.search_base

        # Instantiate `Server` object and establish connection
        server = Server(server_address, port=server_port)
        connection = Connection(server, admin_user, admin_secret, client_strategy=SAFE_SYNC, auto_bind=True)

        # Call out to search LDAP (can ignore second and fourth return values)
        status, _, response, _ = connection.search(search_base, search_filter)


        # For demo purposes, we'll only return the list of distinguished names that were found.
        # For a more robust solution, one could take other values returned from the search functions.
        # NOTE: any byte values (i.e. "raw_dn" should be filtered out)
        response = [r.get("dn") for r in response]
        results = {"result_list": response}

        yield self.status_message("Finished running App Function: '{0}'".format(FN_NAME))

        yield FunctionResult(results, success=status)