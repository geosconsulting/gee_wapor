import datetime
import glob
import os
import platform

os.chdir('tests/immagini')

def da_unix_a_data(data_conv):
    return(datetime.datetime.fromtimestamp(data_conv).strftime('%c'))

epoch = datetime.datetime.utcfromtimestamp(0)
def data_a_unix_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

#oggi = datetime.datetime.now()
#print(oggi)
#oggi_unix = data_a_unix_millis(oggi)
#print(oggi_unix)

start = datetime.datetime.now()
print start.isoformat()
files = glob.glob('*.tif')
somma_transf = 0
for archivo in files:
    somma_transf += os.path.getsize(archivo)/1024
    if platform.system() == 'Windows':
        data_modifica = da_unix_a_data(os.path.getctime(archivo))
    else:
        stat = os.stat(archivo)
        try:
            data_modifica = da_unix_a_data(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            data_modifica = da_unix_a_data(stat.st_mtime)
    print("Il File %s ha dimensione %d data di modifica %s" % (archivo, os.path.getsize(archivo)/1024, data_modifica))
print("Trasferiti %0.2f kb" % (float(somma_transf)))

end = datetime.datetime.now()
print end.isoformat()

trascorso = end - start
trascorso_secondi = trascorso.seconds/1e6
trascorso_microsecondi = trascorso.microseconds
print("Ci ha messo %6f secondi" % trascorso_secondi)
print("Ci ha messo %d microsecondi" % trascorso_microsecondi)