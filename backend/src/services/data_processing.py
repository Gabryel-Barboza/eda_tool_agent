import zipfile
from io import BytesIO

import pandas as pd
from fastapi import UploadFile

from src.agents import db
from src.utils.exceptions import WrongFileTypeError


class DataInserter:
    def __init__(self):
        self.filename: str

    async def process_csv(
        self,
        data: UploadFile,
        isZip: bool = False,
        separator: str = ',',
        header: int = 0,
        date_format: str = '%Y-%m-%d',
    ):
        file = await data.read()
        file_bytes = BytesIO(file)
        print('leitura realizada')

        if isZip:
            # Descompactação e Leitura do primeiro arquivo .csv

            with zipfile.ZipFile(file_bytes) as zip_file:
                filename = next(
                    (name for name in zip_file.namelist() if name.endswith('.csv')),
                    None,
                )

                if not filename:
                    raise FileNotFoundError

                self.filename = filename.lower().replace(' ', '').split('.')[0]

                # Abrir arquivo csv e começar processamento
                with zip_file.open(filename) as csv_file:
                    await self.insert_data_db(
                        data=csv_file,
                        sep=separator,
                        header=header,
                        date_format=date_format,
                    )
        else:
            if data.content_type == 'application/csv':
                self.filename = data.filename.lower().replace(' ', '')

                await self.insert_data_db(
                    data=data, sep=separator, header=header, date_format=date_format
                )
            raise WrongFileTypeError

        return True

    async def insert_data_db(
        self,
        data: BytesIO,
        sep: str = ',',
        header: int = 0,
        date_format: str = '%Y-%m-%d',
    ):
        # Ler dados em chunks para eficiência de memória
        for chunk in pd.read_csv(
            data,
            sep=sep,
            header=header,
            parse_dates=True,
            date_format=date_format,
            chunksize=1000,
        ):
            # Criar tabela de nome do arquivo e inserir dados
            chunk.to_sql(self.filename, con=db._engine, if_exists='append', index=False)

        return True
