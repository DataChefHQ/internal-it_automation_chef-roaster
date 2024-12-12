// var typewriter;
document.addEventListener('DOMContentLoaded', () => {
    const resp = document.getElementById("response");
    typewriter = new Typewriter(resp, {
        loop: false,
        delay: 25,
        cursor: '|',
    });
    typewriter
        .typeString("Let's get started! Describe your Chef and I'll roast them for you.")
        .start();
});


function submitForm() {
    // Show loading spinner and message
    document.getElementById("image-chef").src = "";
    document.getElementById("image-roast").src = "";
    document.getElementById("roast-button").style.display = 'none';
    document.getElementById("roast-button-loading").textContent = 'Roasting... 🔥';
    document.getElementById("roast-button-loading").style.display = 'block';
    document.getElementById("image-chef").style.display = 'none';
    document.getElementById("image-roast").style.display = 'none';
    document.getElementById("bg-image").style.display = 'block';
    document.getElementById("response").innerText = "";
    document.getElementById("share-button").style.display = 'none';

    // Get the prompt text
    var prompt = document.getElementById("prompt").value;
    fetch('/find', {
        method: 'POST',
        body: JSON.stringify({prompt: prompt}),
        headers: {'Content-Type': 'application/json'}
    }).then(
        response => response.json()
    ).then(data => {
        var roastAudio = new Audio(data.audio_url);
        roastAudio.play().catch((error) => {
            console.error("Audio playback failed:", error);
        });

        // Start typing the response
        var resp = document.getElementById("response");
        var typewriter = new Typewriter(resp, {
            loop: false,
            delay: 45,
            cursor: '|',
        });
        typewriter
            .typeString(data.reason)
            .start();

        // Get the image describing the roast
        setTimeout(function () {
            fetch('/roast', {
                method: 'POST',
                body: JSON.stringify({prompt: prompt, chef: data.name}),
                headers: {'Content-Type': 'application/json'}
            }).then(
                response => response.json()
            ).then(data => {
                // Show the Chef image
                document.getElementById("image-chef").src = data.url;
                document.getElementById("roast-button-loading").textContent = 'Generating image... 🔥';
                document.getElementById("image-chef").style.display = 'block';
                document.getElementById("bg-image").style.display = 'none';

                document.getElementById("roast_id").innerText = data.roast_id;

                // Play roast audio and type roast text
                var roastAudio = new Audio(data.roast_audio_s3_url);
                roastAudio.play().catch((error) => {
                    console.error("Audio playback failed:", error);
                });

                var typewriter = new Typewriter(resp, {
                    loop: false,
                    delay: 45,
                    cursor: '|',
                });
                typewriter
                    .typeString(data.roast)
                    .start();
            })
        }, 3000);

        fetch('/image', {
            method: 'POST',
            body: JSON.stringify({roast: data.reason, roast_id: data.roast_id}),
            headers: {'Content-Type': 'application/json'}
        }).then(
            response => response.json()
        ).then(data => {
            // Change the roasting button back for the next roast
            document.getElementById("roast-button").style.display = 'block';
            document.getElementById("roast-button-loading").style.display = 'none';
            document.getElementById("image-roast").src = data.roast_image_url;
            document.getElementById("image-roast").style.display = 'block';
            document.getElementById("share-button").style.display = 'block';
        });

    });
}

function changeText(button) {
    button.textContent = "Roast 😈";
}

function resetText(button) {
    button.textContent = "Roast 👿";
}

function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.textContent = '❄';
    snowflake.style.left = Math.random() * window.innerWidth + 'px';
    snowflake.style.animationDuration = '20s';
    document.body.appendChild(snowflake);

    setTimeout(() => {
        snowflake.remove();
    }, 20000);
}

setInterval(createSnowflake, 600);


function copyToClipboard() {
    // The value to copy to the clipboard
    const currentURL = window.location.href;
    const url = new URL(currentURL);
    url.pathname = document.getElementById("roast_id").innerText;
    const textToCopy = url.href;

    // Use the Clipboard API to write the text
    navigator.clipboard.writeText(textToCopy).then(() => {
        // Show the "Copied" message
        const messageElement = document.getElementById('copiedMessage');
        messageElement.style.display = 'block';

        // Hide the message after 2 seconds
        setTimeout(() => {
            messageElement.style.display = 'none';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}