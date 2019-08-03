# MacJournal to Day One

This script reads a MacJournal export file and import it into Day One. The script was forked from [Kevin McKenzie](https://github.com/Tam-Lin/MacJournaltoDayOne---Python) and updated to work with the newer version of Day One.

## Usage

Example:

```bash
MacJournalToDayOne.py input-file.txt --journal="Staging"
```


### Command Line Options

- First parameter is the file name of the MacJournal export file
- Option `--journal` specifies a pre-existing in Day One to target the import records. The default is `MacJournal Import`.

## How to Use

1. Install the Day One command line tool.
2. Create a new journal in Day One.
3. Export a journal from MacJournal, as text file containing all entries
4. Run MacJournalToDayOne to import to the new journal in Day One.
5. Use Day One to inspect the resulting journal.
6. If satisfied, move the imported journal to your regular journal

## System Requirements

- Python 2.7 (the system Python that came with macOS 10.14 “Mojave”)
- [MacJournal 5.2.8](https://danschimpf.com)
- [Day One](https://dayoneapp.com) 4.0
- The [Day One 2.0](https://help.dayoneapp.com/en/articles/435871-command-line-interface-cli) command line tool.


