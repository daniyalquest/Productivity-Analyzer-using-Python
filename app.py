import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv("tasks.csv")

# Categorize tasks
data['Category'] = data['Task Name'].apply(
    lambda x: 'Work' if 'work' in x.lower() else (
        'Study' if 'study' in x.lower() else (
            'Break' if 'break' in x.lower() else 'Entertainment'
        )
    )
)

# Convert time columns to datetime and calculate duration
data['Start Time'] = pd.to_datetime(data['Start Time'])
data['End Time'] = pd.to_datetime(data['End Time'])
data['Duration'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

# Group by category and calculate total duration
category_duration = data.groupby('Category')['Duration'].sum().reset_index()

# Calculate productive and non-productive time
productive_time = category_duration[category_duration['Category'] == 'Work']['Duration'].sum()
non_productive_time = category_duration[
    category_duration['Category'].isin(['Break', 'Entertainment'])
]['Duration'].sum()

# Analyze hourly activity
data['Hour'] = data['Start Time'].dt.hour
hourly_activity = data.groupby('Hour')['Duration'].sum().reset_index()

# Find most and least productive hours
most_productive_hour = hourly_activity.loc[hourly_activity['Duration'].idxmax()]
least_productive_hour = hourly_activity.loc[hourly_activity['Duration'].idxmin()]

# Print summary
print(f"Total Productive Time: {productive_time} hours")
print(f"Total Non-Productive Time: {non_productive_time} hours")
print(f"Most Productive Hour: {most_productive_hour['Hour']} with {most_productive_hour['Duration']} hours")
print(f"Least Productive Hour: {least_productive_hour['Hour']} with {least_productive_hour['Duration']} hours")

# Plot time spent on each category
sns.barplot(x='Category', y='Duration', data=category_duration)
plt.title('Time Spent on Each Category')
plt.xlabel('Category')
plt.ylabel('Duration (hours)')
plt.show()

# Generate HTML report
report = f"""
<h1>Productivity Report</h1>
<p>Total Productive Time: {productive_time} hours</p>
<p>Total Non-Productive Time: {non_productive_time} hours</p>
<p>Most Productive Hour: {most_productive_hour['Hour']} with {most_productive_hour['Duration']} hours</p>
<p>Least Productive Hour: {least_productive_hour['Hour']} with {least_productive_hour['Duration']} hours</p>
"""
with open("productivity_report.html", "w") as file:
    file.write(report)