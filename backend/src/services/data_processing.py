import zipfile
from io import BytesIO

import pandas as pd

from src.agents import SQLAgent
from src.tools import db


class DataInserter:
    def __init__(self):
        self.agent = SQLAgent()
        self.agent.init_groq_model(model_name='openai/gpt-oss-120b', temperature=0)

    async def process_csv(
        self,
        data: BytesIO,
        isZip: bool = False,
        separator: str = ',',
        header: int = 0,
        date_format: str = '%Y-%m-%d',
    ):
        if isZip:
            file = await data.read()
            data = zipfile.ZipFile(BytesIO(file))

        df = pd.read_csv(data, sep=separator, header=header, date_format=date_format)
        json = df.to_json(orient='records')

        response = self.agent.run(
            'Insert this data in the database, pay attention to use the correct data types for each column',
            db.dialect,
            json,
        )

        return response
