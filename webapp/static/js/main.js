var videoStream;
var frameInterval;
var canvas = document.createElement('canvas');
var context = canvas.getContext('2d');
var frameCount = 0;
var videoElement;
var framesContainer = document.getElementById('framesContainer');

function startRecording() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            videoStream = stream;
            videoElement = document.createElement('video');
            videoElement.srcObject = stream;
            videoElement.autoplay = true;
            document.getElementById('videoContainer').appendChild(videoElement);

            frameInterval = setInterval(captureFrame, 1000 / 1);
        })
        .catch(function(error) {
            console.error('Error accessing camera:', error);
        });
}

function captureFrame() {
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    var imageData = canvas.toDataURL('image/jpeg');

    var frameImage = document.createElement('img');
    frameImage.src = imageData;
    frameImage.classList.add('frame');

    frameCount++;
    console.log('Frame captured: ' + frameCount);

    // Send the captured image data to the server
    sendImageData(imageData);
}


var framesContainer = document.getElementById('framesContainer');

function sendImageData(imageData) {
    fetch('/save_image', {
        method: 'POST',
        body: JSON.stringify({ image_data: imageData }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Create an image element and set its source to the received image data
            var frameImage = document.createElement('img');
            frameImage.src = 'data:image/jpeg;base64,' + data.image_data;
            frameImage.classList.add('frame');

            // Append the image element to the frames container
            framesContainer.appendChild(frameImage);

            console.log('Image data received and displayed');
        })
        .catch(function(error) {
            console.error('Error receiving image data:', error);
        });
}

// function sendImageData(imageData) {
//     fetch('/save_image', {
//         method: 'POST',
//         body: JSON.stringify({ image_data: imageData }),
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//         .then(function(response) {
//             console.log('Image data sent successfully');
//         })
//         .catch(function(error) {
//             console.error('Error sending image data:', error);
//         });
// }

function stopRecording() {
    clearInterval(frameInterval);
    videoStream.getVideoTracks()[0].stop();
    var videoContainer = document.getElementById('videoContainer');
    videoContainer.innerHTML = '';
    frameCount = 0;
}