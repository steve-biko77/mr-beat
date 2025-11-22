# Mr Beat — Step Sequencer / Drum Machine en Python + Kivy

[![Preview](images/preview.jpg)](images/preview.jpg)

**Mr Beat** est un step-sequencer style TR-808/909 entièrement écrit en Python avec :
- Interface graphique fluide en **Kivy**
- Moteur audio ultra-performant basé sur **sounddevice** (latence < 6 ms)
- 16 steps × 8 pistes
- BPM réglable en temps réel (80 → 160)
- Preview des sons au clic
- Synchronisation visuelle parfaite (avec compensation de latence)
- Zéro dépendance à l’ancien `audiostream` (obsolète)

Version moderne et **100 % fonctionnelle** en 2025.

## Fonctionnalités

- 8 pistes préchargées (Kick, Clap, Snare, Shaker, Bass, Pluck, Vocal Chop, Effects)
- Activation/désactivation des steps en temps réel
- Lecture/Pause avec le bouton Play/Stop
- Changement de BPM fluide sans clic ni glitch
- Preview instantané en cliquant sur le nom du son
- Indicateur lumineux synchronisé avec le son joué
- Code propre, modulaire et très performant

## Installation

```bash
git clone https://github.com/ton-pseudo/mr-beat.git
cd mr-beat

# Créser un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate    # Linux/Mac
# ou
venv\Scripts\activate       # Windows
