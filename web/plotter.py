import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from helpers import timeit
import numpy as np
import seaborn as sns


@timeit
def plot(json_results, url, name_clean):
    results_ = {k: v for k, v in json_results[0].items()}

    def get_spectrum(spec, name, colors):
        spec = dict(zip(spec, range(len(spec))))
        y, x = list(
            zip(*sorted(filter(lambda kv: kv[0] in spec, results_.items()), key=lambda kv: spec[kv[0]])))
        make_fig(x, y, name, colors)

    # y, x = list(zip(*sorted(results_.items(), key=lambda kv: kv[1], reverse=True)))

    sns.set(style='whitegrid', font_scale=1.7)

    def label_cleaner(y):
        print(y)
        key = {
            'fakenews': 'fake news',
            'extremeright': 'extreme right',
            'extremeleft': 'extreme left',
            'veryhigh': 'very high veracity',
            'low': 'low veracity',
            'pro-science': 'pro science',
            'mixed': 'mixed veracity',
            'high': 'high veracity'
        }
        for label in y:
            for k, v in key.items():
                if label == k:
                    label = v.title()

            yield label.title()

    def make_fig(x, y, cat, colors='coolwarm_r'):

        y = list(label_cleaner(y))

        y_pos = np.arange(len(y))
        plt.figure(figsize=(8, 8))
        g = sns.barplot(y=y_pos, x=x, palette=colors, orient='h', saturation=.9)
        g.axes.set_xlim(0, max(results_.values()))

        plt.yticks(y_pos, y)

        plt.title('{} - {}'.format(url, cat))
        plt.savefig(
            './static/{}.png'.format(name_clean + '_' + cat), format='png', bbox_inches='tight', dpi=200)

    get_spectrum(
        ['extremeright', 'right', 'right-center', 'center', 'left-center', 'left',
         'extremeleft'], 'Political', 'coolwarm_r')

    get_spectrum(['veryhigh', 'high', 'mixed', 'low'], 'Accuracy', 'viridis')

    get_spectrum(['conspiracy', 'fakenews', 'propaganda', 'pro_science', 'hate'], 'Character', 'husl')
