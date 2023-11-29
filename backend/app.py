from functools import wraps
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from google.cloud import firestore
from google.cloud import storage
import jwt
import os
import datetime
from email.message import EmailMessage
import smtplib
import ssl
from dotenv import load_dotenv
import pandas as pd

app = Flask(__name__)
CORS(app)
load_dotenv()

# Set the path to the service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"F:\Pradeesh\IITM\paradox-backup\backend\paradox23-website-d037d29221a5.json"


# Initialize Firestore client
db = firestore.Client()
bucket_name = 'finance-invoice'
# bucket_name = 'finance-application-testing'
bucket = storage.Client().bucket(bucket_name)

# Define a secret key for JWT token generation
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

def send_email(email, subject, message, file=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = str(email)
    if file:
        msg.add_attachment(file, maintype='application', subtype='octet-stream', filename=file.filename)
    msg.set_content(message)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_address, email_password)
        server.send_message(msg)

# Define a decorator function to protect routes that require authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Verify the JWT token using the PyJWT library
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

            # If the token is valid and has not expired, allow the request to proceed
            current_user = db.collection('users').document(data['user_id']).get().to_dict()
            del current_user['password']

        except:
            return jsonify({"message": "Token is Invalid"}), 401
        
        return f(current_user, *args, **kwargs)
        
    return decorated

@app.route('/')
def home():
    return 'Welcome to the home page!'

@app.route('/login', methods=['POST'])
def login():
    # Retrieve the email and password submitted in the login form
    email = request.form['email']
    password = request.form['password']

    # Query the Firestore database to check if the email exists and the password is correct
    users_ref = db.collection(u'users')
    query = db.collection('users').where('email', '==', email).where('password', '==', password)
    user_docs = query.stream()
    # Check if the user exists and the password is correct
    user_id = None
    for doc in user_docs:
        user_data = doc.to_dict()
        role = user_data['role']
        user_id = doc.id

    if not user_id:
        return jsonify({'success': False, 'error': 'Invalid email or password'}), 200
        # return jsonify({'error': 'Invalid email or password'}), 200

    # Generate a JWT token for the authenticated user
    token_payload = {'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')

    # Return the user data and the authentication token as a JSON response
    response_data = {
        'token': token,
        'success': True,
        'admin': role == 'admin',
        'pod_admin': role == 'pod-admin',
    }
    return jsonify(response_data), 200

@app.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    # Return the user data as a JSON response
    return jsonify(current_user), 200

@app.route('/bills', methods=['POST'])
def add_bill():
    # Retrieve the bill data from the request body
    bill_data = {}
    for key, value in request.form.items():
        bill_data[key] = value

    # Upload the image file to Firebase Cloud Storage
    image_file = request.files.get('bill_image')
    # _, ext = os.path.splitext(image_file.filename)
    image_path = f"bills/{bill_data['bill_number']}_{bill_data['bill_department']}.pdf"
    image_blob = bucket.blob(image_path)
    if not image_blob.exists():
        # File does not exist, upload it
        image_file = request.files.get('bill_image')
        image_blob.upload_from_file(image_file)
    else:
        return jsonify({'success': False, 'error': 'Bill already exists'}), 200

    # Create a new document in the 'bills' collection with the provided data
    bills_ref = db.collection('bills')
    new_bill_ref = bills_ref.document()
    new_bill_ref.set({
        'poc_name': bill_data['poc_name'],
        'poc_email': bill_data['poc_email'],
        'event_name': bill_data['event_name'],
        'poc_phone': bill_data['poc_phone'],
        'bill_department': bill_data['bill_department'],
        'bill_number': bill_data['bill_number'],
        'bill_date': bill_data['bill_date'],
        'bill_type': bill_data['bill_type'],
        'vendor_name': bill_data['vendor_name'],
        'vendor_address': bill_data['vendor_address'],
        'gst_number': bill_data['gst_number'],
        'bill_description': bill_data['bill_description'],
        'bill_amount': bill_data['bill_amount'],
        'bill_amount_in_words': bill_data['bill_amount_in_words'],
        'acc_holder_name': bill_data['acc_holder_name'],
        'acc_number': bill_data['acc_number'],
        'ifsc_code': bill_data['ifsc_code'],
        'bank_name': bill_data['bank_name'],
        'bank_branch': bill_data['branch_name'],
        'bill_status': 'pending',
        'stact_processed': False,
        'stact_processed_on': None,
        'bill_created_on': datetime.datetime.now(),
        'sc_approved': False,
        'sc_approved_on': None,
        'sc_approved_by': None,
        'fc_approved': False,
        'fc_approved_on': None,
        'fc_approved_by': None,
        'voucher_generated': False,
        'voucher_generated_on': None,
        'eas_generated': False,
        'bill_image': image_blob.public_url,
    })

    # Return a success response
    return jsonify({'success': True, 'message': 'Bill added successfully'}), 200

