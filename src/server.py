from flask import Flask, request
from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span, ZipkinAttrs
from py_zipkin.transport import BaseTransportHandler
import time
import uuid

app = Flask(__name__)

class HttpTransport(BaseTransportHandler):
    def get_endpoint(self):
        return "http://192.168.1.104:9411/api/v2/spans"
    
    def send(self, payload):
        import requests
        try:
            response = requests.post(self.get_endpoint(), data=payload, headers={'Content-Type': 'application/json'})
            if response.status_code != 202:
                print(f"Failed to send trace to Zipkin: {response.status_code} - {response.text}")
            else:
                print("Trace sent to Zipkin successfully")
        except Exception as e:
            print(f"Error sending trace to Zipkin: {e}")
    
    def get_max_payload_bytes(self):
        return 1024 * 1024  # 1MB

def do_work():
    time.sleep(0.2)
    return "Hello, World!"

@app.route('/greet', methods=['GET'])
def greet():
    trace_headers = {
        'X-B3-TraceId': request.headers.get('X-B3-TraceId'),
        'X-B3-SpanId': request.headers.get('X-B3-SpanId'),
        'X-B3-ParentSpanId': request.headers.get('X-B3-ParentSpanId'),
        'X-B3-Sampled': request.headers.get('X-B3-Sampled', '1'),
        'X-B3-Flags': request.headers.get('X-B3-Flags', '0'),
    }
    
    print("Received headers:", trace_headers)

    # If traceId is None, generate a new span
    if not trace_headers['X-B3-TraceId']:
        print("No traceId received, starting new trace")
        new_headers = create_http_headers_for_new_span()
        trace_headers.update(new_headers)

    # Generate a new span_id for the server, use client's span_id as parent
    new_span_id = uuid.uuid4().hex[:16]
    zipkin_attrs = ZipkinAttrs(
        trace_id=trace_headers['X-B3-TraceId'],
        span_id=new_span_id,  # New unique span_id for this service
        parent_span_id=trace_headers['X-B3-SpanId'],  # Client's span_id becomes parent
        is_sampled=trace_headers['X-B3-Sampled'] == '1',
        flags=trace_headers['X-B3-Flags']
    )
    
    print("Zipkin attrs - trace_id:", zipkin_attrs.trace_id, 
          "span_id:", zipkin_attrs.span_id, 
          "parent_span_id:", zipkin_attrs.parent_span_id)

    with zipkin_span(
        service_name='greeting-service',
        span_name='greet_endpoint',
        zipkin_attrs=zipkin_attrs,
        transport_handler=HttpTransport(),
        port=5000,
    ):
        result = do_work()
        return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
