import requests
from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span, ZipkinAttrs
from py_zipkin.transport import BaseTransportHandler
import uuid

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

def call_greeting_service():
    # Manually create root trace attributes
    trace_id = uuid.uuid4().hex[:16]  # 16-char traceId
    span_id = uuid.uuid4().hex[:16]   # 16-char spanId
    zipkin_attrs = ZipkinAttrs(
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=None,  # Root span, no parent
        is_sampled=True,
        flags='0'
    )

    with zipkin_span(
        service_name='client-service',
        span_name='call_greeting_service',
        zipkin_attrs=zipkin_attrs,
        transport_handler=HttpTransport(),
        port=0,
    ):
        headers = {
            'X-B3-TraceId': trace_id,
            'X-B3-SpanId': span_id,
            'X-B3-Sampled': '1',
            'X-B3-Flags': '0',
        }
        print("Generated headers inside span:", headers)
        response = requests.get('http://192.168.1.104:5000/greet', headers=headers)
        return response.text

if __name__ == '__main__':
    try:
        result = call_greeting_service()
        print(f"Response from server: {result}")
    except Exception as e:
        print(f"Client error: {e}")
