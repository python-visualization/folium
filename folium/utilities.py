'# -*- coding: utf-8 -*-'
'''
GeoJson
-------

Folium module to apply GeoJSON data to maps, as well as bind data for
choropleth mapping.

'''
from __future__ import print_function
from __future__ import division
from jinja2 import Environment, PackageLoader, Template


def get_templates():
    '''Get Jinja templates'''
    return Environment(loader=PackageLoader('folium', 'templates'))


def color_brewer(len, scheme):
    '''Generate a colorbrewer color scheme of length 'len', type 'scheme.
    Live examples can be seen at http://colorbrewer2.org/'''

    schemes = {'BuGn': ['#EDF8FB', '#CCECE6', '#CCECE6', '#66C2A4', '#41AE76',
                        '#238B45', '#005824'],
               'BuPu': ['#EDF8FB', '#BFD3E6', '#9EBCDA', '#8C96C6', '#8C6BB1',
                        '#88419D', '#6E016B'],
               'GnBu': ['#F0F9E8', '#CCEBC5', '#A8DDB5', '#7BCCC4', '#4EB3D3',
                        '#2B8CBE', '#08589E'],
               'OrRd': ['#FEF0D9', '#FDD49E', '#FDBB84', '#FC8D59', '#EF6548',
                        '#D7301F', '#990000'],
               'PuBu': ['#F1EEF6', '#D0D1E6', '#A6BDDB', '#74A9CF', '#3690C0',
                        '#0570B0', '#034E7B'],
               'PuBuGn': ['#F6EFF7', '#D0D1E6', '#A6BDDB', '#67A9CF', '#3690C0',
                          '#02818A', '#016450'],
               'PuRd': ['#F1EEF6', '#D4B9DA', '#C994C7', '#DF65B0', '#E7298A',
                        '#CE1256', '#91003F'],
               'RdPu': ['#FEEBE2', '#FCC5C0', '#FA9FB5', '#F768A1', '#DD3497',
                        '#AE017E', '#7A0177'],
               'YlGn': ['#FFFFCC', '#D9F0A3', '#ADDD8E', '#78C679', '#41AB5D',
                        '#238443', '#005A32'],
               'YlGnBu': ['#FFFFCC', '#C7E9B4', '#7FCDBB', '#41B6C4', '#1D91C0',
                          '#225EA8', '#0C2C84'],
               'YlOrBr': ['#FFFFD4', '#FEE391', '#FEC44F', '#FE9929', '#EC7014',
                          '#CC4C02', '#8C2D04'],
               'YlOrRd': ['#FFFFB2', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A',
                          '#E31A1C', '#B10026']}

    colors = schemes[scheme]
    return colors[0:len]

def transform_data(data):
    '''Transform Pandas DataFrame into JSON format

    Parameters
    ----------
    data: DataFrame or Series
        Pandas DataFrame or Series

    Returns
    -------
    JSON compatible dict

    Example
    -------
    >>>vis.transform_data(df)
    >>>vis.json_data

    '''

    def type_check(value):
        '''Type check values for JSON serialization. Native Python JSON
        serialization will not recognize some Numpy data types properly,
        so they must be explictly converted.'''
        if pd.isnull(value):
            return None
        elif (isinstance(value, pd.tslib.Timestamp) or
              isinstance(value, pd.Period)):
            return time.mktime(value.timetuple())
        elif isinstance(value, (int, np.integer)):
            return int(value)
        elif isinstance(value, (float, np.float_)):
            return float(value)
        elif isinstance(value, str):
            return str(value)
        else:
            return value

    if isinstance(data, pd.Series):
        json_data = [{type_check(x): type_check(y) for x, y in data.iteritems()}]
    elif isinstance(data, pd.DataFrame):
        json_data = [{y: z for x, y, z in data.itertuples()}]
