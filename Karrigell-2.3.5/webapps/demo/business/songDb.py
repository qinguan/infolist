from PyDbLite import Base
db = {}
try:
    db['chansons'] = Base('chansons.skl').open()
except IOError:
    import createSongBase
    createSongBase.createBase()
    db['chansons'] = Base('chansons.skl').open()

db['recueils'] = Base('recueils.skl').open()
db['dialectes'] = Base('dialectes.skl').open()
db['genres'] = Base('genres.skl').open()
db['chansons_par_recueil'] = Base('chansons_par_recueil.skl').open()
db['chansons_par_dialecte'] = Base('chansons_par_dialecte.skl').open()
    