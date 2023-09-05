# Integrating Jenks Natural Break Optimization with choropleth

Choropleths provide an easy way to visually see data distributions across geography. By default, folium uses the breaks created by numpy.histogram (np.histogram), which generally creates an evenly spaced quantiles.

This works well enough for evenly distributed data, but for unevenly distributed data, these even quantiles can obscure more than they show. To demonstrate this, I have created maps showing the labor force of each US state.

The data was taken from the county-level data and aggregated. Since our geographic data does not have areas representing Puerto Rico or the United States as a whole, I removed those entries while keeping Washington, D.C. in our data set. Already, looking at the first five states alphabetically, we can see that Alaska (AK) has a work force roughly 2% the size of California (CA).

```{code-cell} ipython3
import folium
import numpy as np
import pandas as pd
import json
import requests
```

```{code-cell} ipython3
geo_json_data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()

clf = 'Civilian_labor_force_2011'
labor_force = pd.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_labor_force_2011.csv"
)

labor_force.head()
```

Using default breaks, most states are represented as being part of the bottom quantile. This distribution is similar to what we might expect if US states follow a Power Law or a Zipf distribution.

```{code-cell} ipython3
m = folium.Map(location=[38, -96], zoom_start=4)

folium.Choropleth(
    geo_data=geo_json_data,
    data=labor_force,
    columns=['State', clf],
    key_on='id',
    fill_color='RdBu',
).add_to(m)

m
```

However, when using Jenks natural Breaks Optimization, we now see more granular detail at the bottom of the distribution, where most of our states are located. The upper western states (Idaho, Montana, Wyoming and the Dakotas) are distinguished from their Midwestern and Mountain West neighbors to the south. Gradations in the deep south between Mississippi and Alabama provide more visual information than in the previous map. Overall, this is a richer representation of the data distribution.

One notable drawback of this representation is the legend. Because the lower bins are smaller, the numerical values overlap, making them unreadable.

```{code-cell} ipython3
m = folium.Map(location=[38, -96], zoom_start=4)

choropleth = folium.Choropleth(
    geo_data=geo_json_data,
    data=labor_force,
    columns=['State', clf],
    key_on='id',
    fill_color='RdBu',
    use_jenks=True,
)
choropleth.add_to(m)

choropleth.color_scale.width = 800

m
```
