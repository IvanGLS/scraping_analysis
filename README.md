# Scraping Analysis

This project involves scraping job listings from a website djinni.co and performing an analysis on the collected data.

## Examples
![top 5 most popular technologies](Screenshot_54.png)
![maximum and minimum views for years of experience](Screenshot_55.png)

## Requirements

To run this project, you need the following:

- Python 3.x
- Scrapy library
- Pandas library
- Matplotlib library

## Installation

1. Clone the repository:
   git clone https://github.com/IvanGLS/scraping_analysis
2. Create venv for your project and install requirements
> - python -m venv venv  
> - venv\Scripts\activate (on Windows)
> - source venv/bin/activate (on macOS)
> - pip install -r requirements.txt

## Usage

1. Start the scraping process by running the following command:
> !cd djinni_scrape && scrapy crawl djinni_jobs -a keyword=Python

Replace `"Python"` with the desired keyword to search for job listings.

2. The scraped data will be saved in a CSV file named `djinni.csv`.

3. Analyze the data by running the analysis script:
The script contains code for data cleaning, visualization, and analysis.

4. Explore the analysis results and visualizations generated.

## Project Structure

The project has the following structure:

- `scraping_analysis/`
- `scraping_analysis/djinni_scrape/spiders` - Contains the spider for scraping job listings.
- `scraping_analysis/djinni_scrape/items.py` - Defines the data structure for scraped items.
- `scraping_analysis/djinni_scrape/settings.py` - Contains Scrapy settings for the project.
- `scraping_analysis/djinni_scrape/pipelines.py` - Defines the data pipeline for processing scraped items.
- `analysis.py` - Script for data cleaning, analysis, and visualization.
- `README.md` - Project documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

The project is inspired by the [Scrapy](https://scrapy.org/) framework and makes use of various open-source libraries and tools.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please create an issue or submit a pull request.

## Contact

For questions or inquiries, feel free to contact the project maintainers:

- smirnovivangls@gmail.com
- Project Repository: [scraping-analysis](https://github.com/IvanGLS/scraping_analysis)

