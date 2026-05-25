from ..engine import run_command
import json


def search_store_products(
    query: str,
    limit: int = 10,
    min_price: int | None = None,
    max_price: int | None = None,
):
    cmd = [
        'catalog',
        'search',
        '--business', 'beezle.store',
        '--set', f'/query="{query}"',
        '--set', f'/pagination/limit={limit}',
        '--set', '/context/currency="PKR"',
        *(['--set', f'/filters/price/min={min_price}'] if min_price is not None else []),
        *(['--set', f'/filters/price/max={max_price}'] if max_price is not None else []),
        '--format', 'json',
    ]

    output = run_command(cmd)

    if isinstance(output, str):
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return output

    return output