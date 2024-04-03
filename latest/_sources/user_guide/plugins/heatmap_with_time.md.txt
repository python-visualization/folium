```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# HeatMapWithTime

In this example we show the basic usage of the HeatMapWithTime plugin.

### Data

We generate a random set of points with lat/lon coordinates to draw on the map, and then move these points slowly in a random direction to simulate a time dimension. The points are arranged into a list of sets of data to draw.

```{code-cell} ipython3
import numpy as np

np.random.seed(3141592)
initial_data = np.random.normal(size=(100, 2)) * np.array([[1, 1]]) + np.array(
    [[48, 5]]
)

move_data = np.random.normal(size=(100, 2)) * 0.01

data = [(initial_data + move_data * i).tolist() for i in range(100)]
```

### Weights

In order to control intensity shown on the map, each data entry needs to have a `weight`. Which should be between 0 and 1.
Below we generate weights randomly such that intensity increases over time.

```{code-cell} ipython3
time_ = 0
N = len(data)
itensify_factor = 30
for time_entry in data:
    time_ = time_+1
    for row in time_entry:
        weight = min(np.random.uniform()*(time_/(N))*itensify_factor, 1)
        row.append(weight)
```

```{code-cell} ipython3
m = folium.Map([48.0, 5.0], zoom_start=6)

hm = folium.plugins.HeatMapWithTime(data)

hm.add_to(m)

m
```

### Options

Now we show that the time index can be specified, allowing a more meaningful representation of what the time steps mean. We also enable the 'auto_play' option and change the maximum opacity. See the documentation for a full list of options that can be used.

```{code-cell} ipython3
from datetime import datetime, timedelta

time_index = [
    (datetime.now() + k * timedelta(1)).strftime("%Y-%m-%d") for k in range(len(data))
]
```

```{code-cell} ipython3
m = folium.Map([48.0, 5.0], zoom_start=6)

hm = folium.plugins.HeatMapWithTime(data, index=time_index, auto_play=True, max_opacity=0.3)

hm.add_to(m)

m
```
