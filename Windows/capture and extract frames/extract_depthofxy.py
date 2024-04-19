import csv

def get_depth_at_pixel(csv_file_path, cx, cy):
    """
    Get the depth at a specified pixel coordinate (cx, cy) from a CSV file containing depth data.
    
    Args:
        csv_file_path (str): Path to the CSV file containing depth data.
        cx (int): X-coordinate of the pixel.
        cy (int): Y-coordinate of the pixel.
    
    Returns:
        float: Depth value at the specified pixel coordinate.
    """
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        depth_data = list(reader)
    
    depth_value = float(depth_data[cy][cx])
    
    return depth_value

csv_file_path = "csv/depth_data9.csv"  # Path to your CSV file
cx = 412 # Example pixel x-coordinate
cy = 209  # Example pixel y-coordinate

depth_value = get_depth_at_pixel(csv_file_path, cx, cy)
print(f"Depth value at pixel ({cx}, {cy}): {depth_value}")
