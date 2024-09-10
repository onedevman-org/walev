from .Asset import Asset

# 

class Wallet:
    def __init__(self):
        self.__assets: list[Asset] = []
        
        return
    
    # 
    
    def assets(self):
        return self.__assets
    
    # 
    
    def __searchAsset(self, asset: Asset):
        assets = self.__assets
        asset_count = len(assets)
        
        asset_found = False
        asset_index = 0
        
        if asset_count > 0:
            current_asset: Asset = assets[asset_index]
            asset_found = current_asset.symbol() == asset.symbol()
            
            while asset_index < asset_count and current_asset != None and asset_found:
                current_asset = assets[asset_index]
                asset_found = current_asset.symbol() == asset.symbol()
        
        return asset_index if asset_found else None

    def setAsset(self, asset: Asset):
        asset_index = self.__searchAsset(asset)
                
        if asset_index == None:
            self.__assets.append(asset)
        else:
            self.__assets[asset_index] = asset

    def setAssets(self, assets: list[Asset]):
        for asset in assets:
            self.setAsset(asset)
    
    def removeAsset(self, asset: Asset):
        asset_index = self.__searchAsset(asset)
        
        if asset_index != None:
            self.__assets.pop(asset_index)