import pandas as pd

def main():
    fte_polls = pd.read_csv('./president_primary_polls-1.csv')
    
    adjusted_polls = pd.DataFrame(columns=['rowid', 'pollid', 'pollster', 'location', 'startdate', 'enddate', 'samplesize', 'sampletype', 'methodology', 'candidate', 'percent'])
    
    for row in fte_polls.itertuples(index=True):
        print(row.Index)
        if row.party == "DEM":
            adjusted_row = { 'rowid': row.Index, 'pollid': row.poll_id, 'pollster': row.pollster, 'location': row.state, 'startdate': row.start_date, 'enddate': row.end_date, 'samplesize': row.sample_size, 'sampletype': row.population, 'methodology': row.methodology, 'candidate': row.answer, 'percent': row.pct}

            adjusted_polls = adjusted_polls.append(adjusted_row, ignore_index=True)

    adjusted_polls.to_csv('./primary_polls.csv')

if __name__ == '__main__':
    main()
