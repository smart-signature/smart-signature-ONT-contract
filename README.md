# smart-signature-ONT-contract
###### by punica

test script hash : a75451b23609e04e6606b4a08bc0304bf727ccb5

TestNet ONT&ONG Application => https://developer.ont.io/applyOng

參考範例 https://github.com/ONT-Avocados/python-template



## Introduction

[punica-python](https://github.com/punicasuite/punica-python).

## Getting started

### Setting up the development environment

There are a few technical requirements before we start. Please install the following:

- [Python 3.7](https://www.python.org/downloads/release/python-370/)
- [Git](https://git-scm.com/)

### Introduction

In order to call the method in the contract, we need to fill in the default-config.json file.
The following describes the meaning of each parameter in default-config.json in detail.

```json
{
    "defaultWallet": "wallet.json",
    "password": {
        "AUr5QUfeBADq6BMY6Tp5yuMsUNGpsD7nLZ": "password",
        "AecaeSEBkt5GcBCxwz1F41TvdjX3dnKBkJ": "password",
        "AQvZMDecMoCi2y4V6QKdJBtHW1eV7Vbaof": "password"
    },
    "deployConfig": {
        "name": "contract name ",
        "version": "contract version",
        "author": "the author of contract",
        "email": "email address",
        "desc": "a description for your contract",
        "needStorage": true,
        "payer": "AUr5QUfeBADq6BMY6Tp5yuMsUNGpsD7nLZ",
        "gasPrice": 0,
        "gasLimit": 31000000
    },
    "invokeConfig": {
        "abi": "hello_ontology_abi.json",
        "sleepTime":0,
        "defaultPayer": "AUr5QUfeBADq6BMY6Tp5yuMsUNGpsD7nLZ",
        "gasPrice": 0,
        "gasLimit": 20000,
        "functions": [            
        ]
    }
}
```

`defaultWallet`: Wallet file name under the wallet folder.

`password`: Used to configure the password corresponding to the address in the wallet corpus.

`deployConfig`: Basic contract information, used when contract deployment.

`invokeConfig`: Parameters needed to configure for invoking function in contract.

- `abi` Used to configure the abi file directory, the default is `contracts/build/`.
- `sleepTime` Used to specify the time required to perform a non-pre-execution method.
- `defaultPayer` Used to specify the payer for transaction fee.
- `gasPrice` Used to set the value of gasPrice.
- `gasLimit` Used to set the value of gasLimit.
- `functions` Parameters needed to configure functions in the contract.

Function detailed configuration:

```json
{
    "operation": "testByteArrayListAndStr",
    "args": [
        {
            "name": "bytearrayList",
            "value": [
                "ByteArray:Hello",
                "ByteArray:world"
            ]
        },
        {
            "name": "msgStr",
            "value": "String:hello"
        },
        {
            "name": "msgInt",
            "value": 10
        },
        {
            "name": "msgBool",
            "value": true
        }
    ],
    "signature": {
        "m":1,
        "signers":[
            "AUr5QUfeBADq6BMY6Tp5yuMsUNGpsD7nLZ"
        ]
    },
    "preExec": true
}
```

- `operation` Used to set function name.
- `args` Used to set parameter required by function.
  - `name`: parameter name.
  - `value`: parameter value. In this example, the first parameter value is array and it should be configurated like this example.Elements in the array support basic data types, if the data type of element is int or boolean, you don't need to declare the parameter type, if the data type of element is `String` or `byte[]`, you need to explicitly declare the data type and the declaration format is "data type: data value".
- `signature` Used to set signer.
   - `m` indicates the minimum number of signatures required in the multi-signature. `m=1` indicate Single sign, `m > 2` indicates multi-signature.
   - `signers` indicates all the addresses of signers.
- `preExec` Used to set the execution mode of the function, `true` indicates this transaction will not update state of blockchain, `false` indicates this transaction will update state of blockchain and this operation need pay transaction fee.
