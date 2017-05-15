import matplotlib.pyplot as plt
import numpy as np

hour = 1
day  = 24 * hour
week = 7 * day
month = 4 * week

time_points = ['begin msc (04/15)*', 'end msc (05/16)*', 'first prototype (12/16)', 'now (05/17)']#, 'optimal-projection']

ratio_padded_to_sample_d = float(15000 * 7500 * 2300) / (3000 * 3000 * 200)

feats_bmsc  = week * ratio_padded_to_sample_d
feats_emsc  = 2.5 * hour * ratio_padded_to_sample_d
feats_first = 37 * hour
feats_now   = 27 * hour

t_feats = np.array([feats_bmsc,feats_emsc,feats_first,feats_now])

mc_bmsc = week * ratio_padded_to_sample_d
mc_emsc  = 8 * ratio_padded_to_sample_d * hour
mc_first = 26 * hour
mc_now   = 15 * hour

t_mc     = np.array([mc_bmsc,mc_emsc,mc_first,mc_now])

t_tot = t_feats + t_mc


def plot_bars():

    width = 0.35
    ind = np.arange(len(t_tot), dtype = 'uint32' )
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, t_feats, width)
    rects2 = ax.bar(ind + width, t_mc, width)

    ax.set_ylabel('Runtime [hrs]')
    ax.set_yscale('log')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(time_points)

    ax.legend([rects1[0], rects2[0]], ["Features + Problem Construction","Solving Multicut"])
    ax.set_title("Runtimes Sample D")

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)

    plt.show()


if __name__ == '__main__':
    plot_bars()