@app.route('/pending-bills', methods=['GET'])
@token_required
def get_pending_bills(current_user):
    # Get the current user's department list
    departments_managed = current_user['departments']

    # Query the bills collection for bills with departments in the user's list
    bills_ref = db.collection('bills')
    # Query bills with user's departments and pending status
    query = bills_ref.where('bill_status', '==', 'pending').where('bill_department', 'in', departments_managed)
    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/all-pending-bills', methods=['GET'])
@token_required
def get_all_pending_bills(current_user):
    # Query the bills collection for bills with departments in the user's list
    bills_ref = db.collection('bills')
    # Query bills with user's departments and pending status
    query = bills_ref.where('bill_status', '==', 'pending')
    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/sc-fc-approved', methods=['GET'])
@token_required
def get_sc_fc_approved_bills(current_user):
    # Get the current user's department list
    departments_managed = current_user['departments']

    # Query the bills collection for bills with departments in the user's list
    bills_ref = db.collection('bills')
    # Query bills with user's departments and pending status
    # query = bills_ref.where('bill_status', '==', 'sc_approved').where('bill_department', 'in', departments_managed)
    query = bills_ref.where('fc_approved', '==', True).where('bill_department', 'in', departments_managed)
    
    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/sc-approved', methods=['PUT'])
@token_required
def sc_approve_bill(current_user):
    # Retrieve the bill ID from the request body
    bill_id = request.form['bill_id']
    # Check if the user is authorized to approve the bill
    if current_user['role'] != 'Super Coordinator':
        return jsonify({'error': 'You are not authorized to approve bills'}), 403

    # Update the bill document with the approval details
    bill_ref = db.collection('bills').document(bill_id)
    bill_ref.update({
        'bill_status': 'sc_approved',
        'sc_approved': True,
        'sc_approved_on': datetime.datetime.now(),
        'sc_approved_by': current_user['name'],
    })

    # Return a success response
    return jsonify({'message': 'Bill approved successfully'}), 200

@app.route('/bills/sc-approved-all', methods=['GET'])
@token_required
def get_sc_approved_all_bills(current_user):
    # TODO Check for Core Role
    # Query the bills collection for bills with departments in the user's list
    bills_ref = db.collection('bills')
    # Query bills with user's departments and pending status
    query = bills_ref.where('sc_approved', '==', True).where('fc_approved', '==', False)
    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/fc-approved', methods=['GET'])
@token_required
def get_fc_approved_bills(current_user):
    # TODO Check for Core Role
    # Query the bills collection for bills with departments in the user's list
    bills_ref = db.collection('bills')
    # Query bills with user's departments and pending status
    query = bills_ref.where('bill_status', '==', 'fc_approved')
    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/sr-pending', methods=['GET'])
@token_required
def get_sr_pending_bills(current_user):
    # TODO Check for Core Role

    bills_ref = db.collection('bills')

    query = bills_ref.where('bill_status', '==', 'fc_approved').where('bill_type', '==', 'Student Reimbursement').where('eas_generated', '==', False)
    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/eas-generated', methods=['GET'])
@token_required
def get_eas_generated_bills(current_user):
    # TODO Check for Core Role

    bills_ref = db.collection('bills')

    query = bills_ref.where('eas_generated', '==', True)
    bills = query.stream()

    docs = query.get()

    if len(docs) == 0:
        return jsonify({'message': 'No bills found'}), 200

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/fc-approved', methods=['PUT'])
@token_required
def fc_approve_bill(current_user):
    # TODO Check for Core Role
    # Retrieve the bill ID from the request body
    bill_id = request.form['bill_id']
    # Check if the user is authorized to approve the bill
    if current_user['role'] != 'Core':
        return jsonify({'error': 'You are not authorized to approve bills'}), 403

    # Update the bill document with the approval details
    bill_ref = db.collection('bills').document(bill_id)
    bill_ref.update({
        'bill_status': 'fc_approved',
        'fc_approved': True,
        'fc_approved_on': datetime.datetime.now(),
        'fc_approved_by': current_user['name'],
        'voucher_generated': True,
        'voucher_generated_on': datetime.datetime.now().strftime("%d-%m-%Y")
    })
    return jsonify({'message': 'Bill approved successfully'}), 200

