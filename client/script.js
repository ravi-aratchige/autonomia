// ========================
// SPEECH RECOGNITION SETUP
// ========================

// Check for browser support
const SpeechRecognition =
	window.SpeechRecognition || window.webkitSpeechRecognition;

if (typeof SpeechRecognition !== 'undefined') {
	console.log('The browser acknowledges the speech recognizer.');

	// Initialize recognizer
	const recognizer = new SpeechRecognition();

	// Settings
	recognizer.interimResults = true; // show partial results
	recognizer.continuous = true; // keep listening
	recognizer.lang = 'en-US';

	// Handle results
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

	// Handle errors
	recognizer.onerror = (event) => {
		console.error('Speech recognition error:', event.error);
	};

	// Auto-restart if recognizer stops
	recognizer.onend = () => {
		console.log('Recognizer stopped, restarting...');
		recognizer.start();
	};

	// Start listening
	recognizer.start();
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
