import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = df = pd.read_csv('medical_examination.csv')

# 2
df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2 > 25).astype(int)
#astype(int) converte para true or false diretamente

# 3
df['cholesterol'] = np.where(df['cholesterol']>1, 1,0)
df['gluc'] = np.where(df['gluc']>1, 1,0)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df,id_vars=['cardio'], value_vars=['cholesterol','gluc', 'smoke','alco', 'active', 'overweight'])

    # 6
    df_cat = None
    # Create DataFrame for categorical plot
    df_cat = pd.melt(df, id_vars=['cardio'],  # Variável de agrupamento
                 value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],
                 var_name='variable', 
                 value_name='value')


    # 7
    # 1. Convert the data into long format using pd.melt()
    df_cat = pd.melt(df, 
                 id_vars=['cardio'],
                 value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],
                 var_name='variable',
                 value_name='value')

# 2. Group and count the values
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

# 3. Create the categorical plot
    cat_plot = sns.catplot(x='variable', 
                       y='total', 
                       hue='value', 
                       col='cardio',
                       data=df_cat, 
                       kind='bar',
                       height=5, 
                       aspect=1.2)

    # 4. Customize the plot (optional but recommended)
    cat_plot.set_axis_labels('Variable', 'Total Count')
    cat_plot.set_titles('Cardio: {col_name}')


    # 8
    fig = cat_plot.fig

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df.copy()
    df_heat = df_heat[
    (df_heat['ap_lo'] <= df_heat['ap_hi']) &  # Diastolic <= Systolic
    (df_heat['height'] >= df_heat['height'].quantile(0.025)) &  # Height >= 2.5th percentile
    (df_heat['height'] <= df_heat['height'].quantile(0.975)) &  # Height <= 97.5th percentile
    (df_heat['weight'] >= df_heat['weight'].quantile(0.025)) &  # Weight >= 2.5th percentile
    (df_heat['weight'] <= df_heat['weight'].quantile(0.975))    # Weight <= 97.5th percentile
    ]
    # 12
    corr = df_heat.corr()

    # 13
    mask = mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14
    # Professional figure setup
    fig, ax = plt.subplots(figsize=(12, 10))

    # Set figure background and styling
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(1.0)

    # Set axis background
    ax.set_facecolor('white')

    # Adjust subplot parameters
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95)

    # 15
    # Plot the correlation matrix with the mask
    sns.heatmap(corr, 
                mask=mask,
                annot=True, 
                fmt=".2f", 
                cmap='coolwarm',
                center=0,
                square=True, 
                linewidths=0.5,
                cbar_kws={"shrink": 0.8},
                ax=ax)

    # Customize the plot
    ax.set_title('Correlation Matrix Heatmap', fontsize=16, pad=20)
    ax.tick_params(axis='both', which='major', labelsize=10)

    # 16
    fig.savefig('heatmap.png')
    return fig
