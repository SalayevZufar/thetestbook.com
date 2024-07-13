from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField,validators, EmailField,BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email,InputRequired,ValidationError
from wtforms.widgets import PasswordInput, Select
from app.models import Student
from flask_login import current_user




COUNTRY = [("","Countries"),("Aland Islands","Aland Islands"),("Albania","Albania"),("Algeria","Algeria"),("American Samoa","American Samoa"),("Andorra","Andorra"),("Angola","Angola"),("Anguilla","Anguilla"),("Antarctica","Antarctica"),("Antigua and Barbuda","Antigua and Barbuda"),("Argentina","Argentina"),("Armenia","Armenia"),("Aruba","Aruba"),("Australia","Australia"),("Austria","Austria"),("Azerbaijan","Azerbaijan"),("Bahamas","Bahamas"),("Bahrain","Bahrain"),("Bangladesh","Bangladesh"),("Barbados","Barbados"),("Belarus","Belarus"),("Belgium","Belgium"),("Belize","Belize"),("Benin","Benin"),("Bermuda","Bermuda"),("Bhutan","Bhutan"),("Bolivia","Bolivia"),("Bonaire, Sint Eustatius and Saba","Bonaire, Sint Eustatius and Saba"),("Bosnia and Herzegovina","Bosnia and Herzegovina"),("Botswana","Botswana"),("Bouvet Island","Bouvet Island"),("Brazil","Brazil"),("British Indian Ocean Territory","British Indian Ocean Territory"),("Brunei Darussalam","Brunei Darussalam"),("Bulgaria","Bulgaria"),("Burkina Faso","Burkina Faso"),("Burundi","Burundi"),("Cambodia","Cambodia"),("Cameroon","Cameroon"),("Canada","Canada"),("Cape Verde","Cape Verde"),("Cayman Islands","Cayman Islands"),("Central African Republic","Central African Republic"),("Chad","Chad"),("Chile","Chile"),("China","China"),("Christmas Island","Christmas Island"),("Cocos(Keeling) Islands","Cocos(Keeling) Islands"),("Colombia","Colombia"),("Comoros","Comoros"),("Congo","Congo"),("Congo, Democratic Republic of the Congo","Congo, Democratic Republic of the Congo"),("Cook Islands","Cook Islands"),("Costa Rica","Costa Rica"),("Cote D'Ivoire","Cote D'Ivoire"),("Croatia","Croatia"),("Cuba","Cuba"),("Curacao","Curacao"),("Cyprus","Cyprus"),("Czech Republic","Czech Republic"),("Denmark","Denmark"),("Djibouti","Djibouti"),("Dominica","Dominica"),("Dominican Republic","Dominican Republic"),("Ecuador","Ecuador"),("Egypt","Egypt"),("El Salvador","El Salvador"),("Equatorial Guinea","Equatorial Guinea"),("Eritrea","Eritrea"),("Estonia","Estonia"),("Ethiopia","Ethiopia"),("Falkland Islands(Malvinas)","Falkland Islands(Malvinas)"),("Faroe Islands","Faroe Islands"),("Fiji","Fiji"),("Finland","Finland"),("France","France"),("French Guiana","French Guiana"),("French Polynesia","French Polynesia"),("French Southern Territories","French Southern Territories"),("Gabon","Gabon"),("Gambia","Gambia"),("Georgia","Georgia"),("Germany","Germany"),("Ghana","Ghana"),("Gibraltar","Gibraltar"),("Greece","Greece"),("Greenland","Greenland"),("Grenada","Grenada"),("Guadeloupe","Guadeloupe"),("Guam","Guam"),("Guatemala","Guatemala"),("Guernsey","Guernsey"),("Guinea","Guinea"),("Guinea-Bissau","Guinea-Bissau"),("Guyana","Guyana"),("Haiti","Haiti"),("Heard Island and Mcdonald Islands","Heard Island and Mcdonald Islands"),("Holy See(Vatican City State)","Holy See(Vatican City State)"),("Honduras","Honduras"),("Hong Kong","Hong Kong"),("Hungary","Hungary"),("Iceland","Iceland"),("India","India"),("Indonesia","Indonesia"),("Iran, Islamic Republic of","Iran, Islamic Republic of"),("Iraq","Iraq"),("Ireland","Ireland"),("Isle of Man","Isle of Man"),("Italy","Italy"),("Jamaica","Jamaica"),("Japan","Japan"),("Jersey","Jersey"),("Jordan","Jordan"),("Kazakhstan","Kazakhstan"),("Kenya","Kenya"),("Kiribati","Kiribati"),("Korea, Democratic People's Republic of","Korea, Democratic People's Republic of"),("Korea, Republic of","Korea, Republic of"),("Kosovo","Kosovo"),("Kuwait","Kuwait"),("Kyrgyzstan","Kyrgyzstan"),("Lao People's Democratic Republic","Lao People's Democratic Republic"),("Latvia","Latvia"),("Lebanon","Lebanon"),("Lesotho","Lesotho"),("Liberia","Liberia"),("Libyan Arab Jamahiriya","Libyan Arab Jamahiriya"),("Liechtenstein","Liechtenstein"),("Lithuania","Lithuania"),("Luxembourg","Luxembourg"),("Macao","Macao"),("Macedonia, the Former Yugoslav Republic of","Macedonia, the Former Yugoslav Republic of"),("Madagascar","Madagascar"),("Malawi","Malawi"),("Malaysia","Malaysia"),("Maldives","Maldives"),("Mali","Mali"),("Malta","Malta"),("Marshall Islands","Marshall Islands"),("Martinique","Martinique"),("Mauritania","Mauritania"),("Mauritius","Mauritius"),("Mayotte","Mayotte"),("Mexico","Mexico"),("Micronesia, Federated States of","Micronesia, Federated States of"),("Moldova, Republic of","Moldova, Republic of"),("Monaco","Monaco"),("Mongolia","Mongolia"),("Montenegro","Montenegro"),("Montserrat","Montserrat"),("Morocco","Morocco"),("Mozambique","Mozambique"),("Myanmar","Myanmar"),("Namibia","Namibia"),("Nauru","Nauru"),("Nepal","Nepal"),("Netherlands","Netherlands"),("Netherlands Antilles","Netherlands Antilles"),("New Caledonia","New Caledonia"),("New Zealand","New Zealand"),("Nicaragua","Nicaragua"),("Niger","Niger"),("Nigeria","Nigeria"),("Niue","Niue"),("Norfolk Island","Norfolk Island"),("Northern Mariana Islands","Northern Mariana Islands"),("Norway","Norway"),("Oman","Oman"),("Pakistan","Pakistan"),("Palau","Palau"),("Palestinian Territory, Occupied","Palestinian Territory, Occupied"),("Panama","Panama"),("Papua New Guinea","Papua New Guinea"),("Paraguay","Paraguay"),("Peru","Peru"),("Philippines","Philippines"),("Pitcairn","Pitcairn"),("Poland","Poland"),("Portugal","Portugal"),("Puerto Rico","Puerto Rico"),("Qatar","Qatar"),("Reunion","Reunion"),("Romania","Romania"),("Russian Federation","Russian Federation"),("Rwanda","Rwanda"),("Saint Barthelemy","Saint Barthelemy"),("Saint Helena","Saint Helena"),("Saint Kitts and Nevis","Saint Kitts and Nevis"),("Saint Lucia","Saint Lucia"),("Saint Martin","Saint Martin"),("Saint Pierre and Miquelon","Saint Pierre and Miquelon"),("Saint Vincent and the Grenadines","Saint Vincent and the Grenadines"),("Samoa","Samoa"),("San Marino","San Marino"),("Sao Tome and Principe","Sao Tome and Principe"),("Saudi Arabia","Saudi Arabia"),("Senegal","Senegal"),("Serbia","Serbia"),("Serbia and Montenegro","Serbia and Montenegro"),("Seychelles","Seychelles"),("Sierra Leone","Sierra Leone"),("Singapore","Singapore"),("Sint Maarten","Sint Maarten"),("Slovakia","Slovakia"),("Slovenia","Slovenia"),("Solomon Islands","Solomon Islands"),("Somalia","Somalia"),("South Africa","South Africa"),("South Georgia and the South Sandwich Islands","South Georgia and the South Sandwich Islands"),("South Sudan","South Sudan"),("Spain","Spain"),("Sri Lanka","Sri Lanka"),("Sudan","Sudan"),("Suriname","Suriname"),("Svalbard and Jan Mayen","Svalbard and Jan Mayen"),("Swaziland","Swaziland"),("Sweden","Sweden"),("Switzerland","Switzerland"),("Syrian Arab Republic","Syrian Arab Republic"),("Taiwan, Province of China","Taiwan, Province of China"),("Tajikistan","Tajikistan"),("Tanzania, United Republic of","Tanzania, United Republic of"),("Thailand","Thailand"),("Timor-Leste","Timor-Leste"),("Togo","Togo"),("Tokelau","Tokelau"),("Tonga","Tonga"),("Trinidad and Tobago","Trinidad and Tobago"),("Tunisia","Tunisia"),("Turkey","Turkey"),("Turkmenistan","Turkmenistan"),("Turks and Caicos Islands","Turks and Caicos Islands"),("Tuvalu","Tuvalu"),("Uganda","Uganda"),("Ukraine","Ukraine"),("United Arab Emirates","United Arab Emirates"),("United Kingdom","United Kingdom"),("United States","United States"),("United States Minor Outlying Islands","United States Minor Outlying Islands"),("Uruguay","Uruguay"),("Uzbekistan","Uzbekistan"),("Vanuatu","Vanuatu"),("Venezuela","Venezuela"),("Viet Nam","Viet Nam"),("Virgin Islands, British","Virgin Islands, British"),("Virgin Islands, U.s.","Virgin Islands, U.s."),("Wallis and Futuna","Wallis and Futuna"),("Western Sahara","Western Sahara"),("Yemen","Yemen"),("Zambia","Zambia"),("Zimbabwe","Zimbabwe")]



