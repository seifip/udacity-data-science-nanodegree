_Udacity Data Science Nanodegree project by [Philip Seifi](https://www.seifi.co/)._

# Vegetarian trends at food.com
The interest in vegetarian and vegan food has grown steadily over the past two decades.

The number of searches for 'veganism' in the UK has increased 900% from 2009 to 2019.[1]

And although in 2015, just 3.4% of all Americans said they were vegetarian, fully a quarter of 25- to 34-year-olds identified as such.[2]

In this notebook, I will explore whether this vegetarian trend extends to the users of [food.com](https://www.food.com/), one of the leading online recipe websites.

[1] [Veganism: Why are vegan diets on the rise?](https://www.bbc.com/news/business-44488051)

[2] [The year of the vegan, The Economist](https://worldin2019.economist.com/theyearofthevegan)

## Questions

1. Is there a positive trend in the number of vegetarian recipes posted on food.com between 2008 and 2017?
2. Is there a positive trend in the number of interactions with vegetarian recipes on Food.com between 2008 and 2017?
3. Is there a difference in the ratings vegetarian recipes received compared to non-vegetarian recipes between 2008 and 2017?

## Dataset

I will be using the food.com dataset by Bodhisattwa Prasad Majumder, Shuyang Li, Jianmo Ni, and Julian McAuley.
 
The dataset consists of 180K+ recipes and 700K+ recipe reviews covering 18 years of user interactions and uploads on food.com (formerly GeniusKitchen).

For the purpose of this exploration study, I will only look at the data between 2008 and 2017.

## Files
### In this repository
* `food_com-vegetarian-analysis.ipynb` — Python 3 Jupyter Notebook exploring the dataset
* `/blog/vegetarianism-booming-established-recipe-sites-benefit-suffer-trend.md` — blog post summarizing the findings

### Kaggle
The following two data files were too big to upload to GitHub and can be accessed from [Kaggle](https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions).
* `/input/RAW_recipes.csv` — food.com recipes
* `/input/RAW_interactions.csv` — food.com reviews and ratings

## Libraries used
* `numpy` and `pandas` for data analysis and manipulation
* `matplotlib`, `matplotlib_venn` and `seaborn` for visualizations
* `ast` to evaluate a stringified array into a Python list

