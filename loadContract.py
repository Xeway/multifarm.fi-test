def loadAuroraChefContract(w3, prices, auroraContract, contractAddress, abi, rewardsPerWeek, deathPoolIndices, json):
    totalAllocPoints = auroraContract.functions.totalAllocPoint().call()
    rewardTokenAddress = "0x12c87331f086c3c926248f964f8702c0842fd77f"

    # informations of the pool
    poolInfo = auroraContract.functions.poolInfo(1).call()

    with open("./erc20_abi.json") as f:
        erc20_abi = json.load(f)

    # WETH-NEAR LP contract
    LPToken = w3.eth.contract(address = poolInfo[0], abi = erc20_abi)

    WETHAddress = "0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB"
    NEARAddress = "0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d"

    WETHContract = w3.eth.contract(address = WETHAddress, abi = erc20_abi)
    NEARContract = w3.eth.contract(address = NEARAddress, abi = erc20_abi)

    tvl = (prices["weth"] * (WETHContract.functions.balanceOf(poolInfo[0]).call() / 1e18)) + (prices["wrapped-near"] * (NEARContract.functions.balanceOf(poolInfo[0]).call() / 1e27))
    
    # def calculateTVL(x):
    #     return prices[x] * (LPToken.functions.balanceOf(contractAddress).call() / 1e18)
    
    # tvl = sum(map(calculateTVL, prices))

    price = tvl / (LPToken.functions.totalSupply().call() / 1e18)

    print("tvl:", tvl)
    print("price:", price)