class RegisterForm(FlaskForm):
    first_name = StringField("First Name", 
                             validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder":"First Name"})
    last_name = StringField("Last Name", 
                            validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder":"Last Name"})
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=7, max=20)],render_kw={"placeholder": "Username"})
    email = EmailField("Email",  
                        validators=[Email(),DataRequired()], render_kw={"placeholder":"Email"})
    password = PasswordField("Password", 
                             validators=[DataRequired(), Length(min=7,max=10)],render_kw={"placeholder": "Password"},widget=PasswordInput(hide_value=False))
    birthdate_day = SelectField("Birthdate Day",
                                validators=[DataRequired()], choices=[('', 'Day'),('1', '1'), ('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),('9', '9'),('10', '10'),('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),('21', '21'),('22', '22'),('23', '23'),('24', '24'),('25', '25'),('26', '26'),('27', '27'),('28', '28'),('29', '29'),('30', '30'),('31', '31')])
    birthdate_month = SelectField("Birthdate Month", 
                                validators=[DataRequired()], choices=[("", "Month"),("Jan", "Jan"),("Feb", "Feb"),("Mar", "Mar"),("Apr", "Apr"),("May", "May"),("Jun", "Jun"),("Jul", "Jul"),("Aug", "Aug"), ("Sep", "Sep"),("Oct", "Oct"),("Nov", "Nov"),("Dec", "Dec")])
    birthdate_year = SelectField("Birthdate Year",  
                                validators=[DataRequired()], choices=[("", "Year"),('2015', '2015'), ('2014', '2014'),('2013', '2013'),('2012', '2012'),('2011', '2011'),('2010', '2010'),('2009', '2009'),('2008', '2008'),('2007', '2007'),('2006', '2006'),('2005', '2005'),('2004', '2004'),('2003', '2003'),('2002', '2002'),('2001', '2001'),('2000', '2000'),('1999', '1999'),('1998', '1998'),('1997', '1997'),('1996', '1996'),('1995', '1995'),('1994', '1994'),('1993', '1993'),('1992', '1992'),('1991', '1991'),('1990', '1990'),('1989', '1989'),('1988', '1988'),('1987', '1987'),('1986', '1986'),('1985', '1985'),('1984', '1984'),('1983', '1983'), ('1982', '1982'),('1981', '1981'),('1980', '1980'),('1979', '1979'),('1978', '1978'),('1977', '1977'),('1976', '1976'),('1975', '1975'),('1974', '1974'),('1973', '1973'),('1972', '1972'),('1971', '1971'),('1970', '1970'),('1969', '1969'),('1968', '1968'),('1967', '1967'),('1966', '1966'),('1965', '1965'),('1964', '1964'),('1963', '1963'),('1962', '1962'),('1961', '1961'),('1960', '1960')])
    gender = SelectField("Gender", validators=[DataRequired()] , choices=[('',"Select"),("Male","Male"), ("Femele","Female")], default=(0,"Gender"))
    
    signup_as = SelectField("Signup as",validators=[DataRequired()], choices=[('', "Select"), ("Student","Student"),("Teacher","Teacher")])

    submit = SubmitField("Sign up")

    def validate_username(self, username):
        user = Student.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username already taken. Please choose other one.")
    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email already taken. Please choose other one.")


class LoginForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "Username"})
    password = PasswordField("Password", 
                             validators=[DataRequired()],render_kw={"placeholder": "Password"},widget=PasswordInput(hide_value=False))
    remember = BooleanField('Remember Me')
    submit = SubmitField("Log in")



class UpdateAccountForm(FlaskForm):
    
    first_name = StringField("First Name", 
                             validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder":"First Name"})
    last_name = StringField("Last Name", 
                            validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder":"Last Name"})
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=7, max=20)],render_kw={"placeholder": "Username"})
    email = EmailField("Email",  
                        validators=[Email(),DataRequired()], render_kw={"placeholder":"Email"})
    # password = PasswordField("Password", 
    #                          validators=[DataRequired(), Length(min=7,max=10)],render_kw={"placeholder": "Password"},widget=PasswordInput(hide_value=False))
    bio = TextAreaField("Bio", validators=[], render_kw={"placeholder":"Bio"})
    country = SelectField("Country",  choices=COUNTRY)
    
    address = StringField("Address", render_kw={"placeholder": "Address"})
    phone_number = StringField("Phone number", validators=[ Length(min=10, max=15)],render_kw={"placeholder": "Phone number"})
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg","png","gif"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            student = Student.query.filter_by(username=username.data).first()
            if student:
                raise ValidationError("That username already taken. Please choose other one.")
    def validate_email(self, email):
        if email.data != current_user.email:
            student = Student.query.filter_by(email=email.data).first()
            if student:
                raise ValidationError("That email already taken. Please choose other one.")
    
    def validate_first_name(self, first_name):
        if   "."  in first_name.data:
            raise ValidationError("Name should contain only latters")
    def validate_last_name(self, last_name):
        if "." in last_name.data:
            raise ValidationError("Name should contain only latters")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()],render_kw={"placeholder": "What's on your mind?"})
    picture = FileField("Share your favour", validators=[FileAllowed(["jpg","png","gif","jfif"])])
    content = TextAreaField("Content", validators=[DataRequired()],render_kw={"placeholder": "What are you thinking?"})
    submit = SubmitField("Submit")
    
class SearchForm(FlaskForm): #create form
    username = StringField('Username', validators=[DataRequired(),Length(max=40)],render_kw={"placeholder": "username"})
 