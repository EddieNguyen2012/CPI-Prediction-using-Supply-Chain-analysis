from dash import html, dcc, Input, Output
import plotly.express as px
from Nav_bar import create_navbar
import pandas as pd

RED= '#D85840'
CHERRY = '#5D241A'
WHITE = '#F7F7E6'

ml_prediction = pd.read_csv('Data/ML_Prediction.csv', parse_dates=['DATE'], index_col=['DATE'])
diff_y = pd.read_csv('Data/Diff_CPI.csv', parse_dates=['DATE'], index_col=['DATE'])
original_data = pd.read_csv('Data/final.csv', parse_dates=['DATE'], index_col=['DATE'])
mean_only = pd.read_csv('Data/mean_only_data.csv', parse_dates=['DATE'], index_col=['DATE'])

def update_background(fig, color):
    fig.update_layout(
        paper_bgcolor='#f7f7e6',
        plot_bgcolor='#f7f7e6',
        xaxis=dict(showgrid=True, gridcolor='#5D241A'),  # Change gridline color
        yaxis=dict(showgrid=True, gridcolor='#5D241A', zeroline=True, zerolinecolor='#5D241A'),
        font=dict(family='Poppins', color=color),
        title_x=0.5,
        showlegend=False
    )
    return fig

nav = create_navbar('Methodology and Results',
                    background_fill=RED, text_color=WHITE)

