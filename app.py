import os
import logger
import argparse
from io import BytesIO

from flask import Flask, request, send_file
from waitress import serve

from convert import remove_background_from_image, remove_background_from_image_magick

app = Flask(__name__)

@app.route("/healthz", methods=["GET"])
def health():
    return "ok", 200

@app.route("/", methods=["GET", "POST"])
def index():
    app.logger.info(f"/ Request from {request.remote_addr}")
    file_content = ""

    if request.method == "POST":
        if "file" not in request.files:
            return {"error": "missing post form param 'file'"}, 400

        file_content = request.files["file"].read()

    else:
      return {"error": "Do not use this method here"}, 400

    try:
      app.logger.info(f"Converting {request.files['file'].filename}")
      converted_image = remove_background_from_image_magick(file_content)

      resp = send_file(BytesIO(converted_image), mimetype="image/png")
      app.logger.info(f"Converted {request.files['file'].filename}")

      return resp

    except Exception as e:
      app.logger.error(e)
      return {"error": "internal server error"}, 500

def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "-a",
        "--addr",
        default="0.0.0.0",
        type=str,
        help="IP",
    )

    ap.add_argument(
        "-p",
        "--port",
        default=8080,
        type=int,
        help="Port",
    )

    args = ap.parse_args()
    if os.environ.get('HOST') != None:
        args.addr = os.environ.get('HOST')
    if os.environ.get('PORT') != None:
        args.port = int(os.environ.get('PORT'))
    serve(app, host=args.addr, port=args.port)


if __name__ == "__main__":
    main()