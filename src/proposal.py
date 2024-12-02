from dash import html, dcc
from Nav_bar import create_navbar

RED = '#E84324'
BLUE = '#38499E'
WHITE = '#f7f7e6'

nav = create_navbar('Project Proposal',
                    background_fill=BLUE, text_color=WHITE)

body = html.Div(
    className='proposal-main-body',
    children=[
        html.H1(className='heading',
                children="Proposal: Predicting Inflation in Food and Beverages industry using supply chain pass-through cost analysis"),

        html.H2(className='subheading-1', children="Project Summary"),
        html.Div(className='paragraph', children=
        """This project aims is to explore and create a model that predict the inflation of food and 
            beverages price using the Food and Beverages Consumer Price Index. This model can be used for 
            monitoring material price, food price inflation, or market shifts that supports decision-making 
            processes for companies in F&B as well as Agriculture industry. Moreover, it can give ordinary 
            users forecasted changes (positive or negative) in food and beverages price for daily shopping 
            routines. Ultimately, this project want to explore a new way to integrate more information to the 
            calculation of the F&B Price Index, which may result in more accurate result than the traditional 
            method.

            The proposed model will be trained using historical data of Chained Consumer Price Index, 
            Producer Price Indices, Consumer Expenditures from the Bureau of Labor Statistics (BLS). Another 
            source of data is the Received Price Indices data from the US Department of Agriculture (USDA) to 
            provide insights about the amount of revenue that farmers received per an area of crop unit. By 
            using the supply chain pass-through cost model, we will predict the CPI by using PPI, CE, 
            and RPI as the predictors."""
                 ),
        html.H2(className='subheading-1', children="Data Sources"),
        html.H3(className='subheading-2', children="Bureau of Labor Statistics Data API"),
        html.Div(className='paragraph', children=
        """The main source that provide Food and Beverages Consumer Price Index, Producer Price 
            Index, and Consumer Expenditures. The data is collected monthly by BLS agents, 
            who are randomly assigned to different places across the United States to monitor and 
            report the daily change in item's price. BLS use CPI survey, which collects about 94,
            000 prices and 8,000 rental housing units quotes each month. Those surveys are conducted 
            within businesses and households."""
                 ),
        html.H3(className='subheading-2', children="US Department of Agriculture Data API"),
        html.Div(className='paragraph', children=
        """The Received Price Index from the USDA is gathered through surveys, offering a 
            comprehensive look at the prices farmers receive for their products. Data is collected 
            both monthly and quarterly, providing timely insights into price trends. This index 
            covers a wide geographic range, capturing data at both national and regional levels, 
            which helps reflect the diversity of agricultural markets across the country. These 
            surveys are crucial for tracking the economic conditions faced by agricultural 
            suppliers."""
                 ),
        html.H3(className='subheading-2', children="US Energy Information Administration"),
        html.Div(className='paragraph', children=
        """
            Fill here N/A
            """
                 ),
        html.H2(className='subheading-1', children="Expected Major Findings"),
        html.H3(className='subheading-2', children='1. CPI Forecasting model'),
        html.Div(className='paragraph', children=
        """A model that can forecast the inflation of Food and Beverages industry 
            reflected via the CPI index. Santiago et al. (2024) suggested that firms use the 
            price change along the supply chain as evidence for their pricing strategy. Using 
            the supply chain pass through cost analysis, we will create a model that use the 
            changes in price received by agricultural suppliers (RPI), 
            manufacturers/retailers producer price (PPI), as well as the consumers 
            substitution behavior (CCPI) to predict the inflation (CPI)."""
                 ),
        html.H3(className='subheading-2',
                children='2. Which USDA sectors (e.g., LIVESTOCK, HORTICULTURE, VEGETABLES) have the largest impact on CPI?'),
        html.Div(className='paragraph', children=
        """By analyzing price trends across different agricultural sectors, we aim to 
            determine which commodities contribute most to fluctuations in consumer prices. 
            This insight can help policymakers and businesses understand the drivers of 
            inflation in food markets and anticipate changes in consumer spending patterns. 
            The analysis will also aid in developing predictive models for better forecasting 
            CPI movements."""
                 ),
        html.H3(className='subheading-2', children='3. The comparison of Timeseries and Machine Learning approach.'),
        html.Div(className='paragraph', children=
        """The objective is to compare the effectiveness of traditional time series 
            forecasting methods, such as ARIMA or SARIMAX, with machine learning models, 
            such as XGBoost or LSTM, in predicting the Consumer Price Index (CPI) for food 
            and beverages. Time series models rely on historical CPI data and account for 
            seasonality and trends, while machine learning models can incorporate a broader 
            set of features, such as commodity prices, energy costs, and economic indices. 
            This comparison will evaluate which approach provides more accurate predictions, 
            handles complex relationships better, and adapts more effectively to changing 
            market conditions."""
                 ),
        html.H2(className='subheading-1', children='Preprocessing Steps'),
        html.H3(className='subheading-2', children='1. Data Collection:'),
        html.Div(className='paragraph', children=
        """
            Collecting historical data from the 3 APIs using REST API provided from the BLS, BEA, 
            and USDA official websites.
            """
                 ),
        html.H3(className='subheading-2', children='2. Cleaning and Formatting:'),
        html.Div(className='paragraph', children=
        """Clean the historical data to handle missing values, inconsistent formats, or outliers. 
            Use aggregation, modification, and formatting to form a uniformed, final dataset with the 
            index is the timeframe of the timeseries."""
                 ),
        html.H3(className='subheading-2', children='3. Data Scaling and Normalization:'),
        html.Div(className='paragraph', children=
        """
            Normalize or scale the features to ensure that different features contribute equally to the model.
            """
                 ),
        html.H3(className='subheading-2', children='4. Pre-training analysis:'),
        html.Div(className='paragraph', children=
        """
            Perform statistical analysis, feature engineering and feature selection to prepare for 
            training the model.
            """
                 ),
        html.H3(className='subheading-2', children='5. Model Training/Testing Split:'),
        html.Div(className='paragraph', children=
        """
            Split the dataset into training and testing sets, ensuring that the split maintains 
            the time-series nature of the data. Refit and reevaluate the performance of the model 
            until achieving the desired accuracy.
            """
                 ),
        html.H2(className='subheading-1', children='Data Analysis and Algorithms'),
        html.H3(className='subheading-2', children='Imputation for Food Fish and Horticulture RPI: Due to the similarity in general RPI change over commodities'),
        html.Div(className='paragraph', children=
        """
        I suspect KNN Imputer can be utilized to fill the those missing value. I will implement the KNN Imputer using Scikit_learn,
        then optimize it with GridSearchCV. I will also check to see its correlation with other metrics (except CPI to prevent bias) then adjust
        the features used for the imputation. Finally, we will compare the distribution to achieve the best result.
        """),
        html.H3(className='subheading-2', children='Difference in trends among groups for PPI, CE and RPI'),
        html.Div(className='paragraph', children=
        """
        For this analysis, I want to corporate repeated ANOVA or regression analysis to determine the differences 
        in changes among groups. If the groups have significant differences, we can proceed to use them as features 
        for our predictors. Else, we have to investigate closely using pairwise comparison to figure out the left-out 
        needed features. 
        """),
        html.H3(className='subheading-2', children='Ranking the commodities on their effect to CPI'),
        html.Div(className='paragraph', children=
        """
        For this analysis, we can use multiple regression analysis to check the 
        correlation of the commodities RPI on CPI. We will use the coefficients to rank the importance of the commodity's effect on CPI. Moreover,
        we can also do the same analysis on PPI sectors.
        """),
        html.H3(className='subheading-2', children='Feature importance'),
        html.Div(className='paragraph', children=
        """
        Since I will use Tree-based algorithms XGBoost and Random Forest, I will use SHAPley value to 
        figure out the feature importance for better interpreting the model.
        """),
        html.H3(className='subheading-2', children='Fitting Machine Learning models'),
        html.Div(className='paragraph', children=
        """
        We will fit the data into XGBoost, Random Forest, and LSTM. After that we will optimize XGBoost
        and Random Forest using GridSearchCV and hand-tune LSTM.
        """),
        html.H3(className='subheading-2', children='Lag and Correlation Computation of CPI for ARIMA model fitting'),
        html.Div(className='paragraph', children=
        """
        From the plot above, we can see that CPI does not have seasonality. However, it does not 
        have stationary. So, we will use differenced values of CPI to fit in the ARIMA model. In the preparation part, we will calculate correlation and
        use ACF/PACF plots to determine feature lag. Then we will fit the data into ARIMA and produce predict some short term value for CPI.
        """),
        html.H3(className='subheading-2', children='Model comparison'),
        html.Div(className='paragraph', children=
        """
        After the fitments, we will compare the results of the models to see which one performed best. I expect to use MSE, ROC AUC, and
        Accuracy to evaluate and comparing the models. After finished comparing my models, I will use
        LazyRegressor to further comparing them with other state-of-the-art algorithms.
        """),
        html.H2(className='subheading-1', children='Data Visualization Plan'),
        html.H3(className='subheading-2', children='Descriptive Analysis'),
        html.Div(className='paragraph', children=[
            """
            For this part, I want to make it a little interesting by mapping the time with US presidency periods.:
            """,
            html.Br(),
            html.Br(),
            """
            - Firstly, I will have a diagram that show the supply chain and the index corresponding to each point in it.
            """,
            html.Br(),
            html.Br(),
            """
            - I will make 5 individual timeseries Line Plots on the same row (4 columns) to show how each index, and utility price (in general) 
            changed throughout the time period. Then, below them will be a big CPI timeseries Line Plot. This is to show how different or similar each index 
            progressed comparing to others. I will also include a switch (maybe list box or radio button) to show the plots in different time periods (I plan
            to use 4 years and map with president name)
            """,
            html.Br(),
            html.Br(),
            """
            - For each index group, I will include Pie Chart or Bar chart to show the ranking of effect (weight) that each commodity change has on the 
            general CPI change. (i.e.: for RPI commodities, rank how is the change of each commodity affect the change of the CPI index to show
            how important it is. In the other words, rank the weight of each commodity). This graph has a button or list box so that user
            can switch between index groups.
            """,
            html.Br(),
            html.Br(),
            """
            - For gas price and electricity price, I will use histogram to show what is the common price throughout the timespan as well as the 
            line plot to show the trend of them. 
            """,
            html.Br(),
            html.Br(),
            """
            - Finally, I will use line plot to show differentiated CPI to show the seasonality of CPI change and point out the unusual peak point (anamolies).
            I can also make annotation to highlight the presidency period
            """
        ]),
        html.H3(className='subheading-2', children='Forecasting Analysis'),
        html.Div(className='paragraph', children=[
            """
            - I will show a line plot of prediction of XGBoost and SARIMAX (maybe LSTM) versus the real value. The 
            prediction will be throughout the available dataset and I will highlight (change the background color) where 
            is the training data and where is the prediction data.
            """,
            html.Br(),
            html.Br(),
            """
            - Then, I will include the SHAP beeswarm to show the which feature affect the outcome of the XGBoost model. 
            """,
            html.Br(),
            html.Br(),
            """
            - If possible, I will also include input boxes where user can input indices values and see how the model will predict it.
            (this includes deploying the models, so I need to take time working on it)
            """
        ]),
        html.H3(className='subheading-2', children='Methodology'),
        html.Div(className='paragraph', children=
        """
        - I will show all the mathematical plots and test results that I conducted to back up the claim and visualizations in a page
        """),
        html.H2(className='subheading-1', children='Web page plan'),
        html.H3(className='subheading-2', children='Project Objective page'),
        html.Div(className='paragraph', children=[
            """
            I will have 4 pages:
            """,
            html.Br(),
            html.Br(),
            """
            - Project Landing page: I will display the descriptive analysis plots here as well as some introduction to the project.
            """,
            html.Br(),
            html.Br(),
            """
            - Proposal page (Project Objective): Everything in this markdown file (beside the results) will be displayed in this page. I will also find the 
            references and put them here.
            """,
            html.Br(),
            html.Br(),
            """
            - Forecasting result: I will put the forecasting analysis result over here together and some link to the methodology page
            """,
            html.Br(),
            html.Br(),
            """
            - Methodology (Analytical Methods): As proposed above, I will put all the mathematical results here to demonstrate how I conducted all the analysis.
            """
        ]),
    ],
)

footer = html.Div(
    className='footer',
    children=[
        html.Div(
            className='footer-content-blue',
            children=[
                'Manh Tuong Nguyen',
                html.Br(),
                'Email: tuong62642@gmail.com',
                html.Br(),
                'GitHub: https://github.com/EddieNguyen2012',
                html.Br(),
                'LinkedIn: www.linkedin.com/in/manh-tuong-nguyen'
            ]
        )
    ],
)


def create_page_proposal():
    layout = html.Div(
        className='proposal-page',
        children=[
            nav,
            body,
            footer
        ]
    )
    return layout
