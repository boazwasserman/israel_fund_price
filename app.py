from flask import Flask, request, Response
import parser

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_fund_price_api():
    source_name = request.args.get("source")
    fund_id = request.args.get("id")

    if not source_name or not fund_id:
        return f"error\nMissing required parameters", 400

    try:
        _parser = parser.FundPriceParser(source_name, fund_id)
        price = _parser.parse_price()

        # create csv response
        csv_data = f"fund_id,fund_price,source\n{fund_id},{price},{source_name}"
        return Response(csv_data, mimetype='text/csv')
    
    except Exception as e:
        csv_data = f"error\n{str(e)}"
        return csv_data, 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
