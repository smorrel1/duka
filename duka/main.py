#!/usr/bin/env python3.5

import argparse
import os, time
from datetime import date, timedelta

from duka.app import app
from duka.core import valid_date, set_up_signals
from duka.core.utils import valid_timeframe, TimeFrame

VERSION = '0.2.1'


def main():
    parser = argparse.ArgumentParser(prog='duka', usage='%(prog)s [options]')
    parser.add_argument('-v', '--version', action='version',
                        version='Version: %(prog)s-{version}'.format(version=VERSION))
    parser.add_argument('symbols', metavar='SYMBOLS', type=str, nargs='+',
                        help='symbol list using format EURUSD EURGBP')
    parser.add_argument('-d', '--day', type=valid_date, help='specific day format YYYY-MM-DD (default today)',
                        default=date.today() - timedelta(1))
    parser.add_argument('-s', '--startdate', type=valid_date, help='start date format YYYY-MM-DD (default today)')
    parser.add_argument('-e', '--enddate', type=valid_date, help='end date format YYYY-MM-DD (default today)')
    parser.add_argument('-t', '--thread', type=int, help='number of threads (default 20)', default=5)
    parser.add_argument('-f', '--folder', type=str, help='destination folder (default .)', default='.')
    parser.add_argument('-c', '--candle', type=valid_timeframe,
                        help='use candles instead of ticks. Accepted values M1 M2 M5 M10 M15 M30 H1 H4',
                        default=TimeFrame.TICK)
    parser.add_argument('--header', action='store_true', help='include CSV header (default false)', default=False)
    args = parser.parse_args()

    if args.startdate is not None:
        start = args.startdate
    else:
        start = args.day

    if args.enddate is not None:
        end = args.enddate
    else:
        end = args.day

    set_up_signals()
    print(args.symbols, start, end, args.thread, args.candle, args.folder, args.header)
    app(args.symbols, start, end, args.thread, args.candle, args.folder, args.header)

def main_batch_download():
    '''Download tick series one day at a time.'''
    #  date formats:    website download page   yyyy/mm/dd
    #                   url's                   yyyy/
    #                   python                  yyy/mm/dd
    print('Starting download')
    set_up_signals()
    symbols = ['USDJPY', 'EURUSD', 'GBPUSD']  # first run from Mac, starting 2003, 5, 4, and PC1 stating 2010
    # symbols = ['GBPJPY', 'EURJPY', 'AUDUSD', 'NZDUSD']  # from PC1, starting 2003, 8, 03
    # symbols = ['EURAUD', 'EURNZD', 'GBPAUD', 'EURCAD', 'CADJPY', 'USDCAD', 'GBPCHF', 'NZDCAD', 'EURCHF', 'EURGBP', 'AUDCHF', 'NZDJPY', 'AUDJPY', 'CHFJPY', 'GBPCAD', 'AUDCAD', 'USDCHF', 'GBPNZD']  # not started yet
    # start = date(2003, 5, 4)  # y m d from Mac
    start = date(2010, 1, 1)  # y m d from PC1
    # start = date(2003, 8, 3)  # y m d for GBPJPY group
    # start = date(2003, 12, 7)  # y m d
    # start = date(2004, 4, 25)  # y m d
    # start = date(2004, 9, 26)  # y m d
    for i in range(0, (date.today()-start).days, 7):
        new_start = start + timedelta(days=i)
        end = new_start + timedelta(days=6)
        thread = 25
        candle = TimeFrame.TICK
        folder = '/Volumes/SDcard/' if os.getenv('HOME') == '/Users/stephenmorrell' else '/home/smorrell/'
        folder += 'ForexDataDukas/'
        print('calling app with', symbols, new_start, end, thread, candle, folder, True)
        app(symbols, new_start, end, thread, candle, folder, True)
        if i%(7*4*4) == 0 and i > 0:  # pause every 4 months in case of throttling
            print('sleeping for 5 mins', time.time())
            time.sleep(300)


if __name__ == '__main__':
    if 0:
        main()
    else:
        main_batch_download()

