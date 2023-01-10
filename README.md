# Model for running a bakery
- Start with running 'main'.
- We start with goods, products and recipes imported from files. 
- When initializing, number of last saved day is read from daily reports, and we start this day as the next one.
- If Reports directory is empty, we start with day 1.
- On the end of the day stock of goods and products are saved to data file do be imported next day. 
- Recipes are constant, once they are imported they do not change.
- Reports cover number of days running, monthly report summarizes them all.
- To start over, empty Reports directory.
- Adding new products only through data files:
  - Filling the table in recipes.xlsx, and 
  product with same name must be added to data.xlsx, sheet product init with price and quantity.
  - If we are adding new ingredient to recipes, we must add it to goods init in data.xlsx.