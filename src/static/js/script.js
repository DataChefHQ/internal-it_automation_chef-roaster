
// var typewriter;
document.addEventListener('DOMContentLoaded', () => {
    const resp = document.getElementById("response");
    typewriter = new Typewriter(resp, {
        loop: false,
        delay: 20,
    });
    typewriter
      .typeString("Let's get started! Describe your Chef and I'll roast them for you.")
      .start();
});



function submitForm() {
    // Show loading spinner and message
    document.getElementById("roast-button").style.display = 'none';
    document.getElementById("roast-button-loading").style.display = 'block';

    document.getElementById("image").style.display = 'none';

    // if(typewriter) {
    //     typewriter.stop();
    //     typewriter.changeDeleteSpeed(1);
    //     typewriter.deleteAll().start();
    // }

    // Get the prompt text
    var prompt = document.getElementById("prompt").value;
    fetch('/find', {
        method: 'POST',
        body: JSON.stringify({ message: prompt }),
        headers: { 'Content-Type': 'application/json' }
    }).then(
        response => response.json()
    ).then(data => {
        document.getElementById("roast-button").style.display = 'block';
        document.getElementById("roast-button-loading").style.display = 'none';

        document.getElementById("image").src = data.url;
        document.getElementById("image").style.display = 'block';

        var resp = document.getElementById("response");
        var typewriter = new Typewriter(resp, {
            loop: false,
            delay: 20,
        });
        typewriter
          .typeString(data.reason)
          .start();
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