document.getElementById('capture').addEventListener('click', function (event) {
    event.preventDefault();
    const form = document.forms[0];
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const video = document.getElementById('webcam');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');
    document.getElementById('image_data').value = imageData;
    form.submit();
});
navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
    document.getElementById('webcam').srcObject = stream;
});
