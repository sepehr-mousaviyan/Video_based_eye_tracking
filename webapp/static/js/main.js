var videoStream;
var frameInterval;
var canvas = document.createElement('canvas');
var context = canvas.getContext('2d');
var frameCount = 0;
var videoElement;
var framesContainer = document.getElementById('framesContainer');
var stopRecordingButton = document.getElementById('stopRecordingButton');
var currentForm;

function startRecording() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            videoStream = stream;
            videoElement = document.createElement('video');
            videoElement.srcObject = stream;
            videoElement.autoplay = true;
            document.getElementById('videoContainer').appendChild(videoElement);
            return getForm(); // Return the Promise from getForm()
        })
        .then(function(form) {
            currentForm = form; // Assign the received form to the currentForm variable
            console.log('Current form:', currentForm);
            framesContainer.innerHTML = ''; // Clear the frames container
            showForm(currentForm);
            // Get the current form's time interval
            var timeInterval = currentForm.time_interval * 10000;
            frameInterval = setInterval(captureFrame, 1000 / 0.5);
            setTimeout(stopRecording, timeInterval);
            console.log('Recording finished');
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

    // Check if the current form type is 'special' and call showForm
    if (currentForm && currentForm.type === 'special') {
        showForm(currentForm);
    }
}

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

function stopRecording() {
    clearInterval(frameInterval);
    videoStream.getVideoTracks()[0].stop();
    var videoContainer = document.getElementById('videoContainer');
    videoContainer.innerHTML = '';
    frameCount = 0;
}

function getForm() {
    return fetch('/get_form')
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        return data;
      })
      .catch(function(error) {
        console.error('Error fetching form:', error);
      });
  }

function getWindowSize() {
    var windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    var windowHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    return { window_width: windowWidth, window_height: windowHeight };
}

// Function to fetch and show the form based on form ID
function showForm(formData) {

  // Check the form type and show the appropriate content
  if (formData.type == 'special') {
    fetch('/generate_page', {
        method: 'POST',
        body: JSON.stringify(getWindowSize()),
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
          frameImage.classList.add('form-content', 'fullscreen');
  
          // Clear previous content and append the image element to the frames container
          framesContainer.innerHTML = '';
          framesContainer.appendChild(frameImage);
  
          console.log('Special form displayed');
        })
        .catch(function(error) {
          console.error('Error displaying special form:', error);
        });
  } else if (formData.type === 'video') {
    var videoElement = document.createElement('video');
    videoElement.src = formData.content;
    videoElement.classList.add('form-content', 'fullscreen');
    framesContainer.appendChild(videoElement);
  } else if (formData.type === 'slideshow') {
    var images = formData.content;
    var totalImages = images.length;
    var currentIndex = 0;

    function showNextImage() {
      var imageElement = document.createElement('img');
      imageElement.src = images[currentIndex];
      imageElement.classList.add('form-content', 'fullscreen');
      framesContainer.innerHTML = ''; // Clear previous image
      framesContainer.appendChild(imageElement);
      currentIndex++;

      if (currentIndex === totalImages) {
        clearInterval(slideshowInterval);
      }
    }

    showNextImage(); // Show the first image immediately
    var slideshowInterval = setInterval(showNextImage, 5000);
  } else if (formData.type === 'document') {
    var documentIframe = document.createElement('iframe');
    documentIframe.src = formData.content;
    documentIframe.classList.add('form-content', 'fullscreen');
    framesContainer.appendChild(documentIframe);
  }
}