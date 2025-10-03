import zipfile
from io import BytesIO

import pandas as pd
from fastapi import UploadFile

from src.utils.exceptions import WrongFileTypeError

df: pd.DataFrame | None = None


def get_dataframe():
    """Returns the global pandas DataFrame used."""
    return df


class DataHandler:
    """
    Handles data loading and provides tools for Exploratory Data Analysis (E.D.A.).
    An instance of this class can be used to load a dataset from a CSV file
    and then apply various analysis methods on the loaded pandas DataFrame.
    """

    def __init__(self):
        pass

    async def load_csv(
        self,
        data: UploadFile,
        separator: str = ',',
        header: int = 0,
    ) -> bool:
        """
        Loads data from an uploaded file (CSV or a ZIP containing a CSV)
        into a pandas DataFrame.
        """
        global df
        file = await data.read()
        file_bytes = BytesIO(file)

        if data.content_type == 'application/zip':
            with zipfile.ZipFile(file_bytes) as zip_file:
                csv_filename = next(
                    (name for name in zip_file.namelist() if name.endswith('.csv')),
                    None,
                )

                if not csv_filename:
                    raise FileNotFoundError('No CSV file found in the zip archive.')

                with zip_file.open(csv_filename) as csv_file:
                    df = pd.read_csv(csv_file, sep=separator, header=header)

        elif data.content_type in ['text/csv', 'application/vnd.ms-excel']:
            df = pd.read_csv(file_bytes, sep=separator, header=header)

        else:
            raise WrongFileTypeError(
                f'Unsupported file type: {data.content_type}. '
                'Please upload a CSV or a ZIP file containing a CSV.'
            )

        return True
