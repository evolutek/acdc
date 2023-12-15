var pc = null;

async function connect() {
    pc.addTransceiver('video', {direction: 'recvonly'});

    let offer = await pc.createOffer();
    // console.log(offer);
    pc.setLocalDescription(offer);

    // POST the information to /offer
    let response = await fetch('/offer', {
        body: JSON.stringify({
            sdp: offer.sdp,
            type: offer.type,
        }),
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST'
    });

    await pc.setRemoteDescription(await response.json());

    console.log("Ready!");
}

function start() {
    var config = {
        sdpSemantics: 'unified-plan'
    };

    pc = new RTCPeerConnection(config);

    // Connect audio / video
    pc.addEventListener('track', function(evt) {
        document.getElementById('video').srcObject = evt.streams[0];
    });

    document.getElementById('start').style.display = 'none';
    connect();
    document.getElementById('stop').style.display = 'inline-block';
}

function stop() {
    document.getElementById('stop').style.display = 'none';

    // Close peer connection
    setTimeout(function() {
        pc.close();
        document.getElementById('start').style.display = 'inline-block';
    }, 500);
}
