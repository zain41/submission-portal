from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class ReportReceiver(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the incoming data
        content_length = int(self.headers['Content-Length'])
        # Read the data
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse it to make sure it's valid JSON
            report_data = json.loads(post_data.decode('utf-8'))
            
            # Save it to the file
            with open('test-report.json', 'w') as f:
                json.dump(report_data, f, indent=2)
                
            print("\n✅ Received a test report and saved to test-report.json!")
            
            # Tell GitHub everything went well
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Report saved successfully.")
            
        except Exception as e:
            print(f"\n❌ Error saving report: {e}")
            self.send_response(400)
            self.end_headers()

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('0.0.0.0', port), ReportReceiver)
    print(f"🎧 Receiver listening on http://localhost:{port}")
    print("Waiting for GitHub Actions to send the report...")
    server.serve_forever()