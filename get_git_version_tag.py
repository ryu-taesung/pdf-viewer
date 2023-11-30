import subprocess

def get_git_version_tag():
    output = subprocess.check_output(['git', 'describe']).decode('ASCII').replace('\n','')
    with open('version.txt', 'w') as file:
        file.write(output)
    return output

if __name__ == '__main__':
    get_git_version_tag()