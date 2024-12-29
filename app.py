from flask import Flask, request, Response
import parser
from pathlib import Path
import utils

RUN_WITH_NGROK = False
PORT = 5000

app = Flask(__name__)

if RUN_WITH_NGROK:
    utils.wrap_with_ngrok(PORT)

@app.route("/", methods=["GET"])
def get_fund_price_api():
    source_name = request.args.get("source")
    fund_id = request.args.get("id")

    if not source_name or not fund_id:
        return f"error\nMissing required parameters", 400

    APP_ROOT = Path(__file__).parent
    try:
        _parser = parser.FundPriceParser(source_name, fund_id, config_file=APP_ROOT / "sources.json")
        price = _parser.parse_price()

        # create csv response
        csv_data = f"fund_id,fund_price,source\n{fund_id},{price},{source_name}"
        return Response(csv_data, mimetype='text/csv')
    
    except Exception as e:
        csv_data = f"error\n{str(e)}"
        return csv_data, 500

if __name__ == "__main__":
    app.run(port=PORT)
