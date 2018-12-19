# Paula Choice Scraper
Scrapes the ingredients on [Paula's Choice ingredient dictionary](https://www.paulaschoice.com/ingredient-dictionary?crefn1=name-first-letter&crefv1=1) . Made with Scrapy.

## Installation
To install Scrapy:

```sh
> pip install Scrapy
```

## Usage
For results in json:
```sh
> scrapy crawl paula -o ingredients.json
```

For lined delimited results:
```sh
> scrapy crawl paula -o ingredients.jl
```

Output:
```json
{
    "name": "Gentiana lutea (Gentian) root extract", 
    "rating": "Best", 
    "categories": ["Skin-Soothing", "Antioxidants", "Plant Extracts"], 
    "description": "Part of the gentian plant, constituents of which have skin-soothing and antioxidant benefits."
}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)