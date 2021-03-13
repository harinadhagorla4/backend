# Python Imports
from io import BytesIO

# Third Party Imports
import pandas as pd
import numpy as np

# Local Imports
from bank.models import Ifsc


def dump_to_db(file):
    """
    :param filepath: File path
    :return: Dump the data into the DB
    """
    file_name = file.name
    file_ext = file_name.split('.')[-1]
    if file_ext not in ['xls', 'xlsx']:
        return Response({"message": "Upload a valid Excel File."}, status=status.HTTP_400_BAD_REQUEST)
    file_data = file.read()
    data_frame = pd.read_excel(BytesIO(file_data), engine='openpyxl')
    data_frame = data_frame.replace(np.nan, '')
    # expected_columns = ["BANK", "IFSC", "MICR CODE", "BRANCH", "ADDRESS", "STD CODE", "CITY", "DISTRICT,STATE"]
    # data_frame.columns

    # check df columns and expected columns are equal then allow else return error message
    ifsc_objs = []
    invalid_data = []
    queryset = Ifsc.objects.all()
    for index, row in data_frame.iterrows():
        if row['IFSC'] not in queryset.values_list('ifsc', flat=True):
            ifsc_objs.append(
                Ifsc(bank_name=row["BANK"], ifsc=row["IFSC"], micr_code=row["MICR CODE"], branch=row["BRANCH"],
                     address=row["ADDRESS"], std_code=row["STD CODE"], city=row["CITY"],
                     district=row["DISTRICT"],
                     state=row["STATE"]))
        else:
            invalid_data.append([index, row["BANK"], "Error Message"])
    Ifsc.objects.bulk_create(ifsc_objs)
