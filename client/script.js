// ========================
// SPEECH RECOGNITION SETUP
// ========================

const SpeechRecognition =
	window.SpeechRecognition || window.webkitSpeechRecognition;

let recognizer;
let listening = false;

if (typeof SpeechRecognition !== 'undefined') {
	console.log('The browser acknowledges the speech recognizer.');

	// Initialize recognizer
	recognizer = new SpeechRecognition();
	recognizer.interimResults = true;
	recognizer.continuous = true;
	recognizer.lang = 'en-US';

	recognizer.onresult = (event) => {
		const result = event.results[event.resultIndex];
		const transcript = result[0].transcript.trim();
		const confidence = result[0].confidence;

		if (result.isFinal && transcript) {
			console.log(
				`Final Result: "${transcript}" (Confidence: ${(confidence * 100).toFixed(2)}%)`
			);
			sendToServer(transcript);
		}
	};

	recognizer.onerror = (event) => {
		console.error('Speech recognition error:', event.error);
	};

	recognizer.onend = () => {
		if (listening) {
			console.log('Recognizer stopped, restarting...');
			recognizer.start();
		} else {
			console.log('Recognizer stopped.');
		}
	};

	// Start listening initially
	startListening();
} else {
	console.log('Speech recognition is not supported in this browser.');
}

// ========================
// API CALL FUNCTION
// ========================

function sendToServer(message) {
	console.log('Sending to server:', message);

	fetch('http://localhost:8000/chat', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ message }),
	})
		.then((response) => {
			if (!response.ok) {
				throw new Error(`Server error: ${response.status}`);
			}
			return response.json();
		})
		.then((data) => {
			console.log('Server response:', data.response);
		})
		.catch((err) => {
			console.error('Fetch failed:', err);
		});
}

// ========================
// SERVER TEST BUTTON
// ========================

function testServer() {
	fetch('http://localhost:8000/test')
		.then((response) => {
			if (!response.ok) {
				throw new Error(
					`Server responded with an error! ${response.status}`
				);
			}
			return response.text();
		})
		.then((data) => {
			console.log('Server responded OK!', data);
		})
		.catch((err) => {
			console.error('Fetch failed:', err);
		});
}

const testServerBtn = document.getElementById('test-server-btn');
if (testServerBtn) {
	testServerBtn.addEventListener('click', testServer);
} else {
	console.warn('Button #test-server-btn not found in DOM.');
}

// ========================
// LISTEN/STOP BUTTON
// ========================

const stopBtn = document.querySelector('.stop-btn');
if (stopBtn) {
	stopBtn.addEventListener('click', () => {
		if (listening) {
			stopListening();
		} else {
			startListening();
		}
	});
}

function startListening() {
	if (!recognizer) return;
	listening = true;
	recognizer.start();
	stopBtn.classList.remove('off');
	stopBtn.querySelector('.stop-text').innerHTML = 'Stop<br />Listening';
	console.log('Switched to listening mode.');
}

function stopListening() {
	if (!recognizer) return;
	listening = false;
	recognizer.stop();
	stopBtn.classList.add('off');
	stopBtn.querySelector('.stop-text').innerHTML = 'Start<br />Listening';
	console.log('Switched off listening mode.');
}
