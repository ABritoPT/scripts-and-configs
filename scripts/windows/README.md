# Windows Scripts

Index:
- [SSH Shortcut to TrueNAS](#ssh-shortcut-to-truenas)
- [Subs Processor](#subs-processor)
- [Shutdown i5](#shutdown-i5)
- [Drive Dumps](#drive-dumps)

## SSH Shortcut to TrueNAS

Simple script that SSH's into TrueNAS as root. The `lnk` file launches the script automatically in a PowerShell window.

- Script file: `ssh-r3.ps1` + `SSH R3.lnk`
- Parameters: `none`
- Requirements: `none`

## Subs Processor

Extracts subtitles from a `Subs` folder and places them alongside the respective video file and with a matching name. Takes a path as a parameter that points to a season folder with the following structure:

```
Season 1
├── S01E01.mp4
├── S01E02.mp4
├── S01E03.mp4
...
└── Subs
    ├── S01E01
    │   └── 2_eng.srt
    ├── S01E02
    │   └── 2_eng.srt
    ├── S01E03
    │   └── 2_eng.srt
...
```

The final result will be:
```
Season 1
├── S01E01.mp4
├── S01E01.srt
├── S01E02.mp4
├── S01E02.srt
├── S01E03.mp4
├── S01E03.srt
...
└── Subs
    ├── S01E01
    │   └── 2_eng.srt
    ├── S01E02
    │   └── 2_eng.srt
    ├── S01E03
    │   └── 2_eng.srt
...
```

- Script file: `Subs_processor.vbs`
- Parameters: Path (absolute or relative) to season folder
- Script settings:
    - `SUBS_FOLDER`: Name of the folder with the subtitles (`Subs` by default)
    - `SUB_EXT`: Extension of the subtitle files (`srt` by default)
    - `SUB_LANG`: Desired language of the subtitle file (`eng` by default)
- Requirements: `none`

## Shutdown i5

Remotely shuts down another computer on the network, specifically `i5-andre`.

- Script file: `Shutdown i5.bat`
- Parameters: `none`
- Requirements: `none`

## Drive Dumps

Saves the full path of every file and folder in the specified drive into a `.txt` file with the drive's letter, e.g. `D.txt` for drive `D:`. If the files exists, it will be overwritten.

Main command: `dir /s /b /o:gn`

- `/S` Displays files in specified directory and all subdirectories.
- `/B` Uses bare format (no heading information or summary).
- `/O` List by files in sorted order.
- Then in `:gn`, `g` sorts by folders and then files, and `n` puts those files in alphabetical order.

<!-- -->

- Script file: `drive dumps.bat`
- Parameters: `none`
- Script settings: Drive letters (`D L S Z`)
- Requirements: `none`
- Output: `D.txt`, `L.txt`, `S.txt`, and `Z.txt`