@app.route('/bills/stact-pending', methods=['GET'])
@token_required
def get_stact_pending_bills(current_user):
    # Query the bills collection for bills with departments in the user's list
    bills_ref = db.collection('bills')
    # Query bills with user's departments and pending status
    query = bills_ref.where('bill_status', '==', 'fc_approved').where('stact_processed', '==', False)
    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/stact-process-bill', methods=['PUT'])
@token_required
def stact_process_bill(current_user):
    # Retrieve the bill ID from the request body
    bill_id = request.form['bill_id']
    # Check if the user is authorized to approve the bill
    # if current_user['role'] != 'admin':
    #     return jsonify({'error': 'You are not authorized to approve bills'}), 403
    # Update the bill document with the approval details
    bill_ref = db.collection('bills').document(bill_id)
    bill_ref.update({
        'stact_processed': True,
        'stact_processed_on': datetime.datetime.now(),
    })
    return jsonify({'message': 'Bill approved successfully'}), 200

@app.route('/bills/stact-processed', methods=['GET'])
@token_required
def get_stact_processed_bills(current_user):
    # Query the bills collection for bills with departments in the user's list
    bills_ref = db.collection('bills')
    # Query bills with user's departments and pending status
    query = bills_ref.where('stact_processed', '==', True)
    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)

    # Return the bills as a JSON response
    return jsonify({'bills': bill_list}), 200

@app.route('/bills/reject', methods=['PUT'])
@token_required
def fc_reject_bill(current_user):
    # TODO Check for Core Role
    # Retrieve the bill ID from the request body
    bill_id = request.form['bill_id']
    # Check if the user is authorized to approve the bill
    # if current_user['role'] != 'Core':
    #     return jsonify({'error': 'You are not authorized to approve bills'}), 403

    # First Delete bill from storage
    bill_ref = db.collection('bills').document(bill_id)
    bill_data = bill_ref.get().to_dict()

    image_path = f"bills/{bill_data['bill_number']}_{bill_data['bill_department']}"
    blobs = bucket.list_blobs(prefix=image_path)
    for blob in blobs:
        blob.delete()
    
    # Delete bill from firestore
    bill_ref.delete()


    return jsonify({'message': 'Bill rejected successfully'}), 200

@app.route('/upload-voucher', methods=['POST'])
@token_required
def upload_pdf(current_user):
    pdf_file = request.files['pdf']
    bill_id = request.form['bill_id']
    bill_ref = db.collection('bills').document(bill_id)
    bill_data = bill_ref.get().to_dict()
    bill_number = bill_data['bill_number']
    bill_dept = bill_data['bill_department']
    
    # Upload the PDF file to GCP Storage
    today_date = datetime.datetime.now().strftime("%d-%m-%Y")
    blob = bucket.blob(f"vouchers/{today_date}/{pdf_file.filename}")
    old_blob = bucket.blob(f"bills/{bill_number}_{bill_dept}.pdf")
    new_blob = bucket.copy_blob(old_blob, bucket, f"vouchers/{today_date}/{bill_number}_{bill_dept}.pdf")
    blob.upload_from_file(pdf_file)
    print(f'File {pdf_file.filename} uploaded to {bucket_name}.')
    # Update the bill document with the voucher details
    bill_ref.update({
        'voucher': pdf_file.filename
    })
    # Return a success response
    return jsonify({'message': 'Voucher uploaded successfully'}), 200

@app.route('/bills/get-bill', methods=['POST'])
@token_required
def get_bill(current_user):
    bill_id = request.form['bill_id']
    bill_ref = db.collection('bills').document(bill_id)
    bill_data = bill_ref.get().to_dict()
    return jsonify({'bill': bill_data}), 200

@app.route('/bills/get-len-all-fc-approved', methods=['GET'])
@token_required
def get_all_fc_approved(current_user):
    bill_ref = db.collection('bills')
    query = bill_ref.where('bill_status', '==', 'fc_approved')
    bills = query.get()
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_data['id'] = bill.id
        bill_list.append(bill_data)
    return jsonify({'bills': len(bill_list)}), 200

@app.route('/bills/get-bill-view-url', methods=['POST'])
@token_required
def get_temp_view_url(current_user):
    bill_id = request.form['bill_id']
    bill_ref = db.collection('bills').document(bill_id)
    bill_data = bill_ref.get().to_dict()
    bill_number = bill_data['bill_number']
    bill_dept = bill_data['bill_department']
    bill_name = f"{bill_number}_{bill_dept}"
    blob = bucket.blob(f"bills/{bill_name}.pdf")
    # Generate a signed URL for the bill
    url = blob.generate_signed_url(
        version='v4',
        expiration=datetime.timedelta(minutes=5),
    )
    # Return a success response
    return jsonify({'bill_url': url}), 200

