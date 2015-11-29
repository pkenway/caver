
def log(text):
    with open('cave.log', 'w') as logfile:
        logfile.write(text + '\n')
