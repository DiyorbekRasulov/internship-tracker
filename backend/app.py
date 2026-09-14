from flask import Flask
# pulling Flask  class from the flask package that was installed
# build the app obejct, everything hangs off of variable app
app = Flask(__name__)
# registering the function below for the URL path
# create a function to match the urls
@app.route("/api/health")
def health():
    # dictionary output converted to JSON
    return {"status": "ok"}
# if the file is executed directly, run
if __name__ == "__main__":
    app.run(debug=True, port=5000)