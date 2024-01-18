import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col=['date'])

# Clean data
df = df[(df['value'] >= df['value'].quantile(.025)) &
(df['value'] <= df['value'].quantile(.975))]


def draw_line_plot():
    # Draw line plot
    df_lplot = df.copy(deep=True)
    fig, ax = plt.subplots(figsize=(16, 4), layout='constrained')
    ax.plot(df_lplot['value'])
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', weight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy(deep=True)
    df_bar = df_bar.reset_index()
    df_bar.dtypes
    df_bar['Years'] = df_bar['date'].dt.year
    df_bar['Months'] = df_bar['date'].dt.month_name()
    df_bar.drop(columns=['date'], inplace=True)
    df_bar = df_bar.groupby(['Years', 'Months'], as_index=False, sort=False)['value'].mean()
    df_bar = df_bar.pivot_table(index='Years', columns='Months', values='value', sort=False)
  
    # Draw bar plot
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    labels_indx = np.arange(len(labels)) #list(range(len(labels)))
    df_bar = df_bar.reindex(columns=labels)
    x = df_bar.index
    x_indx = np.arange(len(x))
    bar_width = 0.05

    fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    for i in labels_indx:
      ax.bar(x_indx + (i * bar_width), df_bar.loc[2016:2019, labels[i]].values, width=bar_width, label=labels[i])
    ax.legend(loc=2, title='Months')
    ax.set_xticks(x_indx + 5.5*bar_width, x, rotation=90)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy(deep=True)
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2, figsize=(16, 8), layout='constrained')
    sns.boxplot(x=df_box['year'], y=df_box['value'], hue=df_box['year'], palette='icefire', legend=False ,ax=axs[0])
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')
    axs[0].set_ylim(0, 200000)
    axs[0].set_yticks(np.arange(0, 220000, 20000))

    sns.boxplot(x=df_box['month'], y=df_box['value'],
      hue=df_box['month'], legend=False, 
      order=['Jan', 'Feb', 'Mar', 'Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ax=axs[1])
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')
    axs[1].set_ylim(0, 200000)
    axs[1].set_yticks(np.arange(0, 220000, 20000))

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
