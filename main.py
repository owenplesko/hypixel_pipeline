import requests
from db import store_item
import gzip
import io
import json
import base64
from pynbt import *
import time

def main():
    while True:
        raw_auctions = get_ended_auctions()
        auctions = [sanitize_auction(a) for a in raw_auctions]
        
        for item in auctions:
            try:
                store_item(item["auction_id"], item["price"], item["item"]["id"], json.dumps(item["item"]))
            except:
                pass
            
        time.sleep(60)
    
def sanitize_auction(raw):
    auction = {
        'auction_id': raw['auction_id'],
        'price': raw['price'],
        'timestamp': raw['timestamp'],
        'bin': raw['bin']
    }
    
    item_nbt = decode_item(raw['item_bytes'])
    item_dict = nbt_to_dict(item_nbt['i'][0]['tag']['ExtraAttributes'])
        
    auction['item'] = item_dict
    
    # santize petInfo because its weird
    if(auction['item']['id'] == 'PET'):
        # for some reason petInfo is json string, parse it to a dict
        auction['item']['petInfo'] = json.loads(auction['item']['petInfo'])
        # add pet type to item_id
        auction['item']['id'] = f"{auction['item']['id']}_{auction['item']['petInfo']['type']}"
    
    return auction

def get_ended_auctions():
    req = requests.get("https://api.hypixel.net/v2/skyblock/auctions_ended")
    data = req.json()
    auctions = data['auctions']
    return auctions

def decode_item(b64_str):
    # b64 decode
    gzip_bytes = base64.b64decode(b64_str)
    
    # gunzip
    nbt_bytes = gzip.decompress(gzip_bytes)
    
    # parse nbt data
    with io.BytesIO(nbt_bytes) as nbt_buffer:
        nbt = NBTFile(nbt_buffer)
    
    return nbt

def nbt_to_dict(nbt_obj):
    if isinstance(nbt_obj, TAG_Compound):
        # Convert compound tag to dictionary
        result_dict = {}
        for tag_name, tag_value in nbt_obj.items():
            result_dict[tag_name] = nbt_to_dict(tag_value)
        return result_dict
    elif isinstance(nbt_obj, TAG_List):
        # Convert list tag to list
        return [nbt_to_dict(tag) for tag in nbt_obj]
    else:
        # Other tag types (e.g., TAG_Byte, TAG_String, etc.)
        return nbt_obj.value

if __name__ == "__main__":
    main()