@app.route('/bills/get-voucher-view-url', methods=['POST'])
@token_required
def get_voucher_view_url(current_user):
    bill_id = request.form['bill_id']
    bill_ref = db.collection('bills').document(bill_id)
    bill_data = bill_ref.get().to_dict()
    voucher_name = bill_data['voucher']
    voucher_generated_date = bill_data['voucher_generated_on']
    blob = bucket.blob(f"vouchers/{voucher_generated_date}/{voucher_name}")
    # Generate a signed URL for the bill
    url = blob.generate_signed_url(
        version='v4',
        expiration=datetime.timedelta(minutes=5),
    )
    # Return a success response
    return jsonify({'voucher_url': url}), 200

@app.route('/send-accept-mail', methods=['POST'])
@token_required
def send_accept_mail(current_user):
    pod_email = os.getenv('POD_EMAIL')
    email = request.form['email']
    bill_number = request.form['bill_number']
    bill_description = request.form['bill_description']
    voucher_number = request.form['voucher_number']

    subject = f"Bill Number - {bill_number} - Accepted"

    message = f"Bill Number: {bill_number}\nBill Description: {bill_description}\n\nThe above bill is approved and will be processed in 2-3 working days.\n\n\nThanks & Regards,\nPradeeshwar A\nFinance Core - IITM Paradox'23"

    pod_subject = f"Paradox Voucher Number - {voucher_number}`"

    pod_message = f"Voucher Number: {voucher_number}\n\nThe above voucher is verified. Please check the Paradox Finance Management Portal for necessary details. Kindly process the payment within 2-3 working days.\n\n\nThanks & Regards,\nPradeeshwar A\nFinance Core - IITM Paradox'23"
    
    send_email(email, subject, message)
    send_email(pod_email, pod_subject, pod_message)
    return jsonify({'message': 'Email sent successfully'}), 200

@app.route('/send-reject-mail', methods=['POST'])
@token_required
def send_reject_mail(current_user):
    email = request.form['email']
    remarks = request.form['remarks']
    bill_number = request.form['bill_number']
    bill_description = request.form['bill_description']
    # pdf_file = request.files['pdf']
    # file_data = pdf_file.read()
    # print(email, remarks, bill_number, bill_description, file_data)
    subject = f"Bill Number - {bill_number} - Rejected"

    message = f"Bill Number: {bill_number}\nBill Description: {bill_description}\n\nRemarks: {remarks}\nKindly refill the bill submission form with the required corrections.\n\n\nThanks & Regards,\nPradeeshwar A\nFinance Core - IITM Paradox'23"

    send_email(email, subject, message)
    return jsonify({'message': 'Email sent successfully'}), 200

@app.route('/generate-eas-sr', methods=['GET'])
@token_required
def generate_eas_sr(current_user):
    bills_ref = db.collection('bills')

    query = bills_ref.where('bill_status', '==', 'fc_approved').where('bill_type', '==', 'Student Reimbursement').where('eas_generated', '==', False).select(['voucher', 'vendor_name', 'vendor_address', 'bill_department' 'bill_description', 'bill_date', 'bill_amount'])

    docs = query.get()

    if len(docs) == 0:
        return jsonify({'message': 'No bills to generate EAS'}), 200

    for doc in docs:
        doc_ref = bills_ref.document(doc.id)
        doc_ref.update({'eas_generated': True})

    bills = query.stream()

    # Format the bills as a list of dictionaries
    bill_list = []
    for bill in bills:
        bill_data = bill.to_dict()
        bill_list.append(bill_data)

    now = datetime.datetime.now().date()
    filtered_items = [item for item in bill_list if datetime.datetime.strptime(item['bill_date'], '%Y-%m-%d').date() < now]

    # filtered_items_without_id = [{k: v for k, v in d.items() if k != 'id'} for d in filtered_items]

    # Create a Pandas dataframe from the list of dictionaries
    df = pd.DataFrame(filtered_items)
    # df = pd.read_json(filtered_items_without_id)
    df.to_csv('file.csv', index=False)
    # df.to_excel('file.xlsx')

    return jsonify({'message': 'EAS SR generated successfully'}), 200
    

if __name__ == '__main__':
    app.run(debug=True)