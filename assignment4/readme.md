# CDS Language Analytics: Assignment #4 - Emotion analysis using pretrained models

## Description
This repository aims to use a pretrained emotion calssifier to process a text dataset (the Game of Thrones script), and extract emotion labels for each line spoken in the show. This will then be plotted afterwards, showing the emotional distribution across the shows seasons.

***This code uses CodeCarbon to monitor the environmental effects of running this code. The effects of which can be found in the `out/emissions` folder***

## Setup

1. Make sure to have python and Git Bash installed!

2. Open a Git Bash terminal and use Git to download the repository:
```sh
git  clone  https://github.com/missingusername/cds-lang-git.git
```
3. Navigate to the project folder for this assignment:
```sh
cd  cds-lang-git/assignment2
```
4. Before running the program, you first have to set up a virtual environment with the required dependencies. This can be done by simply running either  `bash win_setup.sh`  or  `bash unix_setup.sh`  depending on your system.

5. Before we can run the script, we first need the Game of Thrones script in `.csv` form. The dataset can be found [here](https://www.kaggle.com/datasets/albenft/game-of-thrones-script-all-seasons?select=Game_of_Thrones_Script.csv), where you can download the `archive.zip` file. When downloaded, unzip the folder and place `Game_of_Thrones_Script.csv` in the `/in` folder of the `assignment4` directory.

6. The script uses Argparse to parse commands to the script from the command line.

| name | flag | description | required |
|--|--|--|--|
| exclude | -e | Emotion labels to exclude while plotting the emotion label distribution. For example, to exclude disgust & neutral, you would use `-e disgust neutral`. | OPTIONAL |

To run the program, you can run the OS-appropriate run script. Here's an example of how to run the script with arguments:
Run basic unix script:
```sh
bash unix_run.sh
```

Example of running windows script, using command line arguments to exclude `neutral` & `fear` label.
```sh
bash win_run.sh -e fear neutral
```

## Takeaways from output

<table>
<tr><th>Logistic Regression</th><th>MLP</th></tr>
<tr><td>

| Class        | Precision | Recall | F1-Score | Support |
|--------------|-----------|--------|----------|---------|
| FAKE         | 0.84      | 0.81   | 0.82     | 628     |
| REAL         | 0.82      | 0.85   | 0.83     | 639     |
| **Accuracy** |           |        | 0.83     | 1267    |
| **Macro Avg**| 0.83      | 0.83   | 0.83     | 1267    |
| **Weighted Avg** | 0.83  | 0.83   | 0.83     | 1267    |

</td><td>

| Class        | Precision | Recall | F1-Score | Support |
|--------------|-----------|--------|----------|---------|
| FAKE         | 0.84      | 0.82   | 0.83     | 628     |
| REAL         | 0.83      | 0.85   | 0.84     | 639     |
| **Accuracy** |           |        | 0.84     | 1267    |
| **Macro Avg**| 0.84      | 0.83   | 0.83     | 1267    |
| **Weighted Avg** | 0.84  | 0.84   | 0.84     | 1267    |

</td></tr> </table>
