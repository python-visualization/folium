"""
Folium Multi-Language Choropleth Solution

This module provides multiple approaches to render folium choropleths 
with different number locales for legends, enabling creation of maps
in multiple languages without changing system locale.

Requirements:
- folium
- pandas
- geopandas (optional, for geojson data)
- selenium (for image generation)
- pillow (for image processing)

Install with: pip install folium pandas selenium pillow
"""

import folium
import pandas as pd
import json
import re
from typing import Dict, List, Optional, Union
import tempfile
import os


class MultiLanguageChoropleth:
    """
    A class to create folium choropleths with customizable number formatting
    for different languages/locales without changing system settings.
    """
    
    def __init__(self):
        self.number_formats = {
            'en': {
                'decimal_separator': '.',
                'thousands_separator': ',',
                'currency_symbol': '$',
                'position': 'before'  # currency position
            },
            'fr': {
                'decimal_separator': ',',
                'thousands_separator': ' ',
                'currency_symbol': '€',
                'position': 'after'
            },
            'de': {
                'decimal_separator': ',',
                'thousands_separator': '.',
                'currency_symbol': '€',
                'position': 'after'
            },
            'es': {
                'decimal_separator': ',',
                'thousands_separator': '.',
                'currency_symbol': '€',
                'position': 'after'
            }
        }
    
    def format_number(self, number: float, locale: str = 'en', 
                     decimals: int = 2, include_currency: bool = False) -> str:
        """
        Format a number according to specified locale conventions.
        
        Args:
            number: The number to format
            locale: Language locale ('en', 'fr', 'de', 'es')
            decimals: Number of decimal places
            include_currency: Whether to include currency symbol
            
        Returns:
            Formatted number string
        """
        if locale not in self.number_formats:
            locale = 'en'  # fallback to English
            
        fmt = self.number_formats[locale]
        
        # Round to specified decimals
        rounded = round(number, decimals)
        
        # Split into integer and decimal parts
        integer_part = int(rounded)
        decimal_part = rounded - integer_part
        
        # Format integer part with thousands separator
        integer_str = f"{integer_part:,}".replace(',', '|TEMP|')
        integer_str = integer_str.replace('|TEMP|', fmt['thousands_separator'])
        
        # Format decimal part
        if decimals > 0 and decimal_part > 0:
            decimal_str = f"{decimal_part:.{decimals}f}"[2:]  # Remove "0."
            formatted = f"{integer_str}{fmt['decimal_separator']}{decimal_str}"
        else:
            formatted = integer_str
            
        # Add currency if requested
        if include_currency:
            if fmt['position'] == 'before':
                formatted = f"{fmt['currency_symbol']}{formatted}"
            else:
                formatted = f"{formatted} {fmt['currency_symbol']}"
                
        return formatted
    
    def create_custom_legend_html(self, values: List[float], colors: List[str], 
                                locale: str = 'en', title: str = "Legend") -> str:
        """
        Create custom HTML legend with locale-specific number formatting.
        
        Args:
            values: List of values for legend
            colors: List of corresponding colors
            locale: Language locale
            title: Legend title
            
        Returns:
            HTML string for custom legend
        """
        legend_html = f'''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 150px; height: auto; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <h4 style="margin-top:0;">{title}</h4>
        '''
        
        for i, (value, color) in enumerate(zip(values, colors)):
            formatted_value = self.format_number(value, locale)
            legend_html += f'''
            <p style="margin: 5px 0;">
                <span style="background-color:{color}; width: 20px; height: 20px; 
                           display: inline-block; margin-right: 5px;"></span>
                {formatted_value}
            </p>
            '''
            
        legend_html += '</div>'
        return legend_html
    
    def inject_locale_javascript(self, locale: str = 'en') -> str:
        """
        Generate JavaScript to modify number formatting in existing legend.
        
        Args:
            locale: Target locale for number formatting
            
        Returns:
            JavaScript code string
        """
        fmt = self.number_formats[locale]
        
        js_code = f'''
        <script>
        // Function to format numbers according to locale
        function formatNumberLocale(num, locale) {{
            const formats = {json.dumps(self.number_formats)};
            const fmt = formats[locale] || formats['en'];
            
            // Convert number to string and parse
            let numStr = parseFloat(num).toFixed(2);
            let parts = numStr.split('.');
            
            // Add thousands separator
            parts[0] = parts[0].replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, fmt.thousands_separator);
            
            // Join with decimal separator
            if (parts[1] && parseFloat('0.' + parts[1]) > 0) {{
                return parts[0] + fmt.decimal_separator + parts[1];
            }}
            return parts[0];
        }}
        
        // Wait for map to load, then modify legend
        setTimeout(function() {{
            // Find all text elements in the legend that contain numbers
            const legendElements = document.querySelectorAll('.legend text, .colorbar text');
            
            legendElements.forEach(function(element) {{
                const text = element.textContent;
                const numberMatch = text.match(/\\d+\\.?\\d*/);
                
                if (numberMatch) {{
                    const originalNumber = parseFloat(numberMatch[0]);
                    const formattedNumber = formatNumberLocale(originalNumber, '{locale}');
                    element.textContent = text.replace(numberMatch[0], formattedNumber);
                }}
            }});
        }}, 1000);
        </script>
        '''
        
        return js_code
    
    def create_choropleth_with_locale(self, map_obj: folium.Map, 
                                    geo_data: Union[str, dict],
                                    data: pd.DataFrame,
                                    columns: List[str],
                                    key_on: str,
                                    locale: str = 'en',
                                    **choropleth_kwargs) -> folium.Map:
        """
        Create a choropleth with custom locale formatting.
        
        Args:
            map_obj: Folium map object
            geo_data: GeoJSON data
            data: DataFrame with data to map
            columns: Columns for choropleth [key_column, value_column]
            key_on: Key in GeoJSON to match with data
            locale: Target locale
            **choropleth_kwargs: Additional arguments for folium.Choropleth
            
        Returns:
            Modified folium map
        """
        # Create the choropleth first
        choropleth = folium.Choropleth(
            geo_data=geo_data,
            data=data,
            columns=columns,
            key_on=key_on,
            **choropleth_kwargs
        ).add_to(map_obj)
        
        # Add JavaScript to modify number formatting
        js_code = self.inject_locale_javascript(locale)
        map_obj.get_root().html.add_child(folium.Element(js_code))
        
        return map_obj


