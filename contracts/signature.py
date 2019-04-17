from boa.interop.Ontology.Runtime import AddressToBase58, Base58ToAddress
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import Notify, CheckWitness
from boa.interop.System.Action import RegisterAction
from boa.builtins import concat, ToScriptHash
from .libs.SafeCheck import *
from .libs.SafeMath import *
from .libs.Utils import *

PublishEvent = RegisterAction("publish", "sign")

################################################################################
# 合约 INFO CONSTANTS
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

PLAYER_PREFIX = b'\x01'
SIGN_PREFIX = b'\x02'

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
    def __init__(self):
        self.signIncome = 0
        self.shareIncome = 0
        self.shares = {}


class sign:
    def __init__(self, id, author, fissionFactor, ipfs_hash, public_key, signature):
        self.id = id
        self.author = author
        self.fissionFactor = fissionFactor
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
            fissionFactor = args[3]
            ipfs_hash = args[4]
            public_key = args[5]
            signature = args[6]
            s = sign(id, author, fissionFactor, ipfs_hash, public_key, signature)
            return publish(acct, s);



def init():
    """
    Constructor of this contract. Only deployer hard-coded can call this function
    and cannot call this function after called once.
    Followings are initialization list for SS.
    """
    Require(CheckWitness(DEPLOYER))                    # only can be initialized by deployer
    Require(not Get(ctx, DEPLOYED_KEY))                # only can deploy once
    #if is_deployed:
    #    Notify("Already initialized!")
    #    return False

    # disable to deploy again
    saveData(DEPLOYED_KEY, 1)

    # the first owner is the deployer
    # can transfer ownership to other by calling `TransferOwner` function
    saveData(OWNER_KEY, DEPLOYER)
     
    # supply the coin. All coin will be belong to deployer.
    #saveData(SPKZ_SUPPLY_KEY, total)
    #deployer_key = concat(OWN_PREFIX, DEPLOYER)
    #saveData(deployer_key, total)
    #Notify(['transfer', '', DEPLOYER, total])
    return True

def publish(acct, sign):
    if len(acct) != 20 or len(sign.author) != 20:
        raise Exception("address length error")
    
    Require(CheckWitness(acct))
    Require(acct == PUBLISHER)

    signKey = concat(SIGN_PREFIX,sign.id)
    sSign = Serialize(sign)
    saveData(signKey, sSign)
    
    PublishEvent(sign)
    return True

def createShare(owner, signId, referral = None):
    if len(owner) != 20 :
        raise Exception("owner address length error")
    
    # owner 前置處理
    Require(CheckWitness(owner)) # 查授權
    pOwner = Get(GetContext(), concat(PLAYER_PREFIX, owner)) 
    pOwner = Deserialize(p) if p else player()

    # sign 前置處理
    sSign = Get(GetContext(), concat(SIGN_PREFIX, signId))
    
    sign = Deserialize(sSign)

    # 查 owner 有沒有生過這 sign 的 share
    Require(signId in pOwner.shares)

    if referral: # 有推薦人
        if len(referral) != 20 :
            raise Exception("owner address length error")

        if referral != owner:
            #Require(signId in pOwner.shares)
    
    # pOwner.shares[sign.id] = in.amount * sign.fissionFactor / 1000;

    # 拿到目标购买国家进行交易
    #param = state(Base58ToAddress(fromAcc), Base58ToAddress(item[2]), item[1] - 1)
    #res = Invoke(0, OntContract, "transfer", [param])
    #if res != b'\x01':
    #    Notify("buy error.")
    #    return False
    # 每一次给合约内部转1个币
    #paramContract = state(Base58ToAddress(fromAcc), selfContractAddress, 1)
    #resContract = Invoke(0, OntContract, 'transfer', [paramContract])
    
    saveData(PLAYER_PREFIX, Serialize(pOwner))
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
