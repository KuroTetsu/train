from flask import Blueprint, jsonify, request
from . import routes
from main.controller import stream

@routes.route('/notes') #return all notes
@routes.route('/notes/<int:id>') #return specific note by id
def get_all_notes(id=0):
    if id:
        all_notes = stream.notes_by_id(id)
    else:
        all_notes = stream.all_notes()

    if not all_notes:
        return jsonify({"result": "data not found"}), 404
    try:
        data = []
        for note in all_notes:
            data.append({
                "id": note.id,
                "note": note.notes,
                "created_on": note.timestamp.timestamp()
            })
    except:
        data = {
            "id": all_notes.id,
            "note": all_notes.notes,
            "created_on": all_notes.timestamp.timestamp()
        }

    response = {
        'result': data
    }
    return jsonify(response), 200

@routes.route('/add', methods=["POST"])
def add_note():
    note = request.form.get("note")
    
    data = stream.add_note(note)

    response = {
        'result': {
            "id": data.id,
            "note": data.notes,
            "create_on": data.timestamp.timestamp()
        }
    }

    return jsonify(response), 200

@routes.route('/delete/<int:id>', methods=["DELETE"])
def delete_note(id):
    data = stream.delete_note(id)
    if data:
        return jsonify(), 204
    else:
        return jsonify({"result":"note not found"}), 404
