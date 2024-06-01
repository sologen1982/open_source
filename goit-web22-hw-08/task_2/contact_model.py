from mongoengine import *

connect(
    db="web22",
    host="mongodb+srv://sologen1982:********@cluster0.fpbsva4.mongodb.net/",
)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
    additional_info = StringField()  # Інші поля для інформаційного навантаження
