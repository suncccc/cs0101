# -*- coding:utf-8 -*-
"""
========================20171019 SDP v2.3 Sample Arbitrage======================

Please refer to https://wiki.mycapital.net/index.php?s=/1&page_id=1 for detailed description.
Or contact us on sdp@mycapital.net
"""

from sys import platform

if platform == "win32":
    from simsdp import *
    from simsdp.sdpconfig import StratConfig

import pandas, numpy
import numpy as np
import pandas as pd

# quote attributes to log
LOG_QUOTE_ATTRS = ['int_time', 'symbol', 'last_px', 'open_px', 'bv1', 'bp1', 'ap1', 'av1']


def on_init(config):
    """
    策略初始化方法，获取配置信息，每个交易session调用一次
    :param config:
    :return:
    """
    CONTEXT.on_init(config)  # 把config存入全局CONTEXT中
    CONTEXT.my_data = {
        'quotes': {},  # Dict: Last quote of each contract
        'sh_contract': None,  # String: LME ticker
        'lme_contract': None,  # String: Shanghai ticker
        'sh_old_contracts': [], # List: Shanghai tickers that are not the dominant/main contract, used to switch dominant contract
        'signal': 0  # Int: signal

    }

    contract = config.contracts[0]
    print contract.symbol,'1'
    CONTEXT.my_data['lme_contract'] = contract.symbol  # rb
    contract = config.contracts[1]
    print contract.symbol,'2'
    CONTEXT.my_data['sh_contract'] = contract.symbol
    print(CONTEXT.my_data['lme_contract'], 'lme_contract')
    print(CONTEXT.my_data['sh_contract'], 'sh_contract')

    CONTEXT.count = 0
    CONTEXT.tick = {"int_time": [],
                    "px_15": [],
                    "px_20": []   # 20 min
                    }
    CONTEXT.test = []
    CONTEXT.signals = []
    # for contract in config.contracts:
    #     if contract.exch == Exchanges.LME:  # London
    #         CONTEXT.my_data['lme_contract'] = contract.symbol
    #     elif contract.exch == Exchanges.SHFE:  # Shanghai
    #         CONTEXT.my_data['sh_old_contracts'].append(contract.symbol)

    # Write log to file
    st_log_ln('id ' + ' '.join(LOG_QUOTE_ATTRS) + ' signal')


