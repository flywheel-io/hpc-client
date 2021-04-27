# Development guide

The basic structure of the python program is as follows:

```
code/
├── Pipfile            Package management
├── Pipfile.lock
│
├── cast.py            Main script
│
├── cluster
│   ├── __init__.py    Cluster type disptach
│   │
│   ├── base.py        Common override points
│   ├── common.py      Fixed functionality; do not modify
│   │
│   ├── lsf.py         \
│   ├── sge.py          >  Off the shelf implementations
│   └── slurm.py       /
│
└── util               Fixed functionality; do not modify
    ├── __init__.py
    ├── defn.py        Data structures definitions
    ├── frame.py       Program setup
    └── net.py         SDK helpers
```

## Adding a new queue type to Cast

To add a new queue type, follow these steps:

1. Make a copy of `cluster/slurm.py` and name it after your queue type.

2. Edit `cluster/__init__.py` so it knows about your new class.

3. Edit your new file's defaults to what makes sense for your use case.

4. Review `cluster/base.py` for the various methods you can override.

5. Avoid modifying or overriding the functions in `cluster/common.py`. We reserve the right to make changes to those functions for future Flywheel features.

6. Avoid modifying the `util` package. Instead, place helper functions on your new class.

7. Update your `cluster` key in `cast.yml` to point at your new code.
