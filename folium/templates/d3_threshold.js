{{ this.get_name() }}.color = d3.scale.threshold()
              .domain({{ domain }})
              .range({{ range }});