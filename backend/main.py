from flask import request, jsonify
from config import app, db
from models import Contact
import re

@app.route("/contacts", methods=["GET"])
def get_contacts():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Contact.query
    
    if search:
        query = query.filter(
            db.or_(
                Contact.first_name.ilike(f'%{search}%'),
                Contact.last_name.ilike(f'%{search}%'),
                Contact.email.ilike(f'%{search}%')
            )
        )
    
    if category:
        query = query.filter(Contact.category == category)
    
    contacts = query.order_by(Contact.first_name).all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    data = request.json
    
    first_name = data.get("firstName", "").strip()
    last_name = data.get("lastName", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    category = data.get("category", "").strip()
    
    if not first_name or not last_name or not email:
        return jsonify({"message": "First name, last name, and email are required"}), 400
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({"message": "Invalid email format"}), 400
    
    existing_contact = Contact.query.filter_by(email=email).first()
    if existing_contact:
        return jsonify({"message": "Email already exists"}), 400
    
    if not category:
        if any(domain in email.lower() for domain in ['gmail.com', 'yahoo.com', 'hotmail.com']):
            category = 'Personal'
        else:
            category = 'Work'
    
    new_contact = Contact(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        category=category
    )
    
    try:
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "Contact created successfully!", "contact": new_contact.to_json()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating contact: {str(e)}"}), 400

@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    
    data = request.json
    
    if "firstName" in data:
        contact.first_name = data["firstName"].strip()
    if "lastName" in data:
        contact.last_name = data["lastName"].strip()
    if "email" in data:
        email = data["email"].strip()
        if email != contact.email:
            existing = Contact.query.filter_by(email=email).first()
            if existing:
                return jsonify({"message": "Email already exists"}), 400
            contact.email = email
    if "phone" in data:
        contact.phone = data["phone"].strip()
    if "category" in data:
        contact.category = data["category"].strip()
    
    try:
        db.session.commit()
        return jsonify({"message": "Contact updated successfully!", "contact": contact.to_json()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating contact: {str(e)}"}), 400

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)
    
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    
    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contact deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting contact: {str(e)}"}), 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
