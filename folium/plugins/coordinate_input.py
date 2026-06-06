from branca.element import MacroElement
from folium.template import Template


class CoordinateInput(MacroElement):
    """
    Add input form to the map for entering coordinates and placing markers at those locations.
    Supports marker removal by double-clicking.

    Parameters
    ----------
    position : str, default 'topleft'
        Corner of the map where the input form will be placed.
        Options: 'topleft', 'topright', 'bottomleft', 'bottomright'
    placeholder : str, default 'Latitude, Longitude'
        Placeholder text for the coordinate input field (e.g., "40.7128, -74.0060")
    button_text : str, default 'Add Marker'
        Text displayed on the submit button
    popup_text : str, default None
        Text to display in marker popups. Use ${lat} and ${lng} for coordinates.
        If None, will show 'Lat: {lat}, Lon: {lng}'
    show_instructions : bool, default True
        Whether to show instructions for removing markers

    Examples
    --------
    >>> m = folium.Map([45.5, -122.3], zoom_start=13)
    >>> CoordinateInput().add_to(m)
    >>> m.save('map.html')

    >>> # With custom settings
    >>> CoordinateInput(
    ...     position='topright',
    ...     placeholder='Enter coordinates',
    ...     button_text='Place Marker',
    ...     popup_text='<b>Coordinates:</b><br>Lat: ${lat}<br>Lon: ${lng}'
    ... ).add_to(m)

    To remove a marker, double-click on it.
    """

    _template = Template(
        r"""
        {% macro script(this, kwargs) %}
            (function() {
                var {{ this.get_name() }}_control = L.control({position: '{{ this.position }}'});

                {{ this.get_name() }}_control.onAdd = function (map) {
                    var div = L.DomUtil.create('div', 'leaflet-control leaflet-bar');
                    div.id = '{{ this.get_name() }}_container';
                    div.style.backgroundColor = 'white';
                    div.style.padding = '10px';
                    div.style.borderRadius = '5px';
                    div.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';

                    var instructionsHtml = '{% if this.show_instructions %}<div style="margin-bottom: 8px; font-size: 10px; color: #666; max-width: 150px;"><em>Double-click marker to remove</em></div>{% endif %}';

                    div.innerHTML = '<div style="font-family: Arial, sans-serif; font-size: 12px; width: 150px;">' +
                        '<div style="margin-bottom: 8px; font-weight: bold;">Add Marker</div>' +
                        instructionsHtml +
                        '<input type="text" id="{{ this.get_name() }}_coords" placeholder="{{ this.placeholder }}" style="width: 100%; padding: 5px; margin-bottom: 5px; box-sizing: border-box;">' +
                        '<button id="{{ this.get_name() }}_btn" style="width: 100%; background-color: #4CAF50; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">{{ this.button_text }}</button>' +
                        '<button id="{{ this.get_name() }}_clear_btn" style="width: 100%; margin-top: 5px; background-color: #f44336; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">Clear All</button>' +
                        '</div>';

                    L.DomEvent.disableClickPropagation(div);

                    return div;
                };

                {{ this.get_name() }}_control.addTo({{ this._parent.get_name() }});

                setTimeout(function() {
                    var btnElement = document.getElementById('{{ this.get_name() }}_btn');
                    var clearBtnElement = document.getElementById('{{ this.get_name() }}_clear_btn');
                    var coordsElement = document.getElementById('{{ this.get_name() }}_coords');
                    var map = {{ this._parent.get_name() }};
                    var markerGroup = L.featureGroup();
                    markerGroup.addTo(map);

                    if (btnElement && coordsElement) {
                        var addMarker = function() {
                            var input = coordsElement.value.trim();
                            var parts = input.split(',');

                            if (parts.length !== 2) {
                                alert('Please enter coordinates in format: latitude, longitude');
                                return;
                            }

                            var lat = parseFloat(parts[0].trim());
                            var lng = parseFloat(parts[1].trim());

                            if (isNaN(lat) || isNaN(lng)) {
                                alert('Please enter valid numbers for coordinates');
                                return;
                            }

                            if (lat < -90 || lat > 90) {
                                alert('Latitude must be between -90 and 90');
                                return;
                            }

                            if (lng < -180 || lng > 180) {
                                alert('Longitude must be between -180 and 180');
                                return;
                            }

                            var marker = L.marker([lat, lng]);

                            var popupText = '{{ this.popup_text }}';
                            if (popupText === '') {
                                popupText = 'Lat: ' + lat.toFixed(4) + '<br>Lon: ' + lng.toFixed(4);
                            } else {
                                popupText = popupText.replace(/\$\{lat\}/g, lat.toFixed(4));
                                popupText = popupText.replace(/\$\{lng\}/g, lng.toFixed(4));
                            }
                            marker.bindPopup(popupText);

                            // Add double-click to remove marker
                            marker.on('dblclick', function() {
                                markerGroup.removeLayer(marker);
                            });

                            markerGroup.addLayer(marker);
                            coordsElement.value = '';
                            marker.openPopup();
                        };

                        btnElement.addEventListener('click', addMarker);

                        coordsElement.addEventListener('keypress', function(e) {
                            if (e.key === 'Enter') {
                                addMarker();
                            }
                        });

                        clearBtnElement.addEventListener('click', function() {
                            if (confirm('Are you sure you want to remove all markers?')) {
                                markerGroup.clearLayers();
                                coordsElement.value = '';
                            }
                        });
                    }
                }, 100);
            })();
        {% endmacro %}
        """
    )

    def __init__(
        self,
        position: str = "topleft",
        placeholder: str = "Latitude, Longitude",
        button_text: str = "Add Marker",
        popup_text: str = "",
        show_instructions: bool = True,
    ):
        super().__init__()
        self._name = "CoordinateInput"

        self.position = position
        self.placeholder = placeholder
        self.button_text = button_text
        self.popup_text = popup_text if popup_text else "Lat: ${lat}<br>Lon: ${lng}"
        self.show_instructions = show_instructions
