# Financial Data Analysis & Trend Detection System

## Description

 This project develops a system that utilizes divide-and-conquer techniques to efficiently process, analyze, and report on financial data, aiding in informed decision-making. 

## Key Components and Algorithms

1. **Merge Sort for Time-Series Data Processing**  
   The system employs merge sort to efficiently sort massive datasets, facilitating the arrangement of financial transactions based on timestamps. This sorting step is vital for enabling subsequent operations such as trend detection and moving average computations.

2. **Kadane’s Algorithm for Maximum Subarray**  
   To identify periods of maximum gain or loss, we implement Kadane’s Algorithm, utilizing a divide-and-conquer approach. This algorithm analyzes stock price changes over time to determine the subarray where profit is maximized, thereby allowing users to pinpoint optimal periods for investment or identify potential downturns.

3. **Fast Closest Pair of Points for Anomaly Detection**  
   The closest pair of points algorithm serves to detect anomalies within transaction logs or price fluctuations. By identifying trades or prices that significantly deviate from typical patterns, this approach can uncover unusual spikes or dips that may indicate fraudulent activities or irregular market behaviors.

## Outline

### Input
The system takes a large dataset of stock prices, cryptocurrency prices, or any other asset that is relevant in a time series analysis context. These datasets are in the format of CSV file.

### Step 1: Sort the Data Using Merge Sort
The dataset is sorted by time to prepare it for further analysis. This ensures that other operations can be executed efficiently on a well-organized dataset.

### Step 2: Find Periods of Maximum Gain or Loss
Applying Kadane’s algorithm, to find the sub-periods where stock prices or transaction volumes exhibit the highest gains or losses. The algorithm can be extended to handle two-dimensional data for comparative analyses across different stocks or regions.

### Step 3: Detect Anomalies Using Closest Pair of Points
The divide-and-conquer closest pair of points algorithm identifies anomalies in transaction logs or price fluctuations, which can be crucial for fraud detection or recognizing unusual market behavior.

### Step 4: Generate Reports
The system produces reports detailing periods of maximum profit or loss, trends in stock or transaction prices, and detected anomalies. Visualizations are in the form of a line graphs, utilizing matplot library.

### Output
The system generates a text report and a image of a graph that summarizes market trends, periods of high performance, and suspicious financial transactions.

## Project Components

### Testing and Benchmarking
Rigorous testing through the use of multiple datasets from mutiple different stocks ensured the correctness of the program.

### Performance Analysis
Through experimental results, analysis of the performance of the sorting algorithms occurred. Relatively speaking, the program is very effiecient in its execution time and memory usage.

### Verification of Functionality
Example output utilizing AAPL dataset from 2010 to 2020:![image](https://github.com/user-attachments/assets/dac80d1a-4e7c-4406-baa9-cdc547260de8)
![image](https://github.com/user-attachments/assets/7917e88a-e95a-441f-9cbb-440e65a9362d)
![image](https://github.com/user-attachments/assets/726d0f4a-775e-488a-8a4f-dd71a6b2847c)



