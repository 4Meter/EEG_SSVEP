# SSVEP-based BCI system: Performance Evaluation and Realization
This project is the final project of the course 'Brain Computer Interfaces: Fundamentals and Applications.'  
If you have any related questions, feel free to contact the author of this repository.
## Introduction
The main aim of this project is to develop a practical understanding of the SSVEP paradigm in EEG and to acquire the skills necessary for developing a viable SSVEP-based application.  
The project will be divided into two parts:  
- In the first part, offline analysis will be conducted using open dataset and self acquired dataset using FBCCE and EEGnet. 
- In the second part, based on the results of the first part, a SSVEP-based game will be implemented using the selected algorithm.
## Data Description
Two dataset are used in this projct. The first dataset is an open dataset, the Benchmark dataset from Tsinghua University, and the second is self acquired data measured specifically for this project.
### Benchmark dataset
<img width="531" alt="benchmark" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/ac47eb30-0296-43fa-9738-4ccad971796a">  

This dataset, sourced from Tsinghua University[1], targets SSVEP speller applications. The data can be downloaded from the website (http://bci.med.tsinghua.edu.cn).  
According to dataset literature, the dataset used a Synamps2 EEG system (Neuroscan, Inc.) to record EEG data at a sampling rate of 1000 Hz. 64 electrodes according to an extended 10–20 system were used to record whole-head EEG. The reference electrode was placed at the vertex (Cz). Electrode impedances were kept below 10 kΩ during recording.  
35 healthy subjects (17 females, aged 17-34 years, mean age: 22 years) focusing on 40 characters flickering at different frequencies (8-15.8 Hz with an interval of 0.2 Hz).  
For each subject, the experiment consisted of 6 blocks. Each block contained 40 trials corresponding to all 40 characters indicated in a random order. Each trial started with a visual cue (a red square) indicating a target stimulus. The cue appeared for 0.5 s on the screen.  
Following the cue offset, all stimuli started to flicker on the screen concurrently and lasted 5 s.   
After stimulus offset, the screen was blank for 0.5 s before the next trial began, which allowed the subjects to have short breaks between consecutive trials. Each trial lasted a total of 6 s.  
The reliability and credibility of this dataset can be thoroughly discussed in the dataset's paper[2], where methods such as FBCCA and JFPM have shown high efficiency.

### Self acquired dataset
In order to test the usability of the system, this project uses actual EEG data measured by author of the porject .
The hardware device used is the OpenBCI Ultracortex Mark IV with Cyton board[3], with dry electrodes, and the EEG data's sampling rate is 125 Hz. 16 electrodes according to an extended 10–20 system were used to record whole-head EEG, with electrode positions shown in the image below:
<img width="602" alt="Electrode_loc" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/4e6a5069-b99d-41ce-85e0-882b7908f72c">

Software part uses OpenBCI GUI to display EEG data in real-time and uses LSL to transmit to other programs, Labrecorder[4] is used to record experimental data, and the flickering stimuli are programmed in Python with four patterns flickering at four frequencies (4.3Hz, 6Hz, 7.6Hz, 10Hz).  
Only one subject was measured this time, with 20 trials for each of the four frequencies, each trial began and ended with an audio cue, and after starting, the subject focused on a specific flickering frequency pattern on the screen, each trial lasted a total of 6 s. Experimental data is stored in the /sa_dataset directory of this repository.
This dataset is used for analyzing the hidden independent components within EEG using ICA with ICLabel, and comparing the brainwave iclabel classified by different preprocessing. With the use of filters and ASR to process the raw data, there is a gradual increase in the trend of IC classified as brain type, the detailed analysis process can be seen in /sa_dataset/SSVEP_Analysis.ipynb, here are the analysis results:  
| Step           | Brain | Muscle | Eye | Heart | Line Noise | Channel Noise | Other |
|----------------|-------|--------|-----|-------|------------|---------------|-------|
| raw            | 10    | 0      | 1   | 1     | 0          | 0             | 4     |
| filtered       | 10    | 0      | 1   | 3     | 0          | 0             | 2     |
| ASR-corrected  | 12    | 0      | 1   | 2     | 0          | 0             | 1     |
<img width="713" alt="ICA_fig" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/ddb8411a-778c-4cd3-ac9b-c7bf5c567d8c">

## System Framework
The final goal of this project is to implement a simple maze game controlled by SSVEP. The workflow of this application is shown below:  
<img width="400" alt="worlflow" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/59ff37df-07c3-4195-a649-2832baf342d1">

### Input/output mechanisms
As mentioned earlier with the Self acquired dataset, EEG data is captured from a EEG headset to the OpenBCI GUI program, and then transmitted to the application for further processing using LSL.

### Signal preprocessing
Considering the real-time nature of the application, signal preprocessing only uses a bandpass filter and notch filter for initial processing of the signals.

### Classification
For classification, the FBCCA[5] algorithm is used. The code for this algorithm is referenced from mnakanishi/TRCA-SSVEP on GitHub. After classification, the predicted command is used within the application.

### Application
A simple maze game is implemented using pygame, where the user starts in the center of the maze. There are patterns at four directions flickering at different frequencies serving as SSVEP stimuli. The game continuously receives EEG classification results to direct the user's movement.

## Validation
Detailed analysis details can be found in the Jupyter notebooks for each dataset. Below is an organized summary of the analysis contents:
### brenchmark dataset
Initial offline analysis using the benchmark dataset was conducted to validate the feasibility and effectiveness of the classification methods.
- FBCCA  
The FBCCA method was validated with results from the dataset's paper[2], testing only the first participant with forty target stimuli across six blocks, totaling 240 trials. The data length used was 5 seconds, and the SSVEP prediction accuracy was 90%, proving the method's viability.
<img width="326" alt="benchmark_fbcca" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/2fedcbb2-8cef-47bb-85f9-48dacb255e49">

- EEGnet  
Additionally, classification was attempted using the commonly used deep learning model, EEGnet[7][8], with 35 participants divided into three groups for training, validation, and testing, consisting of 21, 7, and 7 participants respectively. For this implementation, only four frequencies: 8, 9, 10, and 11 Hz were used. Analysis was conducted using data segments from each trial starting from 0.5 seconds to 5.5 seconds, experimenting with data lengths of 1 second (split into five segments) and 2.5 seconds (split into two segments).
EEGnet's classification test accuracy with 1-second data was 49.88%
<img width="645" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/947b5841-ab64-4141-9e72-5524abbed6c3">
<img width="336" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/b2880884-44ea-4dc4-bb6e-35691e9cfbeb">

EEGnet's classification test accuracy with 2.5-second data was 41.67%  
<img width="631" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/cdb52e76-f098-4e61-8906-48978b3a7c49">
<img width="302" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/7040df92-3412-46b2-9c4e-a436f743af73">

The results indicate that EEGnet struggles to effectively classify the four frequency types of SSVEP, likely due to training and testing with different user data, leading to variations in EEG signals between users. However, accuracies of 41.67% and 49.88%, while above the expected value of 25% for four-class classification, suggest that the model has some discriminating power. Perhaps further feature extraction, particularly in the frequency domain, could enhance the model's classification capabilities. Due to the need for a real-time application in this project, the FBCCA method was chosen as it does not require pre-training and showed higher classification accuracy on the benchmark dataset.

### Self acquired dataset
After validating the classification methods, the same algorithms were tested with personally measured data to verify the system's feasibility.
- FBCCA  
Using all 16 channels with data lengths of five seconds (0.5-5.5 seconds), data were compared after different preprocessing stages, using filtered and then ASR-corrected data to observe any differences.  
The classification accuracy with filtered data using FBCCA was 30.86%, indicating ineffective classification.<img width="323" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/83fa411b-fbee-4699-91c0-f5ef9deb0987">

<img width="631" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/e6dfb271-3ac6-4660-b1d1-b57f01e532eb">  

The classification accuracy with data processed through ASR after filtering was 30.49%, showing no significant difference.<img width="330" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/06563e84-f323-4cc6-8dc9-eb90d0c9ea0c">  

<img width="635" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/09d859d4-bf35-487c-ae2e-cbab3a250013">  

- EEGnet  
EEGnet classification was also attempted, using data segments of one second, with each trial split into five parts. The data was divided into three sections: training, validation, and testing.  
The accuracy for the four-class classification was 30.59%, only slightly above the expected value, indicating that EEGnet also could not effectively classify the signals.
<img width="633" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/99cecbef-c645-4a08-9f16-b41aec7fbc9f">

<img width="311" alt="image" src="https://github.com/4Meter/EEG_SSVEP/assets/97428939/bf653f8e-6edc-4757-8134-151968fe2896">



### Result
This implementation attempts to create a real-time operational SSVEP-based BCI system. Initially, the FBCCA's viability was validated using a benchmark dataset, achieving an accuracy of 90%. However, when testing the system with data measured personally, the classification accuracy dropped to 30.49%. This indicates that the algorithm is ineffective at classifying SSVEP signals with data measured by this system. The presumed reason is the use of dry electrodes which tend to have high impedance during measurement, causing excessive noise. The impedance range with dry electrodes measured was between 20-500 kΩ.

The large variance in electrode impedance, especially compared to the benchmark dataset where impedance was maintained below 10 kΩ, explains the disparity in predictive outcomes when using the FBCCA method. Ultimately, although a usable SSVEP-controlled application was developed, the limitations of the hardware and poor data quality hindered the algorithm's effective classification, resulting in imprecise control over character direction in the application. Nevertheless, this project has deepened the understanding of SSVEP.

## Usage
### Analysis
The analysis code for both datasets is stored in the corresponding folders as Analysis.ipynb  
The analysis is conducted on Google Colab, and you can choose how to run it:  
- Download the files to a local environment and run them, but you need to adjust the data paths and ensure that the required libraries are installed in your local environment.
- Download the files and upload them to a cloud-based Jupyter notebook environment to run them, placing the dataset data in the corresponding path.
#### Dataset Usage
- Benchmark dataset - /benchmark_dataset/Analysis.ipynb  
The data for this dataset must be downloaded from the open dataset's website and added to the corresponding path.
- Self Acquired dataset - /sa_dataset/Analysis.ipynb  
The data used for this analysis is located at /sa_dataset/sa_data.xdf

### Maze Game
1. To run the Maze Game, download or clone this repository.
2. Install the required libraries:
<pre>pip install -r requirement.txt</pre>
3. Navigate to the /MazeGame folder and start the game:
<pre>python maze.py</pre>
(The transmission method for this application is LSL; if you use a different transmission method or data format, you will need to adjust accordingly. You can modify the code in /MazeGame/ssvep_tool.py)

## Demo Video

https://github.com/4Meter/EEG_SSVEP/assets/97428939/6ab41ca4-e7df-4d75-bc4e-f6d376776327

https://github.com/4Meter/EEG_SSVEP/assets/97428939/677d340e-e8a5-415f-9799-1c43eee1df5b

## Reference
[1]	Benchmark Dataset - http://bci.med.tsinghua.edu.cn/download.html  
[2] Y. Wang, X. Chen, X. Gao and S. Gao, "A Benchmark Dataset for SSVEP-Based Brain–Computer Interfaces," in IEEE Transactions on Neural Systems and Rehabilitation Engineering, vol. 25, no. 10, pp. 1746-1752, Oct. 2017, doi: 10.1109/TNSRE.2016.2627556.  
  https://ieeexplore.ieee.org/document/7740878/citations#citations  
[3] OpenBCI Ultracortex Mark IV - https://shop.openbci.com/products/ultracortex-mark-iv  
[4] App-LabRecorder - https://github.com/labstreaminglayer/App-LabRecorder  
[5] Chen X, Wang Y, Gao S, Jung TP, Gao X. Filter bank canonical correlation analysis for implementing a high-speed SSVEP-based brain-computer interface. J Neural Eng. 2015  
https://pubmed.ncbi.nlm.nih.gov/26035476/  
[6] TRCA-SSVEP (FBCCA code) - https://github.com/mnakanishi/TRCA-SSVEP
[7] EEGNet: A Compact Convolutional Network for EEG-based Brain-Computer Interfaces
https://arxiv.org/abs/1611.08024
[8] EEGnet (github) - https://github.com/aliasvishnu/EEGNet
