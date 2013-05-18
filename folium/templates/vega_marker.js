{{ mark }}.on('click', function() {
      var div = $('<div id="{{ div_id }}" style="width: {{ width }}px; height: {{ height }}px;"></div>')[0];
      {{ mark }}.bindPopup(div);
      {{ mark }}._popup.options.maxWidth = {{ max_width }};
      {{ mark }}.openPopup();
      parse('{{ json_out }}', '{{ vega_id }}');
    });