import pysftp

private_key_path = '.ssh/id_rsa'

with pysftp.Connection(private_key=private_key_path) as sftp:

    folder_path = '/var/etc/*'
    backup_dir = '/temalepath'
    
    sftp.put_d(backup_dir, folder_path)
    sftp.close()
        
