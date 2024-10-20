import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yaml
from pathlib import Path

def std(df: pd.DataFrame) -> float:
    return np.std([np.sqrt(row[0]**2 + row[1]**2 + row[2]**2) for row in df.itertuples()])

def mean(df: pd.DataFrame) -> float:
    return np.mean([np.sqrt(row[0]**2 + row[1]**2 + row[2]**2) for row in df.itertuples()])

function_dict: dict = {
    'mean': mean,
    'std': std,
    'meadian': np.median
}

class Drawer(object):
    def __init__(self, input_df: pd.DataFrame, config_dict: dict):
        self.df: pd.DataFrame = input_df
        self.config_dict: dict = config_dict

    def get_figure(self) -> go.Figure:
        fig = make_subplots(rows=self.config_dict['rows'], cols=self.config_dict['cols'], shared_xaxes= True, shared_yaxes= True)
        angles = sorted(set(self.df['angle']))
        y_function_axes: dict = dict([(el, []) for el in self.config_dict['functions']])
        print(y_function_axes)
        for func in self.config_dict['functions']:
            local_res: list = list()
            for angle in angles:
                if func in function_dict:
                    res = function_dict.get(func)(self.df[self.df['angle'] == angle][['x', 'y', 'z']])
                    local_res.append(res)
                    print(res)
            y_function_axes.update({func:local_res})
        for index, (function_name, y_function) in enumerate(y_function_axes.items(), start=1):
            fig.add_trace(go.Scatter(x=angles, y=y_function, text=self.df['angle'], name=function_name), row=index, col=1)
        return fig
    
if __name__ == "__main__":
    csv_path: Path = Path("/home/amir/Desktop/Drawer/csv/test.csv")
    yaml_path: Path = Path("/home/amir/Desktop/Drawer/params/config.yaml")
    df = pd.read_csv(csv_path.as_posix())
    with open(yaml_path, 'r') as stream:
        dict_ = yaml.safe_load(stream)
    drawer= Drawer(df, dict_)
    fig = drawer.get_figure()
    fig.show()