import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import os
import argparse

def plot_gpx(gpx_file_path, output_dir):
    """
    Parses a GPX file, plots the track, and saves it as a PNG image.

    Args:
        gpx_file_path (str): The path to the GPX file.
        output_dir (str): The directory where the PNG image will be saved.
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Parse the GPX file
        with open(gpx_file_path, 'r') as gpx_file_content:
            gpx = gpxpy.parse(gpx_file_content)

        latitudes = []
        longitudes = []

        # Extract latitude and longitude from GPX data
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    latitudes.append(point.latitude)
                    longitudes.append(point.longitude)

        if not latitudes or not longitudes:
            print(f"No track points found in {gpx_file_path}")
            return

        # Generate the plot
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(longitudes, latitudes, marker='o', linestyle='-', color='blue')

        # Set plot title and labels
        ax.set_title(f"GPX Track: {os.path.basename(gpx_file_path)}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True)

        # Save the plot
        output_filename = os.path.join(output_dir, os.path.basename(gpx_file_path).replace('.gpx', '.png'))
        plt.savefig(output_filename)
        plt.close(fig)  # Close the plot to free memory

        print(f"Successfully plotted and saved: {output_filename}")

    except gpxpy.gpx.GPXXMLSyntaxException:
        print(f"Error: Invalid GPX file format in {gpx_file_path}. Could not parse XML.")
    except FileNotFoundError:
        print(f"Error: GPX file not found at {gpx_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {gpx_file_path}: {e}")

if __name__ == "__main__":
    # Initialize ArgumentParser
    parser = argparse.ArgumentParser(description="Plot GPX tracks from data/raw/ and save as PNG images to data/processed/images/.")

    # Add argument for the GPX file path
    # The help message guides the user to place files in data/raw/
    parser.add_argument("gpx_file", help="Path to the GPX file (e.g., data/raw/your_file.gpx or just your_file.gpx if it's in data/raw/)")

    # Add optional argument for the output directory
    parser.add_argument("--output_dir", default="data/processed/images/", help="Directory to save the PNG file (default: data/processed/images/).")

    # Parse arguments
    args = parser.parse_args()

    # Construct the full input file path.
    # If the path doesn't start with 'data/raw/', prepend it.
    # This allows users to provide either the full path or just the filename if it's in data/raw.
    input_gpx_path = args.gpx_file
    if not input_gpx_path.startswith("data/raw/") and not os.path.isabs(input_gpx_path) :
        # Check if it's a simple filename that might be in data/raw
        potential_path = os.path.join("data/raw/", input_gpx_path)
        if os.path.exists(potential_path):
            input_gpx_path = potential_path
        # If it's not a simple filename and not in data/raw, we assume it's a relative path from repo root or absolute.
        # The os.path.join below will handle this, or FileNotFoundError will be caught.

    # Call the plotting function
    plot_gpx(input_gpx_path, args.output_dir)
