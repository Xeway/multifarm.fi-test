def loadAuroraChefContract(w3, prices, auroraContract, contractAddress, rewardsPerWeek, json, pricesModule):
    totalAllocPoints = auroraContract.functions.totalAllocPoint().call()

    # informations of the pool
    poolInfo = auroraContract.functions.poolInfo(1).call()

    with open("./abis/erc20_abi.json") as f:
        erc20_abi = json.load(f)

    # WETH-NEAR LP contract
    LPToken = w3.eth.contract(address = poolInfo[0], abi = erc20_abi)

    WETHContract = w3.eth.contract(address = "0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB", abi = erc20_abi)
    NEARContract = w3.eth.contract(address = "0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d", abi = erc20_abi)

    tvl = (prices["weth"] * (WETHContract.functions.balanceOf(poolInfo[0]).call() / 10**(WETHContract.functions.decimals().call()))) + (prices["wrapped-near"] * (NEARContract.functions.balanceOf(poolInfo[0]).call() / 10**(NEARContract.functions.decimals().call())))
    
    price = tvl / (LPToken.functions.totalSupply().call() / 10**(LPToken.functions.decimals().call()))

    poolRewardsPerWeek = poolInfo[1] / totalAllocPoints * rewardsPerWeek
    rewardPrice = pricesModule.getRewardPrice()

    usdPerWeek = poolRewardsPerWeek * rewardPrice

    stakedTVL = price * (LPToken.functions.balanceOf(contractAddress).call() / 10**(LPToken.functions.decimals().call()))

    weeklyAPR = usdPerWeek / stakedTVL * 100
    yearlyAPR = round(weeklyAPR * 52, 2)

    print("NEAR-WETH LP's APR: " + str(yearlyAPR) + "%")
