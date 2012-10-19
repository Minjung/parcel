#
# Some actual fab targets that you can import into you fabfile
# to provide some extra functions that you will usually need
#

def copy_ssh_key():
    """This copies the local uses id_rsa.pub and id_dsa.pub keys into the authorized_keys
    file on the remote host as the remote user. It creates the authorized_keys file if
    it's missing.
    """
    lpath = os.path.expanduser("~/.ssh/")
    rpath = '~/.ssh/'
    
    files = os.listdir(lpath)
    
    if 'id_rsa.pub' in files or 'id_dsa.pub' in files:
        run('mkdir -p ~/.ssh')
        run('chmod 600 ~/.ssh')
        run('touch ~/.ssh/authorized_keys')

        for fname in ('id_rsa.pub','id_dsa.pub'):
            if fname in files:
                parcel_fname = "parcel_"+fname
                put(os.path.join(lpath,fname),'.ssh/'+parcel_fname)

                # see if the key in the parcel key file. 
                # the remote command returns '0' if the key is in there, and '1' if not
                if int(run('diff %s%s %sauthorized_keys | grep "^<" | wc -l'%(rpath,parcel_fname,rpath)).strip()):
                    run('cat %s%s >> %sauthorized_keys'%(rpath,parcel_fname,rpath))

                run('rm %s%s'%(rpath,parcel_fname))

def setup_debian():
    """Set up the build host for building in a debian way"""
    from parcel.distro import Debian
    Debian().setup()
    