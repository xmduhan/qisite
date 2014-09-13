function copyToClipboard(text) {
    window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
}

function initCopyToClipboard() {
    $("#copyToClipboard").on('click', function () {
        //logger.debug('----copyToClipboard.click----');
        copyToClipboard('hehe!');
    });
}

$(document).ready(function () {
    initCopyToClipboard();
});