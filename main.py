from web3 import Web3, HTTPProvider
import prices
import json
import loadContract

contractAddress = "0x35CC71888DBb9FfB777337324a4A60fdBAA19DDE"
rewardTokenTicker = "BRL"

tokens = {
    "weth": 0,
    "wrapped-near": 0
}

with open("./abis/contract_abi.json") as f:
    abi = json.load(f)

w3 = Web3(HTTPProvider("https://mainnet.aurora.dev"))

auroraContract = w3.eth.contract(address = contractAddress, abi = abi)

currentBlock = w3.eth.get_block_number()

multiplier = auroraContract.functions.getMultiplier(currentBlock, currentBlock + 1).call()

rewardsPerWeek = auroraContract.functions.BRLPerBlock().call() / 1e18 * multiplier * 604800 / 1.1

# we update the 'tokens' dictionnary by adding the prices
prices.getPrices(tokens)

loadContract.loadAuroraChefContract(w3, tokens, auroraContract, contractAddress, rewardsPerWeek, json, prices)