import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


class Dataprocessing:
    """A class for processing data.
    Parameters:
    df (pandas.DataFrame): The input dataframe to be processed.
    """

    def __init__(self, df):
        """Initializes a new instance of the DataProcessing class.
        Parameters:
        df (pandas.DataFrame): The input dataframe to be processed.
        """
        self.df = df

    def preprocessing(self):
        """Preprocesses the data by performing various operations such as dropping duplicates,
        sorting by time, setting time as index, adding additional time-related columns,
        and selecting specific columns.
        Returns:
            pandas.DataFrame: The preprocessed dataframe.
        """
        self.df = self.df.drop_duplicates()
        self.df = self.df.sort_values('time', ascending=True).reset_index(drop=False)
        self.df = self.df.sort_values('time').set_index('time')
        self.df.index = pd.to_datetime(self.df.index).tz_localize('Europe/Helsinki')
        self.df['day'] = self.df.index.day
        self.df['hour'] = self.df.index.hour
        self.df['dayofweek'] = self.df.index.dayofweek
        self.df['month'] = self.df.index.month
        df_processing = self.df[['id', 'lat', 'lon', 'operator', 'power', 'rangeLeft', 'txt_code',
                                 'last_lat', 'last_lon', 'distanceTravelled', 'day', 'hour', 'dayofweek', 'month']]
        return df_processing

    def distance_traveld_discover(self, column_name):
        """Calculate the total distance traveled for each unique value in the specified column.
        Parameters:
        column_name (str): The name of the column to group by.
        Returns:
        pandas.Series: A Series object containing the total distance traveled for each unique value in the specified column.
        """
        df_distance_discover = self.df.groupby(column_name).count()['distanceTravelled']
        return df_distance_discover

    def distance_traveld_discover(self, column_name):
        """Calculate the total distance traveled for each unique value in the specified column.
        Parameters:
        column_name (str): The name of the column to group by.
        Returns:
        pandas.Series: A Series object containing the total distance traveled for each unique value in the specified column.
        """
        df_distance_discover = self.df.groupby(column_name).count()['distanceTravelled']
        return df_distance_discover

    def distance_traveld_discover(self, column_name):
        """Calculate the total distance traveled for each unique value in the specified column.
        Parameters:
        column_name (str): The name of the column to group by.
        Returns:
        pandas.Series: A Series object containing the total distance traveled for each unique value in the specified column.
        """
        df_distance_discover = self.df.groupby(column_name).count()['distanceTravelled']
        return df_distance_discover

    def distance_traveld_discover(self, column_name):
        df_distance_discover = self.df.groupby(column_name).count()['distanceTravelled']
        return df_distance_discover

    def plot_distance_traveled_per_operator(self, df_distance_discover):
        try:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_distance_discover.index, y=df_distance_discover.values))
            fig.update_layout(
                xaxis_title='operator', yaxis_title="Distance Traveled",
                title="Distance Traveled per Operator")
            return fig.show()
        except Exception as e:
            print('Error:', str(e))

    def plot_distance_taveled_day_of_week(self, df_processing):
        df = df_processing.groupby(['dayofweek', 'operator'])[
            'distanceTravelled'].sum().reset_index()
        fig = px.bar(df, x='dayofweek', y='distanceTravelled', color='operator', barmode='group',
                     title='Total Distance Travelled by Day of Week and Operator')
        return fig.show()

    def plot_distance_mean(self, df_processing, scale):
        try:
            if scale in ['hour', 'dayofweek']:
                hu = pd.DataFrame(df_processing.groupby(
                    [scale, 'operator'])['distanceTravelled'].mean())
            return sns.displot(hu, x="distanceTravelled", kind="kde")
        except:
            return "Invalid scale, enter 'hour' or 'dayofweek as scale."

    def hourly_usage(self, df_processing):
        hourly_usage = df_processing.groupby('hour').size()
        max_hourly_usage = hourly_usage.idxmax()
        min_hourly_usage = hourly_usage.idxmin()
        return min_hourly_usage, max_hourly_usage, hourly_usage

    def plot_hourly_usage(self, hourly_usage):
        """Plots the hourly scooter usage.
        Parameters:
        - hourly_usage (pandas.Series): A pandas Series containing the hourly usage data.
        Returns:
        - None
        This function takes a pandas Series object containing the hourly usage data and plots a bar chart
        to visualize the number of rides for each hour of the day. The x-axis represents the hour of the day,
        and the y-axis represents the number of rides.
        """
        fig = go.Figure(data=go.Bar(x=hourly_usage.index, y=hourly_usage.values))
        fig.update_layout(
            title='Hourly Scooter Usage', xaxis_title='Hour of the Day',
            yaxis_title='Number of Rides')
        return fig.show()

    def day_of_week_usage(self, df_processing):
        """Calculates the day of the week with the highest and lowest usage based on the given 
        DataFrame.
        Parameters:
        - df_processing (DataFrame): The DataFrame containing the data to be processed.
        Returns:
        - Tuple[str, str]: A tuple containing the day of the week with the highest usage and the day
        of the week with the lowest usage.
        """
        df_dayOfWeek = pd.DataFrame(df_processing.groupby('dayofweek').size(), columns=['value'])
        df_dayOfWeek.loc[:, 'day_of_week'] = ['Monday', 'Tuesday',
                                              'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return df_dayOfWeek.loc[df_dayOfWeek.value.idxmax(),
                                'day_of_week'], df_dayOfWeek.loc[df_dayOfWeek.value.idxmin(),
                                                                 'day_of_week']
    
    def heatmap_dayly_hourly(self, df_processing):
        """Generates a heatmap of scooter usage intensity by hour and day of the week.
        Parameters:
        - df_processing: pandas DataFrame
            The input DataFrame containing the processed data.
        Returns:
        - fig: plotly Figure
            The generated heatmap figure.
        """
        heatmap_data = df_processing.groupby(['dayofweek', 'hour']).size().unstack(fill_value=0)
        fig = px.imshow(heatmap_data, 
                        labels=dict(x="Hour of Day", y="Day of Week", color="Usage Intensity"),
                        x=heatmap_data.columns, 
                        y=heatmap_data.index,
                        color_continuous_scale="YlGnBu")
        fig.update_layout(title="Scooter Usage Intensity by Hour and Day",
                          xaxis_nticks=24)
        return fig.show()
    
    def plot_start_end_point_ride(self, df_processing):
        """Plots the starting and ending points of scooter rides on a scatter plot.
        Args:
            df_processing (DataFrame): The processed DataFrame containing the scooter ride data.
        Returns:
            a plot showing the starting and ending points of scooter rides.
        """
        df_processing = df_processing.dropna(subset=['lat', 'lon', 'last_lat', 'last_lon'])
        plt.figure(figsize=(10, 5))
        plt.scatter(df_processing['lon'], df_processing['lat'], color='blue', alpha=0.8, label='Start Points')
        plt.scatter(df_processing['last_lon'], df_processing['last_lat'], color='red', alpha=0.5, label='End Points')
        plt.title('Starting and Ending Points of Scooter Rides')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.legend()
        plt.grid(True)
        return plt.show()