def on_book(quote):
    """
    行情处理方法，每收到1笔行情将会调用一次
    :param quote:
    :return:
    """
    CONTEXT.on_book(quote)  # 把quote存入全局CONTEXT中

    CONTEXT.tick["int_time"].append(quote.int_time)


    sh_sym = CONTEXT.my_data['sh_contract']
    l_sym = CONTEXT.my_data['lme_contract']
    if sh_sym is None or quote.symbol == sh_sym or quote.symbol == l_sym:
        # Print dominant/main contract's quotes to log
        st_log_ln(str(CONTEXT.config.strat_id) + \
                  ' ' + ' '.join([str(getattr(quote, x)) for x in LOG_QUOTE_ATTRS]) + \
                  ' ' + str(CONTEXT.my_data['signal']))

    # Record the last quote of each contract
    CONTEXT.my_data['quotes'][quote.symbol] = quote

    # # Handle switching dominant/main contract
    # if CONTEXT.my_data['sh_contract'] is None:
    #     is_sh_quote_all_received = True
    #     for contract in CONTEXT.my_data['sh_old_contracts']:
    #         if contract not in CONTEXT.my_data['quotes']:
    #             is_sh_quote_all_received = False
    #     # Find the dominant/main contract
    #     if is_sh_quote_all_received:
    #         pre_oi_list = [CONTEXT.my_data['quotes'][contract].open_interest for contract in
    #                        CONTEXT.my_data['sh_old_contracts']]
    #         CONTEXT.my_data['sh_contract'] = CONTEXT.my_data['sh_old_contracts'][pre_oi_list.index(max(pre_oi_list))]
    #         CONTEXT.my_data['sh_old_contracts'] = [x for x in CONTEXT.my_data['sh_old_contracts'] if
    #                                                x != CONTEXT.my_data['sh_contract']]

    # Test--------------------------------------
    # Signal Open

    # if 90000000 < quote.int_time < 90005000:
    #     signal = 2
    # elif 145500000 < quote.int_time < 150000000:
    #     signal = -2
    # else:
    #     signal = 0

        # Calculate signal

        
        
        


    # Treshold = 2
    #
    # if quote.int_time > 91000000:
    #
    #
    #     try:
    #         if CONTEXT.my_data['signal'] < -Treshold and (
    #                         CONTEXT.short_position(l_sym) == 0 and CONTEXT.long_position(sh_sym) == 0
    #                                 and CONTEXT.long_position(l_sym) == 0 and CONTEXT.short_position(sh_sym) == 0):
    #             process_strat_signal(sh_sym, OrderDirection.SELL, 1, CONTEXT.my_data['quotes'][sh_sym].bp1)
    #             process_strat_signal(l_sym, OrderDirection.BUY, 1, CONTEXT.my_data['quotes'][l_sym].ap1)
    #         elif CONTEXT.my_data['signal'] > Treshold and (
    #                         CONTEXT.short_position(l_sym) == 0 and CONTEXT.long_position(sh_sym) == 0
    #                                 and CONTEXT.long_position(l_sym) == 0 and CONTEXT.short_position(sh_sym) == 0):
    #             # print CONTEXT.my_data['quotes']
    #             process_strat_signal(sh_sym, OrderDirection.BUY, 1, CONTEXT.my_data['quotes'][sh_sym].ap1)
    #             process_strat_signal(l_sym, OrderDirection.SELL, 1, CONTEXT.my_data['quotes'][l_sym].bp1)
    #         elif CONTEXT.my_data['signal'] < (Treshold*0.25) and (
    #                         CONTEXT.short_position(l_sym) > 0 or CONTEXT.long_position(sh_sym) > 0):
    #             process_strat_signal(sh_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][sh_sym].bp1)
    #             process_strat_signal(l_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][l_sym].ap1)
    #         elif CONTEXT.my_data['signal'] > (-Treshold*0.25) and (
    #                         CONTEXT.long_position(l_sym) > 0 or CONTEXT.short_position(sh_sym) > 0):
    #             process_strat_signal(sh_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][sh_sym].ap1)
    #             process_strat_signal(l_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][l_sym].bp1)
    #         # CONTEXT.test.append(CONTEXT.short_position(sh_sym))
    #         # print np.unique(CONTEXT.test), 'short position...'
    #         # print '---------------------------'
    #         # print 'signal:', CONTEXT.my_data['signal']
    #         # print sh_sym, ' long position:', CONTEXT.long_position(sh_sym)
    #         # print sh_sym, ' short position:', CONTEXT.short_position(sh_sym)
    #         # print l_sym, ' long position:', CONTEXT.long_position(l_sym)
    #         # print l_sym, ' short position:', CONTEXT.short_position(l_sym)
    #     except KeyError:
    #         pass

    # Threshold = 2
    #
    # if 91000000 < quote.int_time > 145500000:
    #
    #     try:
    #         if signal < -Threshold and (
    #                                 CONTEXT.short_position(l_sym) == 0 and CONTEXT.long_position(sh_sym) == 0
    #                     and CONTEXT.long_position(l_sym) == 0 and CONTEXT.short_position(sh_sym) == 0):
    #             process_strat_signal(sh_sym, OrderDirection.SELL, 1, CONTEXT.my_data['quotes'][sh_sym].bp1)
    #             process_strat_signal(l_sym, OrderDirection.BUY, 1, CONTEXT.my_data['quotes'][l_sym].ap1)
    #         elif signal > Threshold and (
    #                                 CONTEXT.short_position(l_sym) == 0 and CONTEXT.long_position(sh_sym) == 0
    #                     and CONTEXT.long_position(l_sym) == 0 and CONTEXT.short_position(sh_sym) == 0):
    #             # print CONTEXT.my_data['quotes']
    #             process_strat_signal(sh_sym, OrderDirection.BUY, 1, CONTEXT.my_data['quotes'][sh_sym].ap1)
    #             process_strat_signal(l_sym, OrderDirection.SELL, 1, CONTEXT.my_data['quotes'][l_sym].bp1)
    #         elif signal < (Threshold * 0.25) and (
    #                         CONTEXT.short_position(l_sym) > 0 or CONTEXT.long_position(sh_sym) > 0):
    #             process_strat_signal(sh_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][sh_sym].bp1)
    #             process_strat_signal(l_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][l_sym].ap1)
    #         elif signal > (-Threshold * 0.25) and (
    #                         CONTEXT.long_position(l_sym) > 0 or CONTEXT.short_position(sh_sym) > 0):
    #             process_strat_signal(sh_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][sh_sym].ap1)
    #             process_strat_signal(l_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][l_sym].bp1)
    #         # CONTEXT.test.append(CONTEXT.short_position(sh_sym))
    #         # print np.unique(CONTEXT.test), 'short position...'
    #         print '---------------------------'
    #         print 'signal:', CONTEXT.my_data['signal']
    #         print sh_sym, ' long position:', CONTEXT.long_position(sh_sym)
    #         print sh_sym, ' short position:', CONTEXT.short_position(sh_sym)
    #         print l_sym, ' long position:', CONTEXT.long_position(l_sym)
    #         print l_sym, ' short position:', CONTEXT.short_position(l_sym)
    #     except KeyError:
    #         pass
    #

    Threshold = 2

    if 91000000 < quote.int_time > 145500000:

        try:
            if signal < -Threshold and (
                                    CONTEXT.short_position(l_sym) == 0 and CONTEXT.long_position(sh_sym) == 0
                        and CONTEXT.long_position(l_sym) == 0 and CONTEXT.short_position(sh_sym) == 0):
                process_strat_signal(sh_sym, OrderDirection.SELL, 1, CONTEXT.my_data['quotes'][sh_sym].bp1)
                process_strat_signal(l_sym, OrderDirection.BUY, 1, CONTEXT.my_data['quotes'][l_sym].ap1)
            elif signal > Threshold and (
                                    CONTEXT.short_position(l_sym) == 0 and CONTEXT.long_position(sh_sym) == 0
                        and CONTEXT.long_position(l_sym) == 0 and CONTEXT.short_position(sh_sym) == 0):
                # print CONTEXT.my_data['quotes']
                process_strat_signal(sh_sym, OrderDirection.BUY, 1, CONTEXT.my_data['quotes'][sh_sym].ap1)
                process_strat_signal(l_sym, OrderDirection.SELL, 1, CONTEXT.my_data['quotes'][l_sym].bp1)
            elif -0.1 < signal < 0.1 and (
                            CONTEXT.short_position(l_sym) > 0 or CONTEXT.long_position(sh_sym) > 0
                        or CONTEXT.long_position(l_sym) > 0 or CONTEXT.short_position(sh_sym) > 0):
                process_strat_signal(sh_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][sh_sym].bp1)
                process_strat_signal(l_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][l_sym].ap1)

            # CONTEXT.test.append(CONTEXT.short_position(sh_sym))
            # print np.unique(CONTEXT.test), 'short position...'
            print '---------------------------'
            print 'signal:', CONTEXT.my_data['signal']
            print sh_sym, ' long position:', CONTEXT.long_position(sh_sym)
            print sh_sym, ' short position:', CONTEXT.short_position(sh_sym)
            print l_sym, ' long position:', CONTEXT.long_position(l_sym)
            print l_sym, ' short position:', CONTEXT.short_position(l_sym)
        except KeyError:
            pass




