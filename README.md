# GPU Price Scaraper
Scraping available GPU listings from HardwareLuxx.


## How to Run

Setup Environment:
```
conda env create -f environment
conda activate gpu-price-scraper
```

Run:
```
scrapy crawl gpu -O data/nvidia.csv
```

The output is also available via [Github Pages](http://eckelt.info/gpu-price-scraper/nvidia.csv).
