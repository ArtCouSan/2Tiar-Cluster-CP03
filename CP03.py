import dask.dataframe as dd
import dask.distributed as distributed
from io import StringIO
from datetime import datetime, timedelta

# Função para baixar os dados de um canal específico de forma assíncrona
async def download_data_async(channel_id):
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.csv"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return pd.read_csv(await StringIO(response.text))

# Inicializar o cliente Dask
client = distributed.Client(dashboard_address='127.0.0.1:58404', worker_dashboard_address='127.0.0.1:58404')

# Baixar dados para cada localidade de forma assíncrona
boston_data = dd.from_delayed([dask.delayed(download_data_async)(12397)])
santiago_data = dd.from_delayed([dask.delayed(download_data_async)(1293177)])
stuttgart_data = dd.from_delayed([dask.delayed(download_data_async)(357142)])
russia_data = dd.from_delayed([dask.delayed(download_data_async)(1061956)])

