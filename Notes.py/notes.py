from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# تحديد مسار ملف notes.json
FILE_PATH = os.path.join(os.path.dirname(__file__), 'notes.json')


# دالة مساعدة لقراءة الملاحظات من ملف JSON
def read_notes():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2)
        return []
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


# دالة مساعدة لكتابة الملاحظات في ملف JSON
def write_notes(notes):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


# GET /notes - استرجاع كل الملاحظات
@app.route('/notes', methods=['GET'])
def get_all_notes():
    notes = read_notes()
    return jsonify(notes), 200


# GET /notes/<id> - استرجاع ملاحظة واحدة بواسطة الـ ID
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note_by_id(note_id):
    notes = read_notes()
    note = next((n for n in notes if n['id'] == note_id), None)

    if not note:
        return jsonify({'message': 'Note not found'}), 404

    return jsonify(note), 200


# POST /notes - إنشاء ملاحظة جديدة
@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400

    notes = read_notes()
    new_id = notes[-1]['id'] + 1 if notes else 1
    new_note = {
        'id': new_id,
        'title': title,
        'content': content
    }

    notes.append(new_note)
    write_notes(notes)

    return jsonify({'message': 'Note created successfully', 'note': new_note}), 201


# PUT /notes/<id> - استبدال كامل للملاحظة (Full Replace)
@app.route('/notes/<int:note_id>', methods=['PUT'])
def replace_note(note_id):
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')

    # في الـ PUT يجب إرسال العنوان والمحتوى معاً لاستبدال الكائن بالكامل
    if not title or not content:
        return jsonify({'message': 'Title and content are required for full replacement'}), 400

    notes = read_notes()
    for idx, n in enumerate(notes):
        if n['id'] == note_id:
            notes[idx] = {
                'id': note_id,
                'title': title,
                'content': content
            }
            write_notes(notes)
            return jsonify({'message': 'Note replaced successfully', 'note': notes[idx]}), 200

    return jsonify({'message': 'Note not found'}), 404


# PATCH /notes/<id> - تعديل جزئي (Partial Update)
@app.route('/notes/<int:note_id>', methods=['PATCH'])
def update_note(note_id):
    data = request.get_json() or {}
    notes = read_notes()
    note = next((n for n in notes if n['id'] == note_id), None)

    if not note:
        return jsonify({'message': 'Note not found'}), 404

    # تعديل القيم المرسلة فقط
    if 'title' in data:
        note['title'] = data['title']
    if 'content' in data:
        note['content'] = data['content']

    write_notes(notes)
    return jsonify({'message': 'Note updated successfully', 'note': note}), 200


# DELETE /notes/<id> - حذف ملاحظة
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    notes = read_notes()
    initial_length = len(notes)
    notes = [n for n in notes if n['id'] != note_id]

    if len(notes) == initial_length:
        return jsonify({'message': 'Note not found'}), 404

    write_notes(notes)
    return jsonify({'message': 'Note deleted successfully'}), 200


# معالجة المسارات غير الموجودة (404 Handler)
@app.errorhandler(404)
def not_found(e):
    return jsonify({'message': 'Route not found'}), 404


# تشغيل السيرفر على البورت 3580
if __name__ == '__main__':
    app.run(port=3580, debug=True)
