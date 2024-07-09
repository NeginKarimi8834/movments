import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

class Dataprocessing:
    class DataProcessing:
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
        df_processing=self.df[['id','lat', 'lon', 'operator', 'power', 'rangeLeft',
        'txt_code', 'last_lat', 'last_lon', 'distanceTravelled','day','hour','dayofweek','month']]
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
    def distance_traveld_discover(self,column_name):
        df_distance_discover=self.df.groupby(column_name).count()['distanceTravelled']
        return df_distance_discover
    
    def plot_distance_traveled_per_operator(self, df_distance_discover):
        try:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_distance_discover.index, y=df_distance_discover.values))
            fig.update_layout(xaxis_title='operator', yaxis_title="Distance Traveled", title="Distance Traveled per Operator")
            return fig.show()
        except Exception as e:
            print('Error:', str(e))
            
    
    def plot_distance_taveled_day_of_week(self,df_processing):
        df=df_processing.groupby(['dayofweek','operator'])['distanceTravelled'].sum().reset_index()
        fig = px.bar(df, x='dayofweek', y='distanceTravelled', color='operator', barmode='group',
                    title='Total Distance Travelled by Day of Week and Operator')
        return fig.show()
    
    def plot_distance_mean(self,df_processing,scale):
        try:
            if scale in ['hour','dayofweek']:
                hu=pd.DataFrame(df_processing.groupby([scale,'operator'])['distanceTravelled'].mean())
            return sns.displot(hu, x="distanceTravelled", kind="kde")
        except:
            return "Invalid scale, enter 'hour' or 'dayofweek as scale."
        

    