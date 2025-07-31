# Automatic TTS Evaluation

A modular framework for automated evaluation of synthesized speech (TTS) based on objective metrics.
## Setup

### Python Version
This framework is tested with Python version 3.11.x

Make sure both your local machine and the cluster environment are running a compatible Python version.
It is strongly recommended to use a virtual environment (venv or conda).

Example setup using venv:

```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 1. Clone repository

```bash
git clone https://github.com/Kostanix/automatic_tts_evaluation.git
cd automatic_tts_evaluation
```

### 2. Install Python dependencies
Install dependencies from txt:
```bash
pip install -r requirements.txt
```

### Install ffmpeg
Some metrics (e.g. Whisper) require ffmpeg for audio conversion. If ffmpeg is not installed:
```bash
# 1. Create directory (if not already done)
mkdir -p ~/mounted_home/bin
cd ~/mounted_home/bin

# 2. Download ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

# 3. Unpack
tar -xf ffmpeg-release-amd64-static.tar.xz
cd ffmpeg-*-static

# 4. Create symlink
ln -s "$(pwd)/ffmpeg" ~/mounted_home/bin/ffmpeg

# 5. Set path (only for current session)
export PATH=~/mounted_home/bin:$PATH

OR

# 5. Set path (permanently)
echo 'export PATH=~/mounted_home/bin:$PATH' >> ~/.bashrc

# 6. Test
ffmpeg -version
```
Note: This guide shows installation on the HdM deeplearning Cluster. If you want to run on another system, please refer to the Setup guide for Whisper: [OpenAI Whisper on GitHub](https://github.com/openai/whisper)
  

## Execute
```bash
python main.py --config config/default.json
```
### Usage of Inline Arguments

The evaluation script supports inline arguments to override settings from the config file. This is useful when testing individual metrics, using different datasets, or switching model options without modifying the config file directly.

### Example: Only evaluate Intelligibility and Speaker Similarity
```bash
python main.py --enable intelligibility similarity
```

### Example: Specify a custom input folder and output CSV file
```bash
python main.py --data_dir my_data --results_file my_results.csv
```

### Example: Use a larger Whisper model
```bash
python main.py --whisper_model large
```

### Available Command-Line Options

| Argument           | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `--config`         | Path to the configuration file (default: `config/default.json`)             |
| `--data_dir`       | Path to the input sample folder                                              |
| `--results_file`   | Path to the output `.csv` results file                                       |
| `--enable`         | List of metrics to enable: `intelligibility`, `prosody`, `similarity`, `mos`|
| `--use_gpu`        | Force GPU usage (`--use_gpu true` or `false`)                               |
| `--log_level`      | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`                          |
| `--whisper_model`  | Whisper model size: `tiny`, `base`, `small`, `medium`, `large`, `turbo`     |

> ℹ️ Note: All CLI arguments override the values defined in the JSON config file.


## Result
All evaluation results are written to:
```
results.csv
```

## Create SSH Access to the Cluster
To run the evaluation framework on the HdM GPU cluster and load your data on it, you need to set up SSH key-based authentication.

### 1. Generate a new SSH key*
If you don’t already have one, create a new SSH key using the following command (works in macOS, Linux, or Git Bash on Windows):
 ```bash
 ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
 ```
- Press enter to accept the default save location (~/.ssh/id_rsa)
- You will now have a private key (id_rsa) and a public key (id_rsa.pub)

### 2. Copy your public key to the cluster
After connecting to the HdM VPN, run:
```bash
ssh-copy-id <username>@deeplearn.mi.hdm-stuttgart.de
```
Replace <username> with your HdM account.
You’ll be prompted for your password once. After this step, login will be passwordless.

### 3. Test SSH connection
```bash
ssh <username>@deeplearn.mi.hdm-stuttgart.de
```
If it logs you in without asking for a password, everything is set up correctly.

### 4. Configure send_to_cluster.sh
In the send_to_cluster.sh script, update the SSH target by editing this line:
```bash
TARGET_USER="kg068"
``` 

### 5. Run script
```bash
bash evaluate_latest_batch.sh
```

### Data structure
The data needs to have a specific structure in order to be read and evaluated by the framework:
```
data/
└── sample_01/
    ├── audio.wav
    ├── metadata.json
    └── reference.wav  # optional
```
Be careful  to also keep the names to "audio.wav", "metadata.json" and "reference.wav" (if you want to use it).
