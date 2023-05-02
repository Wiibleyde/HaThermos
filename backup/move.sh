#!/bin/bash

latest=$(ls -t /var/hathermos/hathermos-backup | head -1)
scp user@127.0.0.1:/var/hathermos/hathermos-backup/$latest [user@]ip_dest:/path/to/dest
```



