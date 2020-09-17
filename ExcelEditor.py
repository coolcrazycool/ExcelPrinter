import pandas as pd
from ast import literal_eval
import xlsxwriter

FILENAME = 'Input_Excel.xlsx'


STRING_LIST = [
"ACQUIRER-ACQUIRER-CLIENT_DEFINED-KEYS_CHANGE",
# "ACQUIRER-ACQUIRER-CLIENT_DEFINED-RESULT_CHECK",
# "ACQUIRER-ACQUIRER-CARD_PIN_CHANGE-ATM_PIN",
# "ACQUIRER-ACQUIRER-VIEW_STATEMENT-ATM_BALANCE",
# "ACQUIRER-ACQUIRER-VIEW_STATEMENT-POS_BALANCE",
# "ACQUIRER-ACQUIRER-DEPOSIT-POS_RETURN",
# "ACQUIRER-ACQUIRER-DEPOSIT-EPOS_RETURN",
]


def keys_reader(input_file):
    with open(input_file, 'r') as file:
        key_list = [line[:-1] for line in file]
    return key_list


def excel_reader(input_file):
    excel_df = pd.read_excel(input_file, sheet_name='Sheet1')
    return excel_df


def excel_writer(output_file, df):
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


def string_equairer(keys_list, df_to_reform, string_to_add):
    for index, value in df_to_reform['id'].iteritems():
        if value in keys_list:
            temp = literal_eval(df_to_reform.at[index, 'CTST'])
            temp.append(string_to_add)
            df_to_reform.at[index, 'CTST'] = list(set(temp))
            keys_list.remove(value)

    for value in keys_list:
        temp_dict = {'name': [None], 'id': [value], 'CTST': [[string_to_add]]}
        temp_df = pd.DataFrame.from_dict(temp_dict)
        df_to_reform = df_to_reform.append(temp_df)
    return df_to_reform


if __name__ == "__main__":
    for element in STRING_LIST:
        list_of_keys = keys_reader('text_files/'+element+'.txt')
        excel_df = excel_reader(FILENAME)
        final_df = string_equairer(list_of_keys, excel_df, element)
        excel_writer(FILENAME, final_df)


