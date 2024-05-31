import os
import pandas as pd
import matplotlib.pyplot as plt

def set_working_directory():
    """Sets the working directory to the directory of the script."""
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

def load_emissions_data(folder_path):
    """Load emissions data from all CSV files in a folder."""
    all_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            all_data.append(df)
    return all_data

def plot_emissions_for_folder(folder_path, out_path):
    """Plot emissions data for a folder as bar charts."""
    all_data = load_emissions_data(folder_path)
    folder_name = os.path.basename(folder_path)
    
    # Initialize master plot for the folder
    fig, axes = plt.subplots(1, len(all_data), figsize=(len(all_data) * 8 ,6))
    if len(all_data) == 1:
        axes = [axes]  # Ensure axes is a list even if there's only one subplot
    
    assignment_emissions = 0
    
    for i, df in enumerate(all_data):
        ax = axes[i]
        project_name = df['project_name'].iloc[0]  # Assuming project_name is the same across all rows
        
        # Calculate total emissions for the current project
        project_total = df['emissions'].sum()
        assignment_emissions += project_total
        
        # Sort projects by emissions descending for bar chart
        df_sorted = df.sort_values(by='emissions', ascending=False)
        
        # Plot bar chart for current project
        ax.bar(df_sorted['task_name'], df_sorted['emissions'], color='skyblue')
        ax.set_title(f'{project_name} - Emissions')
        ax.set_xlabel('Task Name')
        ax.set_ylabel('Emissions')
        ax.set_xticklabels(df_sorted['task_name'], rotation=45, ha='right')
        ax.ticklabel_format(style='plain', axis='y')
    
    # Set master plot title and save it
    fig.suptitle(f'Emissions Summary - {folder_name}')
    plt.tight_layout()
    plt.savefig(os.path.join(out_path, f'{folder_name} chart.png'))
    plt.close()
    
    return assignment_emissions

def plot_assignment_emissions(assignment_emissions, folder_names, out_path):
    """Plot bar chart for total emissions across assignments."""
    plt.figure(figsize=(10, 6))
    plt.bar(folder_names, assignment_emissions, color='skyblue')
    plt.xlabel('Assignment')
    plt.ylabel('Total Emissions')
    plt.title('Total Emissions per Assignment')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(out_path, 'assignment emissions.png'))
    plt.close()

def plot_task_emissions(all_task_emissions, out_path):
    """Plot pie chart for emissions distribution across tasks."""
    task_names = list(all_task_emissions.keys())
    task_emissions = list(all_task_emissions.values())
    
    plt.figure(figsize=(15, 10))
    plt.bar(task_names, task_emissions, color='skyblue')
    plt.xlabel('Task Name')
    plt.ylabel('Emissions')
    plt.title('Emissions Distribution by Task')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(out_path, 'all task emissions.png'))
    plt.close()

def main():
    set_working_directory()

    in_path = os.path.join('..', 'in')
    out_path = os.path.join('..', 'out')
    
    assignment_emissions = []
    all_task_emissions = {}
    folder_names = []

    for folder in sorted(os.listdir(in_path)):
        assignment = folder.split()[0]
        current_folder_path = os.path.join(in_path, folder)
        print(f'Processing folder: {current_folder_path}')
        
        # Plot emissions for current folder
        total_emission = plot_emissions_for_folder(current_folder_path, out_path)
        assignment_emissions.append(total_emission)
        folder_names.append(folder)
        
        # Aggregate task emissions for the final pie chart
        all_data = load_emissions_data(current_folder_path)
        for df in all_data:
            for index, row in df.iterrows():
                project_name = row['project_name']
                task_name = row['task_name']
                specific_task = f'{task_name} ({project_name}) ({assignment})'
                emissions = row['emissions']
                if specific_task in all_task_emissions:
                    all_task_emissions[specific_task] += emissions
                else:
                    all_task_emissions[specific_task] = emissions

    # Sort tasks by emissions descending for the final pie chart
    all_task_emissions = dict(sorted(all_task_emissions.items(), key=lambda task: task[1], reverse=True))

    # Plot total emissions bar chart
    plot_assignment_emissions(assignment_emissions, folder_names, out_path)
    
    # Plot task emissions bar chart
    plot_task_emissions(all_task_emissions, out_path)

if __name__ == "__main__":
    main()
