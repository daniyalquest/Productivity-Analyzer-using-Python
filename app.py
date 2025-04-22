import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the app
st.title("Productivity Analyzer")

# File upload for CSV input
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)
    
    # Show the uploaded data to the user
    st.subheader("Uploaded Data")
    st.write(data)

    # Convert Start Time and End Time columns to datetime format
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    data['End Time'] = pd.to_datetime(data['End Time'])
    
    # Calculate Duration in hours
    data['Duration'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

    # Categorize tasks into Work, Study, Break, Entertainment
    data['Category'] = data['Task Name'].apply(lambda x: 'Work' if 'work' in x.lower() else 
                                                 ('Study' if 'study' in x.lower() else 
                                                  ('Break' if 'break' in x.lower() else 'Entertainment')))

    # Group tasks by category and sum the duration
    category_duration = data.groupby('Category')['Duration'].sum().reset_index()
    
    # Calculate total work time vs non-productive time
    productive_time = category_duration[category_duration['Category'] == 'Work']['Duration'].sum()
    non_productive_time = category_duration[category_duration['Category'].isin(['Break', 'Entertainment'])]['Duration'].sum()

    # Find the most and least productive time slots
    data['Hour'] = data['Start Time'].dt.hour
    hourly_activity = data.groupby('Hour')['Duration'].sum().reset_index()
    
    most_productive_hour = hourly_activity.loc[hourly_activity['Duration'].idxmax()]
    least_productive_hour = hourly_activity.loc[hourly_activity['Duration'].idxmin()]

    # Display the results to the user
    st.subheader("Productivity Insights")
    st.write(f"Total Productive Time: {productive_time:.2f} hours")
    st.write(f"Total Non-Productive Time: {non_productive_time:.2f} hours")
    st.write(f"Most Productive Hour: {most_productive_hour['Hour']} with {most_productive_hour['Duration']:.2f} hours")
    st.write(f"Least Productive Hour: {least_productive_hour['Hour']} with {least_productive_hour['Duration']:.2f} hours")

    # Optional: Display a bar chart for time spent on each category
    st.subheader("Time Spent on Each Category")
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Category', y='Duration', data=category_duration, palette="Blues_d")
    plt.title('Time Spent on Each Category')
    plt.xlabel('Category')
    plt.ylabel('Duration (hours)')
    st.pyplot(plt)

    # Optional: Provide a summary report as HTML
    report = f"""
    <h1>Productivity Report</h1>
    <p>Total Productive Time: {productive_time:.2f} hours</p>
    <p>Total Non-Productive Time: {non_productive_time:.2f} hours</p>
    <p>Most Productive Hour: {most_productive_hour['Hour']} with {most_productive_hour['Duration']:.2f} hours</p>
    <p>Least Productive Hour: {least_productive_hour['Hour']} with {least_productive_hour['Duration']:.2f} hours</p>
    """
    st.subheader("Download Report")
    st.download_button(label="Download Report", data=report, file_name="productivity_report.html", mime="text/html")

else:
    st.info("Please upload a CSV file to get started.")
