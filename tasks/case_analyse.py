"""
split case desc into columns.
"""

import pandas as pd
from service.case_des_service import *


def case_analyse():
    df = pd.read_excel('../data/现货权限自动化用例.xlsx', header=1, sheet_name='现货集中交易')

    headers = df.head(0)
    case_descs = df['CaseDesc']
    print(headers)
    print(case_descs)

    ignore_headers = ['CaseType', 'PreData', 'CaseDesc', 'CaseBranch', 'CustID']
    fees_headers = ['Brokerage', 'TransferFee', 'WithTheFee', 'StampDuty', 'CommissionFee', 'SecondDiscount', 'BaseFee']
    ignore_headers += fees_headers

    for h in ignore_headers:
        del headers[h]

    for head in headers:
        print(head)
        for index, desc in zip(case_descs.keys(), case_descs.values):
            func = 'find_' + head + '("' + str(desc) + '")'
            df.loc[index, head] = eval(func)

    dfw = pd.DataFrame(df)
    dfw.to_excel('../output/output.xlsx', sheet_name='现货集中交易', index=True, header=True)


if __name__ == '__main__':
    case_analyse()
