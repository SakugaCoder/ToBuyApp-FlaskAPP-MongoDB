import pymongo
from flask import Flask, jsonify, request
from bson import ObjectId
from flask_cors import CORS

client = pymongo.MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false")

db = client.tobuydb

app = Flask(__name__)
CORS(app)


@app.route("/get-items",methods= ["GET"])
def getItems():
    items = []
    for item in db.items.find():
        items.append({
            "_id": str(item["_id"]),
            "name": item["name"],
            "description": item["description"],
            "price": item["price"],
            "qty": item["qty"],
            "img_url": item["img_url"]
        })

    return jsonify({
        "message": "ok",
        "status": 200,
         "content": items
    })


@app.route("/new-item", methods=["POST"])
def newItem():
    if request.json is not None:
        try:
            print(request.json)
            inserted_id = str(db.items.insert_one(request.json).inserted_id)

            if inserted_id is not None:
                print(inserted_id)
                return jsonify({"error": False, "status": 200, "id": inserted_id})
            else:
                return jsonify({"error": True, "status": 200})
            
        except Exception as e:
            error_str = f"Error. {e}"
            print(error_str)
            return jsonify({"error": True, "msj": error_str})
        
        return jsonify({"error": False, "status": 200})
    else:
        return jsonify({"error": True, "status": 400})

@app.route("/delete-item/<item_id>",methods=["DELETE"])
def deleteItem(item_id):
    print(f"Deleting {item_id}")
    try:
        deleted_count = db.items.delete_one({"_id": ObjectId(item_id)}).deleted_count
        print(f"Deleted count: {deleted_count}")
        if deleted_count > 0:
            return jsonify({"error": False})
        else:
            return jsonify({"error": True, "msj": "The id doesn't exists"})

    except Exception as e:
        error_str = f"Error {e}"
        print(error_str)
        return jsonify({"error": True, "msj": error_str})


def main():
    app.run(host="0.0.0.0",port=5000)

if __name__ == '__main__':
    main()

