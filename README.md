# Guide manual

Team : Théo Pirouelle

<a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/language-python-blue?style=flat-square" alt="laguage-python" />
</a>

![TestsResult](https://github.com/Dayonixe/SystemPerformanceAnalyser/actions/workflows/python-tests.yml/badge.svg)

---

## Installation

> [!NOTE]
> For information, the code has been developed and works with the following library versions:
> | Library | Version |
> | --- | --- |
> | psutil | 7.0.0 |
> | pytest | 8.4.1 |

---

## User manual

```bash
> python cli.py

usage: cli.py [-h] {collect,show} ...

System Monitor CLI

positional arguments:
  {collect,show}
    collect       Collect system metrics
    show          Show last collected metrics

options:
  -h, --help      show this help message and exit
```

```bash
> python cli.py collect

usage: cli.py collect [-h] [--interval INTERVAL] [--duration DURATION]

options:
  -h, --help           show this help message and exit
  --interval INTERVAL  Interval between collections (in seconds)
  --duration DURATION  Total duration of the collection (in seconds)
```

```bash
> python cli.py show

usage: cli.py show [-h] [--limit LIMIT]

options:
  -h, --help     show this help message and exit
  --limit LIMIT  Number of rows to display
```

```bash
> python cli.py report

usage: cli.py report [-h] [--limit LIMIT] [--save]

options:
  -h, --help     show this help message and exit
  --limit LIMIT  Number of data points to include
  --save         Save report as PNG instead of showing it
```