# DCF Model
## Our Problem
The world of business is filled with an abundance of information. Meaningful insights are often based on lengthy, tedious calculations, requiring hours of data collection, number-crunching, and spreadsheet grinding. Students and analysts should be able to focus on more significant and meaningful tasks, such as generating insights and financial decision-making.

## What We Offer
DeepFinalyst collects data from several sources to evaluate companies based on current market values and future projections. Using a deep learning algorithm and collected data, DeepFinalyst analyzes industry patterns and market trends to enhance cash flow predictions, calculate key financial indices, and ultimately provide valuations for specific companies compared to their market values.

## Construction
DeepFinalyst was constructed in two distinct components. This helped segregate segments of the project with drastically distinct functionalities. 

Language: Python, Flask, and HTML.
Modules and APIs: Tensorflow, Numpy, Goldman Sachs Marquee API, and Financial Modelling Prep API.

**Logic**  
The core logic behind the financial analysis process was developed using Python. By combining Tensorflow's neural network implementations with several financial data APIs, such as Marquee, we developed and trained a deep learning algorithm to recognize current industry trends and patterns. This was used in conjunction with existing financial modelling procedures to calculate important financial indices and conduct a DCF analysis given a specific company. 

**Interface**  
The web interface was built using a combination of HTML, CSS, and JavaScript. We used Flask to integrate the interface with our Python scripts, as well as build and deploy our project. Furthermore, JSON was used to model and facilitate data communications between processes. 

## Development Challenges
Finding the necessary data for DeepFinalyst proved exceptionally difficult, as we had to collect and combine data from several different APIs to create a comprehensive analysis. Additionally, the deep learning algorithm is relatively unstable, as historical training data is only relevant until a certain point, after which it becomes too archaic, leaving very little training data to work with.

## Major Accomplishments
It works!!!

## What We Learned
Don't watch anime while working, especially if it's a good one.

## What's next for DeepFinalyst
There are quite a few optimizations we'd like to add on DeepFinalyst. 

**Financial Modelling**  
Improve our financial models by accounting more investment factors if granted further access to advance and detailed datasets.

**Neural Network**  
With more time, we can train a further complex neural network model - e.g. a convolutional neural network. Such changes would improve the effectiveness of training our deep learning algorithm, as it would better identify and adapt to patterns in market data.
