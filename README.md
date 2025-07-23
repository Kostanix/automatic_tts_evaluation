# Automatic TTS Evaluation

Ein modulares Framework zur automatisierten Bewertung synthetisierter Sprache (TTS) anhand objektiver Metriken.

## Setup

### 1. Repository klonen

```bash
git clone https://github.com/Kostanix/automatic_tts_evaluation.git
cd automatic_tts_evaluation+
```

### 2. Python-Abhängigkeiten installieren

Umgebung erstellen (falls noch nicht vorhanden)
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Abhängigkeiten aus txt installieren
```bash
pip install -r requirements.txt
```

### ffmpeg installieren
Einige Metriken (z. B. Whisper) benötigen ffmpeg zur Audiokonvertierung. Wenn ffmpeg nicht installiert ist:

```bash
# 1. Verzeichnis erstellen (falls noch nicht vorhanden)
mkdir -p ~/mounted_home/bin
cd ~/mounted_home/bin

# 2. ffmpeg herunterladen
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

# 3. Entpacken
tar -xf ffmpeg-release-amd64-static.tar.xz
cd ffmpeg-*-static

# 4. Symlink erstellen
ln -s "$(pwd)/ffmpeg" ~/mounted_home/bin/ffmpeg

# 5. Pfad setzen (nur für aktuelle Session)
export PATH=~/mounted_home/bin:$PATH

ODER

# 5. Pfad setzen (dauerhaft)
echo 'export PATH=~/mounted_home/bin:$PATH' >> ~/.bashrc

# 6. Testen
ffmpeg -version
```

### Ausführen
```bash
python main.py --config config/default.json
```

### Ergebniss
Alle Bewertungen werden gesammelt in:
```
results.csv
```
