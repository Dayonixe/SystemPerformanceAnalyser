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
> | matplotlib | 3.10.5 |
> | psutil | 7.0.0 |
> | pytest | 8.4.1 |

---

## User manual

```bash
> python cli.py

usage: cli.py [-h] {collect,report,report-md} ...

System Monitor CLI

positional arguments:
  {collect,report,report-md}
    collect             Collect system metrics
    report              Generate performance report
    report-md           Generate markdown report with summary and graph

options:
  -h, --help            show this help message and exi
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
> python cli.py report

usage: cli.py report [-h] [--limit LIMIT] [--since SINCE] [--last {hour,day}] [--save]

options:
  -h, --help         show this help message and exit
  --limit LIMIT      Number of data points to include
  --since SINCE      Start datetime (ISO format: YYYY-MM-DDTHH:MM)
  --last {hour,day}  Use a pre-defined time filter
  --save             Save report as PNG instead of showing it
```

```bash
> python cli.py report-md

usage: cli.py report-md [-h] [--limit LIMIT] [--since SINCE] [--last {hour,day}]

options:
  -h, --help         show this help message and exit
  --limit LIMIT      Number of data points to include
  --since SINCE      Start datetime (ISO format: YYYY-MM-DDTHH:MM)
  --last {hour,day}  Use a pre-defined time filter
```