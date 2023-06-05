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
    """)
