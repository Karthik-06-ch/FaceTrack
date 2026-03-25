import plotly.express as px

def plot_attendance_trend(df):
    """Line chart for daily attendance over 30 days."""
    if df.empty:
        return px.line(title="No Data")
    fig = px.line(df, x='date', y='attendees', 
                  title='Daily Attendance Trend (Last 30 Days)',
                  markers=True)
    fig.update_layout(xaxis_title="Date", yaxis_title="Total Attendees", template='plotly_white')
    return fig

def plot_subject_attendance(df):
    """Bar chart for subject-wise participation."""
    if df.empty:
        return px.bar(title="No Data")
    fig = px.bar(df, x='subject', y='count', 
                 title='Total Attendance by Subject', 
                 color='subject')
    fig.update_layout(xaxis_title="Subject", yaxis_title="Count", template='plotly_white', showlegend=False)
    return fig

def plot_present_absent_pie(present_val, absent_val):
    if absent_val < 0:
        absent_val = 0
    df = {"Status": ["Present", "Absent"], "Count": [present_val, absent_val]}
    fig = px.pie(df, values="Count", names="Status", 
                 title="Est. Overall Present/Absent Ratio",
                 color="Status", 
                 color_discrete_map={"Present": "green", "Absent": "darkred"})
    return fig
