from brownie import FundMe,MockV3Aggregator, network, config
#__init__.py this file is created so the python knows to get stuff from other scripts or packages
from scripts.helpful_scripts import get_account, deploy_mocks,LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    account = get_account()
    print(account)

    #if we are on persistant network like rinkeby, use associated address
    #otherwise use mocks 
    #if network.show_active() != "development":
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
        #"0x8A753747A1Fa494EC906cE90E9f37563A8AF630e" #chainlink price feed addy from rinkeby
        print(f"price_feed_address{price_feed_address}")
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        print(f"price_feed_address {price_feed_address}")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),) 
        #publish_source=True is used to verify deployed contract , also th
        #this generates the source code in etherscan 
        #ex. https://rinkeby.etherscan.io/address/0x264B9e3bAD4a8Ce8BE759b3Efb88B8cb9a05D6c3

    print(f"Contract deployed to {fund_me.address}")

def main():
    deploy_fund_me()