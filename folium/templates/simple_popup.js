var {{ pop_name }} = L.popup({maxWidth: '{{ width }}'});
var {{ html_name }} =
    $('<div id="{{ html_name }}" style="width: 100.0%; height: 100.0%;">{{ pop_txt }}</div>')[0];
{{ pop_name }}.setContent({{ html_name }});
