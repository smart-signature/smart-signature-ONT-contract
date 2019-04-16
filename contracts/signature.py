from boa.interop.Ontology.Runtime import AddressToBase58, Base58ToAddress
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import Notify, CheckWitness
from boa.interop.System.Action import RegisterAction
from boa.builtins import concat, ToScriptHash
from .libs.SafeCheck import *
from .libs.SafeMath import *
from .libs.Utils import *

PublishEvent = RegisterAction("publish", "sign")
# ApprovalEvent = RegisterAction("approval", "owner", "spender", "amount")


################################################################################
# TOKEN INFO CONSTANTS
NAME = 'SmartSignature'

DEPLOYER = ToScriptHash('AZgDDvShZpuW3Ved3Ku7dY5TkWJvfdSyih')
OWNER = ToScriptHash("ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6")
PUBLISHER = ToScriptHash("ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6")

################################################################################
# STORAGE KEY CONSTANT
# Belows are storage key for some variable token information.

DEPLOYED_KEY = 'DEPLOYED_SPKZ03'
OWNER_KEY = '___OWNER_SPKZ03'


################################################################################
# STORAGE KEY PREFIX
# Since all data are stored in the key-value storage, the data need to be
# classified by key prefix. All key prefixes length must be the same.

OWN_PREFIX = '_____own_spkz03'
ALLOWANCE_PREFIX = '___allow_spkz03'

PLAYERS_PREFIX = b'\x01'
SHARES_PREFIX = b'\x02'
SIGNS_PREFIX = b'\x01'

################################################################################
# 转账合约
OntContract = Base58ToAddress("AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV")
# 本合约地址
selfContractAddress = GetExecutingScriptHash()
# 开发者账户
developerAcc = 'ARfyRJQJVdUG1NX18rvp6LncWgaXTQUNBq'
# 30天的秒
cycle = 3456000
################################################################################
class player:
    def __init__(self, id):
        self.id = id
        self.signIncome = 0
        self.shareIncome = 0
        self.shares = []

class share:
    def __init__(self, signId, quota):
        self.signId = signId
        self.quota = quota

class sign:
    def __init__(self, id, author, fission_factor, ipfs_hash, public_key, signature):
        self.id = id
        self.author = author
        self.fission_factor = fission_factor
        self.ipfs_hash = ipfs_hash
        self.public_key = public_key
        self.signature = signature


def Main(operation, args):
    """
    :param operation:
    :param args:
    :return:
    """
    # 'init' has to be invokded first after deploying the contract to store the necessary and important info into the blockchain
    if operation == 'init':
        return init()
    if operation == 'publish':
        if len(args) != 7:
            return False
        else:
            acct = args[0]
            id = args[1]
            author = args[2]
            fission_factor = args[3]
            ipfs_hash = args[4]
            public_key = args[5]
            signature = args[6]
            s = sign(id, author, fission_factor, ipfs_hash, public_key, signature)
            return publish(acct, s);



def init():
    """
    Constructor of this contract. Only deployer hard-coded can call this function
    and cannot call this function after called once.
    Followings are initialization list for SS.
    """

    is_witness = CheckWitness(DEPLOYER)
    is_deployed = Get(ctx, DEPLOYED_KEY)
    Require(is_witness)                     # only can be initialized by deployer
    Require(not is_deployed)                # only can deploy once
    #if is_deployed:
    #    Notify("Already initialized!")
    #    return False

    # disable to deploy again
    saveData(DEPLOYED_KEY, 1)

    # the first owner is the deployer
    # can transfer ownership to other by calling `TransferOwner` function
    saveData(OWNER_KEY, DEPLOYER)

    signs = []  # 沒錯就是空的
    shares = [] # 沒錯這也是空的
    saveData(SIGNS_PREFIX, Serialize(signs))
    saveData(SHARES_PREFIX, Serialize(shares))   
    # supply the coin. All coin will be belong to deployer.
    #saveData(SPKZ_SUPPLY_KEY, total)
    #deployer_key = concat(OWN_PREFIX, DEPLOYER)
    #saveData(deployer_key, total)
    #Notify(['transfer', '', DEPLOYER, total])
    return True

def publish(acct, sign):
    if len(acct) != 20 or len(sign.author) != 20:
        raise Exception("address length error")
    
    is_witness = CheckWitness(acct)
    Require(is_witness)
    Require(acct == PUBLISH_ACCT)

    signKey = concat(SIGN_PREFIX,sign.id)
    sSign = Serialize(sign)
    saveData(signKey, sSign)
    
    PublishEvent(sign)
    return True

def createShare(owner, in, signId):
    if len(owner) != 20 :
        raise Exception("owner address length error")
    
    is_witness = CheckWitness(owner)
    Require(is_witness)

    sSigns = Get(GetContext(), SIGNS_PREFIX)
    sShares = Get(GetContext(), SHARES_PREFIX)
    signs = Deserialize(sSigns)
    shares = Deserialize(sShares)
    for item in signs:
        if item.id == signId:
            # 拿到目标购买国家进行交易
            #param = state(Base58ToAddress(fromAcc), Base58ToAddress(item[2]), item[1] - 1)
            #res = Invoke(0, OntContract, "transfer", [param])
            #if res != b'\x01':
            #    Notify("buy error.")
            #    return False
            # 每一次给合约内部转1个币
            #paramContract = state(Base58ToAddress(fromAcc), selfContractAddress, 1)
            #resContract = Invoke(0, OntContract, 'transfer', [paramContract])
    share
    shares.append(share)
    saveData(SHARES_PREFIX, Serialize(shares))
    Notify("create a share success.")
    return True

################################################################################
def saveData(key, value):
    ctx = GetContext()
    Put(ctx, key, value)

def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)

def Require(condition):
	"""
	If condition is not satisfied, return false
	:param condition: required condition
	:return: True or false
	"""
	if not condition:
		Revert()
	return True

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

def Pow(a, b):
    """
    a to the power of b
    :param a the base
    :param b the power value
    :return a^b
    """
    c = 0
    if a == 0:
        c = 0
    elif b == 0:
        c = 1
    else:
        i = 0
        c = 1
        while i < b:
            c = Mul(c, a)
            i = i + 1
    return c
