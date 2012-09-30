from .. import db, common


class Role(common.ConfigurationModel, common.SlugMixin):
    pass


class Group(common.ConfigurationModel):
    associations = db.relationship("GroupAssociation")


class GroupAssociation(common.Model):
    __tablename__ = 'group_association'

    group_id = db.Column(db.BigInteger(unsigned=True),
                         db.ForeignKey('group.id'),
                         nullable=False)

    user_id = db.Column(db.BigInteger(unsigned=True),
                        db.ForeignKey('user.id'),
                        nullable=False)

    role_id = db.Column(db.BigInteger(unsigned=True),
                        db.ForeignKey('role.id'))

    user = db.relationship("User")
    role = db.relationship("Role")
