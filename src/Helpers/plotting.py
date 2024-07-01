from .dependencies import *

def plot_avrg_monthly_returns(average_returns_df: pd.DataFrame, factor_name: str) -> None:
    """
    Plot the average monthly returns for each decile.
    
    Args:
        average_returns_df (pd.DataFrame): A DataFrame with the average monthly returns for each decile.
        factor_name (str): Name of the factor being analyzed.
    """
    average_returns_df['avrg_ret'] *= 100
    average_returns_df.index = range(1, len(average_returns_df) + 1)

    plt.figure(figsize=(14, 6))
    bars = plt.bar(average_returns_df.index, average_returns_df['avrg_ret'], color='red', width=0.5)

    factor_name = factor_name.capitalize()
    plt.title(f'{factor_name} Strategy - Median Monatliche Rendite', fontweight='bold', fontsize=14)
    plt.xlabel('Dezil Faktor-Portfolio')
    plt.ylabel('Median Monatliche Rendite (%)')

    x_labels = [str(i) for i in average_returns_df.index]
    x_labels[0] = 'Low'
    x_labels[-1] = 'High'
    plt.xticks(ticks=average_returns_df.index, labels=x_labels, rotation=0)

    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))

    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.show()

def plot_cumulative_returns(cum_returns: pd.DataFrame, factor_name: str):
    """
    Plot the cumulative returns for each decile.
    
    Args:
    cumulative_returns_df (pd.DataFrame): A DataFrame with the cumulative returns for each decile.
    factor_name (str): The name of the factor.
    """

    cumulative_returns_df = cum_returns * 100
    
    plt.figure(figsize=(14, 6))
  
    cmap = plt.get_cmap('Reds')
    colors = cmap(np.linspace(0.3, 1, len(cumulative_returns_df.columns)))  
    
    for i, decile in enumerate(cumulative_returns_df.columns):
        if decile == 0:
            label = 'Low'
        elif decile == len(cumulative_returns_df.columns) - 1:
            label = 'High'
        else:
            label = f'Decile {int(decile)+1}'
        plt.plot(cumulative_returns_df.index, cumulative_returns_df[decile], label=label, color=colors[i])

    factor_name = factor_name.capitalize()
    plt.title(f'{factor_name} Strategie - Kumulative Rendite', fontweight='bold', fontsize=14)
    plt.ylabel('Kumulative Rendite (%)')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    legend = plt.legend(title='Dezil Faktor-Portfolios', loc='upper left', fontsize='medium', title_fontsize='medium', frameon=True, fancybox=True, framealpha=0.7)
    legend.get_frame().set_edgecolor('black')

    plt.tight_layout()
    plt.show()



def plot_avrg_annual_returns(annual_ret: pd.DataFrame, portfolio: str, factor: str) -> None:
    """
    Plot the annual returns of a specified portfolio ('Low' or 'High') and the S&P 500 portfolio side by side.
    """
    # Determine the portfolio column based on the input string
    portfolio_col = 0 if portfolio.lower() == 'low' else 9
    portfolio_name = 'Low Portfolio' if portfolio.lower() == 'low' else 'High Portfolio'

    # Extract years from DataFrame index for x-axis
    years = annual_ret.index.tolist()
    index = np.arange(len(years))
    
    # Create the bar chart
    plt.figure(figsize=(14, 6))
    bar_width = 0.35

    # Plot bars for the selected portfolio and the S&P 500
    bars1 = plt.bar(index, annual_ret[portfolio_col] * 100, bar_width, label=portfolio_name, color='red')
    bars2 = plt.bar(index + bar_width, annual_ret['sp500'] * 100, bar_width, label='S&P 500', color='#1f77b4')  # Darker blue

    # Add data labels
    for bars, offset in [(bars1, 0), (bars2, bar_width)]:
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    # Set labels, title, and legend
    factor = factor.capitalize()
    plt.ylabel('Jährliche Rendite (%)', fontsize=12)
    plt.title(f'Faktor-{factor}-{portfolio_name} vs. S&P 500 Jährliche Rendite', fontweight='bold', fontsize=14)
    plt.xticks(index + bar_width / 2, years, rotation=0, fontsize=10)
    
    plt.ylim(-60, 100)  # Set y-axis limits based on your data range

    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    legend = plt.legend(title='Portfolios', loc='upper left', fontsize='medium', title_fontsize='medium', frameon=True, fancybox=True, framealpha=0.7)
    legend.get_frame().set_edgecolor('black')
    
    plt.tight_layout()
    plt.show()