body = html.Div(
    className='methodology-main-body',
    children=[
        html.H1(className='heading-1-red', title = 'Methodology and Results'),
        html.H2(className='subheading-1-red', children='Exploratory Data Analysis'),
        html.H3(className='subheading-2-red', children='Basic Properties'),
        html.Div(className='paragraph-red', children=[
            """
            Before working with the data, we will have to get to know it. The data was collected from the 
            government departments' APIs so they are very clean already. Except that because each department has a 
            different way to record time, we need to reformat the date time data into the pandas datetime format for 
            convenience. For Consumer Expenditure Index, the data was collected quarterly. Thus, we will interpolate 
            it into month period to match other data.
            """,
            html.Br(),
            html.Br(),
            """
            After the pre-processing step, the final data's properties are:
            """,
            html.Br(),
            html.Br(),
            html.Img(className='table', src='assets/images/Data Properties.png', alt='Data Properties table'),
            html.Div(className='image-description-red', children='Table 1.1: Table of basic properties of the original data'),
            html.Br(),
            html.Br(),
            """
            And the features are:
            """,
            html.Br(),
            html.Br(),
            html.Img(className='table', src='assets/images/Data Features.png', alt='Data Features table'),
            html.Div(className='image-description-red', children='Table 1.2: Table of original features table'),
            html.Br(),
            html.Br(),
            """
            For the availability, the Received Price Index for Horticulture and Food Fish are not available before 2018. Hence
            we need to perform imputation before proceeding 
            with the analysis. For the missing commodities in RPI, we want use the changes in other commodities to predict
            their price in the past so, we picked KNN Imputation to do it.
            """,
            html.Br(),
            html.Br(),
            html.Div(className='image-frame', children=[
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/KNN_Imputed_boxplot_for_HORTICULTURE_TOTALS.png', alt='Horticulture KNN Imputation result',
                             style={'width': '100%'}),
                    html.Div(className='image-description-red', children='Table 1.3a: Box plot of KNN Imputation result for Horticulture')
                ]),
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/KNN_Imputed_boxplot_for_FOOD_FISH.png', alt='Food Fish KNN Imputation result',
                             style={'width': '100%'}),
                    html.Div(className='image-description-red', children='Table 1.3b: Box plot of KNN Imputation result for Fish Food')
                ])
            ]),
            html.Br(),
            html.Div(className='image-group', children=[
                html.Img(className='image', src='assets/Plots/Imputed_RPI_timeseries.png', alt='RPI Timeseries after KNN Imputation result',
                         style={'width': '70%'}),
                html.Div(className='image-description-red', children='Table 1.3c: Timeseries plot of RPI after KNN Imputation')
            ]),
            html.Br(),
            """
            After the imputation, although the distribution of both features remained similar, the data range shifted significantly.
            There are more outliers appear in the high value range. But, when we compare the imputed values to other RPI
            using the timeseries line plots, they follow the shift of other RPI closely. So, the KNN Imputation can
            estimate the past values of FOOD FISH and HORTICULTURE RPI very well and successfully filled the NA values.
            """
        ]),
        html.H2(className='subheading-1-red', children='Statistical Analysis'),
        html.Div(className='paragraph-red', children=[
            """
            The desired models are Auto-Regressive Integrated Moving Average with eXogeneous (ARIMAX), XGBoost, 
            Long-short-term Memory (LSTM). In these models, ARIMAX require that 
            """,
            html.Br(),
            html.Br(),
            """
            1. The data is stationary
            """,
            html.Br(),
            html.Br(),
            """
            2. The residual series must not exhibit significant serial correlation
            """,
            html.Br(),
            html.Br(),
            """
            3. If the dependent variable required a transformation to achieve stationarity, that same transformation
             would also be applied to the independent-variable candidates,
            """,
            html.Br(),
            html.Br(),
            """
            4. The exogenous variables comprising the final model must not exhibit a significant degree of multicollinearity.
            """,
            html.Br(),
            html.Br(),
            """
            To get started, we will first check the stationary and find out the transformation needed for CPI and then 
            apply it for other features. Also, we will need to check the seasonality as well as serial correlation between
            the independent and dependent variables.
            """
            ]),
        html.H3(className='subheading-2-red', children='ARIMAX Assumption Check: Stationary'),
        html.Div(className='paragraph-red', children=[
            """
            Consumer Price Index as a CPI always increase in a long period. So, transformation is needed to achieve
            stationary for our dependent series. In this case, we performed multi level of differencing and use Adhesive
            Dickey-Fuller (ADF) test to pick the best degree of differencing. Differencing is done by subtracting the
            current value by the previous value in the time order.
            """,
            html.Br(),
            html.Div(className='image-frame', children=[
                html.Div(className='image-group', children=[
                    dcc.Graph(id='plot', figure=update_background(px.line(original_data['Food and Beverages CPI (target)'],
                                                                          width=600,
                                                                          color_discrete_sequence=[RED]), RED)),
                    html.Div(className='image-description-red', children='Figure 2.1a: Timeseries of the original CPI')
                ]),
                html.Div(className='image-group', children=[
                    dcc.Graph(id='plot', figure=update_background(px.line(diff_y,
                                                                          width=600,
                                                                          color_discrete_sequence=[RED]), RED)),
                    html.Div(className='image-description-red', children='Figure 2.1b: Timeseries of one-time-differenced CPI')
                ]),
            ]),
            html.Br(),
            """
            Originally, Ad-Fuller test give out a test statistic of 0.75 with p-value of 0.99. This means that we cannot
            reject the null hypothesis, so there is no stationary in the CPI data. we applied differencing technique on
            the data with degree 1-4 to test out. The result shows that at degree 1, CPI data is already station with
            p-value of 0.025. So we will proceed with one degree of differencing. This means that all other variables
            will also be transformed using one time of differencing.
            """
        ]),
        html.H3(className='subheading-2-red', children='ARIMAX assumption check: Seasonality'),
        html.Div(className='paragraph-red', children=[
            """
            In Figure 2.1b, we see that the differenced CPI series does not show a significant seasonality trend. 
            We will perform seasonality decomposition to confirm it.
            """,
            html.Br(),
            html.Br(),
            html.Div(className='image-group', children=[
                html.Img(className='image', src='assets/Plots/Seasonality_decomposition.png', alt='Seasonality Decomposition Result',
                         style={ 'width': '60%'}),
                html.Div(className='image-description-red', children='Figure 2.2: Seasonality Decomposition Result')
            ]),
            """
            The decomposition shows that there is a trend in the CPI data and also seasonality by month. When double check it using the plot of true CPI value 
            versus trend + seasonal data from the decomposition, the result is very promising.
            """,
            html.Br(),
            html.Br(),
            html.Div(className='image-group', children=[
                html.Img(className='image', src='assets/Plots/SLT_prediction.png', alt='SLT Prediction',
                         style={ 'width': '70%'}),
                html.Div(className='image-description-red', children='Figure 2.3: Seasonal and Trend decomposition using Loess')
            ]),
            """
            The line can capture the general trend of the change of CPI. For extra information, we performed anamoly detection to identify the irregular changes of
            CPI data in the dataset. 
            """,
            html.Br(),
            html.Br(),
            html.Div(className='image-frame', children=[
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/Anamolies_detection.png', alt='Anamolies detection plot',
                             style={ 'width': '100%'}),
                    html.Div(className='image-description-red',
                             children='Figure 2.4a: Residual plot with 95% confidence intervals'),

                ]),
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/Anamolies_points.png', alt='Anamolies points plot',
                             style={ 'width': '100%'}),
                    html.Div(className='image-description-red',
                             children='Figure 2.4: Anamolies points mapped on the diffrenced CPI time series'),

                ]),
            ]),
            """The threshold that we used to classify anamolies is: """,
            html.Br(),
            html.Br(),
            dcc.Markdown(
                """
                ``` 
                lower bound = residual mean - 3 x residual std 
                upper = residual mean + 3 x residual std 
                ```
                """
            ),
            html.Br(),
            html.Br(),
            """
            Based on the threshold, we observe three anomaly points in 
            April 2019, April 2020, and July 2020. In April 2019, the negative spike can be attributed to changes in 
            the Organization of the Petroleum Exporting Countries’ policies earlier that year and the US-China tariff 
            tensions. These factors disrupted the supply chain, likely causing the spike. In April 2020, the global 
            spread of COVID-19 led to a nationwide lockdown in the US. Panic buying of food and beverages due to 
            fears of a prolonged epidemic caused a sharp increase in the CPI index. By July 2020, the CPI spike eased 
            due to reduced consumer spending during the lockdown and government assistance programs.
            """,
            html.Br(),
            html.Br(),
            """
            In conclusion, the one-time-differenced CPI has seasonality and we will account for it in our ARIMAX model 
            so it becomes the Seasonality Autoregressive Integrated Moving Average with eXogeneous variables (SARIMAX)
            """
        ]),
        html.H3(className='subheading-2-red', children='Assumption check: multi-collinearity check'),
        html.Div(className='paragraph-red', children=[
            """
            Initially, when performing the Variance Inflation Factor on all indices (including sub-groups), the test
            statistics are extremely high. To deal with this problem, we performed grouping by calculating the mean 
            value for all the sub groups (i.e.: calculated the mean RPI value using all RPI commodities,...). The final
            data is the one that requires the least grouping but have the best VIF (less than 1.5).
            """,
            html.Div(className='image-group', style={'margin-top': '10px'}, children=[
                html.Img(className='image', src='assets/Plots/VIF_plots.png', alt='VIF plot',
                         style={ 'width': '70%'}),
                html.Div(className='image-description-red',
                         children='Figure 2.5: Bar plot of VIF values of the final data after the feature selection'),

            ]),
            """
            The VIF values of all the features are very close to 1, which indicates that there are almost no
            multi-collinearity among the features and the dependent variable CPI. Hence, we already satisfied all the 
            assumptions for SARIMAX.
            """
        ]),
        html.H2(className='subheading-1-red', children='Feature Engineering'),
        html.Div(className='paragraph-red', children=[
            """
            So far, after the feature selection, our data only has 11 features with 236 rows, which is relatively small.
            Moreover, since this is a time series forecasting problem, we can improve the accuracy of the models by 
            adding lag features, cyclical features and windowing features.
            """
        ]),
        html.H3(className='subheading-2-red', children='Lag Features'),
        html.Div(className='paragraph-red', children=[
            """
            A lag feature is a feature with information about a prior time step of the time series. (Feature-engineering
            API). To create this lag feature, we will use the cross-correlation functions plots of features vs CPI to 
            identify the lags that has the most correlation to the CPI. Then we will create a lag feature at the
             lag for such feature.
            """,
            html.Div(className='image-group', style={'margin-top': '10px'}, children=[
                html.Img(className='image', src='assets/Plots/CCF_of_diff_features_vs_diff_CPI.png', alt='CCF plot',
                         style={ 'width': '70%'}),
                html.Div(className='image-description-red',
                         children='Figure 2.6: Cross-correlation functions plots of all features vs CPI'),

            ]),
            """
            We can see that not all features have significant lag correlation to CPI. We will create lag features for
            variables with significant lag correlations to CPI, focusing on lags with correlations exceeding the 95%
            confidence interval on the CCF plot. After this process, the data size increased to 53 features. However, 
            since lag features creation will shift the data, it will introduce (lag order)s N/A values before the first
            value. For this data, we set 9 as the furthest lag, So we have to discard the first 9 entries of the data to
            maintain the fullness of the data.
            """
        ]),
        html.H3(className='subheading-2-red', children='Cyclical Encoding and Windowing'),
        html.Div(className='paragraph-red', children=[
            """
            For time series data, the timespan (month of the year) has a cyclical characteristic (going back in a cycle
            after a period). Since we identified that CPI has seasonality, we should also convey this data to our models
            in order to represent the seasonality characteristic of CPI.
            """,
            html.Br(),
            html.Br(),
            """
            In time series forecasting, future values can be predicted by creating window features, which is created by
            using mathematical operations on past time series data (Feature engineering API). For this data, we will use
            basic windowing techniques to create mean and standard deviations of CPI in the past 3 windows.
            """
        ]),
        html.H2(className='subheading-1-red', children='Model Training'),
        html.H3(className='subheading-2-red', children='SARIMAX'),
        html.Div(className='paragraph-red', children=[
            """
            For SARIMAX model, we have the following parameters to consider:
            """,
            html.Br(),
            html.Br(),
            """
            - p: Autoregressive lag order
            """,
            html.Br(),
            html.Br(),
            """
            - d: Difference degree
            """,
            html.Br(),
            html.Br(),
            """
            - q: Moving Average lag order
            """,
            html.Br(),
            html.Br(),
            """
            - P: Seasonal autoregressive lag order
            """,
            html.Br(),
            html.Br(),
            """
            - D: Seasonal difference degree
            """,
            html.Br(),
            html.Br(),
            """
            - Q: Moving Average lag order
            """,
            html.Br(),
            html.Br(),
            """
            - S: Seasonal frequency
            """,
            html.Br(),
            html.Br(),
            """
            As our data is monthly, we will use S=12. Moreover, we use d=1 as a result of Ad-Fuller test in the 
            previous part. For other data, we will use AutoCorrelation Function (ACF) Plot and Partial AutoCorrelation
            Function (PACF) Plot to initially identify. However, note that we may need to change all of them during the
            training process.
            """,
            html.H4(className='subheading-2-red', children='ACF and PACF plot'),
            html.Div(className='image-frame', children=[
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/ACF.png', alt='ACF plot',
                             style={ 'width': '90%'}),
                    html.Div(className='image-description-red',
                             children='Figure 3.1a: ACF Plot of Differenced CPI'),

                ]),
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/PACF.png', alt='PACF plot',
                             style={ 'width': '90%'}),
                    html.Div(className='image-description-red',
                             children='Figure 3.1b: PACF plot of diffrenced CPI'),

                ]),
            ]),
            """
            In the ACF plot, the correlation drops within the 95% confidence interval after 8 lags, so we chose a 
            lag order of 8 (q=8). In the PACF plot, the cutoff happens after lag 2, so we selected p=2. The PACF also 
            shows a pattern at multiples of 9, suggesting a 9-month seasonality, so we set S=9.
            """,
            html.Br(),
            """
            For P and Q, we will use grid search strategy and cross validation to test out for the model with the 
            best metrics (AIC, BIC, Ljung-Box p-value). To train the model, we will cut the last 6 months as the test
            set. After the training, the best model is SARIMAX(0,1,0)(0,1,1)[9] with the result:
            """,
            html.Div(className='image-frame', children=[
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/SARIMAX_prediction_whole_data.png', alt='SARIMAX whole data plot',
                             style={'width': '100%'}),
                    html.Div(className='image-description-red',
                             children='Figure 3.2a: SARIMAX result on train data'),

                ]),
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/SARIMAX_prediction.png', alt='SARIMAX result on Test',
                             style={'width': '100%'}),
                    html.Div(className='image-description-red',
                             children='Figure 3.2b: SARIMAX result on test data'),

                ]),
            ]),
            html.Div(className='image-group', children=[
                html.Img(className='image', src='assets/Plots/SARIMAX_diagnosis.png',
                         alt='SARIMAX Diagnosis plots',
                         style={'width': '80%'}),
                html.Div(className='image-description-red',
                         children='Figure 3.2c: SARIMAX Diagnosis plots'),

            ]),
            """
            Some key results that we can tell from this model:
            """,
            html.Br(),
            html.Br(),
            """
            - Frozen Food Manufacturing PPI has a coefficient of -0.0500 with a p-value of 0.000, indicating a significant 
            negative impact on the target variable.
            """,
            html.Br(),
            html.Br(),
            """
            - Dried and Dehydrated Food Manufacturing PPI is also significant with a positive coefficient (0.0480).
            """,
            html.Br(),
            html.Br(),
            """
            - Poultry RPI has a negative coefficient (-0.0075) with a p-value of 0.028, indicating significance as well.
            """,
            html.Br(),
            html.Br(),
            """
            - **Ljung-Box Test (Q)**: The result (0.39) and its probability (0.59) indicate that there is low significant 
            autocorrelation in the residuals at lag 1, suggesting the model is well-fitted.
            """,
            html.Br(),
            html.Br(),
            """
            - **Jarque-Bera Test (JB)**: A high value (61.94) with a very low probability (0.00) indicates that the 
            residuals are not normally distributed, which may need further examination.
            """,
            html.Br(),
            html.Br(),
            """
            - **Heteroskedasticity Test**: The H statistic (1.42) with a significant probability (0.14) suggests that 
            there may be some level of heteroskedasticity in the model.
            """,
            html.Br(),
            html.Br(),
            """
            Based on the prediction on train and test set, we can see that SARIMAX performs very well with MSE around
            0.13 on train set and 0.3 on test set. Even though there are some issue persist with the result like the
            normality of the residuals and heteroskedasticity, we can still see that SARIMAX does it job to predict 
            the CPI change very closely.
            """
        ]),
        html.H3(className='subheading-2-red', children='XGBoost Regression'),
        html.Div(className='paragraph-red', children=[
            """
            For XGBoost, we used TimeSeriesSplit() to create time-splitting-based cross-validation dataset to feed into 
            the model. we chose ``n_splits=10`` due to the small sample size. we also tested other values but 10 gives the 
            best performance in term of MSE and MAE. So far, we used GridSearchCV to tune the model and the best model 
            performance is as follows
            """,
            html.Div(className='image-frame', children=[
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/XG_Boost_prediction_train.png', alt='XGBoost train prediction',
                             style={'width': '100%'}),
                    html.Div(className='image-description-red',
                             children='Figure 3.3a: XGBoost result on train data'),

                ]),
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/XG_Boost_prediction_test.png', alt='XGBoost result on Test',
                             style={'width': '100%'}),
                    html.Div(className='image-description-red',
                             children='Figure 3.3b: XGBoost result on test data'),

                ]),
            ]),
            html.Div(className='image-group', children=[
                html.Img(className='image', src='assets/Plots/MSE_and_MAE_of_best_XGBoost_model.png',
                         alt='XGBoost Diagnosis plots',
                         style={'width': '80%'}),
                html.Div(className='image-description-red',
                         children='Figure 3.3c: MSE and MAE of XGBoost model'),

            ]),
            """
            From the prediction results, we can see that the model can capture the trend acceptably on the training data.
            However, on the test data, it seems not as good. This indicate that the model need more fine-tuning and 
            improvement on the data engineering as well as more entries to improve the learning. Interestingly, on the MSE
            and MAE plots, the metrics on test set are lower than the prediction. This means that even though it can make
            predictions already, the model might be underfit. So, we can see that on this size of data, SARIMAX performs
            better than XGBoost.
            """
        ]),
        html.H3(className='subheading-2-red', children='LSTM Regression Model'),
        html.Div(className='paragraph-red', children=[
            """
                    Long Short-Term Memory is a Neural Network architecture that is widely used to solve regression problem for
                    timeseries data. It captures long-term dependencies in sequential data by using memory cells and gates to
                    regulate information flow. 
                    """,
            html.Br(),
            html.Br(),
            """
            Since the data is simple, we started with very simple structure for this model
            """,
            html.Div(className='image-group', children=[
                html.Img(className='image', src='assets/Plots/LSTM_layers.png',
                         alt='LSTM layers',
                         style={'width': '80%'}),
                html.Div(className='image-description-red',
                         children='Table 5.1: LSTM structure'),
            ]),
            """
            we used data sequencing techniques to combine the all the features into an array and split into 12 sequences for
            the training. Then, we used train_test_split() to split the data into training and validation sets with the ratio
            of 0.8 and 0.2. respectively. The results are as follows:
            """,
            html.Br(),
            html.Br(),
            html.Div(className='image-frame', children=[
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/LSTM_prediction_train.png', alt='LSTM train prediction',
                             style={'width': '100%'}),
                    html.Div(className='image-description-red',
                             children='Figure 5.1a: LSTM result on train data'),

                ]),
                html.Div(className='image-group', children=[
                    html.Img(className='image', src='assets/Plots/LSTM_prediction_test.png', alt='LSTM result on test',
                             style={'width': '100%'}),
                    html.Div(className='image-description-red',
                             children='Figure 5.1b: LSTM result on test data'),

                ]),
            ]),
            html.Div(className='image-group', children=[
                html.Img(className='image', src='assets/Plots/LSTM_learning_curve.png',
                         alt='LSTM Learning curve',
                         style={'width': '80%'}),
                html.Div(className='image-description-red',
                         children='Figure 5.1c: LSTM Learning Curve using validation loss'),

            ]),
            """
            The model get Mean Absolute Error (MAE): 0.9298, Mean Squared Error (MSE): 1.329, Root Mean Squared Error
            (RMSE): 1.1532. So far those metrics are worse than SARIMAX and XGBoost. If we look at the
            learning curve, it converge very quick at first and then suddenly slow down and stable after 400 epochs. This
            indicates that the model is currently underfit. However, the prediction are very close to the real values 
            suggesting that the model has potential to perform better.
            """
        ]),
        html.H2(className='subheading-1-red', children='Feature Importance'),
        html.Div(className='paragraph-red', children=[
            """
            So far, the PPI indices are the ones that contribute the most to the XGBoost model using SHAPley 
            values. 
            """,
            html.Div(className='image-group', children=[
                html.Img(className='image', src='assets/Plots/SHAP_plot.png',
                         alt='SHAPley plot',
                         style={'width': '70%'}),
                html.Div(className='image-description-red',
                         children='Figure 4.1: Feature Importance on data in specific range ranking with Shapley value'),

            ]),
            """
            The SHAPley plot shows that CPI windowing values contribute the most to the high CPI change prediction. PPI and
            mean RPI indices are the most impactful features that contribute to the rest of the CPI changes. So, we can 
            conclude that RPI and PPI values are significant to the CPI changes.
            """,

        ]),
        html.H2(className='subheading-1-red', children='Conclusion'),
        html.Div(className='paragraph-red', children=[
            """
            Predicting CPI values is an essential task in business strategy, economics, or investment decision making. 
            By identifying the changes along the supply chain, we can predict the change in CPI using the models as 
            shown above. We can explain the result of this model as an estimate of inflation of F&B product prices as it 
            reflect the changes in the production cost, which is a major factor in pricing strategy. We can compare the 
            result of those models with the CPI calculated by the traditional method to validate how 'bad' or 'good' the
            inflation in F&B industry is at an exact time span. 
            """,
            html.Br(),
            html.Br(),
            """
            Each model has their own pros and cons compare to each other. For SARIMAX, as a Time series forecasting
            analytics model, the pros are that it can work on relatively small dataset; it can show accurately the 
            current trend of the economy by capturing the changes in previous lags; it is more efficient and easier to
            interpret. However, it can predict accurately in short terms as it rely heavily on the past values, hence if
            the prediction target is further away from the current data, it may be not accurate as the predictors are
            already predicted values.
            """,
            html.Br(),
            html.Br(),
            """XGBoost has all the pros of SARIMAX models and can even solve the cons of SARIMAX. Moreover, 
            if we perform retraining frequently and keep calculating the Feature Importance of the data, 
            we can identify unusual changes along the supply chain. But, this model requires more data to 
            learn the trend before starting to predict correctly. But, with the current state of technology, this is not
            a big problem.""",
            html.Br(),
            html.Br(),
            """LSTM shows some promising potential so far. For deep learning models like LSTM, it requires 
            even more data than traditional machine learning methods like XGBoost. Hence, we need to increase the 
            data size before coming to any conclusion about this model. However, with the prediction on test set and 
            train set, LSTM captured the general trend of CPI and predicted very close to the changes in the test 
            set, even if the test set include data that are more unusual than the training data. Maybe with some scaling
            and additional data, this will be the solution for future development of this project.""",
            html.Br(),
            html.Br(),
            """
            In this project, talking about the performance of all models based on the available data, we can say that
            SARIMAX is performing better than XGBoost in short-term, while LSTM tends to capture the unusual trend very 
            well. By comparing the mean square error and mean
            absolute error, SARIMAX have captured the trend very well and made relatively accurate prediction.
            XGBoost and LSTM worked but currently underfit due to lack of data. But, so far, this is an acceptable
            result with the current dataset.
            """
        ]),
        html.H2(className='subheading-1-red', children='Suggestions'),
        html.Div(className='paragraph-red', children=[
            """1. Data size: Currently, we only examine 5 different indices relating to F&B CPI due to the time 
            constraint. For further improvement, we need to reassess the production cost breakdown to explore new indices 
            that possibly can help explaining the inflation of food consumer price. Moreover, we will extend the data 
            range to further to the past if possible.""",
            html.Br(),
            html.Br(),
            """
            2. Reassess feature selection and data engineering phases: So far, in the feature selection, we only cared
            about the lag order and the multi-collinearity of each feature. For future development, we will reassess the
            features needed using the coefficients and p-value (in SARIMAX), or SHAPley correlation (in XGBoost) to 
            filter out all the features that does not help the determination of CPI.
            """,
            html.Br(),
            html.Br(),
            """
            3. Deploying the model and automated retraining process: To put the model in use, we will implement the
            model to be executable on web services. Then we will create the automated process so that the model can 
            relearn and capture the current trend of CPI better. 
            """
        ])
    ]
)

footer = html.Div(
    className='footer-red',
    children=[
        html.Div(
            className='footer-content-red',
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

def create_page_processing():
    layout = html.Div(
        className='methodology-page',
        children=[
            nav,
            body,
            footer
        ])
    return layout