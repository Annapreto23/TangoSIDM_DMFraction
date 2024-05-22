import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib import cm
from matplotlib import gridspec
from matplotlib.animation import FuncAnimation, ArtistAnimation, writers

# Plot parameters
params = {"font.size": 10, "font.family": "Times", "text.usetex": True, "figure.max_open_warning": 0}
plt.rcParams.update(params)
title_fontsize = 10


class PLOT_NN:
    def __init__(self, io, nn, xnames, ynames, dataname, N, xcols_string, sampling, score = None, epochs = None):
        self.dir = './plots/'
        self.outp = io.ycols[0]
        self.xnames = xnames
        self.ynames = ynames
        self.dataname = dataname
        self.N = N
        self.xcols_string = xcols_string
        self.sampling = sampling
        self.score = score
        if epochs == None:
            self.epochs = nn.epochs
        else:
            self.epochs = epochs
            
        self.orange = '#FF6500'
        self.blue = '#009DFF'
        self.pink = '#D300B0'
        self.green = '#77AA00'
        self.greenblue = '#1F91BF'

        self.title(io, ep=self.epochs, hnodes=list(filter(None, nn.h_nodes)), act=list(filter(None, nn.activation)), drop=list(filter(None, nn.dropout)), optim=nn.optimizer, b=nn.batch_size)

    def title(self, io, **kwargs):
        title = self.dataname
        self.legendtitle = 'None'
        self.plottitle = title + '\n'
        self.savetitle = self.dir + title + '_none'
        self.legendtitle = 'MSE = %.2e ; R$^2$ = %.3f'%tuple(self.score)
        for count, i in enumerate(kwargs):
            self.savetitle += '_' + str(i) + '=' + str(kwargs[i])
            self.plottitle += str(i) + ' = ' + str(kwargs[i])
            if (count%4 == 3 and count != len(kwargs) -1):
                self.plottitle += ' \n '
            else:
                self.plottitle += ' $\mid$ '

    def plot_learning_curve(self, history):
        val_nr = int(len(history.history)/2)
        vals = ('', 'val_')
        val_names = ('train', 'test')
        colors = (self.blue, self.orange)
        fig, ax = plt.subplots(2,1, squeeze=True, sharex=True)
        plt.suptitle(self.plottitle, fontsize=title_fontsize)
        for i in range(val_nr):
            ax[0].plot(history.epoch, history.history[vals[i]+'loss'], label=val_names[i], color=colors[i])
            ax[1].plot(history.epoch, history.history[vals[i]+'R_squared'], color=colors[i])
        ax[0].set_ylabel('MSE')   ; ax[0].set_xlim((0., np.amax(history.epoch)))
        ax[1].set_ylabel('$R^2$') ; ax[1].set_xlim((0., np.amax(history.epoch)))
        ax[1].set_xlabel('epoch')
        ax[0].legend()
        plt.savefig(self.savetitle+'_learning_rate.pdf')

    def plot_input_output(self, x, y, y_pred):
        fig, ax = plt.subplots(y.shape[1],x.shape[1], figsize=(4*x.shape[1],4*y.shape[1]), squeeze=True, sharey=True)
        fig.subplots_adjust(wspace=0, hspace=0)
        ax[0].set_ylabel(self.ynames[0])
        fig.suptitle(self.plottitle, fontsize=title_fontsize-1)
        for i, xname in enumerate(self.xnames):
            idx = np.argsort(x[:,i])
            x_sort = x[:,i][idx]
            y_sort = y_pred[idx]
            ax[i].plot(x[:,i], y, 'o', markersize=4., markerfacecolor=self.blue, mec='none', label='true')
            ax[i].plot(x_sort, y_sort, 'o', markersize=4., markerfacecolor=self.orange, mec='none', label='predict')
            ax[i].set_xlabel(xname)
        lg = plt.legend(title=self.legendtitle)
        lg.get_title().set_fontsize(10)
        plt.savefig(self.savetitle + '_'+self.outp+'.pdf')

    def plot_true_predict(self, y, y_pred):
        label, color, cmap = '', self.greenblue, 'Blues'
        plt.figure(figsize=(6,5))
        plt.title(self.plottitle, fontsize=10)
        plt.plot([np.min(y), np.max(y)], [np.min(y), np.max(y)], '--', dashes=(10,10), color='black', lw=.5)
        plt.scatter(y, y_pred, s=8., marker='o', color=color, edgecolor='none', zorder=1, label=label)
        plt.xlim((np.min(y), np.max(y)))
        plt.ylim((np.min(y), np.max(y)))
        plt.xlabel('true ' + self.ynames[0])
        plt.ylabel('predicted ' + self.ynames[0])
        lg = plt.legend(title=self.legendtitle)
        lg.get_title().set_fontsize(10)
        plt.savefig(self.savetitle+'_'+self.outp+'_test-predict'+'.pdf')

    def plot_output_error(self, y, y_pred, ylim=(-1, 1)):
        y = y.reshape(len(y),) ; y_pred = y_pred.reshape(len(y_pred),)
        label, color, cmap = '', self.greenblue, 'Blues'

        plt.figure(figsize=(6,5))
        plt.title(self.plottitle, fontsize=10)
        plt.plot([np.min(y), np.max(y)], [0.,0.], '--', dashes=(10,10), color='black', lw=.5)
        plt.scatter(y, y_pred - y, s=2., color=color, edgecolor='none', label=label)

        plt.xlabel('true ' + self.ynames[0])
        plt.ylabel('predicted ' + self.ynames[0] + ' - true ' + self.ynames[0])
        plt.ylim(ylim)
        lg = plt.legend(title=self.legendtitle)
        lg.get_title().set_fontsize(10)
        plt.savefig(self.savetitle+'_'+self.outp+'_error.pdf')

    def gif_input_output(self, x, y, Y_pred, epochs):
        fig, ax = plt.subplots(y.shape[1], x.shape[1], figsize=(4 * x.shape[1], 4 * y.shape[1]), squeeze=True, sharey=True)
        fig.subplots_adjust(wspace=0, hspace=0)

        ax[0].set_ylabel(self.ynames[0])
        fig.suptitle(self.plottitle, fontsize=title_fontsize)

        scatters = []
        for i, xname in enumerate(self.xnames):
            ax[i].plot(x[:,i], y, 'o', markersize=4., markerfacecolor=self.blue, mec='none', label='True')
            ax[i].set_xlabel(xname)

            idx = np.argsort(x[:,i])
            x_sort = x[:,i][idx]
            y_sort = Y_pred[0][idx]
            scatter, = ax[i].plot(x_sort, y_sort, 'o', markersize=4., markerfacecolor=self.orange, mec='none', label='predict')
            scatters.append(scatter)

        def update(n, scatters, x, Y_pred):
            for i, scatter in enumerate(scatters):
                idx = np.argsort(x[:,i])
                y_sort = Y_pred[n][idx]
                scatter.set_ydata(y_sort)
            # plt.legend(title= 'MSE = %.2g, $R^2$ = %.2g'%(mse[n], r2[n])+ ' epoch %s'%n)
            plt.legend(title='Epoch %s' % n)
            return scatters

        anim = FuncAnimation(fig, update, fargs = (scatters, x, Y_pred), frames = np.arange(epochs), save_count=20, interval=1000)
        anim.save(self.savetitle+'.gif', dpi=300)

