# pygitsnapshot

Currently : 
- Create a snapshot of a git repository. 
    - User can specify:
        - Path
        - Branch
        - Commit message

TODO:
- Make the module callable such as : 
    - `pygitsnapshot -p /path/to/repo -b master -m "My commit message"` or
    - `pygitsnapshot --path ...`
- Add a command line interface
- Add tests
- Make docs
- Publish the module on pypi


## Usage
```bash
$ python pygitsnapshot.py <source_dir> <destination_dir>
source_dir : Path to the source directory (target of the snapshot)
destination_dir : Path to the destination directory (where the snapshot will be created). If the directory does not exist, or is not a git repository, it will be created and initialized as a git repository.
Optional:
-b --branch <branch_name> : Specify the branch to create the snapshot on
-m --message <commit_message> : Specify the commit message to use
-p --push : Boolean flag to push the changes to the remote
-h --help : Print this help message
```

# License
MIT License : https://opensource.org/licenses/MIT

