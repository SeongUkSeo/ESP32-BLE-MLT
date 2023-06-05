@app.route('/')
def index():
    return render_template_string("""
        <html>
            <body>
                <h1>ESP32 LED Control</h1>
                <button id="onButton">Turn ON</button>
                <button id="offButton">Turn OFF</button>

                <script>
                    document.getElementById("onButton").addEventListener("click", function(event) {
                        fetch('/led', { 
                            method: 'POST', 
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: new URLSearchParams({state: 'ON'}) 
                        })
                        event.preventDefault();
                    });

                    document.getElementById("offButton").addEventListener("click", function(event) {
                        fetch('/led', { 
                            method: 'POST', 
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: new URLSearchParams({state: 'OFF'}) 
                        })
                        event.preventDefault();
                    });
                </script>
            </body>
        </html>
    """)@app.route('/led', methods=['POST'])
def led_control():
    state = request.form.get('state')
    if state in ['ON', 'OFF']:
        try:
            response = requests.get(f"http://{ESP32_IP}/led?state={state}")
            response.raise_for_status()
            return "LED state changed successfully", 200
        except requests.exceptions.HTTPError as errh:
            return f"Http Error: {errh}", 500
        except requests.exceptions.ConnectionError as errc:
            return f"Error Connecting: {errc}", 500
        except requests.exceptions.Timeout as errt:
            return f"Timeout Error: {errt}", 500
        except requests.exceptions.RequestException as err:
            return f"Something went wrong: {err}", 500
    else:
        return "Invalid state. Please send 'ON' or 'OFF'.", 400
