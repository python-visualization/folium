# TagFilterButton

```{code-cell} ipython3
import os
import folium
```

```{code-cell} ipython3
import numpy as np
import random

# Generate base data
data = (np.random.normal(size=(100, 2)) * np.array([[1, 1]]) +
                np.array([[48, 5]]))
# Generate the data to segment by (levels of another pandas column in practical usage)
categories = ['category{}'.format(i+1) for i in range(5)]
category_column = [random.choice(categories) for i in range(len(data))]
```

Create markers, and add tags to each marker. There can be multiple tags per marker, but in this example we add just one.

Then, create the `TagFilterButton` object and let it know which tags you want to filter on.

```{code-cell} ipython3
from folium.plugins import TagFilterButton

# Create map and add the data with additional parameter tags as the segmentation
m = folium.Map([48., 5.], tiles='stamentoner', zoom_start=7)
for i, latlng in enumerate(data):
    category = category_column[i]
    folium.Marker(
        tuple(latlng),
        tags=[category]
    ).add_to(m)

TagFilterButton(categories).add_to(m)

m
```
