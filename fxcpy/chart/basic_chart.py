import numpy as np
import matplotlib
matplotlib.rcParams.update({'font.size' : 8})
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

from mpl_finance import candlestick2_ohlc
from fxcpy.utils.date_utils import to_ole

class BasicChart(object):
    def __init__(self, market_data):
        self.market_data = market_data

    def exponential_average(self, values, window):
        weights = np.exp(np.linspace(-1.,0.,window))
        weights /= weights.sum()
        a = np.convolve(values.values, weights) [:len(values)]
        a[:window]=a[window]
        return a

    def macdfunc(self, idx, values, slow=26, fast=12):
        slow = self.exponential_average(values, slow)
        fast = self.exponential_average(values, fast)
        macd = pd.DataFrame(index=idx)
        macd['slow'] = slow
        macd['fast'] = fast
        macd['macd'] = fast-slow
        return macd

    def plot_macd_indicator(
        self, macd, ema, indices, macd_label, ax=None,
        spines_col='#5998ff', macdcolour='w',
        textsize=6, macdlabel='MACD'
    ):
        if ax is None:
            ax = plt.gca()
        ax.plot(indices, macd, 'r-')
        ax.plot(indices, ema, 'b-')
        ax.fill_between(indices, macd-ema,0, alpha=0.5, facecolor='w')
        ax.spines['top'].set_color(spines_col)
        ax.spines['bottom'].set_color(spines_col)
        ax.spines['left'].set_color(spines_col)
        ax.spines['right'].set_color(spines_col)
        ax.tick_params(axis='x', colors='w')
        ax.tick_params(axis='y', colors='w')
        ax.text(
            0.015, 0.90, macd_label, va='top', color='w',
            transform=ax.transAxes, fontsize=textsize)
        return ax

    def plot_price_chart(
        self, popen, phigh, plow, pclose, ax=None, spines_col='#5998ff'
    ):
        ax.grid(True, linestyle='--', linewidth=0.3)
        ax.yaxis.label.set_color('w')
        ax.spines['top'].set_color(spines_col)
        ax.spines['bottom'].set_color(spines_col)
        ax.spines['left'].set_color(spines_col)
        ax.spines['right'].set_color(spines_col)
        ax.tick_params(axis='x', colors='w')
        ax.tick_params(axis='y', colors='w')
        ax.get_xaxis().set_visible(False)
        candlestick2_ohlc(
            ax, popen, phigh, plow, pclose,
            width=1, colorup='#9eff15', colordown='#ff1717')
        return ax

    def _get_price_action(self, instrument, time_frame, dtfm, dtto):
        # Get the data
        data_gen = market_data.get_price_data(
            instrument,
            time_frame,
            to_ole(dtfm),
            to_ole(dtto)
        )
        data_list = list(data_gen)
        if len(data_list) > 1:
            d = np.concatenate(data_list)
            con_data = d[np.argsort(d['date'])]
        else:
            d = data_list[0]
            con_data = d[np.argsort(d['date'])]
        # Convert to Pandas
        pd_data = pd.DataFrame(con_data, index=con_data['date']).drop('date', axis=1)
        return pd_data
        
    def graph(self, instrument, time_frame, dtfm, dtto):
        """
        """
        fig = plt.figure(facecolor='#07000d')
        fig.clf()
        data =  self._get_price_action(instrument, time_frame, dtfm, dtto)
        date = data.index
        bidopen = data.bidopen
        bidhigh = data.bidhigh
        bidlow = data.bidlow
        bidclose = data.bidclose
        volume = data.volume
        # Date function
        def format_date(x, pos=None):
            thisind = np.clip(int(x + 0.5), 0, N - 1)
            return date[thisind].strftime('%Y-%m-%d %H:%M')
        N = len(date)
        indices = np.arange(len(date))
        # Indicators
        # MACD
        maslow = 26
        mafast = 12
        ema = 9
        macd_label = "MACD (%s, %s, %s)" % (maslow, mafast, ema)
        m = self.macdfunc(date, bidclose, maslow, mafast)
        macd = m.macd
        ema = self.exponential_average(macd, ema)
        # Define artists
        ax_ohlc = plt.subplot2grid(
            (6,4),(0,0), rowspan=5, colspan=4,facecolor='#07000d')
        ax_macd = plt.subplot2grid(
            (6,4), (5,0), sharex=ax_ohlc, rowspan=1,
            colspan=4, facecolor='#07000d')
        # Plot charts
        self.plot_price_chart(
            bidopen, bidhigh, bidlow, bidclose, ax=ax_ohlc)
        self.plot_macd_indicator(macd, ema, indices, macd_label, ax=ax_macd)
        # Tidy updates
        ax_macd.xaxis.set_major_formatter(mticker.FuncFormatter(format_date))
        for label in ax_macd.xaxis.get_ticklabels():
            label.set_rotation(45)  
        fig.autofmt_xdate()
        # Layout customistion
        plt.subplots_adjust(
            left=.10, bottom=.19, right=.93, top=.94, wspace=.20, hspace=.07)
        # Plot Labels 
        plt.suptitle(instrument+' Price Action', color='w')
        plt.ylabel('Price')
        # Legend
        plt.legend(loc=9, ncol=2, prop={'size':7}, fancybox=True, borderaxespad=0.)
        plt.show()
    

