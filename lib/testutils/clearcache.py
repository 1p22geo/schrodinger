import shutil

def rmtemp():
    '''
    Remove the temporary file directory with in-progress and complete renders
    
    Actually executes 'rm -rf static/temp'
    '''
    shutil.rmtree("static/temp")