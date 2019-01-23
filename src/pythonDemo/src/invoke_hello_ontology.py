#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii

from ontology.ont_sdk import OntologySdk
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction
from ontology.utils.contract_data_parser import ContractDataParser
from ontology.utils.utils import deserialize_hex


class InvokeHelloPython(object):
    def __init__(self, sdk: OntologySdk, hex_contract_address: str):
        if not isinstance(sdk, OntologySdk):
            raise RuntimeError('the type of sdk is error')
        if not isinstance(hex_contract_address, str):
            raise RuntimeError('the type of contract address should be str')
        if len(hex_contract_address) != 40:
            raise RuntimeError()
        self.__sdk = sdk
        self.__hex_contract_address = hex_contract_address

    def name(self):
        func = InvokeFunction('name')
        res = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, None, 0, 0, func, True)
        res = ContractDataParser.to_utf8_str(res)
        return res

    def hello(self, msg: str) -> str:
        if not isinstance(msg, str):
            raise RuntimeError('the type of msg should be str')
        func = InvokeFunction('hello')
        func.set_params_value(msg)
        res = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, None, 0, 0, func, True)
        res = ContractDataParser.to_utf8_str(res)
        return res

    def test_hello(self, bool_msg, int_msg, bytes_msg, str_msg, bytes_address_msg: bytes, payer_acct: Account,
                   gas_limit: int, gas_price: int) -> str:
        notify_args = InvokeFunction('testHello')
        notify_args.set_params_value(bool_msg, int_msg, bytes_msg, str_msg, bytes_address_msg)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, payer_acct, gas_limit,
                                                       gas_price, notify_args, False)
        return tx_hash

    def test_list(self, list_msg: list, payer_acct, gas_limit, gas_price):
        func = InvokeFunction('testList')
        func.set_params_value(list_msg)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, payer_acct, gas_limit,
                                                       gas_price, func, False)
        return tx_hash

    def test_dict_pre_exec(self, dict_msg: dict):
        func = InvokeFunction('testMap')
        func.set_params_value(dict_msg)
        value = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, None, 0, 0, func, True)
        return value

    def test_dict(self, dict_msg: dict, pay_acct: Account, gas_limit, gas_price):
        func = InvokeFunction('testMap')
        func.set_params_value(dict_msg)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, pay_acct, gas_limit,
                                                       gas_price, func, False)
        return tx_hash

    def test_struct_list_and_str_pre_exec(self, struct_list, str_msg):
        func = InvokeFunction('testStructListAndStr')
        func.set_params_value(struct_list, str_msg)
        value = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, None, 0, 0, func, True)
        return value

    def test_struct_list_and_str(self, struct_list, str_msg, payer_acct: Account, gas_limit, gas_price):
        func = InvokeFunction('testStructListAndStr')
        func.set_params_value(struct_list, str_msg)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, payer_acct, gas_limit,
                                                     gas_price, func, False)
        return tx_hash

    def test_get_dict(self, key):
        func = InvokeFunction('testGetMap')
        func.set_params_value(key)
        value = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, None, 0, 0, func, True)
        return value

    def test_dict_in_ctx(self, map_msg, payer_acct, gas_limit, gas_price):
        func = InvokeFunction('testMapInMap')
        func.set_params_value(map_msg)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, payer_acct, gas_limit,
                                                       gas_price, func, False)
        return tx_hash

    def test_get_dict_in_ctx(self, key):
        func = InvokeFunction('testGetMapInMap')
        func.set_params_value(key)
        value = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, None, None, 0, 0, func, True)
        return value

    def test_transfer_multi(self, transfer_list, payer_acct, gas_limit, gas_price):
        func = InvokeFunction('transferMulti')
        func.set_params_value(transfer_list)
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__hex_contract_address, payer_acct, payer_acct, gas_limit,
                                                       gas_price, func, False)
        return tx_hash
