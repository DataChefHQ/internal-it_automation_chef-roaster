from flask import jsonify

def find_chef(request):
    return jsonify({"name": "Ali", "reason": "bluh bluh bluh ..."})
