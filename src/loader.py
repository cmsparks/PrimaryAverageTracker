import pandas as pd
import datetime as dt
import math
import regress.lowess as lowess
import regress.primary_weights.weight as p_weights

def run_model():
    polls = pd.read_csv('./data/primary_polls.csv')
    
    polls['startdate'] = pd.to_datetime(polls['startdate'])
    polls['startdate'] = polls['startdate'].map(dt.datetime.toordinal)
    polls['enddate'] = pd.to_datetime(polls['enddate'])
    polls['enddate'] = polls['enddate'].map(dt.datetime.toordinal)
    
    start_regress = polls[['startdate']].min()
    end_regress = dt.datetime.toordinal(dt.datetime.now())
    date_range = np.arange(start_regress, end_regress, 1)

    candidate_groups = polls.groupby(['candidate'])

    for candidate, group in candidate_groups:
        percent_nums = group['percent'].to_numpy()
        dates = group[['startdate','enddate']].mean(axis=1).to_numpy()
        weights = calculate_weights(group)
        trendline = lowess.regress(percent_nums, dates, weights, date_range, kernel, 1, 1, 1)
        trendline.to_csv("./out/"+candidate+"_trendline.csv")

def calculate_weights(group):
    weights = np.zeros(group.size)
    for row in group.itertuples(index=True):
        
        
        weights[row.Index] = 0.0

def weight_sample(poll):
    # f(x) = 3(1-e^(-0.0005x))+1
    return (3 * (1 - math.exp(-0.0005 * poll.samplesize))) + 1

def weight_accuracy(poll):
    return 1

def weight_methodology(poll):
    return {
            'Automated Phone': 1,
            'IVR/Online': 1,
            'IVR/Text': 1,
            'Live Phone': 1,
            'Live Phone/Online': 1,
            'Live Phone/Text': 1,
            'Online': 1,
            'Online/IVR': 1,
            'Text': 1,
            '': 1,
    }[poll.methodology]

def weight_frequency(poll, all_polls):
    s = polls[['startdate']].min()
    e = dt.datetime.toordinal(dt.datetime.now())
    
    frequency = (e - s) / (all_polls.pollster == poll.pollster).sum()
    
    # f(x) = 2e^(-(2/3)x)
    return (2 * math.exp(-(2/3) * frequency))
