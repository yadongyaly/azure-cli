# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
from azure.cli.command_modules.privatedns._client_factory import (cf_privatedns_mgmt_zones, cf_privatedns_mgmt_record_sets)
from azure.cli.command_modules.privatedns._format import (transform_privatedns_zone_table_output, transform_privatedns_link_table_output, transform_privatedns_record_set_output, transform_privatedns_record_set_table_output)


def load_command_table(self, _):

    network_privatedns_zone_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.privatedns.operations#PrivateZonesOperations.{}',
        client_factory=cf_privatedns_mgmt_zones
    )

    network_privatedns_record_set_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.privatedns.operations#RecordSetsOperations.{}',
        client_factory=cf_privatedns_mgmt_record_sets
    )

    with self.command_group("network private-dns zone", network_privatedns_zone_sdk) as g:
        from .aaz.latest.network.private_dns.zone import List as PrivateDNSZoneList, Show as PrivateDNSZoneShow
        from .custom import PrivateDNSZoneCreate
        self.command_table["network private-dns zone create"] = PrivateDNSZoneCreate(loader=self)
        self.command_table["network private-dns zone list"] = PrivateDNSZoneList(loader=self, table_transformer=transform_privatedns_zone_table_output)
        self.command_table["network private-dns zone show"] = PrivateDNSZoneShow(loader=self, table_transformer=transform_privatedns_zone_table_output)
        g.custom_command("import", "import_zone")
        g.custom_command("export", "export_zone")

    with self.command_group("network private-dns link vnet"):
        from .aaz.latest.network.private_dns.link.vnet import List as PrivateDNSLinkVNetList, Show as PrivateDNSLinkVNetShow
        from .custom import PrivateDNSLinkVNetCreate
        self.command_table["network private-dns link vnet create"] = PrivateDNSLinkVNetCreate(loader=self)
        self.command_table["network private-dns link vnet list"] = PrivateDNSLinkVNetList(loader=self, table_transformer=transform_privatedns_link_table_output)
        self.command_table["network private-dns link vnet show"] = PrivateDNSLinkVNetShow(loader=self, table_transformer=transform_privatedns_link_table_output)

    with self.command_group('network private-dns record-set') as g:
        g.custom_command('list', 'list_privatedns_record_set', client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output, table_transformer=transform_privatedns_record_set_table_output)

    supported_records = ['a', 'aaaa', 'mx', 'ptr', 'srv', 'txt']
    for record in supported_records:
        with self.command_group('network private-dns record-set {}'.format(record), network_privatedns_record_set_sdk) as g:
            g.show_command('show', 'get', transform=transform_privatedns_record_set_output, table_transformer=transform_privatedns_record_set_table_output)
            g.command('delete', 'delete', confirmation=True)
            g.custom_command('list', 'list_privatedns_record_set', client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output, table_transformer=transform_privatedns_record_set_table_output)
            g.custom_command('create', 'create_privatedns_record_set', client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output)
            g.custom_command('add-record', 'add_privatedns_{}_record'.format(record), client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output)
            g.custom_command('remove-record', 'remove_privatedns_{}_record'.format(record), client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output)
            g.generic_update_command('update', setter_name='update', custom_func_name='update_privatedns_record_set', transform=transform_privatedns_record_set_output)

    with self.command_group('network private-dns record-set soa', network_privatedns_record_set_sdk) as g:
        g.show_command('show', 'get', transform=transform_privatedns_record_set_output, table_transformer=transform_privatedns_record_set_table_output)
        g.custom_command('update', 'update_privatedns_soa_record', client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output)

    with self.command_group('network private-dns record-set cname', network_privatedns_record_set_sdk) as g:
        g.show_command('show', 'get', transform=transform_privatedns_record_set_output, table_transformer=transform_privatedns_record_set_table_output)
        g.command('delete', 'delete', confirmation=True)
        g.custom_command('list', 'list_privatedns_record_set', client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output, table_transformer=transform_privatedns_record_set_table_output)
        g.custom_command('create', 'create_privatedns_record_set', client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output)
        g.custom_command('set-record', 'add_privatedns_cname_record', client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output)
        g.custom_command('remove-record', 'remove_privatedns_cname_record', client_factory=cf_privatedns_mgmt_record_sets, transform=transform_privatedns_record_set_output)
        g.generic_update_command('update', setter_name='update', custom_func_name='update_privatedns_record_set', transform=transform_privatedns_record_set_output)
