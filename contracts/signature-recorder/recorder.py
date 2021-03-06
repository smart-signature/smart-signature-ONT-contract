from boa.interop.Ontology.Runtime import AddressToBase58, Base58ToAddress
from boa.interop.Ontology.Native import Invoke
# from boa.interop.System.Action import RegisterAction
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from boa.interop.System.Storage import Delete, Get, GetContext, Put
from boa.interop.System.Runtime import CheckWitness, Notify, Serialize, Deserialize
from boa.builtins import concat, ToScriptHash, append, state
# punica compile --contracts signature.py

ctx = GetContext()

# ONT Big endian Script Hash: 0x0100000000000000000000000000000000000000
OntContract = 'AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV'
OntContractAddress = Base58ToAddress(OntContract)
# OntContract = ToScriptHash("AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV")

# ONG Big endian Script Hash: 0x0200000000000000000000000000000000000000
OngContract = 'AFmseVrdL9f9oyCzZefL9tG6UbvhfRZMHJ'
OngContractAddress = Base58ToAddress(OngContract)
# OngContract = ToScriptHash("AFmseVrdL9f9oyCzZefL9tG6UbvhfRZMHJ")

# contract INFO CONSTANTS
selfContractAddress = GetExecutingScriptHash()
DEPLOYER = Base58ToAddress('AbU4AyDhukbj4EFb4fX633th144Rg2sG9A')

################################################################################
# STORAGE KEY CONSTANT
# Belows are storage key for some variable token information.

DEPLOYED_KEY = 'DEPLOYED_RUKA'
OWNER_KEY = 'OWNER____RUKA'

################################################################################
# STORAGE KEY PREFIX
# Since all data are stored in the key-value storage, the data need to be
# classified by key prefix. All key prefixes length must be the same.

SHARE_PREFIX = b'\x01'

################################################################################
def Main(operation, args):
    """
    :param operation:
    :param args:
    :return:
    """
    # 'init' has to be invokded first after deploying the contract to store the necessary and important info into the blockchain
    if operation == 'init':
        return init()
    if operation == 'RecordShare':
        if len(args) == 5 or len(args) == 6:
            owner = args[0]
            signId = args[1]
            symbol = args[2]
            amount = args[3]
            amount2 = args[4]
            sponsor = args[5] if len(args) == 6 else ''
            return RecordShare(owner, signId, symbol, amount, amount2, sponsor)
    if operation == 'transferOntOngtoAccount':
        if len(args) == 3:
            return transferOntOngtoAccount(args[0], args[1], args[2])
    if operation == 'transferOwnership':
        if len(args) == 1:
            return transferOwnership(args[0])
    ####################### Optional methods end ########################
    return False

def init():
    """
    Constructor of this contract. Only deployer hard-coded can call this function
    and cannot call this function after called once.
    Followings are initialization list for SS.
    """
    RequireWitness(DEPLOYER)                           # only can be initialized by deployer
    Require(not Get(ctx, DEPLOYED_KEY))                # only can deploy once
    #if is_deployed:
    #    Notify("Already initialized!")
    #    return False

    # disable to deploy again
    _saveData(DEPLOYED_KEY, 1)

    # the first owner is the deployer
    # can transfer ownership to other by calling `TransferOwner` function
    _saveData(OWNER_KEY, DEPLOYER)
    Notify(["Now owner address: ", DEPLOYER])
    return True

################################################################################

def RecordShare(owner, signId, symbol, amount, amount2, sponsor):
    # owner
    ownerAddress = Base58ToAddress(owner)
    RequireWitness(ownerAddress)

    if symbol == 'ONT':
        contract = OntContract
        tokenContractAddress = OntContractAddress
    if symbol == 'ONG':
        contract = OngContract
        tokenContractAddress = OngContractAddress
    
    param = state(ownerAddress, selfContractAddress, amount)
    res = Invoke(0, tokenContractAddress, 'transfer', [param])
    if res != b'\x01':
        Notify('RecordShare error.\n')
        return False

    share = {
        "contract": contract,
        "symbol": symbol,
        "amount": amount,
        "amount2": amount,
        "sponsor": sponsor,
    }
    shareKey = concat(owner, signId)
    _saveShareRecord(shareKey, share)
    return True

################################################################################

def transferOntOngtoAccount(account, ontAmount, ongAmount):
    """
    Transfers ONT to address.
    :param _account: address to transfer ONT.
    :param ontAmount, ongAmount: quantity of ONT, ONG.
    """
    _onlyOwner()
    Require(_transferOntOngtoAccount(account, ontAmount, ongAmount))
    return True

def transferOwnership(_account):
    """
    Transfers the ownership of this contract to other.
    :param _account: address to transfer ownership.
    """
    _onlyOwner()
    Require(_transferOwnership(_account))
    return True

################################################################################
# INTERNAL FUNCTIONS
# Internal functions checks parameter and storage result validation but these
# wouldn't check the witness validation, so caller function must check the
# witness if necessary.

def _saveData(key, value):
    Put(ctx, key, value)

def _saveShareRecord(shareKey, shareData):
    _shareKey = concat(SHARE_PREFIX, shareKey)
    _saveData(_shareKey, Serialize(shareData))
    Notify([_shareKey, shareData['contract'], shareData['symbol'], shareData['amount'], shareData['sponsor'] ])

def _transferOntOngtoAccount(_account, _ontAmount, _ongAmount):
    param = state(selfContractAddress, Base58ToAddress(_account), _ontAmount)
    res = Invoke(0, OntContractAddress, 'transfer', [param])
    if res != b'\x01':
        Notify('transfer ont error.\n')
        return False
    Notify("transferONT succeed")
    param = state(selfContractAddress, Base58ToAddress(_account), _ongAmount)
    res = Invoke(0, OngContractAddress, 'transfer', [param])
    if res != b'\x01':
        Notify('transfer ong error.\n')
        return False
    Notify("transferONG succeed")
    return True

def _transferOwnership(_account):
    address = Base58ToAddress(_account)
    _saveData(OWNER_KEY, address)
    Notify(["Now owner address: ", address])
    return True

################################################################################
# modifiers

def _onlyOwner():
    """
    Checks the invoker is the contract owner or not. Owner key is saved in the
    storage key `___OWNER`, so check its value and invoker.
    """
    owner = Get(ctx, OWNER_KEY)
    RequireWitness(owner)
    return True

################################################################################
def Require(condition):
	"""
	If condition is not satisfied, return false
	:param condition: required condition
	:return: True or false
	"""
	if not condition:
		Revert()
	return True

def RequireWitness(witness):
	"""
	Checks the transaction sender is equal to the witness. If not
	satisfying, revert the transaction.
	:param witness: required transaction sender
	:return: True if transaction sender or revert the transaction.
	"""
	Require(CheckWitness(witness))
	return True

def Add(a, b):
	"""
	Adds two numbers, throws on overflow.
	"""
	c = a + b
	Require(c >= a)
	return c

def Sub(a, b):
	"""
	Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
	"""
	Require(a>=b)
	return a-b

def Mul(a, b):
	"""
	Multiplies two numbers, throws on overflow.
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
	"""
	if a == 0:
		return 0
	c = a * b
	Require(c / a == b)
	return c

def Div(a, b):
	"""
	Integer division of two numbers, truncating the quotient.
	"""
	Require(b > 0)
	c = a / b
	return c

def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)
