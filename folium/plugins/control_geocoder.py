"""Add geocoder to folium Map.
Based on leaflet plugin: https://github.com/perliedman/leaflet-control-geocoder
"""

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template
from folium.utilities import parse_options


class LocateGeocoder(MacroElement):
    """
   A simple geocoder for Leaflet that by default uses OSM/Nominatim.

 Parameters :

 Option 	       Type 	   Default 	                            Description

 collapsed 	       Boolean 	   true 	                            Collapse control unless hovered/clicked
 expand 	       String 	   "touch" 	                            How to expand a collapsed control: touch or click or hover
 position 	       String 	   "topright" 	                        Control position
 placeholder 	   String 	   "Search..." 	                        Placeholder text for text input
 errorMessage 	   String 	   "Nothing found." 	                Message when no result found / geocoding error occurs
 iconLabel 	       String 	   "Initiate a new search" 	            Accessibility label for the search icon used by screen readers
 geocoder 	       IGeocoder   new L.Control.Geocoder.Nominatim() 	Object to perform the actual geocoding queries
 showUniqueResult  Boolean 	   true 	                            Immediately show the unique result without prompting for alternatives
 showResultIcons   Boolean 	   false 	                            Show icons for geocoding results (if available); supported by Nominatim
 suggestMinLength  Number 	   3 	                                Minimum number characters before suggest functionality is used (if available from geocoder)
 suggestTimeout    Number 	   250 	                                Number of milliseconds after typing stopped before suggest functionality is used (if available from geocoder)
 query 	     	   String	   ""                                   Initial query string for text input
 queryMinLength    Number 	   1 	                                Minimum number of characters in search text before performing a query
 defaultMarkGeocode* Boolean    True                                Hide the markers when False

 *In order to zoom in if markers hided, you must do like this exemple : 

         var control = L.Control.geocoder({
        query: 'Ville',
        placeholder: 'Search here...',
        defaultMarkGeocode: false
         }).on('markgeocode', function(e) { 
         map.setView(e.geocode.center, 11
       ); }).addTo(map); 

  

 """

    _template = Template(u"""
        {% macro script(this, kwargs) %}
            L.Control.geocoder({{this.options|tojson }}).on('markgeocode', function(e) { 
         {{this._parent.get_name()}}.setView(e.geocode.center, 11
       ); }).addTo({{this._parent.get_name()}});

        {% endmacro %}
        """)

    def __init__(self, collapsed=True, expand="touch", position="topright", placeholder="Search...", errorMessage="Nothing found", iconLabel="Initiate a new search", showUniqueResult=True, showResultIcons=False, suggestMinLength=3, suggestTimeout=250, query="", queryMinLength=1, defaultMarkGeocode=True, **kwargs):
        super(LocateGeocoder, self).__init__()
        self._name = 'LocateGeocoder'
        self.options = parse_options(collapsed=collapsed, expand=expand,position=position, placeholder=placeholder,errorMessage=errorMessage,iconLabel=iconLabel, showUniqueResult=showUniqueResult, showResultIcons=showResultIcons, suggestMinLength=suggestMinLength, suggestTimeout=suggestTimeout, query=query, queryMinLength=queryMinLength, defaultMarkGeocode=defaultMarkGeocode, **kwargs)
    

    def render(self, **kwargs):
        super(LocateGeocoder, self).render(**kwargs)
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(CssLink(
                "https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css"))  # noqa
        figure.header.add_child(JavascriptLink(
            "https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"))  # noqa