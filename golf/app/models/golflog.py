from app import db
from models.users import User

class Golf(db.Document):

    meta = {'collection': 'golflog'}
    user = db.ReferenceField(User)
    label = db.StringField()
    clubtype = db.StringField()

    # club head
    hloft = db.FloatField()
    hweight = db.FloatField()
    #size/material/style
    #iron - materials, wood - size, putter - style
    hinfo = db.StringField()
    
    # shaft
    slength = db.FloatField()
    sweight = db.FloatField()
    smaterial = db.StringField()
    sflex = db.StringField()

    # grip
    gdiameter = db.FloatField()
    gweight = db.FloatField()
    gmaterial = db.StringField()

    @staticmethod
    def getGolfClub(user, label):
        return Golf.objects(user=user, label=label).first()
    
    @staticmethod    
    def getAllGolfClubs(user):
        golfclubs = list(Golf.objects(user=user))
        return sorted(golfclubs, key=lambda golfclub: golfclub.label)
    
    @staticmethod #singleto pattern
    def createGolfClub(user, label, clubtype, 
                      hloft, hweight, hinfo, 
                      slength, sweight, smaterial, sflex, 
                      gdiameter, gweight, gmaterial):

        # check if the golf club already exists
        golfclub = Golf.getGolfClub(user=user, label=label)

        # Assume no two identical club labels allowed for one user
        # If the golf club exists, update all the attributes
        if golfclub:
            golfclub.update(clubtype=clubtype, 
                            hloft=hloft, hweight=hweight, hinfo=hinfo, 
                            slength=slength, sweight=sweight, smaterial=smaterial, sflex=sflex, 
                            gdiameter=gdiameter, gweight=gweight, gmaterial=gmaterial)
        
        # If the golf club does not exist, create a new golf club
        else:
            golfclub = Golf(user=user, label=label, clubtype=clubtype, 
                    hloft=hloft, hweight=hweight, hinfo=hinfo, 
                    slength=slength, sweight=sweight, smaterial=smaterial, sflex=sflex, 
                    gdiameter=gdiameter, gweight=gweight, gmaterial=gmaterial).save()

        return golfclub
    