#    每天最后五分钟平仓
    if 145500000 < quote.int_time < 150000000:
        if CONTEXT.long_position(sh_sym) > 0:
            process_strat_signal(sh_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][sh_sym].ap1)
        if CONTEXT.short_position(sh_sym) > 0:
            process_strat_signal(sh_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][sh_sym].ap1)
        if CONTEXT.long_position(l_sym) > 0:
            process_strat_signal(l_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][l_sym].bp1)
        if CONTEXT.short_position(l_sym) >0:
            process_strat_signal(l_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][l_sym].bp1)



def on_bar(bar_quote):
    """
    bar处理方法，每收到bar信息将会调用一次，bar在配置文件中配置
    :param bar:
    :return:
    """
    pass


def on_order_update(ord_status):
    """
    回报处理方法，收到回报将被调用
    :param ord_status:
    :return:
    """
    CONTEXT.on_order_update(ord_status)  # 把回报存入全局CONTEXT中
    CONTEXT.log_response()  # 输出回报到日志


def on_timer():
    """
    定时任务方法，根据设定的时间每隔一段时间调用一次
    :return:

    """
    # 计算过去20分钟移动平均
    MA20 = np.mean(CONTEXT.tick["px_20"])
    CONTEXT.sma20 = MA20
    STD20 = np.std(CONTEXT.tick["px_20"])
    CONTEXT.std20 = STD20

    # print CONTEXT.tick['int_time'][-1]
    # print MA20,'sma'
    # print STD20, 'std20'


    sh_sym = CONTEXT.my_data['sh_contract']
    l_sym = CONTEXT.my_data['lme_contract']

    # print(sh_sym)

    # print(sh_sym)
    # print(l_sym)

    if CONTEXT.my_data['sh_old_contracts'] and sh_sym is not None:
        # Transfer positions from non-dominant contracts to the dominant contract
        # Non-dominant contracts that transferred positions are recorded here
        transferred_syms = []
        net_pos = 0
        for old_sym in CONTEXT.my_data['sh_old_contracts']:
            if old_sym in CONTEXT.my_data['quotes']:
                if CONTEXT.long_position(old_sym) == 0 and CONTEXT.short_position(old_sym) == 0:
                    transferred_syms.append(old_sym)
                else:
                    net_pos += CONTEXT.long_position(old_sym) - CONTEXT.short_position(old_sym)
                    process_strat_signal(old_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][old_sym].ap1)
                    process_strat_signal(old_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][old_sym].bp1)
        if net_pos > 0:
            process_strat_signal(sh_sym, OrderDirection.BUY, net_pos, CONTEXT.my_data['quotes'][sh_sym].ap1)
        elif net_pos < 0:
            process_strat_signal(sh_sym, OrderDirection.SELL, -net_pos, CONTEXT.my_data['quotes'][sh_sym].bp1)

        # Remove non-dominant contracts without positions
        CONTEXT.my_data['sh_old_contracts'] = [x for x in CONTEXT.my_data['sh_old_contracts'] if
                                               x not in transferred_syms]
    elif sh_sym is not None and l_sym is not None and \
                    sh_sym in CONTEXT.my_data['quotes'] and \
                    l_sym in CONTEXT.my_data['quotes'] and \
                    CONTEXT.my_data['quotes'][sh_sym] is not None and \
                    CONTEXT.my_data['quotes'][l_sym] is not None:

        # Calculate signal
        sh_quote = CONTEXT.my_data['quotes'][sh_sym]
        l_quote = CONTEXT.my_data['quotes'][l_sym]
        #-------csun

        # spd = sh_quote.last_px-l_quote.last_px
        # signal = (spd - spd.rolling(20).mean())/spd.rolling(20).std()
        #signal = (sh_quote.last_px / l_quote.last_px - 8.1117818275) * 200
