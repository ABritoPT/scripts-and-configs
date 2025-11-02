# Windows Scripts

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