import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
import datetime
import itertools
from datetime import datetime, date
from utils import Data
import pandas as pd
import numpy as np
from io import StringIO
from textwrap import wrap

resources_path = os.path.join(os.path.dirname(__file__), 'resources')
data_file = os.path.join(resources_path, 'database', "TheGadget" + ".db")
loader = Data(data_file)
dates_data = loader.load_table_data("Dates", "ORDER BY event_date")


def plot_events():
    df = pd.DataFrame(dates_data)
    df['date_column'] = pd.to_datetime(df[1])

    # Extract year and week from the 'date_column'
    df['year'] = df['date_column'].dt.isocalendar().year
    df['week'] = df['date_column'].dt.isocalendar().week

    # Group the data by year and week
    grouped = df.groupby(['year', 'week']).size().reset_index(name='count')

    # Plot the scatter plot
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.suptitle('Events by years and weeks'
    .upper(), fontsize=12, font='Courier New', weight='bold')
    # fig, ax = plt.subplots()
    ax.scatter(grouped['week'], grouped['year'], s=grouped['count'] * 10, alpha=1, marker='s')

    # Set labels and title
    ax.set_xlabel('Week')
    ax.set_ylabel('Year')
    # ax.set_title('Events by years and weeks')

    # Display the plot

    plt.show()