#
        # # -----------------------------
        #
        # CONTEXT.my_data['signal'] = signal
        #
        # if CONTEXT.my_data['signal'] < -1:
        #     process_strat_signal(sh_sym, OrderDirection.BUY, 1, CONTEXT.my_data['quotes'][sh_sym].ap1)
        #     process_strat_signal(l_sym, OrderDirection.SELL, 1, CONTEXT.my_data['quotes'][l_sym].bp1)
        # elif CONTEXT.my_data['signal'] > 1:
        #     process_strat_signal(sh_sym, OrderDirection.SELL, 1, CONTEXT.my_data['quotes'][sh_sym].bp1)
        #     process_strat_signal(l_sym, OrderDirection.BUY, 1, CONTEXT.my_data['quotes'][l_sym].ap1)
        # elif CONTEXT.my_data['signal'] > 0.5 and (
        #         CONTEXT.short_position(sh_sym) > 0 or CONTEXT.long_position(l_sym) > 0):
        #     process_strat_signal(sh_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][sh_sym].ap1)
        #     process_strat_signal(l_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][l_sym].bp1)
        # elif CONTEXT.my_data['signal'] < -0.5 and (
        #         CONTEXT.long_position(sh_sym) > 0 or CONTEXT.short_position(l_sym) > 0):
        #     process_strat_signal(sh_sym, OrderDirection.SELL, 0, CONTEXT.my_data['quotes'][sh_sym].bp1)
        #     process_strat_signal(l_sym, OrderDirection.BUY, 0, CONTEXT.my_data['quotes'][l_sym].ap1)

    # 每隔00分钟 分别清空暂存的价格数据，防止影响后续计算。
    CONTEXT.count += 1
    CONTEXT.tick["px_20"] = []


