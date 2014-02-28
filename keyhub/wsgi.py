from flask import Flask


app = Flask('keyhub')
app.config.from_object('keyhub.config')
print app