def create_sample_data() -> tuple:
    """
    Create sample data for demonstration.
    
    Returns:
        Tuple of (sample_data_df, sample_geojson)
    """
    # Sample data
    sample_data = pd.DataFrame({
        'country': ['USA', 'Canada', 'Mexico', 'Brazil', 'Argentina'],
        'value': [1234567.89, 987654.32, 456789.12, 2345678.90, 876543.21]
    })
    
    # Simple sample GeoJSON (normally you'd load this from a file)
    sample_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "USA"},
                "geometry": {"type": "Polygon", "coordinates": [[[-100, 40], [-90, 40], [-90, 50], [-100, 50], [-100, 40]]]}
            },
            {
                "type": "Feature", 
                "properties": {"name": "Canada"},
                "geometry": {"type": "Polygon", "coordinates": [[[-110, 50], [-90, 50], [-90, 60], [-110, 60], [-110, 50]]]}
            }
        ]
    }
    
    return sample_data, sample_geojson


def demo_multilanguage_choropleth():
    """
    Demonstrate creating choropleths in multiple languages.
    """
    # Initialize the multi-language choropleth handler
    ml_choropleth = MultiLanguageChoropleth()
    
    # Create sample data
    sample_data, sample_geojson = create_sample_data()
    
    # Create maps for different locales
    locales = ['en', 'fr', 'de']
    maps = {}
    
    for locale in locales:
        # Create base map
        m = folium.Map(location=[45, -100], zoom_start=3)
        
        # Add choropleth with custom locale
        m = ml_choropleth.create_choropleth_with_locale(
            map_obj=m,
            geo_data=sample_geojson,
            data=sample_data,
            columns=['country', 'value'],
            key_on='feature.properties.name',
            locale=locale,
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f'Sample Values ({locale.upper()})'
        )
        
        maps[locale] = m
        
        # Save map
        filename = f'choropleth_{locale}.html'
        m.save(filename)
        print(f"Saved map in {locale.upper()} locale as {filename}")
    
    return maps


def save_map_as_image(map_obj: folium.Map, filename: str, 
                     width: int = 1200, height: int = 800):
    """
    Save folium map as image using selenium.
    
    Args:
        map_obj: Folium map object
        filename: Output filename
        width: Image width
        height: Image height
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
        
        # Save map as temporary HTML
        temp_html = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
        map_obj.save(temp_html.name)
        
        # Setup headless browser
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'--window-size={width},{height}')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f'file://{temp_html.name}')
        
        # Wait for map to load
        time.sleep(3)
        
        # Take screenshot
        driver.save_screenshot(filename)
        driver.quit()
        
        # Clean up
        os.unlink(temp_html.name)
        
        print(f"Map saved as image: {filename}")
        
    except ImportError:
        print("Selenium not available. Install with: pip install selenium")
        print("Also need to install ChromeDriver for your system")
    except Exception as e:
        print(f"Error saving image: {e}")


if __name__ == "__main__":
    # Run the demonstration
    print("Creating multi-language choropleths...")
    maps = demo_multilanguage_choropleth()
    
    # Optionally save as images (requires selenium)
    # for locale, map_obj in maps.items():
    #     save_map_as_image(map_obj, f'choropleth_{locale}.png')
    
    print("\nDemonstration complete!")
    print("Check the generated HTML files to see the different number formats.")
    
    # Example of manual number formatting
    ml = MultiLanguageChoropleth()
    print("\nExample number formatting:")
    number = 1234567.89
    for locale in ['en', 'fr', 'de']:
        formatted = ml.format_number(number, locale)
        print(f"{locale.upper()}: {formatted}")