# POLIS: Program Optimization with Local Search
Welcome to the POLIS repository! This repository contains the code for Program Optimization with Local Search (POLIS), 
as presented in our paper titled "Can You Improve My Code? Optimizing Programs with Local Search". 
POLIS is designed to optimize Python-like programs by leveraging local search techniques to improve an objective function.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Results](#results)
- [References](#references)
- [Contact Information](#contact-information)

## Installation

To install and set up the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/FatemehAB/POLIS.git
   cd POLIS
   ```

2. Set up a virtual environment using Python 3.7 and install the required dependencies:
   ```bash
   python3.7 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

To utilize POLIS for program optimization, follow these steps:

1. Modify the configuration file (```config.yaml```) to set the appropriate hyperparameters and file paths.

2. Run the main script with these parameters:

   ```path_to_config```: The path to the config file.
   
   ```agent_num```: A number that determines the trained agent to be used in the experiment.
   
   ```dirsave```: The directory to save the result files.
   
      ```bash
      python main.py --path_to_config PATH_TO_CONFIG --agent_num AGENT_NUM --dirsave DIRECTORY
      ```

## Dataset

POLIS was evaluated with a user study, where participants were instructed and rewarded to write programs that maximized the score of two single-agent games: Lunar Lander and Highway. 
The programs collected during the study are stored in the ```study-LunarLander``` and ```study-highway``` folders. 
You can choose to use one of those programs or create your own program based on the Domain-Specific Language (DSL) defined in our paper for playing Lunar Lander or Highway games.
## Results

For comprehensive results and detailed performance metrics, please refer to our paper [link to paper].

## Reference

Paper: [Link to your paper]

## Contact Information

For any questions or inquiries, please feel free to reach out to us via email at fabdolla [at] ualberta.ca. We appreciate your interest in our work and look forward to hearing from you!
