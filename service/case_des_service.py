import json
import re
from conf import data_dict
from tools.db_oprt_mysql import DataBaseOprtMySQL

cms_json = json.loads('{}')


def get_SecurityType(desc):
    for s in list(data_dict.security_type.keys()):
        if s in desc:
            return s
    return list(data_dict.security_type.keys())[1]


def get_general_commission_template():
    """
    读取权限模板对应的json文件，其中包含CommissionFee和BaseFee信息
    """
    db = DataBaseOprtMySQL.OperateDB(DataBaseOprtMySQL.DataBaseParams.DB5, 'tradingconfigdb')
    db.cur.execute(DataBaseOprtMySQL.SQL.sql_get_com)
    result = db.cur.fetchall()
    # print(result)
    json_obj = json.loads(result[0][0])
    return json_obj


def get_fees_from_db(fee_type, desc):
    market_id, trade_type, security_type = get_fee_params(desc)
    db = DataBaseOprtMySQL.OperateDB(DataBaseOprtMySQL.DataBaseParams.DB5, 'tradingconfigdb')
    db.cur.execute(DataBaseOprtMySQL.SQL.sql_get_fees.format(fee_type, trade_type, security_type, market_id))
    print(DataBaseOprtMySQL.SQL.sql_get_fees.format(fee_type, trade_type, security_type, market_id))
    result = db.cur.fetchall()
    return result[0][0] if result else 0


def get_fees_from_json(json_obj, desc):
    market_id, trade_type, security_type = get_fee_params(desc)
    fees = ('---', "---")
    for i in json_obj:
        if i['marketId']:
            if str(i['marketId']) == str(market_id):
                for j in i['commissionItemList']:
                    if str(j['tradeType']) == str(trade_type) and str(j['securityType']) == str(security_type):
                        fees = (j['minFee'], j['feeRate'])
    return fees


def get_fee_params(desc):
    market_id = find_MarketID(desc)
    trade_type = ''
    for i in data_dict.trade_type:
        if i in desc:
            trade_type = data_dict.trade_type[i]
            break
    security_type = get_SecurityType(desc)
    # print(str(trade_type) + '_' + str(security_type) + '_' + str(market_id))
    return market_id, trade_type, security_type


def find_CaseType(desc):
    return None


def find_PreData(desc):
    return None


def find_CaseDesc(desc):
    return None


def find_CaseBranch(desc):
    return None


def find_CustID(desc):
    return None


def find_EntrustStatus(desc):
    for s in data_dict.intrust_status:
        if '，' + s in desc:
            return s
    return data_dict.intrust_status[0]


def find_DealStatus(desc):
    return find_EntrustStatus(desc)


def find_ErrorCause(desc):
    return None


def find_EntrustQty(desc):
    reg_str = r'[\+|-]?\d+\.?\d+[手|张|股]|[\+|-]?\d+[手|张|股]|[\+|-]?\d+\\[手|张|股]'
    if re.findall(reg_str, desc):
        num = re.split(r'手|张|股', re.findall(reg_str, desc)[0])[0]
        if desc.__contains__('最大可委托数加'):
            return 'MAX+' + num
        elif desc.__contains__('最大可委托数减'):
            return 'MAX-' + num
        elif desc.__contains__('最大可委托数'):
            return 'MAX'
        else:
            return num
    else:
        # 如果未指明数量，可根据预期成交结果以及所属市场，映射撮合的委托数量
        pass
    return None


def find_DealQty(desc):
    return find_EntrustQty(desc)


def find_OrderType(desc):
    keys = list(data_dict.order_type.keys())
    # print(keys)
    keys.sort(key=lambda i: len(i), reverse=True)
    for ot in keys:
        if ot in desc:
            return data_dict.order_type[ot]
    return None


def find_SecurityID(desc):
    result = re.findall(r'(?<=,#)\d{6}(?=,)', desc)
    if result:
        return result[0]
    elif get_SecurityType(desc):
        market_id = find_MarketID(desc)
        return data_dict.security_type_id[market_id + get_SecurityType(desc)]
    else:
        return ''


def find_MarketID(desc):
    if '上海' in desc:
        return '101'
    elif '深圳' in desc:
        return '102'
    else:
        return '101'


def find_FundID(desc):
    return None


def find_AccountSH(desc):
    return None


def find_PartitionSH(desc):
    return None


def find_AccountSZ(desc):
    return None


def find_PartitionSZ(desc):
    return None


def find_Side(desc):
    for i in data_dict.side:
        if i in desc:
            return data_dict.side[i]
    return None


def find_OrdType(desc):
    return find_OrderType(desc)


def find_Price(desc):
    return '昨结价'


def find_MinQty(desc):
    if desc.__contains__('全额成交或撤销'):
        return find_OrderType(desc)
    else:
        return '0'


def find_TimeInForce(desc):
    if '全额成交或撤销' in desc or '立即成交剩余撤销' in desc or '最优五档全额成交剩余撤销' in desc:
        return '3'
    else:
        return '0'


def find_CashMargin(desc):
    return None


def find_MaxPriceLevels(desc):
    if '对手方最优剩余转限价' in desc:
        return '1'
    elif '最优五档全额成交剩余撤销' in desc or '最优五档即时成交剩余转限价' in desc:
        return '5'
    else:
        return '0'


def find_Brokerage(desc):
    fee_type = data_dict.fee_type['经手费']
    return get_fees_from_db(fee_type, desc)


def find_TransferFee(desc):
    fee_type = data_dict.fee_type['过户费']
    return get_fees_from_db(fee_type, desc)


def find_WithTheFee(desc):
    fee_type = data_dict.fee_type['证管费']
    return get_fees_from_db(fee_type, desc)


def find_StampDuty(desc):
    fee_type = data_dict.fee_type['印花税']
    return get_fees_from_db(fee_type, desc)


def find_CommissionFee(desc):
    # 两种方式获取佣金？
    # return get_fees_from_json(cms_json, desc)[1]

    fee_type = data_dict.fee_type['佣金']
    return get_fees_from_db(fee_type, desc)


def find_SecondDiscount(desc):
    return None


def find_BaseFee(desc):
    return get_fees_from_json(cms_json, desc)[0]


def find_LastPrice(desc):
    return None


def find_PrevClosePrice(desc):
    return None


def find_AccruedInterest(desc):
    return None


def find_EntrustUnit(desc):
    return None


def find_TeResponse(desc):
    return None


def find_JysResponse(desc):
    return None


def find_TradeResponse(desc):
    for s in data_dict.order_status:
        if s in desc:
            return data_dict.order_status[s]
    return None
