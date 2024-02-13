import os
import json
import requests
import argparse

def split_scenes_into_files(project_id, drawify_id):
    # Construct the URL to fetch the JSON file
    url = f"https://project-drawify-v2.s3.eu-west-3.amazonaws.com/projects-v3/{drawify_id}/{project_id}/{project_id}.json"
    
    # Create a directory to store the output files, if it does not exist
    output_dir = f"./{project_id}_scenes"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Fetch the JSON file
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Check if "scenes" has more than 1 object
        if len(data["scenes"]) > 1:
            for scene in data["scenes"]:
                # Create a new JSON structure for each scene
                new_data = data.copy()
                new_data["scenes"] = [scene]
                
                # Define the output file name based on the scene id
                output_file_name = f"{project_id}_scenes_{scene['id']}.json"
                output_file_path = os.path.join(output_dir, output_file_name)
                
                # Write the scene-specific JSON data to a file
                with open(output_file_path, 'w') as f:
                    json.dump(new_data, f, indent=4)
                    
            print(f"Successfully split scenes into separate files in {output_dir}.")
        else:
            print("The 'scenes' array does not have more than 1 object.")
    else:
        print("Failed to fetch the JSON file. Please check the URL and try again.")

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Split Drawify scenes into separate JSON files.')
    parser.add_argument('-p', '--project_id', required=True, help='Project ID')
    parser.add_argument('-d', '--drawify_id', required=True, help='Drawify ID')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with provided arguments
    split_scenes_into_files(args.project_id, args.drawify_id)

if __name__ == "__main__":
    main()
