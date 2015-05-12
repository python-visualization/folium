var {{ tile_name }} = L.tileLayer('{{ tile_url }}',{
                            'minZoom': {{minZoom}},
                            'maxZoom': {{maxZoom}},
                            'tms': {{tms}},
                            'continuousWorld': {{continuousWorld}},
                            'noWrap': {{noWrap}},
                            'zoomOffset': {{zoomOffset}},
                            'zoomReverse': {{zoomReverse}},
                            'opacity': {{opacity}} 
                            });