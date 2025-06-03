import folium

# Create a basic map
m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# Add a marker
folium.Marker([37.7749, -122.4194], popup="San Francisco").add_to(m)

# Save to HTML
m.save("interactive_map_example.html")
