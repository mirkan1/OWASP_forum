from wtforms import StringField, Form, SubmitField
from wtforms.validators import DataRequired

class SearchForm(Form):
  search = StringField('search', [DataRequired()])
  submit = SubmitField('Search',
                       render_kw={'class': 'btn btn-success btn-block'})