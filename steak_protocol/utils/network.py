import os

import blockfrost
import ogmios

import pycardano
from pycardano import Network, OgmiosChainContext, BlockFrostChainContext

ogmios_host = os.getenv("OGMIOS_API_HOST", "localhost")
ogmios_port = os.getenv("OGMIOS_API_PORT", "1337")
ogmios_protocol = os.getenv("OGMIOS_API_PROTOCOL", "ws")
ogmios_url = f"{ogmios_protocol}://{ogmios_host}:{ogmios_port}"

kupo_host = os.getenv("KUPO_API_HOST", None)
kupo_port = os.getenv("KUPO_API_PORT", "80")
kupo_protocol = os.getenv("KUPO_API_PROTOCOL", "http")
kupo_url = (
    f"{kupo_protocol}://{kupo_host}:{kupo_port}" if kupo_host is not None else None
)

blockfrost_project_id = os.getenv("BLOCKFROST_PROJECT_ID", None)

network = Network.TESTNET

# Load chain context
if blockfrost_project_id is not None:
    context = BlockFrostChainContext(
        blockfrost_project_id,
        base_url=(
            blockfrost.ApiUrls.mainnet.value
            if network == Network.MAINNET
            else blockfrost.ApiUrls.preview.value
        ),
    )
else:
    try:
        context = OgmiosChainContext(ogmios_url, network=network, kupo_url=kupo_url)
    except Exception:
        try:
            context = ogmios.OgmiosChainContext(
                host=ogmios_host,
                port=int(ogmios_port),
                secure=ogmios_protocol == "wss",
                network=network,
            )
        except Exception as e:
            print("No ogmios available")
            context = None


def show_tx(signed_tx: pycardano.Transaction):
    tx_hash = signed_tx.id.payload.hex()
    print(f"transaction id: {tx_hash}")
    if network == Network.MAINNET:
        print(f"Cexplorer: https://cexplorer.io/tx/{tx_hash}")
    else:
        print(f"Cexplorer: https://preview.cexplorer.io/tx/{tx_hash}")
        print(f"Cexplorer: https://preprod.cexplorer.io/tx/{tx_hash}")
        print(f"Yaci: http://localhost:5173/transactions/{tx_hash}")
