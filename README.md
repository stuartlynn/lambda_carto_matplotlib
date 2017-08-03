# lambda_carto_matplotlib

This is a quick AWS service to plot matplotlib plots from data in [CARTO](https://carto.com/) for popup images 

## Setup

```bash
virtualenv env 
source env/bin/activate 
pip install -r requirements.txt
zappa init
zappa deploy dev 
```
That will set up a set of AWS lambda functios that can plot and return matplotlib images on demand using queries on CARTO 

## Bar Plot

Expects the CARTO Query to have a column called _cat_ and one called _val_
/dev/bar.img?q={query}&username={username}&xlabel={x}&ylabel={y}&title={title}

## Scatter Plot

Expects the CARTO Query to have a column called _cx_ and one called _y_
/dev/scatter.img?q={query}&username={username}&xlabel={x}&ylabel={y}&title={title}


## Pair Plot

Will make a seaborn pair plot of all the variables in the table
/dev/pairplot.img?q={query}&username={username}&xlabel={x}&ylabel={y}&title={title}

more to come...
