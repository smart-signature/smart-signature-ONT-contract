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

PUBLISH_ACCT = 

################################################################################
# STORAGE KEY CONSTANT
# Belows are storage key for some variable token information.

DEPLOYED_KEY = 'DEPLOYED_SPKZ03'
OWNER_KEY = '___OWNER_SPKZ03'
SPKZ_SUPPLY_KEY = '__SUPPLY_SPKZ03'


################################################################################
# STORAGE KEY PREFIX
# Since all data are stored in the key-value storage, the data need to be
# classified by key prefix. All key prefixes length must be the same.

OWN_PREFIX = '_____own_spkz03'
ALLOWANCE_PREFIX = '___allow_spkz03'


SIGN_PREFIX = b'\x01'
APPROVE_PREFIX = b'\x02'
################################################################################
# 转账合约
OntContract = Base58ToAddress("AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV")
# 本合约地址
selfContractAddress = GetExecutingScriptHash()
# 开发者账户
developerAcc = 'ARfyRJQJVdUG1NX18rvp6LncWgaXTQUNBq'
# 国家
REGION = 'region'
# 倒计时结束时间
ENDTIME = 'endtime'
# 最后一次购买人
LASTBUY = 'lastbuy'
# 30天的秒
cycle = 3456000
################################################################################
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
    if operation == 'name':
        return NAME
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

    if operation == 'approve':
        if len(args) != 3:
            return False
        owner  = args[0]
        spender = args[1]
        amount = args[2]
        return approve(owner,spender,amount)
    if operation == 'allowance':
        if len(args) != 2:
            return False
        owner = args[0]
        spender = args[1]
        return allowance(owner,spender)

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

    # supply the coin. All coin will be belong to deployer.
    #total = INIT_SUPPLY * FACTOR
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
    # fromBalance = Get(ctx,fromKey)
    saveData(signKey,sign)

    #toKey = concat(BALANCE_PREFIX,to_acct)
    #toBalance = Get(ctx,toKey)
    
    saveData(toKey,toBalance + amount)
    PublishEvent(sign)
    return True


def approve(owner,spender,amount):
    if len(spender) != 20 or len(owner) != 20:
        raise Exception("address length error")
    if CheckWitness(owner) == False:
        return False
    if amount > balanceOf(owner):
        return False
    key = concat(concat(APPROVE_PREFIX,owner),spender)
    Put(ctx, key, amount)
    ApprovalEvent(owner, spender, amount)
    return True

def transfer(from_acct,to_acct,amount):
    if len(to_acct) != 20 or len(from_acct) != 20:
        raise Exception("address length error")
    if CheckWitness(from_acct) == False:
        return False

    fromKey = concat(BALANCE_PREFIX,from_acct)
    fromBalance = Get(ctx,fromKey)
    if amount > fromBalance:
        return False
    if amount == fromBalance:
        Delete(ctx,fromKey)
    else:
        Put(ctx,fromKey,fromBalance - amount)

    toKey = concat(BALANCE_PREFIX,to_acct)
    toBalance = Get(ctx,toKey)
    Put(ctx,toKey,toBalance + amount)
    TransferEvent(from_acct, to_acct, amount)
    return True



def name():
    """
    :return: name of the token
    """
    return NAME


def balanceOf(account):
    """
    :param account:
    :return: the token balance of account
    """
    if len(account) != 20:
        raise Exception("address length error")
    return Get(ctx,concat(BALANCE_PREFIX,account))


def transfer(from_acct,to_acct,amount):
    """
    Transfer amount of tokens from from_acct to to_acct
    :param from_acct: the account from which the amount of tokens will be transferred
    :param to_acct: the account to which the amount of tokens will be transferred
    :param amount: the amount of the tokens to be transferred, >= 0
    :return: True means success, False or raising exception means failure.
    """
    if len(to_acct) != 20 or len(from_acct) != 20:
        raise Exception("address length error")
    if CheckWitness(from_acct) == False:
        return False

    fromKey = concat(BALANCE_PREFIX,from_acct)
    fromBalance = Get(ctx,fromKey)
    if amount > fromBalance:
        return False
    if amount == fromBalance:
        Delete(ctx,fromKey)
    else:
        Put(ctx,fromKey,fromBalance - amount)

    toKey = concat(BALANCE_PREFIX,to_acct)
    toBalance = Get(ctx,toKey)
    Put(ctx,toKey,toBalance + amount)
    TransferEvent(from_acct, to_acct, amount)
    return True





def approve(owner,spender,amount):
    """
    owner allow spender to spend amount of token from owner account
    Note here, the amount should be less than the balance of owner right now.
    :param owner:
    :param spender:
    :param amount: amount>=0
    :return: True means success, False or raising exception means failure.
    """
    if len(spender) != 20 or len(owner) != 20:
        raise Exception("address length error")
    if CheckWitness(owner) == False:
        return False
    if amount > balanceOf(owner):
        return False
    key = concat(concat(APPROVE_PREFIX,owner),spender)
    Put(ctx, key, amount)
    ApprovalEvent(owner, spender, amount)
    return True


def transferFrom(spender,from_acct,to_acct,amount):
    """
    spender spends amount of tokens on the behalf of from_acct, spender makes a transaction of amount of tokens
    from from_acct to to_acct
    :param spender:
    :param from_acct:
    :param to_acct:
    :param amount:
    :return:
    """
    if len(spender) != 20 or len(from_acct) != 20 or len(to_acct) != 20:
        raise Exception("address length error")
    if CheckWitness(spender) == False:
        return False

    fromKey = concat(BALANCE_PREFIX, from_acct)
    fromBalance = Get(ctx, fromKey)
    if amount > fromBalance:
        return False

    approveKey = concat(concat(APPROVE_PREFIX,from_acct),spender)
    approvedAmount = Get(ctx,approveKey)
    toKey = concat(BALANCE_PREFIX,to_acct)
    toBalance = Get(ctx, toKey)
    if amount > approvedAmount:
        return False
    elif amount == approvedAmount:
        Delete(ctx,approveKey)
        Delete(ctx, fromBalance - amount)
    else:
        Put(ctx,approveKey,approvedAmount - amount)
        Put(ctx, fromKey, fromBalance - amount)

    Put(ctx, toKey, toBalance + amount)
    TransferEvent(from_acct, to_acct, amount)

    return True

def saveData(key, value):
    ctx = GetContext()
    Put(ctx, key, value)


def allowance(owner,spender):
    """
    check how many token the spender is allowed to spend from owner account
    :param owner: token owner
    :param spender:  token spender
    :return: the allowed amount of tokens
    """
    key = concat(concat(APPROVE_PREFIX,owner),spender)
    return Get(ctx,key)

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