def plot_joint_pdf(returns_df: pd.DataFrame, factor: str) -> None:
    """
    Plot the joint PDFs of two portfolios and the benchmark returns in 3D, side by side.

    Args:
    returns_df (pd.DataFrame): DataFrame containing the daily returns with '0' and '9' as portfolios and 'sp500' as the benchmark.
    factor (str): The name of the factor to be displayed in the plot titles.
    """
    # Define the portfolio names
    portfolio_name1 = "Low"
    portfolio_name2 = "High"
    factor = factor.capitalize()

    def get_joint_pdf(ax, backtest_returns, benchmark_returns, portfolio_name, norm):
        # Transform to uniform distribution
        def transform_to_uniform(data):
            return (data.rank(method='first') / (len(data) + 1)).values

        # Prepare data for KDE
        backtest_data = transform_to_uniform(backtest_returns)
        benchmark_data = transform_to_uniform(benchmark_returns)
        joint_data = np.vstack((backtest_data, benchmark_data)).T

        # Fit KDE
        kde = KernelDensity(kernel='gaussian', bandwidth=0.1)
        kde.fit(joint_data)

        # Create grid for 3D plot
        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)
        X, Y = np.meshgrid(x, y)
        xy_grid = np.vstack([X.ravel(), Y.ravel()]).T
        densities = np.exp(kde.score_samples(xy_grid)).reshape(X.shape)

        # Plot in 3D
        surf = ax.plot_surface(X, Y, densities, cmap='coolwarm', edgecolor='none', norm=norm)
        ax.set_title(f'Joint PDF - {portfolio_name} Portfolio vs. S&P 500 ({factor})', fontweight='bold', fontsize=14)
        ax.set_xlabel(f'{portfolio_name} Rendite (Uniform)')
        ax.set_ylabel('S&P 500 Rendite (Uniform)')
        ax.set_zlabel('Density')
        ax.invert_yaxis()

        return densities

    # Ensure data alignment and remove NaNs
    returns_df = returns_df.dropna(subset=[0, 9, 'sp500'])

    # Extract the returns
    backtest_returns1 = returns_df[0]
    backtest_returns2 = returns_df[9]
    benchmark_returns = returns_df['sp500']

    # Create a GridSpec to manage layout
    fig = plt.figure(figsize=(20, 8))
    gs = GridSpec(1, 3, width_ratios=[1, 1, 0.05], wspace=0.3)

    # Initial plots to determine common z_max
    ax_temp1 = fig.add_subplot(gs[0], projection='3d')
    ax_temp2 = fig.add_subplot(gs[1], projection='3d')
    densities1 = get_joint_pdf(ax_temp1, backtest_returns1, benchmark_returns, portfolio_name1, norm=None)
    densities2 = get_joint_pdf(ax_temp2, backtest_returns2, benchmark_returns, portfolio_name2, norm=None)

    z_max = max(densities1.max(), densities2.max())
    norm = Normalize(vmin=0, vmax=z_max)

    # Clear temporary axes and replot with consistent normalization
    fig.clear()
    ax1 = fig.add_subplot(gs[0], projection='3d')
    ax2 = fig.add_subplot(gs[1], projection='3d')
    get_joint_pdf(ax1, backtest_returns1, benchmark_returns, portfolio_name1, norm)
    get_joint_pdf(ax2, backtest_returns2, benchmark_returns, portfolio_name2, norm)

    ax1.set_zlim(0, z_max)
    ax2.set_zlim(0, z_max)

    # Add a color bar for both plots
    cbar_ax = fig.add_subplot(gs[2])
    mappable = plt.cm.ScalarMappable(cmap='coolwarm', norm=norm)
    cbar = fig.colorbar(mappable, cax=cbar_ax)
    cbar.set_label('Density')

 
    plt.show()