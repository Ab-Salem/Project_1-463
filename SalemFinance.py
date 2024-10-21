import csv
import matplotlib.pyplot as plt
import math
from datetime import datetime
from typing import List, Tuple

# Function to read the CSV file and parse the data
def read_csv(file_path: str) -> List[dict]:
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                'Date': datetime.strptime(row['Date'], '%m/%d/%Y'),  # Update the format here
                'Last': float(row['Last'].replace('$', '').replace(',', '')),
                'Volume': int(row['Volume']),
                'Open': float(row['Open'].replace('$', '').replace(',', '')),
                'High': float(row['High'].replace('$', '').replace(',', '')),
                'Low': float(row['Low'].replace('$', '').replace(',', ''))
            })
    return data

# Merge Sort implementation
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
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1
    return data

# Kadane’s Algorithm implementation for maximum subarray
def kadane(arr: List[float]) -> Tuple[int, int, float]:
    max_current = max_global = arr[0]
    start = end = s = 0

    for i in range(1, len(arr)):
        if arr[i] > max_current + arr[i]:
            max_current = arr[i]
            s = i
        else:
            max_current += arr[i]

        if max_current > max_global:
            max_global = max_current
            start = s
            end = i

    return start, end, max_global

# Closest Pair of Points using a divide-and-conquer approach
def closest_pair(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    if len(points) <= 1:
        return float('inf'), None, None

    points = sorted(points, key=lambda point: point[0])  # Sort by x-coordinate
    return closest_pair_recursive(points)

def closest_pair_recursive(points: List[Tuple[float, float]]) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
    if len(points) <= 3:
        return brute_force_closest_pair(points)

    mid = len(points) // 2
    mid_point = points[mid]

    left_half = points[:mid]
    right_half = points[mid:]

    d_left, p1_left, p2_left = closest_pair_recursive(left_half)
    d_right, p1_right, p2_right = closest_pair_recursive(right_half)

    d = min(d_left, d_right)
    min_pair = (p1_left, p2_left) if d == d_left else (p1_right, p2_right)

    # Check points in the strip
    strip = [point for point in points if abs(point[0] - mid_point[0]) < d]
    d_strip, p1_strip, p2_strip = closest_strip(strip, d)

    if d_strip < d:
        return d_strip, p1_strip, p2_strip
    else:
        return d, min_pair[0], min_pair[1]

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

def closest_strip(strip: List[Tuple[float, float]], d: float) -> Tuple[float, Tuple[float, float], Tuple[float, float]]:
    min_distance = d
    p1, p2 = None, None
    strip = sorted(strip, key=lambda point: point[1])  # Sort by y-coordinate

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j][1] - strip[i][1]) < min_distance:
                dist = math.dist(strip[i], strip[j])
                if dist < min_distance:
                    min_distance = dist
                    p1, p2 = strip[i], strip[j]

    return min_distance, p1, p2

# Function to generate report and plot results
def generate_report(data: List[dict]) -> None:
    # Sort the data by date
    data = merge_sort(data)
    
    dates = [entry['Date'] for entry in data]
    closing_prices = [entry['Last'] for entry in data]  # Updated key

    # Plot closing prices over time
    plt.figure(figsize=(12, 6))
    plt.plot(dates, closing_prices, label='Closing Prices', color='blue')
    plt.title('Stock Price Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('stock_price_trend.png')  # Save the plot as a PNG file
    plt.close()  # Close the plot to free up memory

    # Finding maximum gain or loss using Kadane's algorithm
    max_gain_period = kadane(closing_prices)
    
    # Finding the closest pair of points
    points = [(entry['Last'], entry['Volume']) for entry in data]  # Updated key
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
        f.write(report)

    print("Report generated successfully. Check 'financial_analysis_report.txt' for details.")

# Main function to execute the program
def main():
    # Path to your CSV file
    file_path = 'historicalquotes.csv'
    
    # Step 1: Load the data
    data = read_csv(file_path)

    # Step 2: Generate the report
    generate_report(data)

if __name__ == '__main__':
    main()