def plot_monthly_costs():
    # source: https://blog.nuclearsecrecy.com/2015/06/12/what-remains-of-the-manhattan-project/
    # Monthly costs of the Manhattan Project, 1943 through 1946. From the Manhattan District 
    # History, Volume 5, Appendix A.

    fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
    df = pd.read_csv(os.path.join(resources_path, "database", "expenses.txt"), sep='\t', index_col=0, names=['date', 'amount'], header=None, skipinitialspace = True)
    df = df.replace({'\$': '', ',': ''}, regex=True)
    # df[1] = df[1].to_datetime()
    #df.index = pd.DatetimeIndex(df.index)

    df['date_txt'] = df.index.astype(str)
    df['date_neu'] = pd.DatetimeIndex(df.index) #, freq="-1MS")
    #print(df)
    #df.index = pd.to_datetime(df.index)
    #ind = np.arange(len(df)) 
    #t = df.index
    df['amount'] = df['amount'].astype(int) // 1000
    
    interval = 31 * df.index
    y_pos = np.arange(len(df))
    #print(df)
    #print(df.dtypes)
    # fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    #plt.xticks(y_pos, y)
    #plt.gca().invert_yaxis()
    #ax.set_ylim(ax.get_ylim()[::-1])
    #ax.set_xticks(np.arange(0, 125 + 5, 5))
    #ax[0].tick_params(labeltop=True, labelright=True)
    ax.set_ylim([0, 125])
    ax.set_ylabel('Millions of Dollars', fontsize=12, font='Courier New', weight='bold')
    ax.set_yticks(np.arange(0, 125 + 5, 5))
    ax.set_xticks(df['date_neu']) # .astype(dtype='datetime64[ns]'))
    
    plt.xticks(rotation=90)
    plt.grid(axis='both', which='major', zorder=5)
    plt.grid(axis='x', which='major', ds='steps-post')
    plt.grid(axis='y', which='major', ds='steps')
    ax.tick_params(which='both', width=0)
    ax.grid(ls="solid")

    # Define the date format
    date_form = DateFormatter("%m-%y")
    ax.xaxis.set_major_formatter(date_form)

    #ax.tick_params(which='major', length=0, color='b')
    #ax.tick_params(which='minor', length=10, color='r')
    #ax.grid(zorder=-4.0)
    #ax.set_axisbelow(True)
    ax.bar(df['date_neu'], width=25, height=df['amount'], color='black')
    plt.plot([], [], ' ', label="""
    Manhattan District        
           ——————
      actual monthly    
       expenditures    \n
                                plate b    """
    .upper())
    fig.legend(loc="outside lower right", fontsize=12, edgecolor='black')
    #ax.plot(df['date_neu'], df['amount'])
    #ax.xaxis_date()
    #plt.text(400, 100, "bfgsdfgdfgsdfgla", in_layout=False)
    # place a text box in upper left in axes coords
    textstr = "note: total expenditure\n           as of 31 dec. 1942\n           was 16 millions.".upper()
    props = dict(boxstyle='square', edgecolor='black', facecolor='white', alpha=1)
    plt.text(0.025, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    ax1 = ax.twinx()
    ax1.set_ylim(ax.get_ylim())
    ax1.set_yticks(np.arange(0, 125 + 5, 5))
    
    plt.show()

def plot_age_distribution():
    # source: https://blog.nuclearsecrecy.com/2015/06/12/what-remains-of-the-manhattan-project/
    # Age distribution at Los Alamos, May 1945. Top graph is total civilian personnel, bottom is 
    # scientific employees only. 
    # Keep in mind this was 70 years ago, so anyone in their 20s then would be in their 90s now. 
    # Source: Manhattan District History, Book 8, Volume 2, Appendix, Graph 1.
    pass

def plot_employment_by_month():
    # source: https://blog.nuclearsecrecy.com/2013/11/01/many-people-worked-manhattan-project/
    # This report has two very interesting graphs in it. The first is this one, showing total 
    # employment by month, broken into the various important Manhattan Project categories:
    pass

def plot_hires_and_terminations():
    # source: https://blog.nuclearsecrecy.com/2013/11/01/many-people-worked-manhattan-project/
    # Digging around a bit more in the aforementioned personnel statistics of the Manhattan 
    # Project (a thrilling read, I assure you), I found this rather amazing graph of the total 
    # number of hires and terminations by the project:

    fig, ax = plt.subplots(figsize=(10, 10))
    fig.suptitle('''
    Manhattan District Contractors\n \
    Hires and Terminations\n \
    through 31 Decemver 1946'''
    .upper(), fontsize=12, fontfamily='Domino Mask', weight='bold')

    clinton = [400, 380, 180, 160, 220, 215]
    hanford = [130, 90, 20, 10, 110, 80]
    other = [60, 70, 100, 80, 30, 20]

    #diff = list(set(hanford) - set(other))
    diff = [sum(x) for x in zip(clinton, hanford)]

    N = 6
    X = np.arange(N)
    #menMeans = (20, 35, 30, 35, 27)
    #womenMeans = (25, 32, 34, 20, 25)
    ind = np.arange(N) # the x locations for the groups
    width = 0.35
    # fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])

    ax.bar(ind, clinton, width=0.25, color='black', edgecolor='black')
    ax.bar(ind, hanford, width=0.25, bottom=clinton, color='gray', hatch='.', edgecolor='black')
    ax.bar(ind, other, width=0.25, bottom=diff, color='gray', hatch='x', edgecolor='black')
    #ax.bar(ind, data[0], width=0.25, bottom=580, color='trans', edgecolor='white')

    #ax.bar(ind + 0.30, clinton, width=0.25, color='black')
    #ax.bar(ind + 0.30, clinton, width=0.25, bottom=clinton, color='gray', hatch='.', edgecolor='black')
    #ax.bar(ind + 0.30, clinton, width=0.25, bottom=hanford, color='gray', hatch='x', edgecolor='black')
    #ax.bar(ind + 0.30, data[1], width=0.25, bottom=570, color='white', edgecolor='white')

    #ax.bar(ind + 2.00, data[0], width = 0.25, color='black')
    #ax.bar(ind + 2.00, data[0], width=0.25, bottom=400, color='gray', hatch='.', edgecolor='black')
    #ax.bar(ind + 2.00, data[0], width=0.25, bottom=540, color='gray', hatch='x', edgecolor='black')

    #ax.bar(ind + 0.25, data[1], width = 0.25)
    #ax.bar(ind + 0.50, data[2], width = 0.25)
    #ax.bar(ind, 10, width=0.25, color='r')

    H_T = ['Hires\n', 'Termi-\nnations']
    ticks = ['total', 'Operations \n& Research', 'Design & \nConstruction']
    labels = ['Clinton Eng. Works', 'Hanford Eng. Works', 'All Other Areas']
    #ticks += ticks
    #labels = zip(H_T, ticks)
    #ticks = itertools.product(H_T, ticks)
    all_ticks = [y+'\n'+x.upper() for x in ticks for y in H_T]

    ax.set_axisbelow(True)
    plt.grid(axis='y', which='major', zorder=-1.0)

    ax.set_ylim([0, 640])
    ax.set_ylabel('Thousands')
    #ax.set_title('bla')
    ax.set_xticks(ind, all_ticks)
    ax.set_yticks(np.arange(0, 640 + 1, 40))

    ax1 = ax.twinx()
    ax1.set_ylim(ax.get_ylim())
    ax1.set_yticks(ax.get_yticks())

    #ax.legend(labels=['Hires', 'Termin'])
    ax.legend(labels=labels, loc="upper right", fontsize=12, edgecolor='black', bbox_to_anchor=(0.9, 0.9))
    handles, labels = ax.get_legend_handles_labels()
    #ax.legend(handles, labels, title='Line', loc='upper left')

    plt.tight_layout()
    plt.show()


def plot_personnel_and_expenses():
    # source: https://ethos.lps.library.cmu.edu/article/id/22/
    pass

def plot_main_sites():
    # source: http://www.smithdray1.net/k25heritage/savek25.htm
    fig, ax = plt.subplots(figsize=(10, 7))
    #fig = plt.figure()
    #ax = fig.add_axes([0,0,1,1])
    fig.suptitle('Manhattan Project sites'.upper(), fontsize=12, font='Courier New', weight='bold')
    #ax.axis('equal')
    projects = ['Oak Ridge', 'Los Alamos', 'Hanford', 'R&D Universities', 'SpecOp Materials', 'Govt Overhead', 'Hvy. Water Plants', 'Other']
    millions = [1188.352, 74.055, 390.124, 69.681, 103.369, 37.255, 26.768, 124]
    explode = [0.2 for x in range(8)]
    # explode.append(0.5)
    # explode.insert(0, 0.5)

    def absolute_value(val):
        a  = np.round(val/100.*sum(millions), 0)
        return str(a) + '\nbn US$'

    ax.pie(millions, labels = projects, autopct=absolute_value, explode=explode)
    plt.show()

def plot_y12_vs_k25():
    # source: http://www.smithdray1.net/k25heritage/savek25.htm
    # data taken from: https://blog.nuclearsecrecy.com/2013/05/17/the-price-of-the-manhattan-project/
    fig, ax = plt.subplots(figsize=(10, 7))
    #fig = plt.figure()
    #ax = fig.add_axes([0,0,1,1])
    fig.suptitle('Oak Ridge site expenses'.upper(), fontsize=12, font='Courier New', weight='bold')
    # ax.axis('equal')
    data_oak_ridge = StringIO("""K-25 Gaseous Diffusion Plant 	$512,166,000 	$8,150,000,000 	27%
        Y-12 Electromagnetic Plant 	$477,631,000 	$7,600,000,000 	25%
        Clinton Engineer Works, HQ and central utilities 	$155,951,000 	$2,480,000,000 	8%
        Clinton Laboratories 	$26,932,000 	$430,000,000 	1%
        S-50 Thermal Diffusion Plant 	$15,672,000 	$250,000,000 	1%""")

    data_all = StringIO("""OAK RIDGE (Total) 	$1,188,352,000 	$18,900,000,000 	63%
        —K-25 Gaseous Diffusion Plant 	$512,166,000 	$8,150,000,000 	27%
        —Y-12 Electromagnetic Plant 	$477,631,000 	$7,600,000,000 	25%
        —Clinton Engineer Works, HQ and central utilities 	$155,951,000 	$2,480,000,000 	8%
        —Clinton Laboratories 	$26,932,000 	$430,000,000 	1%
        —S-50 Thermal Diffusion Plant 	$15,672,000 	$250,000,000 	1%
        HANFORD ENGINEER WORKS 	$390,124,000 	$6,200,000,000 	21%
        SPECIAL OPERATING MATERIALS 	$103,369,000 	$1,640,000,000 	5%
        LOS ALAMOS PROJECT 	$74,055,000 	$1,180,000,000 	4%
        RESEARCH AND DEVELOPMENT 	$69,681,000 	$1,110,000,000 	4%
        GOVERNMENT OVERHEAD 	$37,255,000 	$590,000,000 	2%
        HEAVY WATER PLANTS 	$26,768,000 	$430,000,000 	1%""")

    #data = data.split('\n').split('\t')
    df_oak_ridge = pd.read_csv(data_oak_ridge, sep='\t', index_col=0, header=None, skipinitialspace = True)
    df_data_all = pd.read_csv(data_all, sep='\t', index_col=0, header=None, skipinitialspace = True)

    df_oak_ridge = df_oak_ridge.replace({'\$': '', ',': ''}, regex=True)
    df_data_all = df_data_all.replace({'\$': '', ',': ''}, regex=True)

    df_oak_ridge[1] = ['\n'.join(wrap(x, 12)) for x in  df_oak_ridge[1]]
    #df_data_all[1] = ['\n'.join(wrap(x, 12)) for x in  df_data_all[1]]
    df_data_all = df_data_all[~df_data_all.index.str.contains('—|B')]
    df_data_all[1] = df_data_all[1].astype(int) // 1e6
    df_data_all = df_data_all.iloc[::-1]
    #print(df_oak_ridge)
    print(df_data_all)

    # pie chart as of smithdray1.net:
    #ax.pie(df_oak_ridge[1], labels = df_oak_ridge.index, autopct='%1.2f%%', startangle=-25)

    # hbar as of nuclearsecrecy.com:
    ind = np.arange(7)
    all_ticks = ind
    #ax.set_xticks(ind, all_ticks)
    #ax.set_xlim([26768000, 1188352000])
    ax.set_xlabel('Millions of 1945 US dollars', fontsize=12, font='Courier New', weight='bold')
    colors=['#557b43', '#42688a', '#46a2aa', '#ee8d35', '#f1bb67', '#d45a59', '#428dcc']
    colors.reverse()

    plt.grid(axis='both', which='major', zorder=5)
    plt.grid(axis='x', which='major', ds='steps-post')
    plt.grid(axis='y', which='major', ds='steps')
    #ax.tick_params(which='both', width=0)
    #ax.grid(ls="solid")

    ax.barh(df_data_all.index, width=df_data_all[1], height=0.35, color=colors)
    ax.set_xticks([0, 75, 150, 300, 450, 600, 750, 900, 1050, 1200])

    plt.tight_layout()
    plt.show()


# plot_events()
# plot_main_sites()
#plot_y12_vs_k25()
# plot_monthly_costs()
# plot_hires_and_terminations()

