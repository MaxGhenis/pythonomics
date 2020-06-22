# Pythonomics: Intro to economic analysis in Python

*Author: Max Ghenis (mghenis@gmail.com)*

**Topics:**

* Loading data with `pandas`
* Preprocessing data
* Merging data
* Regression with `statsmodels`
* Output to $\LaTeX$ with `stargazer`

**Case study:** Effect of Alaska Permanent Fund Dividend on poverty rate,
as measured by the Supplemental Poverty Measure.
Difference in differences research design.



## How to use this notebook

This is called **Google Colab**, a cloud **Jupyter notebook** editor that 
also connects to Google Drive, supports real-time collaboration and comments, etc.

Notebooks are organized into cells, specifically **Markdown cells** (like this one, also accepts `$\LaTeX$`) and **Code cells** (like the cell below with the `[1]` at the left.

You can run and edit the notebook in Playground mode,
or make a copy to ensure your edits are saved.

Code cells can take any Python code and show the result (for simple commands,
you don't need to `print`, it just shows up).

1 + 1

Try getting your name to show up in the two cells below (note that strings require quotes, either single or double will do).

# This is a comment. Type your name in quotes below to create the variable.
my_name = 'max'

Now start typing `my_name`, but press Tab after `my`. Colab autocompletes known variables as well as function documentation.

my_name

Now add a code cell below this to create and print a variable called `my_hometown` with your hometown as a string; cells can have multiple lines of code each.

my_hometown = 'Oxnard'
my_hometown

## Python basics

**Lists** are defined with square brackets, e.g. `[1, 3, -4]` and `['a', 'b', 'c']`.

This is similar to `c(1, 3, 4)` and `c('a', 'b', 'c')` in `R`.

*You can also put mismatching data types in Python lists,
which makes them similar to R lists,
but in most cases you won't need to do that.*

l = [1, 3, 4]
l

You can get a specific element of a list using `list[element_number]` -- but note Python numbering starts at zero!

l[0]

This means it can only be accessed from elements `l[0]`, `l[1]`, and `l[2]`.

We can test whether `l[3]` throws an error using the following code
(this also allows the notebook to continue running, where leaving it as an
error would halt it).

try:
    l[3]
except:
    print('List l cannot be accessed as l[3]')

You can apply functions to each element of a list with a `for` loop, a technique called *list comprehension*.

*We'll learn more data-analysis ways to do this soon.*

[i * 2 for i in l]

## Setup

Python is a vast general-purpose language, so you have to use packages relevant to your field of study.

For tabular data analysis, like what you'd do in R or Python, always
load the `pandas` and `numpy` packages.
`pandas` gives access to R-style `DataFrame`s, and `numpy` is
the vector-math backbone for `pandas` that can also be used for
random number generation, matrix math, logical operations, and more.

![](https://miro.medium.com/max/800/1*9IU5fBzJisilYjRAi-f55Q.png)

(`pandas` actually gets its name from `pan`el `da`ta)

The `import` keyword loads packages.

import pandas
import numpy

numpy.exp(1)

numpy.power(3, 2)

### Aliases

When loading a package, you can give it an **alias** with the `as` keyword to make it more concise to load.

Widely used packages have canonical aliases, and `pandas` and `numpy` have been
de facto assigned `pd` and `np`, respectively. Try this out here:

(Also try hitting Tab after the `as`!)

import pandas as pd
import numpy as np

Now you can call functions and constants in the packages using the shorter aliases.

np.sin(np.pi / 2)

### Loading modules and functions

*Note: Not needed for today's class, but will be good to know for viewing other Python code.*

Some packages have multiple *modules*, or sets of related functions, which can be loaded separately. For example, `numpy`'s `random` module contains functions
for generating random numbers.

from numpy import random

You can even import specific functions from packages or modules.
For example, `randn` generates numbers from the standard normal distribution.

from numpy.random import randn

Now each of these three function calls does the same thing:
generate 10 random numbers from the standard normal distribution.

randn(10)

random.randn(10)

# Type out the third, using the np prefix from before.
# Also try using tab after the dots for code completion and and open parenthesis
# for function documentation.
# ANSWER:
np.random.randn(10)

## Vector operations in `numpy` and `pandas`

Vector/array operations are integral to scientific computing in Python. Like `gen` in Stata and `apply` in R, `numpy` and `pandas` include rich
sets of vectorized functions to run common code over records quickly.

One way to take advantage of this is to pass lists to `numpy` functions; this often produces a new `array` with the same number of elements.

np.exp([0, 1, 2])

Arrays can be passed into other functions, and aggregated!

np.exp([0, 1, 2]).sum()

**Exercise:** If Jamie invests \$1 per year and gets 5% return each year, how much will they have after 3 years?

Here's a brute-force way, but how can you use lists?

np.power(1.05, 1) + np.power(1.05, 2) + np.power(1.05, 3)

# Try to do the same more concisely by passing a list to `np.power`.
# ANSWER:
np.power(1.05, [1, 2, 3]).sum()

## Exploratory analysis in `pandas`

Time for real data! Let's import data to use in the regression analysis, using the `pandas` `read_csv` function. `read_csv` takes local file paths or URLs, and automatically decompresses files.

Since this is a large file, we'll start by saving the raw file, and then creating a copy to work with. If you mess something up with `cps`, just re-run starting with the `cps = ` cell to avoid re-downloading it.

cps_raw = pd.read_csv('https://github.com/UBICenter/pfd_spm/raw/master/data/spm_state.csv.gz')

cps = cps_raw.copy(deep=True)  # This creates a real copy (not a reference).

`cps` is now a `pandas` `DataFrame` object.

We can see the first and last five records by just printing the dataset.

cps

This microdata file is a combination of (a) historical Supplemental Poverty Measure (SPM) estimates from the Columbia Center on Poverty and Social Policy, and (b) demographics from the Current Population Survey March Supplement (ASEC) files, from IPUMS. It has the following columns:
* **`year`**: Year; covers 1967 to 2015. (Reporting year, not the following year the survey was administered, as CPS IPUMS defines `year`.)
* **`statefip`**: FIPS code for the respondent's US state of residence.
* **`age`**: Respondent age.
* **`female`**: Whether respondent is female.
* **`poor`**: Whether the respondent's SPM unit (comparable to household) has resources below their SPM poverty threshold.
* **`w`**: Respondent's survey weight.

We can see summary statistics with the `describe` command.

cps.describe()

***Interpretation question:*** What share of *records* is poor in the dataset? Does this represent the average poverty rate over the period?

ANSWER: 17.55% of records are poor (mean of `poor`).
The average poverty rate will differ, as it will have to be weighted by `w`.

### Working with `pandas` `DataFrame`s

To get a single column from a `DataFrame`, use `df['column_name']`.

cps['year']

You can manipulate these directly--no `for` loops needed. For example, here's a column representing $age^2$.

cps['age'] ** 2

The syntax to add or revise a column is the same: `df['column'] = values` (no `<-` like in `R`!).

Since the treatment group is individuals in Alaska, we'll need a flag to identify them. Noting that Alaska is FIPS code 2, let's add this here.

cps['alaska'] = cps['statefip'] == 2

To select multiple columns, use double-brackets:
`df[['col1', 'col2']]`. This is really telling `pandas`,
"I'm giving you a list of column names, give me a `DataFrame`
with those columns."

Let's use that to check how our `alaska` assignment worked.

cps[['statefip', 'alaska']]

That's not so helpful, given the number of rows.

Instead a good way to check is the `groupby` function.
We don't have time to go through the full power of `groupby`, but let's see one example.

cps.groupby('alaska')['statefip'].unique()

...and one more fun one to show inline Jupyter plots.

*Note: This is not the poverty rate since it's not weighted!*

cps.groupby('year')['poor'].mean().plot()

***Exercise:*** Add three new columns to `cps` for the regression:
1. **`age2`** for $age^2$
2. **`post`** for the post period (the Permanent Fund Dividend was introduced in 1982)
3. **`alaska_post`** for the DD variable (hint: since those are both `True`/`False` rather than 0/1, use the `&` operator instead of `*`)

# Add age2, post, and alaska_post here:
# ANSWER:
cps['age2'] = cps.age ** 2
cps['post'] = cps.year >= 1982
cps['alaska_post'] = cps.post & cps.alaska

### Filtering data

The last thing we want to do before running regressions is
filtering `DataFrame`s. Doing this is similar to selecting specific columns, but in this case we want to pass a `True`/`False` vector to the square brackets. For example, here are all the people in Alaska:

cps[cps['alaska']]

We could do a DD with the full dataset, but
we'd probably want year fixed effects if we did. Instead, let's just filter for first year of the Permanent Fund Dividend, and the year before that (1981 and 1982), using the `isin` function, and make it a new `DataFrame`.

cps8182 = cps[cps['year'].isin([1981, 1982])]

## Regressions in `statsmodels`

`statsmodels` is the primary Python package for statistical analysis like regression. We'll start by loading the `api` module, which provides a common way of specifying regressions.

import statsmodels.api as sm

We'll use the `WLS` function for weighted least squares, since our survey data is weighted. Let's see what that looks like with tab completion

# Type sm.WLS( and hit tab to see the documentation.

OK, so the first argument is the outcome, for us that'll be poverty status. The second is the regressors, and the third will be the weights.

We're going to try something that will throw an error, so we'll use the `try`/`except` statement to ensure the notebook can fully run, this time also printing the error message we'd have gotten.

try:
    sm.WLS(cps8182['poor'], cps8182[['alaska', 'post', 'alaska_post']],
           cps8182['w'])
except Exception as e:
    print(e)

Huh, that's a weird error. Let's use the `SEARCH STACK OVERFLOW` feature to find a solution (only shows up in Colab if removing the `try`/`except` structure).

...

...

OK, let's multiply it by 1 to transform bools to integers and try again.

cps8182 *= 1

sm.WLS(cps8182['poor'], cps8182[['alaska', 'post', 'alaska_post']],
       cps8182['w'])

No error! But this just constructs the model, we now have to fit it.

Let's save the fitted model as an object.

dd = sm.WLS(cps8182['poor'], cps8182[['alaska_post', 'alaska', 'post']],
            cps8182['w']).fit()

To see the results, use `.summary()`.

dd.summary()

Notice anything missing?

One last step (for real!):

cps8182 = sm.add_constant(cps8182)

dd = sm.WLS(cps8182['poor'], cps8182[['alaska_post', 'alaska', 'post', 'const']],
            cps8182['w']).fit()

dd.summary()

Let's add some controls.

dd_controls = sm.WLS(cps8182['poor'], 
                     cps8182[['alaska_post', 'alaska', 'post',
                              'female', 'age', 'age2', 'const']],
                     cps8182['w']).fit()

dd_controls.summary()

## Publication-grade regression tables in `stargazer`

`stargazer` is a popular R package for creating $\LaTeX$ regression tables,
which has now been (mostly) ported to Python.

To install the latest version, go straight to GitHub (also available other ways).

try:
    import stargazer
except ImportError:
    !pip install git+https://github.com/mwburke/stargazer.git    

from stargazer import stargazer as sg

sg.Stargazer([dd, dd_controls])

sg.Stargazer([dd, dd_controls]).render_latex()