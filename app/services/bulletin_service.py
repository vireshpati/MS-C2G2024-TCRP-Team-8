import logging
from firebase_admin import firestore

logging.basicConfig(level=logging.INFO)

class BulletinService:
    def __init__(self):
        self.db = firestore.client()

    def create_request_post(self, request_data):
        try:
            doc_ref = self.db.collection('requests').add(request_data)
            logging.info("Request created successfully.")
        except Exception as e:
            logging.error(f"Error in create_request: {e}")
=
    def create_comment_reply(self, uid, comment_data):
        try:
            doc_ref = self.db.collection('requests').document(comment_data['post_uid'])
            doc_ref.update({
                'number_of_comments': firestore.Increment(1)
            })
            doc_ref = self.db.collection('comments').add(comment_data)
            logging.info("Comment created successfully.")
        except Exception as e:
            logging.error(f"Error in create_commentt: {e}")

    def get_request_post(self, post_uid):
        try:
            doc_ref = self.db.collection('requests').document(post_uid)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                logging.warning(f"Request not found for post_uid: {post_uid}")
                return None
        except Exception as e:
            logging.error(f"Error retrieving request: {e}")
            return None

    def get_comment_replies(self, post_uid):
        try:
            docs_ref = self.db.collection('comments')
            docs = docs_ref.where('post_uid', '==', post_uid).stream()
            all_comments = []
            for doc in docs:
                comment_data = doc.to_dict()
                all_comments.append(comment_data)
            return all_comments
        except Exception as e:
            logging.error(f"Error retrieving all comments: {e}")

    def get_relavent_requests(self, page, limit):
        try:
            docs_ref = self.db.collection('requests')
            now = datetime.datetime.utcnow()
            docs = docs_ref.where('deleted', '==', False).where('resolved', '==', resolved_requests) \
                            .where('date_help_needed', '>=', now).limit(limit).offset(offset).stream()
            all_requests = []
            for doc in docs:
                request_data = doc.to_dict()
                all_requests.append(request_data)
            return all_requests
        except Exception as e:
            logging.error(f"Error retrieving relavent requests: {e}")

    def update_request_post(self, request_data):
        try:
            doc_ref = self.db.collection('requests').document(request_data['post_uid'])
            doc_ref.set(request_data, merge=True)
            logging.info("Request updated successfully.")
        except Exception as e:
            logging.error(f"Error updating request: {e}")

    def toggle_request_resolved_status(self, post_uid):
        try:
            request_data = self.get_request_post(post_uid)
            if not request_data:
                logging.warning(f"Request not found for post_uid: {post_uid}")
                raise ValueError(f"Request not found for post_uid: {post_uid}")
            request_data['resolved'] = not request_data['resolved']
            self.update_request_post(request_data)
            return request_data
        except Exception as e:
            logging.error(f"Error toggling request resolved status request: {e}")
            raise

    def delete_request_post(self, post_uid):
        try:
            doc_ref = self.db.collection('requests').document(post_uid)
            doc_ref.delete()
            logging.info("Request deleted successfully.")
        except Exception as e:
            logging.error(f"Error deleting request: {e}")


