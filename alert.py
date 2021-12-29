# company: DTN
# test: assignment
# date: 06/11/2020
# author: Utpal Sarkar
# description: Printing a lightning strike with the correct asset name and asset owner

import os
import sys
import json
import logging
from helper.quad_key_converter import converter

logger = None
zoom_level = 12


##############################################################
# setup_logger()
# This function helps to basic logging message with readable format
def setup_logger():
    global logger
    if logger is not None:
        return
    logger = logging.getLogger()
    logging.basicConfig(
        level=os.environ.get('LOG_LEVEL', logging.INFO),
        format=f'%(asctime)s %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(message)s'
    )


##############################################################
# create_asset_quad_key_as_key(asset_file)
# This function iterate over asset file and convert it in dict with a quadkey as key
# It will help to find out the asset with quad key easily.
# inputs: asset file path
# returns: dict of asset where quadkey as key
def create_asset_quad_key_as_key(asset_file):
    asset_against_quad_key = dict()
    try:
        with open(asset_file, 'r') as asset_file:
            assets = json.loads(asset_file.read())
            for asset in assets:
                asset_against_quad_key.update({asset.get('quadKey'): {'assetName': asset.get(
                    'assetName'), 'assetOwner': asset.get('assetOwner')}})
    except IOError:
        logger.error("asset_file: Either File is not exist or it is corrupted")
    except Exception as ex:
        logger.error(f'UnknownException: {ex}')
    return asset_against_quad_key


##############################################################
# read_line_from_file(lightning_file, asset_file)
# This function take per line lightning strike data as an input
# This check the the lightning strike's lat/long against -232
# asset's quadkey value
# inputs: lightning_file path and asset_file path
# output: printing on the console "lightning alert for
# <assetOwner>:<assetName>"
def read_line_from_file(lightning_file, asset_file):
    assets = create_asset_quad_key_as_key(asset_file)
    if len(assets) == 0:
        logger.error("asset file is empty")
        sys.exit()
    try:
        with open(lightning_file, 'r') as lightning_file:
            lines = lightning_file.readlines()
            lightning_quad_key = list()
            for line in lines:
                strike = json.loads(line)
                quad_key = converter(strike.get('latitude'), strike.get('longitude'), zoom_level)
                if strike.get('flashType') in [0, 1] and \
                        quad_key not in lightning_quad_key and \
                        assets.get(quad_key):
                    lightning_quad_key.append(quad_key)
                    print(f'lightning alert for '
                          f'{assets.get(quad_key).get("assetOwner")}:'
                          f'{assets.get(quad_key).get("assetName")}')
                if strike.get('flashType') == 9 and assets.get(quad_key):
                    print(f'heartbeat alert for '
                          f'{assets.get(quad_key).get("assetOwner")}:'
                          f'{assets.get(quad_key).get("assetName")}')
    except IOError:
        logger.error("lightning_file: Either File is not exist or it is corrupted")
    except Exception as ex:
        logger.error(f'UnknownException: {ex}')


if __name__ == "__main__":
    setup_logger()
    try:
        read_line_from_file(sys.argv[1], sys.argv[2])
    except IndexError:
        logger.error("Please provide lightning file and asset file as input")
    except Exception as e:
        logger.error(f'UnknownException: {e}')
