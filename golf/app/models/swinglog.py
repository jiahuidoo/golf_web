from app import db
from models.users import User
from models.golflog import Golf

class Swing(db.Document):

    meta = {'collection': 'swinglog'}
    user = db.ReferenceField(User)
    datetime = db.DateTimeField()
    speed = db.FloatField()
    label = db.StringField()
    distance = db.FloatField()

    def computeDistance(self):
        ''''
        Formula:
        estimated_distance = (280 - abs(48- club_length)*10 - abs(club_head_loft - 10)*1.25) * swingSpeed/96
        club_length = club_head_height + shaft_length
        club_head_height = club_head_size/400 for WoodHead
                            1 for IronHead
                            1 for Blade style and 0.5 otherwise for PutterHead  
        '''
        
        # Retrieve the golf club
        club = Golf.getGolfClub(self.user, self.label)

        # Compute the head height based on the type of clubhead
        if club.clubtype == "Wood":
            # size / 400
            club_head_height = float(club.hinfo) / 400

        elif club.clubtype == "Iron":
            club_head_height = 1 

        # if style is Blade, height is 1, else 0.5
        else:
            club_head_height = 1 if club.hinfo == "Blade" else 0.5

        club_length = club_head_height + club.slength #shaft_length
        
        # Compute the estimated swing distance
        estimated_distance = (280 - abs(48-club_length)*10 - abs(club.hloft - 10)*1.25) * self.speed/96
        return estimated_distance

    @staticmethod
    def getSwings(user):
        return Swing.objects(user=user)
    
    @staticmethod
    def getAllSwings():
        return Swing.objects()         
        
    @staticmethod
    def createSwing(user, datetime, speed, label, distance=0.0):

        club = Golf.getGolfClub(user=user, label=label)
        
        if club:
            # truncate and insert
            # Delete any existing swing made by given user, golf club at the same datetime
            Swing.objects(user=user, datetime=datetime, label=label).delete()
            return Swing(user=user, datetime=datetime, speed=speed, label=label, distance=distance).save()
        
        # If golf club does not exist, return None
        return club
    