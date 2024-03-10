from matplotlib import pyplot as plt


def plot_histogramh(series, title_text="",xlabel="",ylabel=""):
    plt.figure(figsize=(10, 6))
    plt.barh(series.index, series.values, color='skyblue')
    plt.title(title_text)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()  # Adjust layout to make room for the country names

    # Set the fontsize of the y-axis (country names) labels
    plt.gca().tick_params(axis='y', labelsize='small')  # 'small' is an example size

    plt.show()


def plot_histogram(series, title_text="",xlabel="",ylabel=""):
    plt.figure(figsize=(10, 6))
    plt.bar(series.index, series.values, color='skyblue')
    plt.title(title_text)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()  # Adjust layout to make room for the country names

    # Set the fontsize of the y-axis (country names) labels
    plt.gca().tick_params(axis='y', labelsize='small')  # 'small' is an example size

    plt.show()

