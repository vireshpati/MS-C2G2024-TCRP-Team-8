import firebase_admin
from firebase_admin import credentials, firestore, messaging

SERVICE_ACCOUNT_PATH = "f9c8ad7b0a81cb6acbf415830d536defcc650c33.json"

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def store_fcm_token(user_id, fcm_token):
    """Stores the FCM token for a user."""
    try:
        db.collection("users").document(user_id).set({
            "fcmToken": fcm_token
        }, merge=True)
        print(f"FCM token stored for user {user_id}")
    except Exception as e:
        print(f"Error storing FCM token: {e}")

def get_fcm_token(user_id):
    """Retrieves the FCM token for a user."""
    try:
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict().get("fcmToken")
        else:
            print(f"No such user with ID: {user_id}")
            return None
    except Exception as e:
        print(f"Error retrieving FCM token: {e}")
        return None

def send_message_to_user(fcm_token, message_body):
    """Sends a notification to a user using their FCM token."""
    if not fcm_token:
        print("FCM token is required to send the message.")
        return

    message = messaging.Message(
        notification=messaging.Notification(
            title="New Message",
            body=message_body,
        ),
        token=fcm_token,
    )

    try:
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
    except Exception as e:
        print(f"Error sending message: {e}")

def send_batch_message(fcm_tokens, message_body):
    """Sends a batch of messages to multiple users."""
    if not fcm_tokens:
        print("FCM tokens are required to send the messages.")
        return

    messages = [
        messaging.Message(
            notification=messaging.Notification(
                title="New Message",
                body=message_body,
            ),
            token=token,
        )
        for token in fcm_tokens
    ]

    try:
        response = messaging.send_all(messages)
        print(f"Successfully sent batch message: {response}")
    except Exception as e:
        print(f"Error sending batch message: {e}")