def on_day_finish():
    """
    交易日结束，每个交易session结束时将被调用
    :return:
    """
    CONTEXT.print_order()  # 打印订单状态
    CONTEXT.log_order()  # 输出订单状态到日志
    CONTEXT.on_day_finish()  # 清空每天的变量 记录PnL


def on_sim_end():
    """
    回测结束, 所有回测完成之后调用
    :return:
    """
    df = pd.DataFrame()
    df['signal'] = CONTEXT.signals
    print 'to csv'
    df.to_csv('signal.csv')

    try:

        CONTEXT.plot_pnl_graph()  # 输出PnL的图
    except ImportError:
        print '*' * 60
        print 'Install matplotlib to plot PnL'
        print '*' * 60



def main():
    """
    main call: 本地模拟函数入口，只在本地Windows模拟下调用
    """
    # ==================策略配置项===================
    import os
    st1 = StratConfig.StratItem(os.path.splitext(os.path.basename(os.path.realpath(__file__)))[0],
                                stratid=-1)  # 新建策略：参数为策略名以及策略id

    # 订阅合约（可订阅多个）
    """
    合约配置格式：
    "Name|Rank(Main/2nd Main)|Exchange|FeedType|Maxpos(per order)|Account Number"
    """
    st1.contracts.append("hc|R1|SHFE|12|1|Account1")
    st1.contracts.append("rb|R1|SHFE|12|1|Account2")
    #
    # st1.contracts.append("cu|R1|SHFE|12|5|Account1")
    # st1.contracts.append("CU3M||LME|25|1|Account2")

    # 配置账户（支持多账户）
    """
    账户配置格式：
    "Name|Cash Amount|Currency"
    """
    st1.accounts.append("Account1|1000000|CNY")
    st1.accounts.append("Account2|1000000|CNY")

    st1.file_path = "config/"  # 配置策略读写路径
    st1.strat_param_file = "config/strat_param.txt"  # 配置策略参数文件


    # ===================回测主配置项===================
    cfg1 = StratConfig()  # 新建主配置文件
    cfg1.strat_item.append(st1.items())  # 讲策略添加到回测主配置中
    cfg1.start_date = 20170320  # 开始日期，日夜盘
    cfg1.end_date = 20170321  # 结束日期
    cfg1.begin_time = 90000000  # 开始时间
    cfg1.end_time = 150000000  # 结束时间（凌晨+24hrs）
    cfg1.day_night_flag = 0  # 日夜盘：日盘(0), 夜盘(1), 日夜盘连续(2)
    cfg1.flag_cross_day_position = True  # 设置是否带仓位到下一个session
    cfg1.time_interval = 60  # 定时器间隔(秒)
    cfg1.bar_interval = 0  # bar行情时间间隔(分钟), 数据库直接提取bar行情, 不订阅tick行情
    cfg1.quote_delay_type = 25
    cfg1.quote_delay_value = 3000
    # ===================执行回测任务===================
    python_execute_task(cfg1.tojson())




# =================DO NOT MODIFY BEYOND THIS POINT=================
# Main call
if __name__ == '__main__':
    main()

