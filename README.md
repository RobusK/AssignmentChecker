# Copy detector

A simple script to detect very similar files via Levenshtein distance (edit distance).

## Requirements
[Python 3](https://www.python.org/downloads/)

## Installation
    $ pip3 install -r requirements.txt
    
## Usage

    $ python3 run.py -f java -p 1 example
Returns 

     example\HalloWelt.java
     example\HelloWorld.java
     EditDist=8, 7.02%
     
### Params

     $ python3 run.py -h
     
     usage: run.py [-h] [-f TYPE] [-t THRESHHOLD] [-p THREADS] [-l] [-m MAX] [-nc]  
                   input                                                            
                                                                                    
     Find edit distance between files.                                              
                                                                                    
     positional arguments:                                                          
       input                 Input dir for files                                    
                                                                                    
     optional arguments:                                                            
       -h, --help            show this help message and exit                        
       -f TYPE, --type TYPE  File type to look for (default: java)                  
       -t THRESHOLD, --threshold THRESHOLD                                       
                             Threshold under which files should be      
                             reported (default: 0.1)                                
       -p THREADS, --threads THREADS                                                
                             Number of threads (default: 1)                         
       -m MAX, --max MAX     Max file size in kB (default: 10)                       
       -nc, --no-colors      Don't use colors in output         
       -l, --loyola          Loyola sakai directory format                        
