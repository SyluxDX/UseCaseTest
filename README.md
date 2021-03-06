# Use case Tester

Test use cases define in script with configurations

### ToDo
 - Add option to copy files/all workdir to a output folder

 ## Description
 Cycle throught every Versions, copy to Work Directory, and run all test's scripts.

 ## Arguments
 - -v, --verbose : Increase output Verbosity, printing test's outputs to stdout;
 - -q, --quiet : Decrease output Verbosity, prints only final results. This does not disable the logging to file;
 - -p, --path : Global script path;
 - -w, --workdir : Work Directory, will be joined with global path;
 - -t, --test : Use Case tests folder, will be joined with global path;
 - -vs, --version : Scripts Versions Folder, will be joined with global path;
 - -r, --report : Result Report Folder, will be joined with global path. Filename are format with YYYY-mm-dd_HHMMSS.log;
 - -u, --useconfig : Use Case test's default configuration name

 ## Folders Structure
    .
    ├── results                     # Logging output folder
    ├── tests                       # Use tests Folders
    │   ├── (testname01)
    |   │   ├── (testname.py)       # Use case scripts
    |   │   ├── ...
    |   │   └── useconfig.json      # Use case configurations
    │   ├── ...
    │   └── (testnamexx)
    ├── versions                    # Scripts Versions folders
    │   ├── (x.y.z)
    │   ├── ...
    │   └── (x.y.k)
    ├── workdir                     # Temp Folder where verions are copied to and tests are runned
    ├── use_test.py                 # Main Script
    └── utils.py                    # Collection of functions

> Folder and files with parameters, i.e.: (testname01), can have any name

## Use Configurations
The Use tests can be runned in one the following configuraions:
 - single : Run test script once and exit;
 - cronjob: Run test script multiple times and exit.

These configurations have the following possible fields:
| Field Name | Required in | Type | Description |
| --- | --- | --- | --- |
| runType | single, cronjob | string | indicate the test run mode, must be single or cronjob |
| entrypoint | single, cronjob | string | test main script |
| interval | cronjob | int | interval, in seconds, between runs |
| numRuns | cronjob | int | total number of runs |
| clearWorkdir | single, cronjob | bool | clear workdir before running test  |


### Configuration examples
#### Single mode
```json
{
    "runType": "single",
    "entrypoint": "simple.py"
}
```

### Cronjob mode
```json
{
    "runType": "cronjob",
    "entrypoint": "time.py",
    "interval": 2,
    "numRuns": 10
}
```