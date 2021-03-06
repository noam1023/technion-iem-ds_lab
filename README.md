
# Exercise submission checker

This project is a web server for students to upload, build and execute programming tasks in C++,Python, Java etc.

The server runs in a Docker container, on a linux host.

It is developed as a small scale alternative to [CodeRunner](https://moodle.org/plugins/qtype_coderunner) .
#### Maturity: In development, pre alpha.

# Getting Started
<b>TODO</b> -- add content <br>

For support, send mail to the repository maintainer

## System Requirements
- ubuntu 18.04
- docker
- ssh access (for management and file uploading) 
## Installing

Refer to intallation.md

# Running tests of the server
TBD

#Contributing
 use pull requests in github

# Directory structure
The source code is stored in thie repo, and the auxiary data (which compises the matchers, runners, test configurations, data files for each test) is stored in a different repo. This separation ease the maintance of both repos and prevents the need to rebuild the docker image for changes in homework configurations.
## Data directory
The data directory can be anywhere in the host file system and must have the following structure: <br>
```
{data-dir}
       data/   <---- each course has its own sub dirirectory, named as the course ID 
           94219/
              ex1/
                data files
              ex2/
                data files
       matchers/
       runners/
       hw_config.json
```

The path to the data directory is passed to the server in environment variable **CHECKER_DATA_DIR** as a full path.
<br>
<br>

## storing the database
 The database (job submissions) is stored in sqlite3 file in a directory that must be writable in the host machine.
## storing the log output
The logger output is written to a directory in the host file system that must be writable.

All the above directories are mounted in the **run_docker.sh** script.

# Instructions for the Tutor
As the tutor, you have to prepare:
- code that will execute the program
- code that verify the output is correct
    - _hint_: https://regex101.com/
- input data (the input test vector)
- output data (the output for the input for a correct solution)
    - optionally, another input and output tagged GOLDEN 


These coding parts are called __runner__ and __matcher__ (aka comparator)

Choosing the runner and matcher is done by reading a configuration file (located at {data-dir}/hw_settings.json)

You can see the current content in ```host_address/admin/show_ex_config```
   
Modifying/adding values is by uploading a new version of the file (in the admin page)
  

For example,
- in ex 1, a C/C++ program, exact text match is needed
- in ex 2, a Python program, there is a complicated scenario that requires regular expression.

The config file json will look like:
```
{
"94201":
 [ {
     "id": 1,
     "matcher" : "exact_match.py",
     "runner" :"check_cmake.sh",
     "timeout" : 5
   },
   {
     "id": 2,
     "matcher" : "tester_ex2.py",
     "runner" :"check_py.sh",
     "data_dir": "relative/path/to/DATA_DIR", <<< optional
     "timeout" : 20
    }
 ]
}
```    



## Uploading data to the server
Use ssh and put the data files  in {data-dir}/data/courseId<br>
 e.g.
  /mydata/data/94219/ref_hw_3_input
 /mydata/data/94219/ref_hw_3_output
 /mydata/data/94219/data_files_folder
 
 
It will be mapped into the server's file system (This is done in run_docker.sh)
<br>

## Using the correct runner
Depending on the assignment, choose an existing runner or write a new one.<br>
The runners are bash scripts that are run in a shell (for security) and accepts as arguments
the filename of the tested code, input data file, reference output file and matcher file name.<Br>
The script return 0 for success. <br>
NOTE: Comparison is done by running the matcher from within the runner script.
This will be changed in a future version.

These runners are already implemented:
  - check_cmake.sh: run cmake, make and execute the executable found.
  - check_py.sh: run the file ```main.py``` in the supplied archive
   (or just this file if no archive is used)
  - check_sh.sh: run the file using bash
   
     
## Adding/Modifying matcher
All matchers are written in Python3. 

Before writing a new one, check the existing scripts  - maybe you can use one of them as a baseline.
1. save the new ```tester.py``` in ```{data-dir}/matchers``` dir.<br>
    The script must implement ```check(output_from_test_file_name,reference_file_name)``` <br>
    and return True if the files are considered a match.<br>
    For example ```def check(f1,ref): return True```<br>
    <strong>currently, you need to implement</strong> <br>
    <pre>
    if __name__ == "__main__":
        good = check(sys.argv[1], sys.argv[2])
        exit(0 if good else ExitCode.COMPARE_FAILED) </pre> 
    
2. Update the config file by uploading an updated version.<br>
    The current config can be seen at ```http://your-host/admin/show_ex_config ```<br>
    and uploading from the admin page at ```http://your-host/admin```
    <br>
    **Normally there is no need even to restart the docker container since the matcher and runner are called in a new shell for every executed test.**
    
    
To rebuild the docker image and immediately run it:<br>
    
    
 build a new Docker container, stop the current one, start the new one:
```
$ ssh myhost
(myhost) $ cd checker
(myhost) $ git pull
(myhost) $ cd scripts && ./again.sh
```

# Running the web application
The webapp runs as a Docker container.<br>
First, build the container: (in the project root directory)
> docker build **.** -t server:<current_tag>
 
then run it
> cd scripts && ./run_docker.sh server

OR  if you just want to build - stop - start fresh again:
> cd scripts &&  ./again.sh


# Reliability
I created a monitoring account that checks the server every couple minutes and send me email if the server is down. 

There is known problem that occasionally the server hangs.
 In such a case, ssh to the host, and execute ```scripts/restart_container.sh```
#Security
* The Docker container runs as user _nobody_, who has minimal privilages.
* The submitted code is run in a subprocess with limitations on
  * execution time (for each exercise we set a timeout value)
  * network connectivity (not implemented yet)
    
# Debugging
During development, it is easier to run only the python code without Docker:
 ``` 
 cd ~/checker
 source venv/bin/activate
 python3 run.py
  ```
  
  ## gunicorn
  
  To run with gunicorn (one step closer to the realworld configuration):
  ```
  cd ~/checker
  source venv/bin/activate
  gunicorn3 -b 0.0.0.0:8000 --workers 3 serverpkg.server:app
```
