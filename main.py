
from flask import Flask, render_template, request
import pandas as pd 
import numpy as np 

app = Flask(__name__)
megaframe = pd.read_csv(r'ihme_impact.csv')
megaframe2 = pd.read_csv(r'who_impact.csv')
vacs = megaframe['vaccine'].unique().tolist()
countries = megaframe['country'].unique().tolist()
years = megaframe['year'].unique().tolist()
num_cols = {'pop_est': 'Population Estimates',
            'vac_coverage': 'Vaccine Coverage Estimates',
            'fvp': 'Fully Vaccinated Persons',
            'cases_averted': 'Cases Averted',
            'dalys_averted': 'DALYs Averted',
            'deaths_averted': 'Deaths Averted',
            'cumulative_protected': 'Cumulative Protected Population',
            'percent_protected': 'Percent Population Protected',
            'daly_by_pop': 'DALYs By Population'}

@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template("dashboard.html", countries=countries, vaccines=vacs, years=years, num_cols=num_cols)
    else:
        #print(request.json)
        vac = request.json['vac']
        #print(vac)
        country = request.json['country']
        #print(country)
        year_start = request.json['year']
        #print(year_start)
        y_ax = request.json['y_ax']
        if vac == '':
            conditions1 = ((megaframe['year']>=int(year_start))&(megaframe['country']==country)&(megaframe['vaccine']=='PCV3'))
            conditions2 = ((megaframe2['year']>=int(year_start))&(megaframe2['country']==country)&(megaframe2['vaccine']=='PCV3')) 
        else:
            conditions1 = ((megaframe['year']>=int(year_start))&(megaframe['country']==country)&(megaframe['vaccine']==vac))
            conditions2 = ((megaframe2['year']>=int(year_start))&(megaframe2['country']==country)&(megaframe2['vaccine']==vac))
        year_data = megaframe.loc[conditions1,'year'].values.tolist()
        #print(year_data)
        ihme_data = megaframe.loc[conditions1, y_ax].fillna(0).values.tolist()
        who_data = megaframe2.loc[conditions2, y_ax].fillna(0).values.tolist()
        d = {'ihme_data': ihme_data, 'who_data': who_data, 'year_data': year_data}
        return d
    
if __name__ == "__main__":
    app.run(debug=True)