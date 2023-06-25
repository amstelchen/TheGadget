import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import datetime
from datetime import datetime
from utils import Data
import pandas as pd

resources_path = os.path.join(os.path.dirname(__file__), 'resources')
data_file = os.path.join(resources_path, 'database', "TheGadget" + ".db")
loader = Data(data_file)
dates_data = loader.load_table_data("Dates", "ORDER BY event_date")

df = pd.DataFrame(dates_data)
df['date_column'] = pd.to_datetime(df[1])

# Extract year and week from the 'date_column'
df['year'] = df['date_column'].dt.isocalendar().year
df['week'] = df['date_column'].dt.isocalendar().week

# Group the data by year and week
grouped = df.groupby(['year', 'week']).size().reset_index(name='count')

# Plot the scatter plot
fig, ax = plt.subplots()
ax.scatter(grouped['week'], grouped['year'], s=grouped['count'] * 10, alpha=1, marker='s')

# Set labels and title
ax.set_xlabel('Week')
ax.set_ylabel('Year')
ax.set_title('Events by years and weeks')

# Display the plot
plt.show()
