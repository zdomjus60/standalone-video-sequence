# Standalone Video Sequence

Un **eseguibile standalone** che riproduce una sequenza di brevi video **con audio sincronizzato**, funzionante su **Windows** e **Linux** — senza richiedere un lettore video esterno.

Questo progetto è ideale per installazioni artistiche, chioschi interattivi, presentazioni o qualsiasi scenario in cui sia necessaria una riproduzione video automatica e senza interruzioni con audio dedicato o continuo.

## Caratteristiche

-   **Nessun lettore video esterno richiesto:** Tutto è gestito dall'eseguibile.
-   **File eseguibile singolo:** Distribuito come un singolo file `.exe` (Windows) o binario (Linux) grazie a PyInstaller.
-   **Riproduzione audio sincronizzata:** Supporta tracce audio dedicate per ogni video o una traccia audio continua per un gruppo di video.
-   **Transizioni fluide:** Implementa dissolvenze audio per transizioni più morbide tra i video.
-   **Configurazione semplice:** La sequenza di riproduzione è definita tramite un semplice file di testo (`videolist.txt`).
-   **Compatibilità cross-platform:** Funziona su sistemi operativi Windows e Linux.

## Requisiti di Sviluppo

Per sviluppare o ricompilare il progetto, avrai bisogno di:

-   Python 3.x
-   `opencv-python`
-   `pygame`
-   `pyinstaller`
-   **FFmpeg:** Necessario per l'estrazione dell'audio dai file video (vedi la sezione "Estrazione Audio").

Puoi installare le dipendenze Python con pip:

```bash
pip install opencv-python pygame pyinstaller
```

## Utilizzo

1.  **Prepara i tuoi video:** Assicurati che i tuoi file video siano in un formato compatibile (es. `.mp4`).
2.  **Prepara l'audio (Opzionale):**
    *   Se i tuoi video hanno già tracce audio incorporate o preferisci file audio separati, assicurati che siano nello stesso formato (es. `.mp3`).
    *   Puoi usare lo script `extract_audio.py` per estrarre l'audio dai tuoi file video (vedi "Estrazione Audio").
3.  **Configura `videolist.txt`:** Modifica il file `videolist.txt` per definire la sequenza di riproduzione.

    ### Formato di `videolist.txt`

    Ogni riga nel `videolist.txt` rappresenta un elemento nella sequenza di riproduzione. Le righe vuote o che iniziano con `#` vengono ignorate.

    #### Video con Audio Dedicato

    Per riprodurre un video con un file audio specifico:

    ```
    video_file.mp4, audio_file.mp3
    ```

    *   `video_file.mp4`: Il percorso del file video.
    *   `audio_file.mp3`: Il percorso del file audio da riprodurre con questo video. Se omesso, il video verrà riprodotto senza audio. Se il campo è vuoto (es. `video_file.mp4,`), il sistema cercherà un file audio con lo stesso nome del video ma con estensione `.mp3` (es. `video_file.mp3`).

    #### Gruppi di Video con Audio Continuo

    Per riprodurre una sequenza di video con una singola traccia audio continua in sottofondo:

    ```
    CONTINUOUS_AUDIO_GROUP, continuous_background_audio.mp3
    video1.mp4
    video2.mp4
    END_CONTINUOUS_AUDIO_GROUP
    ```

    *   `CONTINUOUS_AUDIO_GROUP, continuous_background_audio.mp3`: Inizia un blocco di audio continuo. `continuous_background_audio.mp3` è il file audio che verrà riprodotto per tutti i video all'interno di questo gruppo.
    *   `video1.mp4`, `video2.mp4`: I video all'interno del gruppo.
    *   `END_CONTINUOUS_AUDIO_GROUP`: Termina il blocco di audio continuo.

4.  **Esegui il programma:**

    *   **Dallo script Python:**
        ```bash
        python standalone_video_with_audio.py
        ```
    *   **Dall'eseguibile standalone:** Esegui il file generato da PyInstaller (es. `standalone_video_with_audio.exe` su Windows o `standalone_video_with_audio` su Linux).

## Estrazione Audio

Lo script `extract_audio.py` ti permette di estrarre automaticamente le tracce audio dai tuoi file video e salvarle come file `.mp3`. Questo è utile se i tuoi video non hanno tracce audio separate o se vuoi usare una traccia audio specifica.

**Requisito:** Devi avere **FFmpeg** installato e accessibile nel tuo PATH di sistema.

Per estrarre l'audio da tutti i file `.mp4` nella directory corrente:

```bash
python extract_audio.py
```

Lo script creerà file `.mp3` corrispondenti (es. `video.mp4` -> `video.mp3`).

## Costruire l'Eseguibile Standalone

Il progetto utilizza PyInstaller per creare un singolo file eseguibile.

1.  Assicurati di aver installato PyInstaller (`pip install pyinstaller`).
2.  Esegui lo script di build appropriato per il tuo sistema operativo:
    *   **Windows:**
        ```bash
        build_exe.bat
        ```
    *   **Linux:**
        ```bash
        ./build_exe.sh
        ```

    Questi script utilizzeranno `standalone_video_with_audio.spec` per configurare la build di PyInstaller. L'eseguibile risultante si troverà nella directory `dist/`.

## Licenza

[TODO: Aggiungere informazioni sulla licenza, es. MIT, GPL, ecc.]

## Contribuzioni

Le contribuzioni sono benvenute! Si prega di fare riferimento alle linee guida di contribuzione (se presenti) o di aprire una issue per discutere le modifiche proposte.
