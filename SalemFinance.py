import csv
import matplotlib.pyplot as plt
import math
from datetime import datetime
from typing import List, Tuple

#*** FUNCTION TO READ THE CSV FILE AND PARSE THE DATA INTO A LIST OF DICTIONARIES ***
def read_csv(file_path: str) -> List[dict]:
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                'Date': datetime.strptime(row['Date'], '%m/%d/%Y'),  # Convert string date to datetime object
                'Last': float(row['Last'].replace('$', '').replace(',', '')),  
                'Volume': int(row['Volume']),  
                'Open': float(row['Open'].replace('$', '').replace(',', '')),  
                'High': float(row['High'].replace('$', '').replace(',', '')),  
                'Low': float(row['Low'].replace('$', '').replace(',', '')) 
            })
    return data

#*** MERGE SORT IMPLEMENTATION TO SORT DATA BY DATE ***
def merge_sort(data: List[dict]) -> List[dict]:
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]  
        right_half = data[mid:]  

        merge_sort(left_half)  
        merge_sort(right_half)  

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i]['Date'] < right_half[j]['Date']:
                data[k] = left_half[i]  # Add smaller element to sorted array
                i += 1
            else:
                data[k] = right_half[j]  # Add smaller element to sorted array
                j += 1
            k += 1

        while i < len(left_half):
            data[k] = left_half[i]  # Add remaining elements from left half
            i += 1
            k += 1

        while j < len(right_half):
            data[k] = right_half[j]  # Add remaining elements from right half
            j += 1
            k += 1
    return data

#*** KADANE’S ALGORITHM IMPLEMENTATION TO FIND MAXIMUM SUBARRAY ***
def kadane(arr: List[float]) -> Tuple[int, int, float]:
    max_current = max_global = arr[0]
    start = end = s = 0

    for i in range(1, len(arr)):
        if arr[i] > max_current + arr[i]:  # Start new subarray if current element is greater
            max_current = arr[i]
            s = i  # Reset start index
        else:
            max_current += arr[i]

        if max_current > max_global:  # Update global maximum if needed
            max_global = max_current
            start = s
            end = i

    return start, end, max_global

#*** CLOSEST PAIR OF POINTS USING A DIVIDE-AND-CONQUER APPROACH ***
def closest_pair(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    if len(points) <= 1:
        return float('inf'), None, None  # No points to compare

    points = sorted(points, key=lambda point: point[0])  # Sort by x-coordinate
    return closest_pair_recursive(points)

#*** RECURSIVE HELPER FUNCTION FOR CLOSEST PAIR ***
def closest_pair_recursive(points: List[Tuple[float, float]]) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
    if len(points) <= 3:
        return brute_force_closest_pair(points)  # Use brute force for small datasets

    mid = len(points) // 2
    mid_point = points[mid]

    left_half = points[:mid]
    right_half = points[mid:]

    d_left, p1_left, p2_left = closest_pair_recursive(left_half)  # Recursive call for left half
    d_right, p1_right, p2_right = closest_pair_recursive(right_half)  # Recursive call for right half

    d = min(d_left, d_right)  # Determine the minimum distance from both halves
    min_pair = (p1_left, p2_left) if d == d_left else (p1_right, p2_right)

    # Check points in the strip
    strip = [point for point in points if abs(point[0] - mid_point[0]) < d]  # Points within distance d
    d_strip, p1_strip, p2_strip = closest_strip(strip, d)  

    if d_strip < d:  # If closer pair is found in the strip
        return d_strip, p1_strip, p2_strip
    else:
        return d, min_pair[0], min_pair[1]  # Return the best pair found

#*** BRUTE FORCE CLOSEST PAIR FUNCTION ***
def brute_force_closest_pair(points: List[Tuple[float, float]]) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
    min_distance = float('inf')
    p1, p2 = None, None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = math.dist(points[i], points[j]) 
            if dist < min_distance:  
                min_distance = dist
                p1, p2 = points[i], points[j]

    return min_distance, p1, p2

#*** CLOSEST STRIP FUNCTION TO CHECK PAIRS OF POINTS WITHIN A STRIP ***
def closest_strip(strip: List[Tuple[float, float]], d: float) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
    min_distance = d
    p1, p2 = None, None
    strip = sorted(strip, key=lambda point: point[1])  # Sort by y-coordinate

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j][1] - strip[i][1]) < min_distance:  # Check within distance d
                dist = math.dist(strip[i], strip[j])  # Calculate distance
                if dist < min_distance:  # Update if a closer pair is found
                    min_distance = dist
                    p1, p2 = strip[i], strip[j]

    return min_distance, p1, p2

#*** FUNCTION TO GENERATE REPORT AND PLOT RESULTS ***
def generate_report(data: List[dict]) -> None:
    # Sort the data by date
    data = merge_sort(data)
    
    dates = [entry['Date'] for entry in data]
    closing_prices = [entry['Last'] for entry in data]  

    # Plot closing prices over time
    plt.figure(figsize=(12, 6))
    plt.plot(dates, closing_prices, label='Closing Prices', color='blue')  # Create line plot
    plt.title('Stock Price Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('stock_price_trend.png')  # Save the plot as a PNG file
    plt.close() 

    # Finding maximum gain or loss using Kadane's algorithm
    max_gain_period = kadane(closing_prices)  
    
    # Finding the closest pair of points
    points = [(entry['Last'], entry['Volume']) for entry in data]  
    distance, point1, point2 = closest_pair(points)  

    report = f"""
    Financial Data Analysis Report

    1. Data Overview:
    - Start Date: {dates[0].date()}
    - End Date: {dates[-1].date()}
    - Number of trading days: {len(dates)}

    2. Maximum Gain Period:
    - Start Date: {dates[max_gain_period[0]].date()}
    - End Date: {dates[max_gain_period[1]].date()}
    - Total Gain: ${max_gain_period[2]:.2f}

    3. Closest Pair of Points:
    - Point 1: {point1}
    - Point 2: {point2}
    - Distance: {distance:.2f}

    4. Visualization:
    - A plot of the stock price trend has been saved as 'stock_price_trend.png'
    """

    with open('REPORT.txt', 'w') as f:
        f.write(report)  # Write the report to a text file

    print("Report generated successfully. Check 'financial_analysis_report.txt' for details.")

#*** MAIN FUNCTION TO EXECUTE THE PROGRAM ***
def main():
   
    file_path = 'historicalquotes.csv'
    data = read_csv(file_path)
    generate_report(data)

if __name__ == '__main__':
    main()  
